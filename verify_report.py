#!/usr/bin/env python3
"""Veles Phase-4 verification gate for the Green Transition digital report.

Checks the shipped index.html for structural integrity, link hygiene,
chart wiring, content density, CJK leaks, and the binding-term close.
Run from the repository root:  python3 verify_report.py
"""
import re
import sys
from html.parser import HTMLParser

SRC_PATH = "index.html"
VOID = {"meta", "link", "br", "hr", "img", "input", "source", "area", "base", "col", "embed", "track", "wbr"}


class WellFormed(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(tag)


def main():
    src = open(SRC_PATH, encoding="utf-8").read()
    checks = []

    parser = WellFormed()
    parser.feed(src)
    checks.append(("HTML parse", not parser.errors and not parser.stack,
                   f"errors={parser.errors[:3]} unclosed={parser.stack[:3]}"))

    ids = set(re.findall(r'id="([^"]+)"', src))
    hrefs = set(re.findall(r'href="#([^"]+)"', src))
    checks.append(("Anchors resolve", hrefs <= ids, f"missing={hrefs - ids}"))

    canvases = set(re.findall(r'<canvas id="([^"]+)"', src))
    lookups = set(re.findall(r'getElementById\("([^"]+)"\)', src))
    checks.append(("Chart canvases wired", canvases <= lookups, f"orphan={canvases - lookups}"))

    links = re.findall(r'href="(https?://[^"]+)"', src)
    bad = [l for l in links if "(" in l or ")" in l or not l.startswith("https://")]
    checks.append(("External links clean", len(links) >= 10 and not bad,
                   f"{len(links)} links, bad={bad}"))

    cjk = re.findall(r"[\u4e00-\u9fff]", src)
    checks.append(("No CJK leaks", not cjk, f"{len(cjk)} CJK chars"))

    sections = len(re.findall(r"<section id=", src))
    main = src.split("<main>")[1].split("</main>")[0]
    words = len(re.sub(r"<[^>]+>", " ", main).split())
    lines = src.count("\n") + 1
    checks.append(("Content density", sections >= 8 and words >= 1800 and lines >= 500,
                   f"{sections} sections, {words} words, {lines} lines"))

    checks.append(("Interactive charts", len(canvases) >= 4, f"{len(canvases)} canvases"))

    checks.append(("Binding term present",
                   "Binding term" in src and "Read every green-transition headline" in src,
                   "closing directive"))

    checks.append(("No placeholder text",
                   not re.search(r"lorem|TODO|FIXME|placeholder", src, re.I), "clean"))

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(("PASS " if ok else "FAIL ") + name + " - " + detail)

    if failed:
        print(f"\nVeles Phase-4 gate: FAIL - {len(failed)} check(s)")
        return 1
    print("\nVeles Phase-4 gate: PASS - all checks green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
