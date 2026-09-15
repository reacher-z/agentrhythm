#!/usr/bin/env python3
"""Check that the readable resource index mirrors the canonical JSON index."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
resources = json.loads((ROOT / 'dist' / 'resources.json').read_text())['resources']
markdown = (ROOT / 'dist' / 'resources.md').read_text()

assert markdown.startswith('# AgentRhythm resource index\n')
for resource in resources:
    assert f"## {resource['title']}\n" in markdown
    assert f"- Research task: {resource['task']}\n" in markdown
    assert f"- Relevance: {resource['relevance']}\n" in markdown
    for label, url in resource['source_links'].items():
        assert f"  - [{label}]({url})\n" in markdown
print(f'validated {len(resources)} Markdown resource entries')
