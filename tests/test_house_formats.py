"""Behavioral checks for the three desk formats and legacy compatibility."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "plugins" / "apac-equity-desk" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from render_market_wrap import render as close
from render_market_color import render as theme
from render_morning_brief import render as morning

FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class HouseFormatTests(unittest.TestCase):
    def test_close_keeps_all_sector_names_and_final_company_updates(self):
        pack = fixture("japan_close_house.json")
        result = close(pack)
        market = pack["markets"][0]
        previous = -1
        for field in ("lead", "local_policy", "fx_rates", "macro_data", "sector_laggards", "sector_leaders"):
            for entry in market[field]:
                paragraph = entry["summary"] if isinstance(entry, dict) else entry
                position = result.index(paragraph)
                self.assertGreater(position, previous)
                previous = position
        self.assertGreater(result.index("EXAMPLE INDUSTRIAL:"), previous)
        self.assertIn("Example Trading B -0.9%", result)
        self.assertNotIn("n/a", result)
        self.assertNotIn("None identified", result)
        self.assertNotIn("Tomorrow:", result)

    def test_optional_close_sections_are_omitted_not_invented(self):
        pack = fixture("japan_close_house.json")
        for key in ("local_policy", "fx_rates", "macro_data", "sector_laggards", "sector_leaders", "corporate_headlines"):
            pack["markets"][0].pop(key)
        result = close(pack)
        self.assertNotIn("Corporate Headlines", result)
        self.assertIn(pack["markets"][0]["lead"][0]["summary"], result)

    def test_open_market_cannot_be_rendered_as_close(self):
        pack = fixture("japan_close_house.json")
        pack["markets"][0]["session"] = "open"
        with self.assertRaisesRegex(ValueError, "session=closed"):
            close(pack)

    def test_theme_preserves_opposing_evidence_and_distinct_exposures(self):
        pack = fixture("optical_theme_house.json")
        result = theme(pack)
        for observation in pack["mixed_evidence"] + pack["implications"] + pack["watch"]:
            self.assertIn(observation, result)
        self.assertIn("alternative explanation", result)
        self.assertIn("EXAMPLE-LENS-A TT Equity  \nEXAMPLE-LENS-B TT Equity", result)
        self.assertNotIn("Catalyst:", result)

    def test_inline_sources_survive_each_format(self):
        for renderer, name in ((close, "japan_close_house.json"), (theme, "optical_theme_house.json"), (morning, "japan_morning_house.json")):
            pack = fixture(name)
            result = renderer(pack)
            self.assertIn("[Synthetic desk fixture](https://example.com/synthetic-desk-data)", result)
            self.assertTrue(result.startswith("DRAFT — HUMAN APPROVAL REQUIRED"))
            self.assertIn("SYNTHETIC EXAMPLE", result)

    def test_morning_opens_with_local_tape_before_overnight(self):
        pack = fixture("japan_morning_house.json")
        result = morning(pack)
        self.assertIn("{JA} JAPAN MORNING", result)
        self.assertLess(result.index("NKY +0.05%"), result.index("US equities softened"))
        self.assertLess(result.index("US equities softened"), result.index("AI hardware is the main drag"))
        self.assertIn("4.28% before ending New York at 4.24%", result)

    def test_pre_open_requires_expectations_and_rejects_live_tape(self):
        pack = fixture("japan_morning_house.json")
        pack["session"] = "pre_open"
        with self.assertRaisesRegex(ValueError, "cannot contain"):
            morning(pack)
        pack.pop("opening_tape")
        pack["pre_open_setup"] = ["Japan is yet to open; watch whether the overnight rates move weighs on exporters."]
        result = morning(pack)
        self.assertIn("{JA} JAPAN PRE-OPEN", result)
        self.assertNotIn("NKY +0.05%", result)

    def test_bad_timestamp_and_broken_source_references_fail(self):
        pack = fixture("japan_close_house.json")
        pack["as_of"] = "2026-09-18T15:45:00"
        with self.assertRaisesRegex(ValueError, "timezone"):
            close(pack)
        pack = fixture("japan_close_house.json")
        pack["markets"][0]["lead"][0]["source_ids"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "Unknown source"):
            close(pack)

    def test_no_unsupplied_joke_is_added_and_supplied_aside_is_kept(self):
        pack = fixture("japan_close_house.json")
        result = close(pack)
        self.assertNotIn("desk joke", result)
        pack["markets"][0]["desk_aside"] = "A supplied desk joke."
        result = close(pack)
        self.assertLess(result.index("A supplied desk joke."), result.index("Corporate Headlines"))

    def test_renderers_accept_json_from_command_line(self):
        with tempfile.TemporaryDirectory() as folder:
            for script, name in (("render_market_wrap.py", "japan_close_house.json"), ("render_market_color.py", "optical_theme_house.json"), ("render_morning_brief.py", "japan_morning_house.json")):
                destination = Path(folder) / (script + ".md")
                result = subprocess.run([sys.executable, str(SCRIPTS / script), str(FIXTURES / name), "--output", str(destination)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("SYNTHETIC EXAMPLE", destination.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
