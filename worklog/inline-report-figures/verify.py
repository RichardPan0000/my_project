# -*- coding: utf-8 -*-
"""Validate inline resources, SVG markup and fragment navigation without a browser."""
from pathlib import Path
from html.parser import HTMLParser
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[2]

class Document(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.ids, self.links, self.assets = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'img' or (tag == 'script' and 'src' in attrs) or (tag == 'link' and attrs.get('rel') == 'stylesheet'):
            self.assets.append(attrs)

missing_docs = set()
for path in root.glob('*.html'):
    source = path.read_text(encoding='utf-8')
    doc = Document()
    doc.feed(source)
    assert len(doc.ids) == len(set(doc.ids)), path.name + ': duplicate IDs'
    assert not doc.assets, path.name + ': external rendering resources'
    svgs = re.findall(r'<svg\b[\s\S]*?</svg>', source)
    for s in svgs:
        ET.fromstring(s)
    for link in doc.links:
        if link.startswith('#'):
            assert link[1:] in doc.ids, (path.name, link)
        elif link.endswith('.md') and not (root / link).exists():
            missing_docs.add(link)
        elif '.html' in link:
            target, _, fragment = link.partition('#')
            assert (root / target).is_file(), (path.name, link)
            if fragment:
                other = Document()
                other.feed((root / target).read_text(encoding='utf-8'))
                assert fragment in other.ids, (path.name, link)
    print('{}: {} valid SVGs; no external render assets; fragment navigation valid'.format(path.name,len(svgs)))
assert sum([148744,599942,194019]) == 942705
assert sum([375298,184059,500106]) == 1059463
for name in ['pv-accuracy', 'load-accuracy']:
    source = (root / (name + '-20261031.html')).read_text(encoding='utf-8')
    for metric in ['mape', 'mae']:
        assert re.search(r'<button[^>]+data-metric="' + metric + r'"[^>]+disabled', source)
print('Paired totals and unavailable metric states valid.')
print('Existing missing Markdown destinations: {}'.format(len(missing_docs)))
