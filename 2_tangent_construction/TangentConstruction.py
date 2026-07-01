# TangentConstruction.py
# Animation that demonstrates the construction of the tangent function using Manim.

from manim import *


class TangentConstruction(MovingCameraScene):
    def construct(self):

        # ── Helpers ────────────────────────────────────────────────────────────

        def create_axes(
            x_range, y_range,
            x_length=10, y_length=6, color=WHITE,
            x_ticklabels=None, y_ticklabels=None,
            x_label=None, y_label=None,
        ):
            axes = Axes(
                x_range=x_range,
                y_range=y_range,
                x_length=x_length,
                y_length=y_length,
                axis_config={"color": color},
            )
            if x_ticklabels:
                axes.get_x_axis().add_labels(x_ticklabels)
            if y_ticklabels:
                axes.get_y_axis().add_labels(y_ticklabels)
            if x_label:
                x_label = axes.get_x_axis_label(x_label)
            if y_label:
                y_label = axes.get_y_axis_label(y_label)
            return axes, x_label, y_label

        def safe_tan(a, clip=10.0):
            t = np.tan(a)
            if not np.isfinite(t):
                return clip
            return float(np.clip(t, -clip, clip))

        # ── Timing constants ───────────────────────────────────────────────────

        text_fade_time  = 1.4   # FadeIn/Write duration for text
        short_pause     = 1.0   # brief beat
        read_pause      = 2.0   # time to read a line of text
        long_pause      = 3.0   # time to absorb a key concept
        pulse_time      = 0.8   # highlight animation duration
        highlight_pause = 1.5   # pause after a highlight before fade-out
        bullet_pause    = 2.0   # pause between property bullets

        EPSILON = 0.08  # angular gap near asymptotes

        # ── Texts ──────────────────────────────────────────────────────────────

        title = Tex(r"La funzione tangente").scale(1.25)

        intro_text = Tex(
            r"Consideriamo un ", r"punto $P$", " sulla ", r"circonferenza goniometrica"
        ).to_edge(DOWN)
        intro_text[1].set_color(GREEN)
        intro_text[3].set_color(BLUE)

        definition_text_1 = Tex(
            r"Tracciamo la ", r"retta tangente", r" alla circonferenza nel punto $(1,0)$"
        ).to_edge(DOWN)
        definition_text_1[1].set_color(YELLOW)

        definition_text_2 = Tex(
            r"Estendiamo $OP$ fino a incontrare la retta tangente nel punto ", r"$Q$"
        ).to_edge(DOWN)
        definition_text_2[1].set_color(RED)

        definition_text_3 = Tex(
            r"L'ordinata di $Q$ è la ", r"\emph{tangente}",
            r" dell'angolo $\alpha$: ", r"$y_Q = \tan \alpha$"
        ).to_edge(DOWN)
        definition_text_3[1].set_color(RED)
        definition_text_3[3].set_color(RED)

        animation_text = Tex(
            r"Variamo ora l'angolo ", r"$\alpha$",
            r" e registriamo la posizione di ", r"$y_Q$"
        ).to_edge(DOWN)
        animation_text[1].set_color(GREEN)
        animation_text[3].set_color(RED)

        function_text_1 = Tex(r"Immaginiamo di fare altri giri, in entrambi i sensi\dots").to_edge(DOWN)
        function_text_2 = Tex(r"\dots il grafico costruito si ripete con periodo $\pi$").to_edge(DOWN)

        final_text_1a = Tex(
            r"Otteniamo la \emph{funzione tangente} che associa:", tex_environment="flushleft"
        )
        final_text_1b_left  = Tex(r"a \emph{ogni} $x \neq \dfrac{\pi}{2}+k\pi$",      tex_environment="center").set_color(GREEN)
        final_text_1b_arrow = Tex(r"$\rightarrow$",                                    tex_environment="center")
        final_text_1b_right = Tex(r"il \emph{corrispondente} valore $\tan x$",         tex_environment="center").set_color(RED)
        final_text_1b = VGroup(final_text_1b_left, final_text_1b_arrow, final_text_1b_right).arrange(RIGHT, buff=0.2)

        final_text_2_title  = Tex(r"La funzione $f(x)=\tan x$ ha:",                                                    tex_environment="flushleft")
        final_text_2_item_1 = Tex(r"$\bullet$ dominio: $\mathbb{R}-\left\{\frac{\pi}{2}+k\pi,\;k\in\mathbb{Z}\right\}$", tex_environment="flushleft")
        final_text_2_item_2 = Tex(r"$\bullet$ immagine: $\mathbb{R}$",                                                 tex_environment="flushleft")
        final_text_2_item_3 = Tex(r"$\bullet$ periodo: $\pi$",                                                         tex_environment="flushleft")
        final_text_2_item_4 = Tex(r"$\bullet$ simmetria: rispetto all'origine",                                        tex_environment="flushleft")

        # ── Axes ───────────────────────────────────────────────────────────────

        # y_scale = y_length / (y_max - y_min) = 6/3 = 2  →  matches circle radius=2 scene units
        example_axes, example_x_label, example_y_label = create_axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            x_ticklabels={1: MathTex(r"1"), -1: MathTex(r"-1")},
            y_ticklabels={1: MathTex(r"1"), -1: MathTex(r"-1")},
            x_label=r"x",
            y_label=r"y",
        )

        # Same y_scale=2 so that T scene-y = 2·tan α = construction_axes.c2p(0, tan α)[1]
        construction_axes, construction_x_label, construction_y_label = create_axes(
            x_range=[0, TAU + 0.5, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_ticklabels={
                PI / 2: MathTex(r"\frac{\pi}{2}"),
                PI:     MathTex(r"\pi"),
                3*PI/2: MathTex(r"\frac{3\pi}{2}"),
                TAU:    MathTex(r"2\pi"),
            },
            y_ticklabels={1: MathTex(r"1"), -1: MathTex(r"-1")},
            x_label=r"\alpha",
            y_label=r"\tan \alpha",
        )

        extended_axes, extended_x_label, extended_y_label = create_axes(
            x_range=[-2*TAU - 1, 2*TAU + 1, PI],
            y_range=[-4, 4, 1],
            x_length=16,
            y_length=6,
            x_ticklabels={
                -4*PI: MathTex(r"-4\pi"),
                -3*PI: MathTex(r"-3\pi"),
                -2*PI: MathTex(r"-2\pi"),
                -PI:   MathTex(r"-\pi"),
                0:     MathTex(r"0"),
                PI:    MathTex(r"\pi"),
                2*PI:  MathTex(r"2\pi"),
                3*PI:  MathTex(r"3\pi"),
                4*PI:  MathTex(r"4\pi"),
            },
            y_ticklabels={2: MathTex(r"2"), -2: MathTex(r"-2")},
            x_label=r"x",
            y_label=r"y",
        )

        # ── Example scene objects ──────────────────────────────────────────────

        O_example       = Dot([0, 0, 0])
        O_example_label = MathTex(r"O").next_to(O_example, DL, buff=0.1).scale(0.6)
        example_circle  = Circle(radius=2, color=BLUE)

        # Use α = π/6 so tan α = 1/√3 ≈ 0.577 (nicely within the axes bounds)
        ex_angle = PI / 6

        example_line = Line(
            ORIGIN,
            example_circle.point_from_proportion(ex_angle / TAU),
            color=GREEN,
        )
        example_arc = (
            Sector(radius=0.5, angle=ex_angle, color=GREEN, fill_color=GREEN)
            .set_opacity(0.2)
        )
        P_example       = Dot(example_circle.point_from_proportion(ex_angle / TAU), color=GREEN)
        P_example_label = MathTex(r"P").next_to(P_example, UP, buff=0.1).scale(0.6)
        example_angle_label = MathTex(r"\alpha").move_to([0.7, 0.15, 0]).scale(0.6)

        # Tangent line at x=1 in math → scene x=2  (y_scale=2)
        ex_tan_x = 2.0
        example_tangent_line = Line(
            start=[ex_tan_x, -3.0, 0],
            end=[ex_tan_x,  3.0, 0],
            color=YELLOW,
            stroke_width=2,
        )
        example_tangent_line_label = MathTex(r"x=1").scale(0.6).next_to(
            [ex_tan_x, 3.0, 0], UP, buff=0.05
        )

        # Q = intersection of line OP with the tangent line x=1
        ex_Q_y = ex_tan_x * np.tan(ex_angle)   # scene units (= 2·tan α)
        example_Q = Dot([ex_tan_x, ex_Q_y, 0], color=RED)
        example_Q_label = MathTex(r"Q").next_to(example_Q, RIGHT, buff=0.1).scale(0.6)

        # Extended line from O through P to Q
        example_line_OQ = Line(ORIGIN, [ex_tan_x, ex_Q_y, 0], color=GREEN)

        # Vertical segment (1,0)→Q on the tangent line = the "tangent" length
        example_tan_segment = Line(
            [ex_tan_x, 0, 0],
            [ex_tan_x, ex_Q_y, 0],
            color=RED,
            stroke_width=6,
        )
        example_tan_label = MathTex(r"\tan\alpha").scale(0.6).next_to(
            example_tan_segment, RIGHT, buff=0.08
        )

        # ── Construction scene objects ─────────────────────────────────────────

        circle = Circle(radius=2, color=BLUE).shift(construction_axes.c2p(0, 0))
        angle  = ValueTracker(0)

        line = always_redraw(lambda: Line(
            circle.get_center(),
            circle.point_from_proportion(angle.get_value() / TAU),
            color=GREEN,
        ))
        arc = always_redraw(lambda:
            Sector(radius=0.5, angle=angle.get_value(), color=GREEN, fill_color=GREEN)
            .shift(circle.get_center())
            .set_opacity(0.2)
        )

        # Vertical tangent line at x=1 on the circle (scene: circle_center + RIGHT*2)
        const_tan_line = Line(
            start=circle.get_center() + RIGHT * 2 + DOWN * 5,
            end=circle.get_center()   + RIGHT * 2 + UP   * 5,
            color=YELLOW,
            stroke_width=1.5,
        )

        # Line from O extending through P to reach x=1 tangent line → Q
        def Q_scene_pos():
            a = angle.get_value()
            ca = np.cos(a)
            sa = np.sin(a)
            if abs(ca) < 1e-6:
                return circle.get_center() + np.array([2, np.sign(sa) * 30, 0])
            factor = 2.0 / ca
            return circle.get_center() + factor * np.array([ca, sa, 0])

        Q_line = always_redraw(lambda: Line(
            circle.get_center(),
            Q_scene_pos(),
            color=GREEN,
            stroke_width=1.5,
        ))
        Q_dot = always_redraw(lambda: Dot(Q_scene_pos(), color=RED, radius=0.07))

        # Three separate curve segments (one per branch of the tangent)
        tangent_curve_1 = VMobject(color=RED)
        tangent_curve_2 = VMobject(color=RED)
        tangent_curve_3 = VMobject(color=RED)

        dot_on_circle = Dot(circle.point_from_proportion(0), color=GREEN)
        dot_on_curve  = Dot(construction_axes.c2p(0, 0),     color=RED)

        p_label   = always_redraw(lambda: MathTex("P").next_to(dot_on_circle, UR, buff=0.1).scale(0.6))
        y_Q_label = always_redraw(lambda: MathTex("y_Q").next_to(dot_on_curve, RIGHT, buff=0.1).scale(0.6))
        dashed_line = always_redraw(lambda: DashedLine(
            start=Q_scene_pos(),
            end=dot_on_curve.get_center(),
            color=GRAY,
            dash_length=0.1,
        ))

        # Asymptote dashed lines on construction axes
        asym_pi2   = DashedLine(
            construction_axes.c2p(PI / 2, -2),
            construction_axes.c2p(PI / 2,  2),
            color=YELLOW, dash_length=0.12, stroke_width=1.5,
        )
        asym_3pi2  = DashedLine(
            construction_axes.c2p(3*PI/2, -2),
            construction_axes.c2p(3*PI/2,  2),
            color=YELLOW, dash_length=0.12, stroke_width=1.5,
        )

        def make_updater(curve):
            def updater(mob):
                a    = angle.get_value()
                t    = safe_tan(a)
                x_sc = construction_axes.c2p(a, 0)[0]
                y_sc = 2.0 * t                          # matches construction_axes.c2p(0,t)[1] when y_scale=2
                pt   = np.array([x_sc, y_sc, 0])
                if mob.has_points():
                    mob.add_line_to(pt)
                else:
                    mob.set_points([pt])
                dot_on_circle.move_to(circle.point_from_proportion(a / TAU))
                dot_on_curve.move_to(pt)
            return updater

        # ── Extended graph objects ─────────────────────────────────────────────

        # 8 branches of tan on [-4π, 4π]:
        # asymptotes at -7π/2, -5π/2, -3π/2, -π/2, π/2, 3π/2, 5π/2, 7π/2
        EX_CLIP = 3.8    # y_range boundary
        # Angular distance from each asymptote where |tan| = EX_CLIP exactly:
        # tan(π/2 - δ) = EX_CLIP  →  δ = arctan(1/EX_CLIP)
        # Each branch is plotted only up to this δ so the curve never gets clipped.
        delta = np.arctan(1.0 / EX_CLIP)   # ≈ 0.257 rad

        Y_DASH     = 2.0
        delta_dash = np.arctan(1.0 / Y_DASH)   # ≈ 0.4636 rad: |tan| = 2, where the dashes start

        ext_asym_xs = [-7*PI/2, -5*PI/2, -3*PI/2, -PI/2, PI/2, 3*PI/2, 5*PI/2, 7*PI/2]

        # Solid portions (centre of each branch, far from asymptotes)
        ext_solid_ranges = [
            (-4*PI,                  -7*PI/2 - delta_dash),
            (-7*PI/2 + delta_dash,   -5*PI/2 - delta_dash),
            (-5*PI/2 + delta_dash,   -3*PI/2 - delta_dash),
            (-3*PI/2 + delta_dash,   -  PI/2 - delta_dash),
            (-  PI/2 + delta_dash,      PI/2 - delta_dash),
            (   PI/2 + delta_dash,    3*PI/2 - delta_dash),
            ( 3*PI/2 + delta_dash,    5*PI/2 - delta_dash),
            ( 5*PI/2 + delta_dash,    7*PI/2 - delta_dash),
            ( 7*PI/2 + delta_dash,    4*PI),
        ]
        extended_tan_branches = VGroup(*[
            extended_axes.plot(np.tan, x_range=[a, b, 0.003], color=RED)
            for (a, b) in ext_solid_ranges
        ])

        # Dashed tail portions: one per branch end near each asymptote
        # (show that the curve approaches ±∞ without a hard cut)
        ext_tail_ranges = [
            (-7*PI/2 - delta_dash,   -7*PI/2 - delta),    # right end of left-edge branch
            (-7*PI/2 + delta,        -7*PI/2 + delta_dash),# left end of next branch
            (-5*PI/2 - delta_dash,   -5*PI/2 - delta),
            (-5*PI/2 + delta,        -5*PI/2 + delta_dash),
            (-3*PI/2 - delta_dash,   -3*PI/2 - delta),
            (-3*PI/2 + delta,        -3*PI/2 + delta_dash),
            (-  PI/2 - delta_dash,   -  PI/2 - delta),
            (-  PI/2 + delta,        -  PI/2 + delta_dash),
            (   PI/2 - delta_dash,      PI/2 - delta),
            (   PI/2 + delta,           PI/2 + delta_dash),
            ( 3*PI/2 - delta_dash,    3*PI/2 - delta),
            ( 3*PI/2 + delta,         3*PI/2 + delta_dash),
            ( 5*PI/2 - delta_dash,    5*PI/2 - delta),
            ( 5*PI/2 + delta,         5*PI/2 + delta_dash),
            ( 7*PI/2 - delta_dash,    7*PI/2 - delta),
            ( 7*PI/2 + delta,         7*PI/2 + delta_dash),  # left end of right-edge branch
        ]
        extended_tan_tails = VGroup(*[
            DashedVMobject(
                extended_axes.plot(np.tan, x_range=[a, b, 0.003], color=RED),
                num_dashes=8, dashed_ratio=0.5,
            )
            for (a, b) in ext_tail_ranges
        ])

        # Vertical asymptote lines on extended axes
        extended_asymptotes = VGroup(*[
            DashedLine(
                extended_axes.c2p(x, -EX_CLIP),
                extended_axes.c2p(x,  EX_CLIP),
                color=YELLOW, dash_length=0.1, stroke_width=1.2,
            )
            for x in ext_asym_xs
        ])

        # ── Animation ─────────────────────────────────────────────────────────

        # Title
        self.play(FadeIn(title, shift=0.15 * UP), run_time=text_fade_time)
        self.wait(read_pause)
        self.play(FadeOut(title), run_time=text_fade_time)

        # Example: introduce P on the unit circle
        self.play(FadeIn(intro_text, shift=0.15 * UP), run_time=text_fade_time)
        self.play(
            Create(example_axes), Create(O_example), Create(O_example_label),
            Create(example_circle), Write(example_x_label), Write(example_y_label),
        )
        self.play(Create(P_example), Create(P_example_label))
        self.wait(short_pause)
        self.play(Create(example_line), Create(example_arc), Create(example_angle_label))
        self.wait(read_pause)

        # Introduce the tangent line at (1,0)
        self.play(ReplacementTransform(intro_text, definition_text_1))
        self.wait(read_pause)
        self.play(Create(example_tangent_line), Write(example_tangent_line_label))
        self.wait(long_pause)

        # Extend OP to meet the tangent line at T
        self.play(ReplacementTransform(definition_text_1, definition_text_2))
        self.wait(read_pause)
        self.play(ReplacementTransform(example_line, example_line_OQ))
        self.play(Create(example_Q), Create(example_Q_label))
        self.wait(long_pause)

        # Show the tangent segment and its label
        self.play(ReplacementTransform(definition_text_2, definition_text_3))
        self.wait(read_pause)
        self.play(Create(example_tan_segment), Write(example_tan_label))
        self.wait(long_pause)

        example_group = VGroup(
            P_example, P_example_label, example_line_OQ, example_arc,
            example_tan_segment, example_tan_label, definition_text_3,
            example_angle_label, O_example, O_example_label,
            example_Q, example_Q_label,
            example_tangent_line, example_tangent_line_label,
        )
        self.play(*[FadeOut(mob) for mob in example_group])
        self.wait(short_pause)

        # Construction: animate the tangent curve being drawn
        self.play(FadeIn(animation_text, shift=0.15 * UP), run_time=text_fade_time)
        self.wait(read_pause)
        self.play(
            ReplacementTransform(example_axes,    construction_axes),
            ReplacementTransform(example_x_label, construction_x_label),
            ReplacementTransform(example_y_label, construction_y_label),
            ReplacementTransform(example_circle,  circle),
            run_time=2,
        )
        self.play(Create(line), Create(arc))
        self.play(Create(const_tan_line))
        # always_redraw objects go straight in with add(); plain Dots can still use FadeIn.
        self.add(tangent_curve_1, Q_line, dashed_line)
        self.play(*[FadeIn(mob) for mob in [
            dot_on_circle, dot_on_curve, Q_dot, p_label, y_Q_label,
        ]])
        self.wait(short_pause)

        # ── Branch 1: α from 0 to π/2 - ε ────────────────────────────────────
        tangent_curve_1.add_updater(make_updater(tangent_curve_1))
        self.play(angle.animate.set_value(PI / 2 - EPSILON), run_time=5, rate_func=smoothererstep)
        tangent_curve_1.clear_updaters()

        # Show first asymptote
        self.play(Create(asym_pi2), run_time=0.4)
        self.wait(short_pause)

        # Jump to start of branch 2 (below the asymptote)
        angle.set_value(PI / 2 + EPSILON)
        dot_on_circle.move_to(circle.point_from_proportion((PI / 2 + EPSILON) / TAU))
        dot_on_curve.move_to(construction_axes.c2p(
            PI / 2 + EPSILON, safe_tan(PI / 2 + EPSILON)
        ))
        self.add(tangent_curve_2)

        # ── Branch 2: α from π/2 + ε to 3π/2 - ε ─────────────────────────────
        tangent_curve_2.add_updater(make_updater(tangent_curve_2))
        self.play(angle.animate.set_value(3 * PI / 2 - EPSILON), run_time=8, rate_func=smoothererstep)
        tangent_curve_2.clear_updaters()

        # Show second asymptote
        self.play(Create(asym_3pi2), run_time=0.4)
        self.wait(short_pause)

        # Jump to start of branch 3
        angle.set_value(3 * PI / 2 + EPSILON)
        dot_on_circle.move_to(circle.point_from_proportion((3 * PI / 2 + EPSILON) / TAU))
        dot_on_curve.move_to(construction_axes.c2p(
            3 * PI / 2 + EPSILON, safe_tan(3 * PI / 2 + EPSILON)
        ))
        self.add(tangent_curve_3)

        # ── Branch 3: α from 3π/2 + ε to 2π ─────────────────────────────────
        tangent_curve_3.add_updater(make_updater(tangent_curve_3))
        self.play(angle.animate.set_value(TAU), run_time=4, rate_func=smoothererstep)
        tangent_curve_3.clear_updaters()

        # Replace dynamic curves with clean plots and flash them
        for crv in [tangent_curve_1, tangent_curve_2, tangent_curve_3]:
            self.remove(crv)

        def const_plot(x_start, x_end):
            return construction_axes.plot(
                np.tan, x_range=[x_start, x_end, 0.005], color=RED
            )

        tan_seg_1 = const_plot(0,                    PI / 2  - EPSILON)
        tan_seg_2 = const_plot(PI / 2  + EPSILON,  3*PI / 2  - EPSILON)
        tan_seg_3 = const_plot(3*PI / 2 + EPSILON,  TAU)
        tan_full  = VGroup(tan_seg_1, tan_seg_2, tan_seg_3)
        self.add(tan_full)
        self.play(ShowPassingFlash(tan_full.copy().set_color(YELLOW), time_width=0.5, run_time=2))
        self.play(FadeOut(y_Q_label), FadeOut(dashed_line))
        self.wait(read_pause)

        # Transition to extended axes
        construction_circle_group = VGroup(
            circle, dot_on_circle, dot_on_curve, p_label,
            line, arc, Q_dot, Q_line, const_tan_line,
            asym_pi2, asym_3pi2,
        )
        self.play(
            *[FadeOut(mob) for mob in construction_circle_group],
            ReplacementTransform(animation_text, function_text_1),
        )
        self.wait(read_pause)

        construction_plane_group = VGroup(
            construction_axes, construction_x_label, construction_y_label, tan_full,
        )
        VGroup(extended_axes, extended_x_label, extended_y_label,
               extended_tan_branches, extended_tan_tails, extended_asymptotes).scale(0.75)

        # Dashed continuations beyond ±4π
        continuation_left = DashedVMobject(
            extended_axes.plot(np.tan, x_range=[-4*PI - 0.7, -4*PI + 0.02, 0.005], color=RED),
            num_dashes=5, dashed_ratio=0.5,
        )
        continuation_right = DashedVMobject(
            extended_axes.plot(np.tan, x_range=[4*PI - 0.02,  4*PI + 0.7,  0.005], color=RED),
            num_dashes=5, dashed_ratio=0.5,
        )

        self.play(construction_plane_group.animate.scale(0.75).move_to(extended_axes.get_center()))
        # tan_full has 3 branches, extended_tan_branches has 9 — different counts,
        # so we fade one out and the other in instead of a ReplacementTransform.
        self.play(
            ReplacementTransform(construction_axes,    extended_axes),
            ReplacementTransform(construction_x_label, extended_x_label),
            ReplacementTransform(construction_y_label, extended_y_label),
            FadeOut(tan_full),
            FadeIn(extended_tan_branches),
            FadeIn(extended_tan_tails),
            run_time=2,
        )
        self.play(
            ReplacementTransform(function_text_1, function_text_2),
            FadeIn(extended_asymptotes),
            FadeIn(continuation_left),
            FadeIn(continuation_right),
        )
        self.wait(read_pause)

        # Final section: scale graph up, show definition and properties
        self.play(FadeOut(function_text_2))
        self.wait(short_pause)

        extended_graph = VGroup(
            extended_axes, extended_x_label, extended_y_label,
            extended_tan_branches, extended_tan_tails, extended_asymptotes,
            continuation_left, continuation_right,
        )
        self.play(
            extended_graph.animate.scale(0.5).move_to(UP * 3.2),
            self.camera.frame.animate.move_to(UP * 1.5),
            run_time=2,
        )
        self.wait(short_pause)

        # "Otteniamo la funzione tangente..."
        final_text_1a.next_to(extended_graph, DOWN, buff=0.5)
        self.play(FadeIn(final_text_1a, shift=0.15 * UP), run_time=text_fade_time)
        self.wait(read_pause)
        final_text_1b.next_to(final_text_1a, DOWN, buff=0.35)
        self.play(FadeIn(final_text_1b_left, shift=0.15 * UP), run_time=text_fade_time)
        self.wait(read_pause)
        self.play(
            FadeIn(final_text_1b_arrow, shift=0.15 * UP),
            FadeIn(final_text_1b_right, shift=0.15 * UP),
            run_time=text_fade_time,
        )
        self.wait(long_pause)
        self.play(FadeOut(final_text_1a), FadeOut(final_text_1b))
        self.wait(short_pause)

        # "La funzione f(x)=tan x ha: ..."
        final_text_2_title.next_to(extended_graph, DOWN, buff=0.8)
        self.play(Write(final_text_2_title), run_time=text_fade_time)
        self.wait(bullet_pause)

        final_text_2_item_1.next_to(final_text_2_title,  DOWN, buff=0.3, aligned_edge=LEFT)
        final_text_2_item_2.next_to(final_text_2_item_1, DOWN, buff=0.2, aligned_edge=LEFT)
        final_text_2_item_3.next_to(final_text_2_item_2, DOWN, buff=0.2, aligned_edge=LEFT)
        final_text_2_item_4.next_to(final_text_2_item_3, DOWN, buff=0.2, aligned_edge=LEFT)

        # Bullet 1 - domain: ℝ minus π/2 + kπ (x-axis with a gap at each asymptote)
        self.play(Write(final_text_2_item_1), run_time=text_fade_time)
        domain_gap = 0.35   # gap in radians left on each side of an asymptote
        domain_seg_ranges = [
            (-4*PI,                  -7*PI/2 - domain_gap),
            (-7*PI/2 + domain_gap,   -5*PI/2 - domain_gap),
            (-5*PI/2 + domain_gap,   -3*PI/2 - domain_gap),
            (-3*PI/2 + domain_gap,   -  PI/2 - domain_gap),
            (-  PI/2 + domain_gap,      PI/2 - domain_gap),
            (   PI/2 + domain_gap,    3*PI/2 - domain_gap),
            ( 3*PI/2 + domain_gap,    5*PI/2 - domain_gap),
            ( 5*PI/2 + domain_gap,    7*PI/2 - domain_gap),
            ( 7*PI/2 + domain_gap,    4*PI),
        ]
        domain_highlight = VGroup(*[
            Line(
                extended_axes.c2p(a, 0), extended_axes.c2p(b, 0),
                color=YELLOW, stroke_width=8,
            )
            for (a, b) in domain_seg_ranges
        ])
        self.play(Create(domain_highlight), run_time=pulse_time)
        self.wait(highlight_pause)
        self.play(FadeOut(domain_highlight), run_time=0.4)
        self.wait(bullet_pause)

        # Bullet 2 - range: all reals
        self.play(Write(final_text_2_item_2), run_time=text_fade_time)
        y_axis_highlight = Line(
            extended_axes.c2p(0, -EX_CLIP), extended_axes.c2p(0, EX_CLIP),
            color=YELLOW, stroke_width=8,
        )
        arrow_up   = Arrow(extended_axes.c2p(0,  EX_CLIP), extended_axes.c2p(0,  EX_CLIP + 0.6), color=YELLOW, buff=0)
        arrow_down = Arrow(extended_axes.c2p(0, -EX_CLIP), extended_axes.c2p(0, -EX_CLIP - 0.6), color=YELLOW, buff=0)
        self.play(Create(y_axis_highlight), FadeIn(arrow_up), FadeIn(arrow_down), run_time=pulse_time)
        self.wait(highlight_pause)
        self.play(FadeOut(y_axis_highlight), FadeOut(arrow_up), FadeOut(arrow_down), run_time=0.4)
        self.wait(bullet_pause)

        # Bullet 3 - period: π (highlight two adjacent branches, then a brace)
        self.play(Write(final_text_2_item_3), run_time=text_fade_time)
        central_branch = extended_axes.plot(
            np.tan, x_range=[-PI/2 + delta, PI/2 - delta, 0.003],
            color=YELLOW, stroke_width=6,
        )
        next_branch = extended_axes.plot(
            np.tan, x_range=[PI/2 + delta, 3*PI/2 - delta, 0.003],
            color=YELLOW, stroke_width=6,
        )
        self.play(Create(central_branch), run_time=0.9)
        self.wait(0.4)
        self.play(Create(next_branch), run_time=0.9)
        self.wait(0.4)
        period_brace = Brace(central_branch, DOWN, color=YELLOW)
        period_label = period_brace.get_tex(r"\pi").set_color(YELLOW)
        self.play(FadeIn(period_brace), FadeIn(period_label), run_time=pulse_time)
        self.wait(highlight_pause)
        self.play(
            *[FadeOut(mob) for mob in [central_branch, next_branch, period_brace, period_label]],
            run_time=0.5,
        )
        self.wait(bullet_pause)

        # Bullet 4 - symmetry about the origin
        self.play(Write(final_text_2_item_4), run_time=text_fade_time)

        def sym_pair(x_val):
            dot_pos    = Dot(extended_axes.c2p( x_val, np.tan( x_val)), color=YELLOW)
            dot_neg    = Dot(extended_axes.c2p(-x_val, np.tan(-x_val)), color=YELLOW)
            origin_dot = Dot(extended_axes.c2p(0, 0), color=YELLOW, radius=0.06)
            connector  = DashedLine(dot_pos.get_center(), dot_neg.get_center(), color=YELLOW, dash_length=0.08)
            return VGroup(dot_pos, dot_neg, origin_dot, connector)

        for x_sym, fadeout_time in [(PI / 5, 0.5), (PI / 3, 0.6)]:
            pair = sym_pair(x_sym)
            dot_pos, dot_neg, origin_dot, connector = pair
            self.play(
                FadeIn(dot_pos), FadeIn(dot_neg), FadeIn(origin_dot), Create(connector),
                run_time=pulse_time,
            )
            self.wait(highlight_pause)
            self.play(FadeOut(pair), run_time=fadeout_time)
            self.wait(short_pause)

        self.wait(long_pause)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(short_pause)
