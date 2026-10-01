"""V07 Dijkstra relaxations with subtitle timing — silent preview.

Graph layout is fixed for all cues; only dist labels and edge highlights change.
Silent preview uses authored cue durations; measured audio can replace them later.
Storyboard: tests/visual-levels/V07/storyboard.json (scene V07Scene).
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

# Fixed layout: positions never change after init (continuity constraint).
POS_S = LEFT * 4.5
POS_A = LEFT * 1.5 + UP * 1.5
POS_B = LEFT * 1.5 + DOWN * 1.5
POS_T = RIGHT * 2.5


def _node(letter, pos):
    circle = Circle(radius=0.4, color=BLUE_C, stroke_width=3).move_to(pos)
    tag = Text(letter, font_size=30).move_to(pos)
    return VGroup(circle, tag)


class V07Scene(Scene):
    def construct(self):
        self.camera.background_color = "#101c27"
        here = Path(__file__).resolve().parent
        manifest = Path(os.environ.get("GNOS_MANIFEST", here / "audio" / "timing_manifest.json"))
        player = CuePlayer(self, manifest, "V07Scene")

        title = Text("Dijkstra: track each relax", font_size=30).to_edge(UP, buff=0.35)

        node_s = _node("s", POS_S)
        node_a = _node("a", POS_A)
        node_b = _node("b", POS_B)
        node_t = _node("t", POS_T)

        edge_sa = Line(POS_S, POS_A, color=GREY_A, stroke_width=4)
        edge_sb = Line(POS_S, POS_B, color=GREY_A, stroke_width=4)
        edge_at = Line(POS_A, POS_T, color=GREY_A, stroke_width=4)
        edge_bt = Line(POS_B, POS_T, color=GREY_A, stroke_width=4)

        w_sa = Text("4", font_size=24).move_to((POS_S + POS_A) / 2 + UP * 0.35)
        w_sb = Text("2", font_size=24).move_to((POS_S + POS_B) / 2 + DOWN * 0.35)
        w_at = Text("3", font_size=24).move_to((POS_A + POS_T) / 2 + UP * 0.35)
        w_bt = Text("7", font_size=24).move_to((POS_B + POS_T) / 2 + DOWN * 0.35)

        dist_s = Text("dist(s)=0", font_size=20, color=GREEN).move_to(POS_S + DOWN * 0.85)
        dist_a = Text("dist(a)=inf", font_size=20).move_to(POS_A + DOWN * 0.85)
        dist_b = Text("dist(b)=inf", font_size=20).move_to(POS_B + DOWN * 0.85)
        dist_t = Text("dist(t)=inf", font_size=20).move_to(POS_T + DOWN * 0.85)

        dist_a_hit = Text("dist(a)=4", font_size=20, color=YELLOW).move_to(dist_a.get_center())
        dist_b_hit = Text("dist(b)=2", font_size=20, color=YELLOW).move_to(dist_b.get_center())
        dist_t_hit = Text("dist(t)=7", font_size=20, color=YELLOW).move_to(dist_t.get_center())

        caption = Text(
            "shortest dist(t)=7 via s-a-t; subtitles matched cues",
            font_size=22,
            color=TEAL_C,
        ).to_edge(DOWN, buff=0.35)

        player.play(
            "init",
            Write(title),
            Create(edge_sa),
            Create(edge_sb),
            Create(edge_at),
            Create(edge_bt),
            Create(node_s),
            Create(node_a),
            Create(node_b),
            Create(node_t),
            FadeIn(w_sa),
            FadeIn(w_sb),
            FadeIn(w_at),
            FadeIn(w_bt),
            FadeIn(dist_s),
            FadeIn(dist_a),
            FadeIn(dist_b),
            FadeIn(dist_t),
            run_time=4,
        )
        player.play(
            "relax-s-a",
            Indicate(node_s),
            Indicate(node_a),
            edge_sa.animate.set_color(YELLOW),
            Transform(dist_a, dist_a_hit),
            run_time=3,
        )
        player.play(
            "relax-s-b",
            Indicate(node_s),
            Indicate(node_b),
            edge_sb.animate.set_color(YELLOW),
            Transform(dist_b, dist_b_hit),
            run_time=3,
        )
        player.play(
            "relax-a-t",
            Indicate(node_a),
            Indicate(node_t),
            edge_at.animate.set_color(YELLOW),
            Transform(dist_t, dist_t_hit),
            run_time=3,
        )
        player.play("done", Indicate(node_t), FadeIn(caption), run_time=2)
        player.finish(os.environ.get("GNOS_TIMELINE_PREFIX", str(here / "V07Scene")))
