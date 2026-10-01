"""V09 wave propagation, stable camera (silent preview).

Concept: follow propagation without decorative camera motion.
Camera is static (plain Scene, no camera motion). One wavelength
lambda is marked with a double-arrow; the lambda callout follows the
tracked crest as phase advances.
"""
import os
import sys
from pathlib import Path

import numpy as np
from manim import *

V09_DIR = Path(__file__).resolve().parent
SCRIPTS = Path("/Users/choclate/Desktop/Gnos/skills/manim-voice-animation/scripts")
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from cue_player import CuePlayer

AMP = 1.2
LAM = 2.0
K = np.pi  # 2*pi/LAM with LAM=2


def crest_x(phase_value):
    return (phase_value + np.pi / 2) / K


class V09Scene(Scene):
    def construct(self):
        self.camera.background_color = "#101c27"
        default_manifest = V09_DIR / "audio" / "timing_manifest.json"
        manifest = Path(os.environ.get("GNOS_MANIFEST", str(default_manifest)))
        player = CuePlayer(self, manifest, "V09Scene")

        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-2, 2, 1],
            x_length=12,
            y_length=3.2,
            tips=False,
            axis_config={"color": GREY_B},
        ).shift(DOWN * 0.4)

        phase = ValueTracker(0.0)

        wave = always_redraw(
            lambda: FunctionGraph(
                lambda x: AMP * np.sin(K * x - phase.get_value()),
                x_range=[-6, 6, 0.05],
                color=TEAL_C,
            ).shift(DOWN * 0.4)
        )

        crest_dot = Dot(point=RIGHT * 0.5 + UP * 0.8, color=YELLOW, radius=0.12)

        def follow_crest(mob):
            x = crest_x(phase.get_value())
            mob.move_to(np.array([x, AMP - 0.4, 0]))

        crest_dot.add_updater(follow_crest)

        wavelength_arrow = DoubleArrow(
            start=RIGHT * 0.5 + UP * 1.8,
            end=RIGHT * 2.5 + UP * 1.8,
            color=ORANGE,
            buff=0.05,
            stroke_width=4,
        )

        def follow_arrow(mob):
            x = crest_x(phase.get_value())
            mob.put_start_and_end_on(
                np.array([x, AMP + 0.6, 0]),
                np.array([x + LAM, AMP + 0.6, 0]),
            )

        wavelength_arrow.add_updater(follow_arrow)

        lambda_label = Text("lambda = one wavelength", font_size=24, color=ORANGE)

        def follow_label(mob):
            x = crest_x(phase.get_value())
            mob.move_to(np.array([x + LAM / 2, AMP + 1.2, 0]))

        lambda_label.add_updater(follow_label)

        direction_arrow = Arrow(
            start=LEFT * 5.5 + DOWN * 2.8,
            end=LEFT * 4.0 + DOWN * 2.8,
            color=GREY_A,
            buff=0,
            stroke_width=4,
        )
        direction_label = Text("direction", font_size=20, color=GREY_A).next_to(
            direction_arrow, UP, buff=0.08
        )
        fixed_note = Text("fixed camera", font_size=20, color=GREY_A).to_corner(
            UL, buff=0.4
        )

        player.play(
            "wave_shown",
            Create(axes),
            Create(wave),
            FadeIn(crest_dot),
            FadeIn(wavelength_arrow),
            FadeIn(lambda_label),
            FadeIn(direction_arrow),
            FadeIn(direction_label),
            FadeIn(fixed_note),
            run_time=3.0,
        )
        player.play(
            "crest_tracked",
            phase.animate.set_value(2 * np.pi),
            run_time=5.0,
        )
        crest_dot.clear_updaters()
        wavelength_arrow.clear_updaters()
        lambda_label.clear_updaters()
        player.finish(
            os.environ.get("GNOS_TIMELINE_PREFIX", str(V09_DIR / "audio" / "lesson"))
        )
