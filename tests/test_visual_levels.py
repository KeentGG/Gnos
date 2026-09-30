"""Visual-levels contract: 41 prompts; S+V built locally, with selected MCP artifacts.

Fast by default (no renders). Checks structure, artifact presence, and honesty:
no SVG fallbacks, no learner-record writes.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VDIR = ROOT / "tests" / "visual-levels"


class VisualLevelsTests(unittest.TestCase):
    def test_matrix_has_41_prompts(self):
        matrix = json.loads((VDIR / "matrix.json").read_text())
        self.assertEqual(len(matrix), 41)
        ids = [m["id"] for m in matrix]
        for track in "ESV":
            self.assertEqual(len([i for i in ids if i.startswith(track)]), 10)
        self.assertEqual(len([i for i in ids if i.startswith("P")]), 11)
        for m in matrix:
            for key in ("id", "track", "level", "subject", "claim", "brief",
                        "must_include", "continuity", "acceptance", "skill_route", "output"):
                self.assertIn(key, m)
            self.assertNotEqual(m["output"], "output.svg", f'{m["id"]}: no SVG outputs allowed')

    def test_all_folders_have_prompt_and_meta(self):
        matrix = json.loads((VDIR / "matrix.json").read_text())
        for m in matrix:
            d = VDIR / m["id"]
            self.assertTrue((d / "prompt.md").exists(), m["id"])
            self.assertTrue((d / "meta.json").exists(), m["id"])

    def test_no_svg_diagram_outputs(self):
        # Manim's media/ render cache legitimately contains text SVGs; the ban
        # is on SVG files claimed as E/P diagram artifacts at folder top level.
        svgs = [p for p in VDIR.glob("*/output.svg")]
        self.assertEqual(svgs, [], f"SVG fallbacks forbidden: {svgs}")

    def test_simulation_track_built(self):
        for i in range(1, 11):
            pid = f"S{i:02d}"
            out = VDIR / pid / "sim.html"
            self.assertTrue(out.exists(), pid)
            self.assertGreater(out.stat().st_size, 2000, pid)
            txt = out.read_text(errors="ignore")
            self.assertNotIn("fetch(", txt, pid)
            self.assertIn("reset", txt.lower(), pid)

    def test_video_track_built(self):
        for i in range(1, 11):
            pid = f"V{i:02d}"
            self.assertTrue((VDIR / pid / "storyboard.json").exists(), pid)
            sb = json.loads((VDIR / pid / "storyboard.json").read_text())
            scenes = sb.get("scenes", [sb] if "scenes" not in sb else [])
            self.assertTrue(scenes, pid)
            mp4 = VDIR / pid / "preview.mp4"
            self.assertTrue(mp4.exists(), pid)
            self.assertGreater(mp4.stat().st_size, 10000, pid)

    def test_ep_track_honest_pending(self):
        # E/P outputs must come from the real MCP servers, never faked files.
        for prefix in ("E", "P"):
            for i in range(1, 12 if prefix == "P" else 11):
                pid = f"{prefix}{i:02d}"
                d = VDIR / pid
                self.assertFalse(list(d.glob("*.svg")), pid)
                meta = json.loads((d / "meta.json").read_text())
                self.assertIn(meta.get("producer"), ("excalidraw-mcp", "pinepaper-mcp"), pid)

    def test_gallery_and_scores_exist(self):
        self.assertTrue((VDIR / "index.html").exists())
        self.assertTrue((VDIR / "scores.auto.json").exists())
        page = (VDIR / "index.html").read_text()
        for pid in ("S01", "V01", "E01", "P01"):
            self.assertIn(pid, page)

    def test_no_learner_pollution(self):
        # Visual tests must not write real learner records.
        for m in json.loads((VDIR / "matrix.json").read_text()):
            txt = (VDIR / m["id"] / "prompt.md").read_text()
            self.assertNotIn("learners/", txt)

    def test_p11_pinepaper_widget_is_embedded_and_present(self):
        widget = VDIR / "P11" / "output.html"
        self.assertTrue(widget.is_file(), "P11 gallery iframe needs a real HTML export")
        self.assertIn('src="P11/output.html"', (VDIR / "index.html").read_text())
        self.assertIn("P11", {m["id"] for m in json.loads((VDIR / "matrix.json").read_text())})
        self.assertGreater(widget.stat().st_size, 2000)


if __name__ == "__main__":
    unittest.main()
