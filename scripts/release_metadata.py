#!/usr/bin/env python3
"""Synchronize first-party release versions locally; never invoke Git or network."""
import argparse
import json
from pathlib import Path
import re


def paths(root):
    root=Path(root)
    items=[root/'package.json',root/'gemini-extension.json']
    items+=sorted(root.glob('.*-plugin/*.json'))
    items+=sorted(root.glob('.gemini/*.json'))+sorted(root.glob('.pi/*.json'))
    return list(dict.fromkeys(p for p in items if p.is_file()))


def versions(root):
    rows=[]
    for path in paths(root):
        data=json.loads(path.read_text())
        if 'version' in data:rows.append((str(path),'{}'.format(data['version'])))
        for plugin in data.get('plugins',[]):
            if 'version' in plugin:rows.append((str(path)+'#'+plugin.get('name','plugin'),plugin['version']))
    return rows


def update(root,version):
    if not isinstance(version,str) or not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)',version):
        raise ValueError('stable semantic version required, e.g. 1.5.0')
    pending=[]
    for path in paths(root):
        if path.is_symlink():raise ValueError('symlinked metadata refused')
        data=json.loads(path.read_text())
        if 'version' in data:data['version']=version
        for plugin in data.get('plugins',[]):
            if 'version' in plugin:plugin['version']=version
        pending.append((path,json.dumps(data,indent=2)+'\n'))
    # Validate all JSON before any writes; caller reviews diffs before committing.
    for path,content in pending:path.write_text(content)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('version',nargs='?')
    p.add_argument('--check',action='store_true')
    args=p.parse_args();root=Path(__file__).resolve().parents[1]
    if args.check:
        expected=json.loads((root/'package.json').read_text())['version']
        stale=[path for path,value in versions(root) if value!=expected]
        if stale:p.exit(1,'version drift: '+', '.join(stale)+'\n')
        print(f'all release versions match {expected}');return
    if not args.version:p.error('version or --check required')
    try:update(root,args.version)
    except (ValueError,OSError,TypeError) as exc:p.exit(2,str(exc)+'\n')
    print('metadata updated locally; review changelog and diffs before release')


if __name__=='__main__':main()
