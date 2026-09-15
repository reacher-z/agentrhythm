#!/usr/bin/env python3
"""Render the independent AgentRhythm resource index as Markdown."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "dist" / "resources.json"
OUTPUT = ROOT / "dist" / "resources.md"


def main():
    data = json.loads(RESOURCES.read_text())
    lines = [
        "# AgentRhythm resource index",
        "",
        "This Markdown index mirrors the canonical [resource JSON](https://agentrhythm.org/resources.json). "
        "Use each linked original source for authorship, citation, version, licensing, metrics, and reuse conditions.",
        "",
    ]
    for resource in data["resources"]:
        lines.extend([
            f"## {resource['title']}",
            "",
            f"- Research task: {resource['task']}",
            f"- Relevance: {resource['relevance']}",
            "- Original sources:",
        ])
        lines.extend(f"  - [{name}]({url})" for name, url in resource["source_links"].items())
        lines.append("")
    OUTPUT.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
