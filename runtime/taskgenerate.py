"""Explicit opt-in live task generation; does NOT execute candidate code.

No default endpoint/model. A call cap is not a dollar billing limit. Graders stay
local and are never sent to the provider. Run grading separately in isolation.
"""
import argparse
import json
from pathlib import Path
import sys
from runtime.providers import OpenAICompatible
from runtime.taskbench import load_tasks,generate


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tasks',type=Path,default=Path(__file__).resolve().parents[1]/'evals/tasks/tasks.json')
    p.add_argument('--base-url',required=True)
    p.add_argument('--model',required=True)
    p.add_argument('--key-env',default='OPENAI_API_KEY')
    p.add_argument('--max-calls',type=int,required=True)
    p.add_argument('--max-output-tokens',type=int,default=2048)
    p.add_argument('--allow-network',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if not args.allow_network:p.error('--allow-network required: provider may bill requests')
    try:
        if args.output.exists():raise ValueError('output must be new')
        tasks=load_tasks(args.tasks)
        provider=OpenAICompatible(args.base_url,args.key_env,max_output_tokens=args.max_output_tokens)
        result=generate(tasks,provider,args.model,args.max_calls)
        # Exclusive creation; never overwrite previous runs.
        import os
        fd=os.open(args.output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:json.dump(result,f,indent=2)
        print(json.dumps(dict(responses=len(result['responses']),errors=len(result['errors']),model=args.model)))
        return int(bool(result['errors']))
    except (ValueError,OSError,KeyError,TypeError):
        print('Generation failed; check endpoint, task suite and configuration',file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
