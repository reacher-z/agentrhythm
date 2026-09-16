#!/usr/bin/env python3
"""Verify the Atom resource feed mirrors the canonical resource index."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
resources = json.loads((ROOT / "dist" / "resources.json").read_text())["resources"]
ns = {"atom": "http://www.w3.org/2005/Atom"}
root = ET.parse(ROOT / "dist" / "resources.xml").getroot()
assert root.findtext("atom:id", namespaces=ns) == "https://agentrhythm.org/resources.xml"
entries = root.findall("atom:entry", ns)
assert len(entries) == len(resources)
for entry, resource in zip(entries, resources):
    assert entry.findtext("atom:title", namespaces=ns) == resource["title"]
    summary = entry.findtext("atom:summary", namespaces=ns)
    assert resource["task"] in summary and resource["relevance"] in summary
    links = {link.attrib.get("rel"): link.attrib.get("href") for link in entry.findall("atom:link", ns)}
    assert links["alternate"] == "https://agentrhythm.org/questions/"
    assert links["related"] in resource["source_links"].values()
for page in (ROOT / "dist" / "index.html", ROOT / "dist" / "questions" / "index.html"):
    html = page.read_text()
    assert 'type="application/atom+xml" title="Research resource feed" href="/resources.xml"' in html
sitemap = (ROOT / "dist" / "sitemap.xml").read_text()
assert "https://agentrhythm.org/resources.xml" in sitemap
assert "https://agentrhythm.org/resources.json" in sitemap
assert "https://agentrhythm.org/resources.xml" in (ROOT / "dist" / "llms.txt").read_text()
print(f"validated {len(resources)} Atom resource entries")
