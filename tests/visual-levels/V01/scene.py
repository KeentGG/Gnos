"""V01 L01 — Dot along line, one cue (silent preview).

Concept: on y = 2x, y grows twice as fast as x; the learner watches one
change — a dot traveling along the line.

Storyboard: tests/visual-levels/V01/storyboard.json
(Class V01Scene, cue v01a.)

Silent preview (authored durations, no speech, no network):
    .venv/bin/python skills/manim-voice-animation/scripts/voice_synthesizer.py \
        --storyboard tests/visual-levels/V01/storyboard.json \
        --out tests/visual-levels/V01/audio --silent
    .venv/bin/python skills/manim-voice-animation/scripts/render_pipeline.py \
        render tests/visual-levels/V01/scene.py V01Scene \
        -q l -o tests/visual-levels/V01/preview.mp4

Review checklist (at playback size): first frame shows title, axes, line,
and dot; the dot visibly travels the full line during cue v01a; the
"y = 2x" label stays in frame and is highlighted while the narration
names it; the ending holds the dot at the line end.
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

# Line endpoints in x; y follows y = 2x. Kept inside the 16:9 frame.
X_START = -1.5
X_END = 1.5


class V01Scene(Scene):
    def construct(self):
        self.camera.background_color = "#101c27"
        manifest = Path(os.environ.get(
            "GNOS_MANIFEST",
            Path(__file__).resolve().parent / "audio" / "timing_manifest.json"))
        player = CuePlayer(self, manifest, "V01Scene")

        title = Text("Dot along y = 2x", font_size=36).to_edge(UP, buff=0.4)
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-6, 6, 2], x_length=7, y_length=4.2,
            tips=False, axis_config={"color": GREY_B},
        ).shift(DOWN * 0.35)
        line = axes.plot(lambda x: 2 * x, x_range=[X_START, X_END], color=TEAL_C)
        label = Text("y = 2x", font_size=28, color=TEAL_C).next_to(
            axes.c2p(X_END, 2 * X_END), RIGHT, buff=0.25)
        dot = Dot(axes.c2p(X_START, 2 * X_START), color=YELLOW)

        # Static context is on stage; the cue's single change is the travel.
        self.add(axes, line, title, label, dot)

        # One play for the one cue: the dot rides the line while the spoken
        # term's label is signaled. run_time fits inside cue v01a (6.0s).
        player.play(
            "v01a",
            dot.animate.move_to(axes.c2p(X_END, 2 * X_END)),
            Indicate(label),
            run_time=4,
        )
        player.finish(Path(__file__).resolve().parent / "preview")
