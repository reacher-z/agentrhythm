#!/usr/bin/env python3
"""Build a standard Atom feed from AgentRhythm's canonical resource index."""
import hashlib
import json
from datetime import date
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dist" / "resources.json"
OUTPUT = ROOT / "dist" / "resources.xml"
ATOM = "http://www.w3.org/2005/Atom"
ET.register_namespace("", ATOM)


def tag(name):
    return f"{{{ATOM}}}{name}"


def primary_source(links):
    for label in ("Paper", "arXiv", "Project", "Article"):
        if label in links:
            return links[label]
    return next(iter(links.values()))


def main():
    data = json.loads(SOURCE.read_text())
    feed = ET.Element(tag("feed"))
    ET.SubElement(feed, tag("id")).text = "https://agentrhythm.org/resources.xml"
    ET.SubElement(feed, tag("title")).text = "AgentRhythm research resources"
    ET.SubElement(feed, tag("updated")).text = date.fromisoformat(data["updated"]).isoformat() + "T00:00:00Z"
    ET.SubElement(feed, tag("link"), {"rel": "self", "href": "https://agentrhythm.org/resources.xml", "type": "application/atom+xml"})
    ET.SubElement(feed, tag("link"), {"rel": "alternate", "href": "https://agentrhythm.org/questions/", "type": "text/html"})
    ET.SubElement(feed, tag("subtitle")).text = data["scope"]
    for resource in data["resources"]:
        entry = ET.SubElement(feed, tag("entry"))
        digest = hashlib.sha256(resource["title"].encode()).hexdigest()
        ET.SubElement(entry, tag("id")).text = f"urn:agentrhythm:resource:{digest}"
        ET.SubElement(entry, tag("title")).text = resource["title"]
        ET.SubElement(entry, tag("updated")).text = date.fromisoformat(data["updated"]).isoformat() + "T00:00:00Z"
        ET.SubElement(entry, tag("link"), {"rel": "alternate", "href": "https://agentrhythm.org/questions/", "type": "text/html"})
        ET.SubElement(entry, tag("link"), {"rel": "related", "href": primary_source(resource["source_links"]), "type": "text/html", "title": "Original source"})
        ET.SubElement(entry, tag("category"), {"term": resource["task"]})
        ET.SubElement(entry, tag("summary"), {"type": "text"}).text = f"Research task: {resource['task']}. Relevance: {resource['relevance']}"
    ET.indent(feed, space="  ")
    OUTPUT.write_text('<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(feed, encoding="unicode") + "\n")


if __name__ == "__main__":
    main()
