#!/usr/bin/env python3
"""Verify the human question directory mirrors AgentRhythm's canonical resources."""
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
resources = json.loads((ROOT / 'dist' / 'resources.json').read_text())['resources']
html = (ROOT / 'dist' / 'questions' / 'index.html').read_text()

class Directory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.h3, self.links = set(), [], set()
        self.in_h3 = False
        self.parts = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article' and attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'h3':
            self.in_h3, self.parts = True, []
        if tag == 'a' and attrs.get('href', '').startswith('https://'):
            self.links.add(attrs['href'])
    def handle_endtag(self, tag):
        if tag == 'h3':
            self.h3.append(''.join(self.parts).strip())
            self.in_h3 = False
    def handle_data(self, data):
        if self.in_h3:
            self.parts.append(data)

directory = Directory(); directory.feed(html)
assert len(resources) == 29
for resource in resources:
    # Source text is checked independently from the public task anchors.
    assert resource['title'] in directory.h3, resource['title']
    for url in resource['source_links'].values():
        assert url in directory.links, url
assert len(directory.h3) == len(resources)
print(f'validated {len(resources)} question-directory entries and source links')
