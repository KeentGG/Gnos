"""V04 basis rotation: tracker-driven Rotate of e1/e2 with det readout.

Storyboard notes:
- concept ID: math.basis.rotation-det
- prereq: vectors as arrows on a grid; rotation preserves area.
- hypotheses: R(alpha) rotates e1=[1,0] and e2=[0,1] together;
  alpha 0 -> 90 deg; det(R) = 1 throughout.
- success check: learner predicts e1->[0,1], e2->[-1,0] and det=1
  before the sweep, then verifies arrows and readout agree after.
- silent preview: durations authored in storyboard.json (4.0 + 5.0 = 9s).
- aspect 16:9 bounds: x in [-7.11, 7.11], y in [-4.0, 4.0]. Stable camera.
- NO LaTeX: Text + DecimalNumber(mob_class=Text) only; no MathTex/Tex.

Design note: ValueTracker alpha drives the Rotate of both arrows via
always_redraw (rotation matrix applied per frame). The det DecimalNumber
shares the same tracker, so the readout cannot drift from the figure.
All animation passes through CuePlayer.play plus finish.
"""
from pathlib import Path
import math
import os
import sys
from manim import *

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/manim-voice-animation/scripts"))
from cue_player import CuePlayer


class V04Scene(Scene):
    """Rotate e1/e2 together with shared tracker; det readout stays 1."""

    def construct(self):
        manifest = Path(
            os.environ.get(
                "GNOS_MANIFEST",
                str(Path(__file__).parent / "audio" / "timing_manifest.json"),
            )
        )
        player = CuePlayer(self, manifest, "V04Scene")

        alpha = ValueTracker(0.0)

        def rotate_vec(x, y):
            # Rotate helper: R(alpha) applied to (x, y); driven by tracker.
            a = float(alpha.get_value())
            c = math.cos(a)
            s = math.sin(a)
            return [x * c - y * s, x * s + y * c, 0]

        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            x_length=13,
            y_length=7,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1},
        )

        title = Text("Basis rotate: e1 e2 det tracker", font_size=28).to_edge(
            UP, buff=0.3
        )

        # Rotate of two arrows driven by alpha tracker.
        e1_arrow = always_redraw(
            lambda: Arrow(
                ORIGIN, rotate_vec(2.0, 0.0), color=GREEN, stroke_width=6, buff=0
            )
        )
        e2_arrow = always_redraw(
            lambda: Arrow(
                ORIGIN, rotate_vec(0.0, 2.0), color=TEAL, stroke_width=6, buff=0
            )
        )

        e1_label = Text("e1", font_size=26, color=GREEN)
        e1_label.add_updater(
            lambda mob: mob.next_to(e1_arrow.get_end(), RIGHT, buff=0.15)
        )
        e2_label = Text("e2", font_size=26, color=TEAL)
        e2_label.add_updater(
            lambda mob: mob.next_to(e2_arrow.get_end(), UP, buff=0.15)
        )

        # Det readout wired to the same tracker as the geometry.
        det_num = DecimalNumber(
            1.0, num_decimal_places=2, mob_class=Text, color=BLUE, font_size=28
        )
        det_num.add_updater(
            lambda mob: mob.set_value(
                math.cos(float(alpha.get_value())) ** 2
                + math.sin(float(alpha.get_value())) ** 2
            )
        )
        det_row = VGroup(Text("det =", font_size=28, color=BLUE), det_num).arrange(
            RIGHT, buff=0.12
        )
        det_row.to_corner(UR, buff=0.4).shift(DOWN * 0.7)

        alpha_num = DecimalNumber(
            0.0, num_decimal_places=0, mob_class=Text, color=YELLOW, font_size=28
        )
        alpha_num.add_updater(
            lambda mob: mob.set_value(
                float(alpha.get_value()) * 180.0 / math.pi
            )
        )
        tracker_row = VGroup(
            Text("tracker alpha =", font_size=24, color=YELLOW), alpha_num
        ).arrange(RIGHT, buff=0.12)
        tracker_row.next_to(det_row, DOWN, buff=0.2)

        # c1_basis: basis shown at identity, tracker at zero, det reads 1.
        player.play(
            "c1_basis",
            Create(plane),
            Create(e1_arrow),
            Create(e2_arrow),
            FadeIn(title),
            FadeIn(e1_label),
            FadeIn(e2_label),
            FadeIn(det_row),
            FadeIn(tracker_row),
            run_time=2.0,
        )
        # c2_rotate: tracker sweeps 0 -> 90 deg; arrows + readouts move together.
        player.play(
            "c2_rotate",
            alpha.animate.set_value(math.pi / 2),
            run_time=4.0,
        )

        for mob in (e1_label, e2_label, det_num, alpha_num):
            mob.clear_updaters()
        e1_arrow.clear_updaters()
        e2_arrow.clear_updaters()
        player.finish(
            os.environ.get(
                "GNOS_TIMELINE_PREFIX", str(Path(__file__).parent / "lesson")
            )
        )
