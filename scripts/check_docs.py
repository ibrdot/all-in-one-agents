#!/usr/bin/env python3
"""Check maintained project Markdown local links, GitHub heading anchors and SVGs.

Imported skill corpora and archived plans are outside this maintained-doc scope.
External HTTP URLs are listed, not asserted reachable by this offline checker.
"""
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote,urlsplit
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]


def anchors(text):
    used={};result=set()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',text,re.M):
        title=re.sub(r'<[^>]+>','',title).lower()
        slug=''.join(c for c in title if c in ' -_' or unicodedata.category(c)[0] in 'LN').replace(' ','-')
        n=used.get(slug,0);used[slug]=n+1;result.add(slug+(f'-{n}' if n else ''))
    result.update(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)',text))
    return result


def documents(root):
    root=Path(root)
    return sorted(set(root.glob('*.md'))|set(p for p in (root/'docs').rglob('*.md') if 'plans' not in p.relative_to(root/'docs').parts))


def check(root=ROOT):
    root=Path(root).resolve();errors=[];external=set();docs=documents(root)
    for path in docs:
        text=re.sub(r'```.*?```','',path.read_text(),flags=re.S)
        prev=0
        for hashes in re.findall(r'^(#{1,6})\s+.+?\s*#*$',text,re.M):
            lvl=len(hashes)
            if prev and lvl>prev+1:
                errors.append(f'{path.relative_to(root)}: heading level skip h{prev} -> h{lvl}')
            prev=lvl
        for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)',text):
            parts=urlsplit(target)
            if parts.scheme in ('http','https','mailto'):external.add(target);continue
            if parts.scheme:continue
            dest=(path.parent/unquote(parts.path)).resolve() if parts.path else path
            if not dest.is_relative_to(root):errors.append(f'{path.relative_to(root)}: escapes repo: {target}');continue
            if not dest.exists():errors.append(f'{path.relative_to(root)}: missing {target}');continue
            if parts.fragment and dest.suffix=='.md' and unquote(parts.fragment) not in anchors(dest.read_text()):
                errors.append(f'{path.relative_to(root)}: missing anchor {target}')
    svgs=list(root.glob('docs/**/*.svg'))+list(root.glob('assets/**/*.svg'))
    for svg in svgs:
        try:
            element=ET.parse(svg).getroot()
            if element.tag!='{http://www.w3.org/2000/svg}svg' or not element.get('viewBox'):raise ValueError('SVG namespace/viewBox required')
            if any(e.tag.endswith('script') or any(k.lower().startswith('on') for k in e.attrib) for e in element.iter()):raise ValueError('active SVG content')
        except (ET.ParseError,ValueError) as exc:errors.append(f'{svg.relative_to(root)}: {exc}')
    return dict(documents=len(docs),local_svg_files=len(svgs),external_urls=sorted(external),errors=errors)


if __name__=='__main__':
    import json
    report=check();print(json.dumps(report,indent=2));raise SystemExit(bool(report['errors']))
