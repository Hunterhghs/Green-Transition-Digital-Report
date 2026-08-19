"""Unit tests for the Veles Phase-4 gate on the shipped index.html.

Run from the repository root:  python3 -m unittest test_report.py -v
"""
import re
import unittest
from html.parser import HTMLParser

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


class ReportGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("index.html", encoding="utf-8") as f:
            cls.src = f.read()
        cls.main = cls.src.split("<main>")[1].split("</main>")[0]
        cls.ids = set(re.findall(r'id="([^"]+)"', cls.src))
        cls.canvases = set(re.findall(r'<canvas id="([^"]+)"', cls.src))

    def test_html_parses(self):
        parser = WellFormed()
        parser.feed(self.src)
        self.assertEqual(parser.errors, [])
        self.assertEqual(parser.stack, [])

    def test_anchors_resolve(self):
        hrefs = set(re.findall(r'href="#([^"]+)"', self.src))
        self.assertTrue(hrefs <= self.ids, f"missing targets: {hrefs - self.ids}")

    def test_chart_canvases_wired(self):
        lookups = set(re.findall(r'getElementById\("([^"]+)"\)', self.src))
        self.assertTrue(self.canvases <= lookups, f"orphan canvases: {self.canvases - lookups}")

    def test_external_links_clean(self):
        links = re.findall(r'href="(https?://[^"]+)"', self.src)
        bad = [l for l in links if "(" in l or ")" in l or not l.startswith("https://")]
        self.assertGreaterEqual(len(links), 10)
        self.assertEqual(bad, [])

    def test_no_cjk_leaks(self):
        self.assertEqual(re.findall(r"[\u4e00-\u9fff]", self.src), [])

    def test_content_density(self):
        sections = len(re.findall(r"<section id=", self.src))
        words = len(re.sub(r"<[^>]+>", " ", self.main).split())
        lines = self.src.count("\n") + 1
        self.assertGreaterEqual(sections, 8)
        self.assertGreaterEqual(words, 1800)
        self.assertGreaterEqual(lines, 500)

    def test_interactive_charts(self):
        self.assertGreaterEqual(len(self.canvases), 4)

    def test_binding_term_present(self):
        self.assertIn("Binding term", self.src)
        self.assertIn("Read every green-transition headline", self.src)

    def test_no_placeholders(self):
        self.assertIsNone(re.search(r"lorem|TODO|FIXME|placeholder", self.src, re.I))


if __name__ == "__main__":
    unittest.main()
