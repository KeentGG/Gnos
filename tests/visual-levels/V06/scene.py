"""V06: Riemann sum refinement 4 -> 8 -> 16 for x^2 on [0, 1].

Storyboard notes:
- concept ID: math.integral.riemann-refinement.
- prereq: learner reads area under y = x squared on [0, 1] as an integral.
- success check: learner predicts the error shrinks as n doubles, then
  compares with the readout.
- one clear change per cue: c1 shows axes/curve/n=4 bars with the large
  error, c2 replaces bars with n=8 and the error drops, c3 replaces bars
  with n=16 and the error is smallest; every updater is cleared at the end.
- silent preview: storyboard.json carries explicit durations; the scene
  reads audio/timing_manifest.json (GNOS_MANIFEST override supported).
- aspect 16:9 bounds: frame x in [-7.11, 7.11], y in [-4.0, 4.0]. Axes
  (x_length 6.5, y_length 4.0, shifted LEFT*1.2 + DOWN*0.55) span about
  x [-4.45, 2.05] and y [-2.55, 1.45]; labels are pinned to corners.
- camera: stable. The bar replacement is the only structural change.
- No LaTeX: labels use Text only; Axes carry no numbers; the numeric
  readout is a DecimalNumber with mob_class=Text updated in place.
"""

import os
import sys
from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "skills/manim-voice-animation/scripts"))
from cue_player import CuePlayer  # noqa: E402

TRUE_INTEGRAL = 1.0 / 3.0


def right_riemann_error(n):
    """Right-endpoint error of x^2 on [0, 1] against the true integral."""
    dx = 1.0 / n
    total = sum(((k * dx) ** 2) * dx for k in range(1, n + 1))
    return total - TRUE_INTEGRAL


class V06Scene(Scene):
    """Refine Riemann bars 4 -> 8 -> 16; error readout shares one tracker."""

    def construct(self):
        manifest = Path(
            os.environ.get("GNOS_MANIFEST", HERE / "audio" / "timing_manifest.json")
        )
        player = CuePlayer(self, manifest, "V06Scene")

        axes = Axes(
            x_range=[0, 1.2, 0.5],
            y_range=[0, 1.2, 0.5],
            x_length=6.5,
            y_length=4.0,
            axis_config={"stroke_width": 2},
            tips=False,
        ).shift(LEFT * 1.2 + DOWN * 0.55)

        f = lambda x: x**2  # noqa: E731
        curve = axes.plot(f, x_range=[0, 1], color=BLUE_C, stroke_width=4)

        def make_bars(n):
            dx = 1.0 / n
            bars = VGroup()
            for k in range(1, n + 1):
                x_right = k * dx
                x_left = x_right - dx
                bottom_left = axes.c2p(x_left, 0)
                top_right = axes.c2p(x_right, f(x_right))
                width = top_right[0] - bottom_left[0]
                height = max(top_right[1] - bottom_left[1], 0.001)
                bar = Rectangle(
                    width=width,
                    height=height,
                    color=TEAL,
                    fill_opacity=0.55,
                    stroke_width=1,
                )
                bar.move_to((bottom_left + top_right) / 2)
                bars.add(bar)
            return bars

        title = Text("Riemann sum for x^2 on [0, 1]", font_size=32).to_edge(
            UP, buff=0.3
        )
        x_tag = Text("x", font_size=24).next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
        y_tag = Text("y = x^2", font_size=24).next_to(
            axes.y_axis.get_end(), UP, buff=0.15
        )
        integral_note = Text("integral = 0.3333", font_size=22, color=GREY_B)

        n_label_4 = Text("n = 4", font_size=30)
        n_label_8 = Text("n = 8", font_size=30)
        n_label_16 = Text("n = 16", font_size=30)
        for label in (n_label_4, n_label_8, n_label_16):
            label.to_corner(UR, buff=0.6)
        integral_note.next_to(n_label_4, DOWN, buff=0.15).align_to(n_label_4, RIGHT)

        # Shared state: one tracker feeds the readout, so the displayed error
        # cannot drift from the animation driving it. Glyphs update in place;
        # no Text is rebuilt per frame.
        err_tracker = ValueTracker(right_riemann_error(4))
        error_value = DecimalNumber(
            right_riemann_error(4),
            num_decimal_places=4,
            mob_class=Text,
            font_size=28,
            color=YELLOW,
        )
        error_value.add_updater(lambda mob: mob.set_value(err_tracker.get_value()))
        error_readout = (
            VGroup(Text("error = ", font_size=28, color=YELLOW), error_value)
            .arrange(RIGHT, buff=0.12)
            .to_corner(UL, buff=0.6)
        )

        bars_4 = make_bars(4)
        bars_8 = make_bars(8)
        bars_16 = make_bars(16)

        # c1_n4: establish axes, curve, four bars, and the large error.
        player.play(
            "c1_n4",
            Create(axes),
            Create(curve),
            Write(title),
            FadeIn(bars_4),
            FadeIn(n_label_4),
            FadeIn(integral_note),
            FadeIn(error_readout),
            FadeIn(x_tag),
            FadeIn(y_tag),
            run_time=3.0,
        )
        # c2_n8: replace bars 4 -> 8; the error readout drops with them.
        player.play(
            "c2_n8",
            FadeTransform(bars_4, bars_8),
            FadeTransform(n_label_4, n_label_8),
            err_tracker.animate.set_value(right_riemann_error(8)),
            run_time=3.0,
        )
        bars_4.clear_updaters()
        # c3_n16: replace bars 8 -> 16; the error reaches its smallest value.
        player.play(
            "c3_n16",
            FadeTransform(bars_8, bars_16),
            FadeTransform(n_label_8, n_label_16),
            err_tracker.animate.set_value(right_riemann_error(16)),
            run_time=3.0,
        )
        bars_8.clear_updaters()

        # Ending clean: no updater may remain attached after its section.
        error_value.clear_updaters()
        bars_16.clear_updaters()
        n_label_16.clear_updaters()
        player.finish(
            os.environ.get("GNOS_TIMELINE_PREFIX", str(HERE / "lesson"))
        )
