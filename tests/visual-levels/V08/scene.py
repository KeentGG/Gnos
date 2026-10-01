"""V08 projectile cue-timed motion (silent preview).

Concept: at the apex the vertical component vy is zero while the
horizontal component vx is unchanged; the apex callout lands exactly
on the apex cue. One ValueTracker drives the dot, the vx/vy arrows,
and the readouts together, so numbers and geometry cannot disagree.

Storyboard: tests/visual-levels/V08/storyboard.json
(Class V08Scene, cues launch/apex/landing.)

Silent preview (authored durations, no speech):
    /Users/choclate/Desktop/Gnos/.venv/bin/python \
        skills/manim-voice-animation/scripts/voice_synthesizer.py \
        --storyboard tests/visual-levels/V08/storyboard.json \
        --out tests/visual-levels/V08/audio --silent
    /Users/choclate/Desktop/Gnos/.venv/bin/python \
        skills/manim-voice-animation/scripts/render_pipeline.py \
        render tests/visual-levels/V08/scene.py V08Scene \
        -q l -o tests/visual-levels/V08/preview.mp4
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

HERE = Path(__file__).resolve().parent

# Single physics state in SI units: v0 = 8.0 m/s at 45 degrees, g = 9.8 m/s^2.
V0 = 8.0
ANGLE = PI / 4
G = 9.8
VX = V0 * float(np.cos(ANGLE))  # ~5.66 m/s, constant for the whole flight.
VY0 = V0 * float(np.sin(ANGLE))  # ~5.66 m/s at launch, zero at the apex.
T_APEX = VY0 / G  # ~0.58 s; cue timing puts the apex callout on this frame.
T_MAX = 2 * VY0 / G  # ~1.15 s total flight.
APEX_H = VY0 ** 2 / (2 * G)  # ~1.63 m.
RANGE = VX * T_MAX  # ~6.53 m.


class V08Scene(Scene):
    def construct(self):
        manifest = Path(os.environ.get(
            "GNOS_MANIFEST", HERE / "audio" / "timing_manifest.json"))
        player = CuePlayer(self, manifest, "V08Scene")

        title = Text("Projectile: vx vs vy", font_size=32).to_edge(UP, buff=0.35)
        axes = Axes(
            x_range=[0, 8, 2], y_range=[0, 4, 1],
            x_length=8, y_length=4.5,
            tips=False, axis_config={"color": GREY_B},
        ).shift(DOWN * 0.35)
        units_note = Text(
            "SI units: m, m/s", font_size=20, color=GREY_B
        ).to_edge(DOWN, buff=0.35)

        def pos(t):
            # Same state the ParametricFunction trajectory below is drawn from.
            return axes.c2p(VX * t, max(0.0, VY0 * t - 0.5 * G * t * t))

        def vy_now():
            return VY0 - G * tracker.get_value()

        # Full trajectory curve; the dot below rides this exact path.
        trajectory = ParametricFunction(
            lambda u: axes.c2p(VX * u, VY0 * u - 0.5 * G * u * u),
            t_range=[0, T_MAX, 0.02], color=YELLOW, stroke_width=3,
        )

        tracker = ValueTracker(0.0)

        # Projectile dot driven by the shared tracker (no per-frame rebuilds).
        projectile = Dot(pos(0.0), color=RED, radius=0.12)
        projectile.add_updater(lambda mob: mob.move_to(pos(tracker.get_value())))

        arrow_scale = 0.25
        min_stub = 0.05  # Rendering floor so a zero-length Arrow never errors.

        def vx_arrow_mobject():
            start = projectile.get_center()
            return Arrow(
                start, start + RIGHT * max(min_stub, VX * arrow_scale),
                buff=0.02, stroke_width=5, color=TEAL,
            )

        def vy_arrow_mobject():
            start = projectile.get_center()
            length = vy_now() * arrow_scale
            if abs(length) < min_stub:
                length = min_stub if length >= 0 else -min_stub
            return Arrow(
                start, start + UP * length,
                buff=0.02, stroke_width=5, color=BLUE_C,
            )

        vx_arrow = always_redraw(vx_arrow_mobject)
        vy_arrow = always_redraw(vy_arrow_mobject)

        # Text readouts (no LaTeX): DecimalNumber with Text glyphs, updated
        # in place from the same tracker state as the geometry.
        vx_number = DecimalNumber(
            VX, mob_class=Text, num_decimal_places=2,
            font_size=26, color=TEAL,
        )
        vy_number = DecimalNumber(
            VY0, mob_class=Text, num_decimal_places=2,
            font_size=26, color=BLUE_C,
        )
        vy_number.add_updater(lambda mob: mob.set_value(vy_now()))
        readout = VGroup(
            VGroup(Text("vx =", font_size=24, color=TEAL), vx_number,
                   Text("m/s", font_size=20, color=TEAL)).arrange(RIGHT, buff=0.12),
            VGroup(Text("vy =", font_size=24, color=BLUE_C), vy_number,
                   Text("m/s", font_size=20, color=BLUE_C)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL).shift(DOWN * 0.9)

        # Apex marker: hidden until the apex cue, then fades in exactly on
        # the frame the dot reaches the top of the arc (vy = 0).
        apex_marker = VGroup(
            Dot(pos(T_APEX), color=YELLOW, radius=0.16),
            Text("apex  vy = 0 m/s", font_size=22, color=YELLOW).next_to(
                pos(T_APEX), UP, buff=0.15),
        )
        range_note = Text(
            f"range {RANGE:.2f} m", font_size=22, color=GREY_B
        ).to_edge(DOWN, buff=0.9)

        # Live arrows ride the dot; static objects join via cue choreography.
        self.add(vx_arrow, vy_arrow)

        # Cue launch: model on screen, dot held at the launch point.
        player.play(
            "launch",
            Write(title), Create(axes), Create(trajectory),
            FadeIn(projectile), FadeIn(vx_arrow), FadeIn(vy_arrow),
            FadeIn(readout), FadeIn(units_note),
            run_time=4.0,
        )
        # Cue apex: dot climbs to the top while the apex callout fades in,
        # completing exactly on the apex frame.
        player.play(
            "apex",
            tracker.animate.set_value(T_APEX),
            FadeIn(apex_marker),
            run_time=5.0,
        )
        # Cue landing: dot descends to the ground, vy arrow flips downward.
        player.play(
            "landing",
            tracker.animate.set_value(T_MAX),
            FadeIn(range_note),
            run_time=4.0,
        )
        # Section over: detach updaters so nothing fires past its section.
        projectile.clear_updaters()
        vy_number.clear_updaters()
        # No trailing wait: finish() holds each cue to its authored duration
        # and rejects unplayed cues.
        player.finish(str(HERE / "V08Scene"))
