#!/usr/bin/env python3
"""Report JSONL token costs using explicit user-supplied USD/1M token prices.
Record: {"model":"my-model","input":100,"output":20,"route":"chat"}
Prices: {"my-model":{"input":"2.50","output":"10.00"}}
Exit 0: success, 1: total exceeds budget, 2: invalid input/configuration.
No network, default prices, inferred prices, or silently skipped records.
"""
import argparse
from contextlib import nullcontext
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

MILLION = Decimal(1000000)


def amount(value, label):
    if isinstance(value, bool):
        raise ValueError(f'{label}: expected finite nonnegative decimal')
    try:
        number = Decimal(str(value))
    except InvalidOperation:
        raise ValueError(f'{label}: expected finite nonnegative decimal') from None
    if not number.is_finite() or number < 0:
        raise ValueError(f'{label}: expected finite nonnegative decimal')
    return number


def load_prices(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not data:
        raise ValueError('pricing must be a nonempty model-to-prices object')
    result = {}
    for model, rates in data.items():
        if not model or not isinstance(rates, dict) or set(rates) != {'input', 'output'}:
            raise ValueError(f'pricing for {model!r}: require input and output rates only')
        result[model] = (amount(rates['input'], 'input price'), amount(rates['output'], 'output price'))
    return result


def validate_record(rec, prices):
    if not isinstance(rec, dict):
        raise ValueError('record must be an object')
    model = rec.get('model')
    if not isinstance(model, str) or model not in prices:
        raise ValueError(f'model {model!r} missing from pricing configuration')
    for field in ('input', 'output'):
        if type(rec.get(field)) is not int or rec[field] < 0:
            raise ValueError(f'{field}: require nonnegative integer token count')
    route = rec.get('route', 'unrouted')
    if not isinstance(route, str) or not route:
        raise ValueError('route must be a nonempty string')
    return model, route


def report(paths, prices):
    models, routes, calls, total = {}, {}, 0, Decimal(0)
    for path in paths:
        context = nullcontext(sys.stdin) if path == '-' else open(path, encoding='utf-8')
        with context as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                    model, route = validate_record(rec, prices)
                except (ValueError, TypeError) as exc:
                    raise ValueError(f'{path}: line {number}: {exc}') from None
                pin, pout = prices[model]
                cost = (rec['input'] * pin + rec['output'] * pout) / MILLION
                row = models.setdefault(model, dict(model=model, calls=0, input=0, output=0, cost=Decimal(0)))
                row['calls'] += 1
                row['input'] += rec['input']
                row['output'] += rec['output']
                row['cost'] += cost
                routes[route] = routes.get(route, Decimal(0)) + cost
                total += cost
                calls += 1
    model_rows = []
    for row in sorted(models.values(), key=lambda r: (-r['cost'], r['model'])):
        model_rows.append({**{k: v for k, v in row.items() if k != 'cost'}, 'cost_usd': format(row['cost'], '.6f')})
    return dict(calls=calls, total_usd=format(total, '.6f'), models=model_rows,
                routes=[dict(route=k, cost_usd=format(v, '.6f')) for k, v in sorted(routes.items(), key=lambda kv: (-kv[1], kv[0]))]), total


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', help='JSONL files; defaults to stdin')
    parser.add_argument('--pricing', required=True, help='Explicit USD/1M prices JSON file')
    parser.add_argument('--budget', help='Fail with exit 1 if total exceeds this USD amount')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args(argv)
    try:
        if args.files.count('-') > 1:
            raise ValueError('stdin may only be read once')
        prices = load_prices(args.pricing)
        budget = amount(args.budget, 'budget') if args.budget is not None else None
        result, total = report(args.files or ['-'], prices)
    except (OSError, UnicodeError, ValueError, TypeError, InvalidOperation) as exc:
        print(f'cost report error: {exc}', file=sys.stderr)
        return 2
    result['budget_exceeded'] = budget is not None and total > budget
    if args.format == 'json':
        print(json.dumps(result, indent=2))
    else:
        print('USD rates supplied by caller; verify pricing and log completeness.')
        for row in result['models']:
            print(f"{row['model']}: {row['calls']} calls, ${row['cost_usd']}")
        print(f"TOTAL: {result['calls']} calls, ${result['total_usd']}")
        for row in result['routes']:
            print(f"  route {row['route']}: ${row['cost_usd']}")
        if result['budget_exceeded']:
            print('Budget exceeded')
    return 1 if result['budget_exceeded'] else 0


if __name__ == '__main__':
    sys.exit(main())
