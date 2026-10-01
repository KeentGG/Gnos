"""V02: secant tends to tangent for f(x) = x^2 at x = 2 (Text only, no LaTeX)."""
from pathlib import Path
import os
import sys
from manim import *

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/manim-voice-animation/scripts"))
from cue_player import CuePlayer


class V02Scene(Scene):
    """Two cues, same axes: coarse secant (slope 5) then refined secant + tangent (4.25 -> 4.0)."""

    def construct(self):
        default_manifest = Path(__file__).resolve().parent / "audio" / "timing_manifest.json"
        manifest = Path(os.environ.get("GNOS_MANIFEST", default_manifest))
        player = CuePlayer(self, manifest, "V02Scene")

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 10, 2],
            x_length=7.0,
            y_length=4.0,
            axis_config={"color": GREY_B, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.5)

        f = lambda x: x ** 2
        curve = axes.plot(f, x_range=[0, 3.2], color=BLUE_C, stroke_width=4)
        curve_label = Text("f(x) = x^2", font_size=24, color=BLUE_C).to_corner(UR, buff=0.4)

        dot_a = Dot(point=axes.c2p(2, 4), color=RED, radius=0.09)
        dot_b = Dot(point=axes.c2p(3, 9), color=ORANGE, radius=0.07)
        dot_fine_target = Dot(point=axes.c2p(2.25, 5.0625), color=ORANGE, radius=0.07)

        secant_coarse = axes.get_secant_slope_group(
            x=2,
            graph=curve,
            dx=1.0,
            secant_line_length=4.0,
            secant_line_color=YELLOW,
        )
        secant_fine = axes.get_secant_slope_group(
            x=2,
            graph=curve,
            dx=0.25,
            secant_line_length=4.0,
            secant_line_color=GREEN,
        )
        tangent = axes.get_secant_slope_group(
            x=2,
            graph=curve,
            dx=0.01,
            secant_line_length=4.0,
            secant_line_color=RED,
        )
        tangent_label = Text("tangent slope = 4.0", font_size=22, color=RED).to_corner(UR, buff=0.4).shift(DOWN * 0.5)

        readout_a = Text("secant slope = 5.0", font_size=28, color=YELLOW).to_corner(UL, buff=0.4).shift(DOWN * 0.5)
        readout_b = Text("secant 4.25 -> tangent 4.0", font_size=26, color=GREEN).to_corner(UL, buff=0.4).shift(DOWN * 0.5)

        # v02a: establish same axes, curve, and coarse secant slope 5.
        player.play(
            "v02a",
            Create(axes),
            Create(curve),
            Write(curve_label),
            Create(dot_a),
            Create(dot_b),
            Create(secant_coarse),
            Write(readout_a),
            run_time=3.0,
        )
        # v02b: refine secant toward x=2 and reveal tangent slope 4.
        player.play(
            "v02b",
            Transform(secant_coarse, secant_fine),
            Transform(dot_b, dot_fine_target),
            Create(tangent),
            Write(tangent_label),
            ReplacementTransform(readout_a, readout_b),
            run_time=4.0,
        )

        player.finish("preview")
