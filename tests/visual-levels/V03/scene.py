"""V03 BFS animation 3 cues — silent preview, Text only (no LaTeX).

Storyboard: tests/visual-levels/V03/storyboard.json
(Class V03Scene, cues v03a/v03b/v03c visiting A, B, C.)

Silent preview (authored durations, no speech, no network):
    /Users/choclate/Desktop/Gnos/.venv/bin/python \
        skills/manim-voice-animation/scripts/voice_synthesizer.py \
        --storyboard tests/visual-levels/V03/storyboard.json \
        --out tests/visual-levels/V03/audio --silent
    GNOS_MANIFEST=tests/visual-levels/V03/audio/timing_manifest.json \
    /Users/choclate/Desktop/Gnos/.venv/bin/python \
        skills/manim-voice-animation/scripts/render_pipeline.py \
        render tests/visual-levels/V03/scene.py V03Scene \
        -q l -o tests/visual-levels/V03/preview.mp4
"""
import os
import sys
from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
ROOT = Path("/Users/choclate/Desktop/Gnos")
SCRIPTS = ROOT / "skills" / "manim-voice-animation" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from cue_player import CuePlayer


class V03Scene(Scene):
    """BFS visit order A then B then C; fixed layout, queue readout pinned."""

    def construct(self):
        manifest = Path(
            os.environ.get(
                "GNOS_MANIFEST",
                str(HERE / "audio" / "timing_manifest.json"),
            )
        )
        player = CuePlayer(self, manifest, "V03Scene")

        # Stable layout: explicit coordinates reused for every cue.
        # Positions never move; only the visited color changes.
        pos_a = LEFT * 3.5
        pos_b = UP * 1.5 + RIGHT * 0.5
        pos_c = DOWN * 1.5 + RIGHT * 0.5

        title = Text("BFS visit order: A then B then C", font_size=30).to_edge(
            UP, buff=0.35
        )

        circle_a = Circle(radius=0.45, color=BLUE_C, stroke_width=4).move_to(pos_a)
        circle_b = Circle(radius=0.45, color=BLUE_C, stroke_width=4).move_to(pos_b)
        circle_c = Circle(radius=0.45, color=BLUE_C, stroke_width=4).move_to(pos_c)
        label_a = Text("A", font_size=30).move_to(circle_a.get_center())
        label_b = Text("B", font_size=30).move_to(circle_b.get_center())
        label_c = Text("C", font_size=30).move_to(circle_c.get_center())
        # Node A starts visited so the first cue's final state shows it.
        circle_a.set_color(YELLOW)

        edge_ab = Arrow(
            circle_a.get_center(), circle_b.get_center(), color=GREY_A, buff=0.55
        )
        edge_ac = Arrow(
            circle_a.get_center(), circle_c.get_center(), color=GREY_A, buff=0.55
        )

        # Pinned queue readout: fixed corner panel through all cues.
        queue_a = Text("queue: B, C", font_size=24, color=YELLOW).to_corner(
            UL
        ).shift(DOWN * 0.9)
        queue_b = Text("queue: C", font_size=24, color=YELLOW).move_to(
            queue_a, aligned_edge=LEFT
        )
        queue_c = Text("queue: empty", font_size=24, color=YELLOW).move_to(
            queue_a, aligned_edge=LEFT
        )
        order_caption = Text(
            "BFS order A, B, C; only color changed.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.4)

        # Cue v03a -- narration: start at A, visit A, queue holds B and C.
        # Visible: full graph at fixed positions plus queue readout.
        # Change: base state plus node A visited.
        player.play(
            "v03a",
            Write(title),
            Create(circle_a),
            Create(circle_b),
            Create(circle_c),
            Write(label_a),
            Write(label_b),
            Write(label_c),
            Create(edge_ab),
            Create(edge_ac),
            Write(queue_a),
            run_time=3.0,
        )

        # Cue v03b -- narration: take B from the queue and visit it.
        # Visible: node B plus queue readout. Change: B turns visited.
        player.play(
            "v03b",
            circle_b.animate.set_color(YELLOW),
            ReplacementTransform(queue_a, queue_b),
            run_time=2.0,
        )

        # Cue v03c -- narration: take C, visit it, queue empty, order A B C.
        # Visible: node C, queue readout, final caption. Change: C visited,
        # final frame keeps the order claim readable silent.
        player.play(
            "v03c",
            circle_c.animate.set_color(YELLOW),
            ReplacementTransform(queue_b, queue_c),
            Write(order_caption),
            run_time=3.0,
        )

        player.finish(
            os.environ.get("GNOS_TIMELINE_PREFIX", str(HERE / "timeline"))
        )
