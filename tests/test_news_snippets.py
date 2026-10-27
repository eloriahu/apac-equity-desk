"""Behavioral checks for sourced news-item rendering and cutoff labelling."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins" / "apac-equity-desk" / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "china_news_snippets.json"
sys.path.insert(0, str(SCRIPTS))
from render_news_snippets import render


class NewsSnippetsTests(unittest.TestCase):
    def setUp(self):
        self.pack = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_preserves_order_figures_qualifications_and_adjacent_sources(self):
        original = deepcopy(self.pack)
        result = render(self.pack)
        previous = -1
        sources = {source["id"]: source for source in self.pack["sources"]}
        for item in self.pack["items"]:
            prefix = item["headline"] + ": " if "headline" in item else ""
            position = result.index(prefix + item["summary"])
            self.assertGreater(position, previous)
            previous = position
            paragraph = result[position:].split("\n\n", 1)[0]
            for ref in item["source_ids"]:
                self.assertIn(sources[ref]["url"], paragraph)
        self.assertEqual(self.pack, original)
        self.assertGreater(result.index("Data gaps for review:"), previous)

    def test_digest_does_not_require_tape_or_impose_flash_length(self):
        self.pack["items"] *= 7
        result = render(self.pack)
        self.assertGreater(len(result.split()), 250)
        self.assertEqual(result.count(self.pack["items"][0]["summary"]), 7)
        self.assertNotIn("Things to watch", result)
        self.assertNotIn("No single catalyst", result)
        self.assertIn("China News Snippets:", result)

    def test_pre_open_and_retrospective_cutoffs_are_visible(self):
        result = render(self.pack)
        self.assertIn("PRE-OPEN | Information cutoff 2026-05-06T08:15:00+08:00", result)
        self.assertTrue(result.startswith("DRAFT — HUMAN APPROVAL REQUIRED"))
        self.assertIn("SYNTHETIC EXAMPLE", result)
        self.pack["retrospective"] = True
        self.assertIn("RETROSPECTIVE PRE-OPEN", render(self.pack))

    def test_contradictory_session_or_unzoned_cutoff_fails(self):
        for update in ({"session": "open"}, {"session": "closed"},
                       {"opening_tape": ["Observed opening move"]},
                       {"as_of": "2026-05-06T08:15:00"},
                       {"retrospective": "false"}):
            with self.subTest(update=update):
                pack = deepcopy(self.pack)
                pack.update(update)
                with self.assertRaises(ValueError):
                    render(pack)

    def test_uncited_or_broken_source_items_fail(self):
        for refs in (None, [], "company", ["missing"], [42]):
            with self.subTest(refs=refs):
                self.pack["items"][0]["source_ids"] = refs
                with self.assertRaises(ValueError):
                    render(self.pack)

    def test_empty_or_malformed_items_fail(self):
        for items in ([], "headline", [None], [{"summary": ""}],
                      [{"summary": "a\nb", "source_ids": ["company"]}],
                      [{"headline": "", "summary": "A fact.", "source_ids": ["company"]}]):
            with self.subTest(items=items):
                self.pack["items"] = items
                with self.assertRaises(ValueError):
                    render(self.pack)

    def test_cli_matches_renderer(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "snippets.md"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "render_news_snippets.py"),
                 str(FIXTURE), "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), render(self.pack))


if __name__ == "__main__":
    unittest.main()
