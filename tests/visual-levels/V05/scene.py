"""V05 pendulum numbers tied to geometry — silent cue-driven preview.

Concept: displayed theta equals drawn swing angle (both in deg) because
geometry and readout derive from one shared theta ValueTracker.
Storyboard: tests/visual-levels/V05/storyboard.json (V05Scene: swing-out, swing-back).

Silent preview (authored durations, no speech):
    /Users/choclate/Desktop/Gnos/.venv/bin/python skills/manim-voice-animation/scripts/voice_synthesizer.py \
        --storyboard tests/visual-levels/V05/storyboard.json --out tests/visual-levels/V05/audio --silent
    GNOS_MANIFEST=tests/visual-levels/V05/audio/timing_manifest.json \
    /Users/choclate/Desktop/Gnos/.venv/bin/python skills/manim-voice-animation/scripts/render_pipeline.py \
        render tests/visual-levels/V05/scene.py V05Scene -q l -o tests/visual-levels/V05/preview.mp4
"""
from pathlib import Path
import os
import sys

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills" / "manim-voice-animation" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from cue_player import CuePlayer

PIVOT_Y = 2.0
L_VAL = 2.5
OUT_DEG = 30.0
BACK_DEG = -30.0


class V05Scene(Scene):
    def construct(self):
        self.camera.background_color = "#101c27"
        here = Path(__file__).parent
        manifest = Path(os.environ.get("GNOS_MANIFEST", str(here / "audio" / "timing_manifest.json")))
        player = CuePlayer(self, manifest, "V05Scene")

        pivot = np.array([0.0, PIVOT_Y, 0.0])

        def bob_point(deg):
            rad = deg * DEGREES
            return pivot + L_VAL * np.array([np.sin(rad), -np.cos(rad), 0.0])

        theta = ValueTracker(0.0)

        pivot_dot = Dot(pivot, color=WHITE, radius=0.08)
        pivot_label = Text("pivot", font_size=20, color=GREY_B).next_to(pivot_dot, UP, buff=0.12)

        # Static vertical reference so the drawn swing angle is inspectable.
        plumb = DashedLine(pivot, pivot + DOWN * 2.9, color=GREY_D, stroke_width=2)

        string = Line(pivot, bob_point(0.0), color=GREY_B, stroke_width=5)
        bob = Dot(bob_point(0.0), color=YELLOW, radius=0.18)

        theta_title = Text("theta", font_size=24, color=WHITE)
        readout = DecimalNumber(
            0.0, num_decimal_places=1, mob_class=Text,
            font_size=36, color=YELLOW,
        )
        deg_unit = Text("deg", font_size=24, color=GREY_B)
        readout_row = VGroup(readout, deg_unit).arrange(RIGHT, buff=0.15)
        readout_block = VGroup(theta_title, readout_row).arrange(DOWN, buff=0.12)
        readout_block.move_to(RIGHT * 4.2 + UP * 1.2)

        l_label = Text("L", font_size=24, color=GREY_B)
        l_label.move_to((pivot + bob_point(0.0)) / 2.0 + RIGHT * 0.3)

        title = Text("Pendulum angle = readout", font_size=28, color=WHITE).to_edge(UP, buff=0.3)

        def sync(mob):
            deg = theta.get_value()
            target = bob_point(deg)
            string.put_start_and_end_on(pivot, target)
            bob.move_to(target)
            readout.set_value(deg)
            l_label.move_to((pivot + target) / 2.0 + RIGHT * 0.3)

        string.add_updater(sync)

        self.add(title, plumb, pivot_dot, pivot_label, string, bob, readout_block, l_label)

        player.play("swing-out", theta.animate.set_value(OUT_DEG), run_time=4.0)
        player.play("swing-back", theta.animate.set_value(BACK_DEG), run_time=4.0)

        string.clear_updaters()
        player.finish(str(here / "lesson"))
