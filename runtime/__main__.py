"""Explicit live runtime CLI. Run `python3 -m runtime --help`."""
import argparse
import json
import os
import tempfile
from pathlib import Path
from runtime.core import Memory
from runtime.providers import OpenAICompatible
from runtime.orchestrator import Agent, index_skills


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True, help='Reviewed HTTPS OpenAI-compatible endpoint, including /v1')
    parser.add_argument('--key-env', default='OPENAI_API_KEY', help='Environment variable name, NOT a token')
    parser.add_argument('--embedding-model', required=True)
    parser.add_argument('--allow-network', action='store_true', help='Explicit consent for remote requests and possible billing')
    sub = parser.add_subparsers(dest='command', required=True)
    idx = sub.add_parser('index', help='Build a fresh semantic skill index; embedding charges are separate')
    idx.add_argument('--skills', type=Path, default=Path('skills'))
    idx.add_argument('--database', type=Path, required=True)
    run = sub.add_parser('run', help='Run one task with retrieved skills and optional memory')
    run.add_argument('--database', type=Path, required=True)
    run.add_argument('--memory', type=Path)
    run.add_argument('--models', type=Path, required=True, help='JSON list of explicit model prices/capabilities')
    run.add_argument('--task', required=True)
    run.add_argument('--output', type=Path, required=True, help='New directory, contains potentially confidential output')
    run.add_argument('--budget', required=True, help='Estimated chat USD budget; excludes embeddings')
    run.add_argument('--output-tokens', type=int, default=1024)
    run.add_argument('--debate-models', nargs='+')
    run.add_argument('--judge')
    args = parser.parse_args()
    if not args.allow_network: parser.error('--allow-network is required')
    provider = OpenAICompatible(args.base_url, args.key_env,
                                max_output_tokens=getattr(args, 'output_tokens', 1024))
    stores = []
    try:
        if args.command == 'index':
            if args.database.exists(): raise ValueError('use a new database path for a full index rebuild')
            if not args.skills.is_dir(): raise ValueError('skill root does not exist')
            fd, temporary = tempfile.mkstemp(dir=args.database.parent, prefix='.skill-index-')
            os.close(fd)
            store = Memory(temporary)
            try:
                count = index_skills(args.skills, store, lambda text: provider.embed(args.embedding_model, text), args.embedding_model)
                if count == 0: raise ValueError('no skills indexed')
                store.close()
                # Hard link refuses concurrent replacement of an existing target.
                os.link(temporary, args.database)
            finally:
                store.close()
                os.unlink(temporary)
            print(json.dumps(dict(indexed=count, database=str(args.database))))
        else:
            if not args.database.is_file(): raise ValueError('skill database does not exist')
            if args.memory and not args.memory.is_file(): raise ValueError('memory database does not exist')
            if args.output.exists(): raise ValueError('output directory must be new')
            store = Memory(args.database); stores.append(store)
            memory = Memory(args.memory) if args.memory else None
            if memory: stores.append(memory)
            agent = Agent(store, memory, lambda text: provider.embed(args.embedding_model, text),
                          args.embedding_model, provider, json.loads(args.models.read_text()))
            report = agent.run(args.task, args.output, args.budget, output_tokens=args.output_tokens,
                               debate_models=args.debate_models, judge=args.judge)
            print(json.dumps(report, indent=2))
            return int(report['status'] != 'completed')
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as exc:
        # Do not print raw provider output or environment values.
        print(f'runtime failed ({type(exc).__name__}); check configuration and local artifacts', file=__import__('sys').stderr)
        return 2
    finally:
        for store in stores: store.close()
    return 0


if __name__ == '__main__': raise SystemExit(main())
