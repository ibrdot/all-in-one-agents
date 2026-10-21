#!/usr/bin/env python3
"""Read-only review hints. Python files use AST; diffs/other files use heuristics.
Exit 0: no findings, 1: review findings, 2: input/parse failure.
This is neither an AI-authorship detector nor a complete security analyzer.
"""
import argparse
import ast
import json
from pathlib import Path
import re
import sys

SQL = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b', re.I)
MESSAGES = {
    'swallowed-exception': 'Exception handler discards the error; verify intended recovery.',
    'dynamic-exec': 'Dynamic execution requires review of input trust boundaries.',
    'sql-interp': 'Dynamically constructed SQL passed to a query method; prefer bound parameters.',
}


def finding(path, line, rule):
    return dict(path=str(path), line=line, rule=rule, message=MESSAGES[rule])


def python_findings(text, path):
    tree = ast.parse(text, filename=str(path))
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.body and all(isinstance(n, (ast.Pass, ast.Continue)) for n in node.body):
            hits.append(finding(path, node.lineno, 'swallowed-exception'))
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in ('eval', 'exec'):
            hits.append(finding(path, node.lineno, 'dynamic-exec'))
        if isinstance(node.func, ast.Attribute) and node.func.attr in ('execute', 'executemany', 'raw') and node.args:
            arg = node.args[0]
            dynamic = isinstance(arg, (ast.JoinedStr, ast.BinOp)) or (isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute) and arg.func.attr == 'format')
            literals = [n.value for n in ast.walk(arg) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
            if dynamic and any(SQL.search(s) for s in literals):
                hits.append(finding(path, node.lineno, 'sql-interp'))
    return hits


def heuristic(line, path, number):
    if line.lstrip().startswith(('#', '//', '*')):
        return []
    rules = []
    if re.search(r'\b(?:eval|exec)\s*\(', line):
        rules.append('dynamic-exec')
    if re.search(r'except[^:]*:\s*(?:pass|continue)\b|catch\s*(?:\([^)]*\))?\s*\{\s*\}', line):
        rules.append('swallowed-exception')
    return [finding(path, number, rule) for rule in rules]


def diff_findings(text):
    hits, path, number = [], None, None
    for line in text.splitlines():
        if line.startswith('diff --git '):
            path, number = None, None
        elif line.startswith('+++ '):
            raw = line[4:].split('\t', 1)[0]
            path = None if raw == '/dev/null' else raw.removeprefix('b/')
            number = None
        elif line.startswith('@@ '):
            match = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
            if not match:
                raise ValueError('malformed unified diff hunk')
            number = int(match.group(1))
        elif path is not None and number is not None:
            if line.startswith('+'):
                hits.extend(heuristic(line[1:], path, number))
                number += 1
            elif line.startswith(' '):
                number += 1
    return hits


def sarif(hits):
    return {'version': '2.1.0', '$schema': 'https://json.schemastore.org/sarif-2.1.0.json', 'runs': [{
        'tool': {'driver': {'name': 'skillpack-audit', 'rules': [
            {'id': k, 'shortDescription': {'text': v}} for k, v in MESSAGES.items()]}},
        'results': [{'ruleId': f['rule'], 'level': 'warning', 'message': {'text': f['message']},
                     'locations': [{'physicalLocation': {'artifactLocation': {'uri': Path(f['path']).as_posix()},
                                    'region': {'startLine': max(1, f['line'])}}}]} for f in hits]}]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', help='Files to scan; omitted: unified diff on stdin')
    parser.add_argument('--format', choices=['text', 'json', 'sarif'], default='text')
    args = parser.parse_args(argv)
    hits = []
    try:
        if not args.files:
            hits = diff_findings(sys.stdin.read())
        for name in args.files:
            path = Path(name)
            text = path.read_text(encoding='utf-8')
            if path.suffix == '.py':
                hits.extend(python_findings(text, path))
            else:
                for i, line in enumerate(text.splitlines(), 1):
                    hits.extend(heuristic(line, path, i))
    except (OSError, UnicodeError, SyntaxError, ValueError) as exc:
        print(f'audit error: {exc}', file=sys.stderr)
        return 2
    hits.sort(key=lambda f: (f['path'], f['line'], f['rule']))
    if args.format == 'sarif':
        print(json.dumps(sarif(hits), indent=2))
    elif args.format == 'json':
        print(json.dumps({'findings': hits, 'count': len(hits)}, indent=2))
    else:
        for f in hits:
            print(f"{f['path']}:{f['line']}: [{f['rule']}] {f['message']}")
        print(f'{len(hits)} finding(s); review hints, not proof of a vulnerability')
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main())
