"""Explicit local memory put/search/delete. No network or automatic capture.

Embeddings are supplied as JSON from one caller-selected embedding space. The
CLI never creates fake vectors or requests credentials. SQLite is not encrypted.
"""
import argparse
import json
import math
import os
from pathlib import Path
import sqlite3
import sys
from runtime.core import Memory, vector


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    put=sub.add_parser('put');put.add_argument('--input',type=Path,required=True)
    search=sub.add_parser('search');search.add_argument('--embedding',type=Path,required=True)
    search.add_argument('--embedding-model',required=True)
    search.add_argument('--limit',type=int,default=5)
    search.add_argument('--min-score',type=float,default=.25)
    delete=sub.add_parser('delete');delete.add_argument('--id',required=True)
    for command in (put,search,delete):command.add_argument('--database',type=Path,required=True)
    args=p.parse_args();store=None
    try:
        path=args.database.absolute()
        if any(x.is_symlink() for x in (path,*path.parents)):raise ValueError('symlink database path refused')
        if args.command=='put':
            entry=json.loads(args.input.read_text())
            for key in ('id','text','embedding_model'):
                if not isinstance(entry[key],str) or not entry[key].strip():raise ValueError('nonempty fields required')
            vector(entry['embedding'])
            if not isinstance(entry.get('metadata',{}),dict):raise ValueError('metadata must be an object')
            json.dumps(entry,allow_nan=False)
            # Exclusive private creation for a new DB; no permissions changes to
            # pre-existing operator-owned databases. No cross-process lock here.
            if not path.exists():
                fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd)
            store=Memory(path)
            store.put(entry['id'],entry['text'],entry['embedding'],entry['embedding_model'],entry.get('metadata'))
            print(json.dumps(dict(saved=entry['id'])))
        else:
            if not path.is_file():raise ValueError('existing database required')
            if args.command=='search':
                embedding=json.loads(args.embedding.read_text());vector(embedding)
                if args.limit<1 or not math.isfinite(args.min_score) or not -1<=args.min_score<=1:raise ValueError('invalid search bounds')
                # Read-only URI: reads must not create or alter a database.
                store=Memory.__new__(Memory)
                store.db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
                print(json.dumps(dict(results=store.search(embedding,args.embedding_model,args.limit,args.min_score)),indent=2))
            else:
                store=Memory(path);store.delete(args.id)
                print(json.dumps(dict(deleted=args.id)))
        return 0
    except (ValueError,OSError,KeyError,TypeError,sqlite3.Error,RecursionError):
        print('Memory operation failed; check input, path and embedding space',file=sys.stderr);return 2
    finally:
        if store is not None:store.close()


if __name__=='__main__':raise SystemExit(main())
