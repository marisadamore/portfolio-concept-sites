#!/usr/bin/env python3
"""Inspect rendered HTML for deterministic accessibility signals."""
from __future__ import annotations
import argparse, json
from html.parser import HTMLParser
from pathlib import Path

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(); self.lang=""; self.title=""; self.in_title=False; self.h=[]; self.ids=[]; self.refs=[]; self.images=[]; self.controls=[]; self.iframes=[]; self.positive_tabindex=[]; self.landmarks=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="html": self.lang=str(a.get("lang", ""))
        if tag=="title": self.in_title=True
        if tag in {f"h{i}" for i in range(1,7)}: self.h.append(int(tag[1]))
        if a.get("id"): self.ids.append(str(a["id"]))
        for key in ("aria-labelledby","aria-describedby","aria-controls"):
            if a.get(key): self.refs.extend(str(a[key]).split())
        if tag=="img": self.images.append({"src":a.get("src",""),"has_alt":"alt" in a,"alt":a.get("alt")})
        if tag in {"button","input","select","textarea"}: self.controls.append({"tag":tag,"id":a.get("id",""),"name":a.get("aria-label") or a.get("title") or ""})
        if tag=="iframe": self.iframes.append({"src":a.get("src",""),"title":a.get("title","")})
        if str(a.get("tabindex","")).lstrip("+").isdigit() and int(str(a["tabindex"]))>0: self.positive_tabindex.append({"tag":tag,"tabindex":a["tabindex"]})
        if tag in {"main","nav","header","footer","aside"} or a.get("role") in {"main","navigation","banner","contentinfo","complementary"}: self.landmarks.append(tag)
    def handle_endtag(self, tag):
        if tag=="title": self.in_title=False
    def handle_data(self, data):
        if self.in_title: self.title+=data

def inspect(path):
    p=Inspector(); p.feed(path.read_text(encoding="utf-8")); issues=[]; warnings=[]; passes=[]
    if not p.lang: issues.append("Document language is missing")
    else: passes.append(f"Document language declared: {p.lang}")
    if not p.title.strip(): issues.append("Document title is missing")
    else: passes.append("Document has a title")
    if p.h.count(1)!=1: issues.append(f"Expected one H1; found {p.h.count(1)}")
    else: passes.append("Page has one H1")
    jumps=[(a,b) for a,b in zip(p.h,p.h[1:]) if b>a+1]
    if jumps: warnings.append(f"Heading level jumps found: {jumps}")
    missing_alt=[i["src"] for i in p.images if not i["has_alt"]]
    if missing_alt: issues.append(f"Images missing alt attributes: {missing_alt}")
    else: passes.append("All images have alt attributes")
    duplicates=sorted({x for x in p.ids if p.ids.count(x)>1})
    if duplicates: issues.append(f"Duplicate IDs: {duplicates}")
    unresolved=sorted({x for x in p.refs if x not in p.ids})
    if unresolved: issues.append(f"Unresolved ARIA ID references: {unresolved}")
    if p.positive_tabindex: issues.append(f"Positive tabindex changes focus order: {p.positive_tabindex}")
    untitled=[x["src"] for x in p.iframes if not x["title"]]
    if untitled: issues.append(f"Iframes missing titles: {untitled}")
    if "main" not in p.landmarks: warnings.append("No main landmark detected")
    return {"file":str(path),"confirmed_issues":issues,"warnings":warnings,"passed_checks":passes,"manual_tests_required":["keyboard and visible focus","320px reflow and 200% zoom","screen-reader flow and names","contrast in every state","reduced motion and slider controls","assistive-technology and disabled-user testing"]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("target",type=Path); ap.add_argument("--json",type=Path); args=ap.parse_args(); files=[args.target] if args.target.is_file() else sorted(args.target.rglob("*.html")); result={"pages":[inspect(f) for f in files]}; text=json.dumps(result,indent=2,ensure_ascii=False); print(text); args.json and args.json.write_text(text+"\n",encoding="utf-8")
if __name__=="__main__": main()
