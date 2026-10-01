"""V10 — Surface + gradient path camera reveal (2D contour view).

Concept: gradient steps on f(x,y) = x^2 + y^2 descend circular level
sets toward the minimum; a single justified zoom confirms the bottom.
2D contour projection keeps the render fast (<90s at -ql); no LaTeX.

Storyboard: storyboard.json (scene V10Scene, cues contour/path/zoom).
Silent preview (authored durations, no speech):
    /Users/choclate/Desktop/Gnos/.venv/bin/python \
        skills/manim-voice-animation/scripts/voice_synthesizer.py \
        --storyboard tests/visual-levels/V10/storyboard.json \
        --out tests/visual-levels/V10/audio --silent
    GNOS_MANIFEST=tests/visual-levels/V10/audio/timing_manifest.json \
    /Users/choclate/Desktop/Gnos/.venv/bin/python \
        skills/manim-voice-animation/scripts/render_pipeline.py \
        render tests/visual-levels/V10/scene.py V10Scene \
        -q l -o tests/visual-levels/V10/preview.mp4
"""
from pathlib import Path
import os
import sys
from manim import *

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills" / "manim-voice-animation" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from cue_player import CuePlayer

# One surface throughout: f(x, y) = x^2 + y^2, level sets are circles.
ETA = 0.22
FACTOR = 1.0 - 2.0 * ETA  # exact gradient-descent shrink per step
START = (2.5, 1.5)
N_STEPS = 8


def descent_points():
    x, y = START
    pts = [(x, y)]
    for _ in range(N_STEPS):
        x, y = x * FACTOR, y * FACTOR
        pts.append((x, y))
    return pts


class V10Scene(Scene):
    def construct(self):
        self.camera.background_color = "#101c27"
        here = Path(__file__).resolve().parent
        manifest = Path(os.environ.get("GNOS_MANIFEST", here / "audio" / "timing_manifest.json"))
        player = CuePlayer(self, manifest, "V10Scene")

        title = Text("Gradient path descends to the minimum", font_size=30).to_edge(UP, buff=0.3)
        surface_label = Text(
            "f(x,y) = x^2 + y^2 - one surface throughout",
            font_size=20, color=TEAL_C,
        ).next_to(title, DOWN, buff=0.15)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.5, y_length=5.5,
            tips=False, axis_config={"color": GREY_B},
        ).shift(DOWN * 0.45)
        center = axes.c2p(0, 0)
        unit = 5.5 / 6.0  # scene units per data unit

        levels = [0.5, 1.5, 3.0, 5.0, 7.5]
        palette = [BLUE_C, BLUE, TEAL_C, TEAL, GREEN_C]
        contours = VGroup(*[
            Circle(radius=(c ** 0.5) * unit, color=col, stroke_width=3).move_to(center)
            for c, col in zip(levels, palette)
        ])

        pts = descent_points()
        scene_pts = [axes.c2p(x, y) for x, y in pts]
        path_line = VMobject(color=YELLOW, stroke_width=4)
        path_line.set_points_as_corners(scene_pts)
        path_dots = VGroup(*[
            Dot(p, radius=0.07, color=YELLOW) for p in scene_pts
        ])
        start_tag = Text("start (highest)", font_size=18, color=YELLOW).next_to(
            scene_pts[0], RIGHT, buff=0.15)

        minimum_dot = Dot(center, radius=0.13, color=GREEN)
        minimum_label = Text("minimum (0,0) - lowest point", font_size=22, color=GREEN)
        minimum_label.move_to(RIGHT * 3.4 + DOWN * 2.2)
        final_caption = Text(
            "Check: next step moves inward; the one zoom only confirms the minimum.",
            font_size=18, color=GREY_A,
        ).to_edge(DOWN, buff=0.25)

        # Zoom target: diagram only, so titles and captions stay pinned/readable.
        board = VGroup(axes, contours, path_line, path_dots, minimum_dot)

        player.play(
            "contour",
            Write(title), FadeIn(surface_label),
            Create(axes), Create(contours),
            run_time=3,
        )
        player.play(
            "path",
            Create(path_line), FadeIn(path_dots), FadeIn(start_tag),
            run_time=4,
        )
        player.play(
            "zoom",
            board.animate.scale(1.15),
            FadeIn(minimum_dot), FadeIn(minimum_label), FadeIn(final_caption),
            run_time=3,
        )
        player.finish(os.environ.get(
            "GNOS_TIMELINE_PREFIX", str(here / "timeline" / "V10Scene")))
