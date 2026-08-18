#!/usr/bin/env python3
"""Collect deterministic audit signals from a local HTML document."""

from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.in_title = False
        self.descriptions: list[str] = []
        self.headings: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, object]] = []
        self.inputs_without_labels: list[str] = []
        self.ids: set[str] = set()
        self.label_fors: set[str] = set()
        self.pending_heading: dict[str, str] | None = None
        self.pending_link: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(str(data["id"]))
        if tag == "title":
            self.in_title = True
        elif tag == "meta" and str(data.get("name", "")).lower() == "description":
            self.descriptions.append(str(data.get("content", "")).strip())
        elif tag in {f"h{i}" for i in range(1, 7)}:
            self.pending_heading = {"level": tag[1], "text": ""}
        elif tag == "a":
            self.pending_link = {"href": str(data.get("href", "")), "text": ""}
        elif tag == "img":
            self.images.append({"src": data.get("src", ""), "has_alt": "alt" in data, "alt": data.get("alt")})
        elif tag == "label" and data.get("for"):
            self.label_fors.add(str(data["for"]))
        elif tag in {"input", "select", "textarea"}:
            input_type = str(data.get("type", "text")).lower()
            if input_type not in {"hidden", "submit", "button", "reset"} and not data.get("aria-label") and not data.get("aria-labelledby"):
                element_id = str(data.get("id", ""))
                if element_id:
                    self.inputs_without_labels.append(element_id)
                else:
                    self.inputs_without_labels.append(f"{tag} without id")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag in {f"h{i}" for i in range(1, 7)} and self.pending_heading:
            self.pending_heading["text"] = self.pending_heading["text"].strip()
            self.headings.append(self.pending_heading)
            self.pending_heading = None
        elif tag == "a" and self.pending_link:
            self.pending_link["text"] = self.pending_link["text"].strip()
            self.links.append(self.pending_link)
            self.pending_link = None

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.pending_heading is not None:
            self.pending_heading["text"] += data
        if self.pending_link is not None:
            self.pending_link["text"] += data


def audit(path: Path) -> dict[str, object]:
    parser = AuditParser()
    parser.feed(path.read_text(encoding="utf-8"))
    unlabeled = [item for item in parser.inputs_without_labels if item.endswith("without id") or item not in parser.label_fors]
    empty_links = [link for link in parser.links if not link["text"]]
    findings: list[dict[str, str]] = []
    title = "".join(parser.title_parts).strip()
    if not title:
        findings.append({"priority": "P1", "category": "SEO", "finding": "Missing page title"})
    if not parser.descriptions or not parser.descriptions[0]:
        findings.append({"priority": "P2", "category": "SEO", "finding": "Missing meta description"})
    if sum(1 for heading in parser.headings if heading["level"] == "1") != 1:
        findings.append({"priority": "P1", "category": "Accessibility", "finding": "Page should have one clear H1"})
    for image in parser.images:
        if not image["has_alt"]:
            findings.append({"priority": "P1", "category": "Accessibility", "finding": f"Image missing alt attribute: {image['src']}"})
    for element in unlabeled:
        findings.append({"priority": "P1", "category": "Accessibility", "finding": f"Form control lacks an accessible label: {element}"})
    for link in empty_links:
        findings.append({"priority": "P1", "category": "Accessibility", "finding": f"Link has no text alternative: {link['href']}"})
    return {"file": str(path), "title": title, "meta_descriptions": parser.descriptions, "headings": parser.headings, "image_count": len(parser.images), "link_count": len(parser.links), "findings": findings, "manual_checks_required": ["keyboard and focus", "contrast and states", "zoom and reflow", "screen-reader flow", "form errors", "motion"]}


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("html", type=Path)
    cli.add_argument("--json", type=Path)
    args = cli.parse_args()
    result = audit(args.html)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.json:
        args.json.write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
