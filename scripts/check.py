#!/usr/bin/env python3
"""Validate generated HTML links, guide parity, metadata, and public content boundaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.ids=[]; self.h1=0; self.images=[]; self.meta={}
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag=='h1': self.h1+=1
        if tag=='img': self.images.append(attrs)
        if tag=='meta': self.meta[attrs.get('name',attrs.get('property',''))]=attrs.get('content','')
        for key in ['href','src']:
            if attrs.get(key): self.refs.append(attrs[key])

def main():
    pages={}; errors=[]
    for path in ROOT.rglob('*.html'):
        parser=Page(); parser.feed(path.read_text()); pages[path.resolve()]=parser
    for path, page in pages.items():
        source=path.read_text(); name=str(path.relative_to(ROOT))
        redirect='http-equiv="refresh"' in source
        if len(page.ids)!=len(set(page.ids)): errors.append(f'{name}: duplicate IDs')
        if not redirect:
            if page.h1!=1: errors.append(f'{name}: expected one H1')
            for key in ['description','viewport','og:title','og:image']:
                if not page.meta.get(key): errors.append(f'{name}: missing {key}')
        for image in page.images:
            if 'alt' not in image: errors.append(f'{name}: missing image alt')
        for ref in page.refs:
            url=urlsplit(ref)
            if url.scheme or url.netloc: continue
            target=(ROOT/unquote(url.path.lstrip('/'))) if url.path.startswith('/') else path.parent/unquote(url.path) if url.path else path
            target=target.resolve()
            if not target.exists(): errors.append(f'{name}: missing {ref}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids: errors.append(f'{name}: missing fragment {ref}')
        if '/wiki/' in name and re.search(r'Technical SO|ScriptableObject|EnemyBuildConfig|SaveData|0021fcdc|10-testing|github.com/Wolfs0ng/CarnageClub|<pre|\.asset\b',source,re.I):
            errors.append(f'{name}: internal content in public guide')
        if 'dmytro-tarasenko-54511564' in source: errors.append(f'{name}: old LinkedIn URL')
    guide=json.loads((ROOT/'content/guide.json').read_text())
    for lang in ['ua','en']:
        folder=ROOT/'projects/carnage-club/wiki'/lang
        expected={p['slug']+'.html' for p in guide['pages']}
        if {p.name for p in folder.glob('*.html')}!=expected: errors.append(f'{lang}: guide page mismatch')
        search=json.loads((folder/'search.json').read_text())
        if {p['url'] for p in search}!=expected: errors.append(f'{lang}: search index mismatch')
    if errors:
        print('\n'.join(errors));sys.exit(1)
    print(f'PASS: {len(pages)} HTML pages, all local links and anchors, metadata, image labels, guide language parity, search coverage, and public-content boundaries.')

if __name__=='__main__':main()
