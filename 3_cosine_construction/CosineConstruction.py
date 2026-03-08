# CosineConstruction.py
# Animation that demonstrates the construction of the cosine function using Manim.
# Key idea: cos α = x_P = sin(π/2 - α) = y_Q, where Q is the point at the complementary angle.

from manim import *


class CosineConstruction(MovingCameraScene):
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

        # ── Timing constants ───────────────────────────────────────────────────

        text_fade_time  = 1.4   # FadeIn/Write duration for text
        short_pause     = 1.0   # brief beat
        read_pause      = 2.0   # time to read a line of text
        long_pause      = 3.0   # time to absorb a key concept
        pulse_time      = 0.8   # highlight animation duration
        highlight_pause = 1.5   # pause after a highlight before fade-out
        bullet_pause    = 2.0   # pause between property bullets

        # ── Texts ──────────────────────────────────────────────────────────────

        title = Tex(r"La funzione coseno").scale(1.25)

        intro_text = Tex(
            r"Consideriamo un ", r"punto $P$", " sulla ", r"circonferenza goniometrica"
        ).to_edge(DOWN)
        intro_text[1].set_color(GREEN)
        intro_text[3].set_color(BLUE)

        definition_text_1 = Tex(
            r"L'ascissa di $P$ è detta ", r"\emph{coseno}",
            r" dell'angolo $\alpha$: ", r"$x_P = \cos \alpha$"
        ).to_edge(DOWN)
        definition_text_1[1].set_color(RED)
        definition_text_1[3].set_color(RED)

        definition_text_2 = Tex(
            r"ed è uguale al \emph{seno} del suo ", r"complementare", r": ",
            r"$\cos\alpha = \sin\!\left(\dfrac{\pi}{2}-\alpha\right)$"
        ).to_edge(DOWN)
        definition_text_2[1].set_color(TEAL)
        definition_text_2[3].set_color(RED)

        animation_text = Tex(
            r"Variamo ora l'angolo ", r"$\alpha$",
            r" e registriamo la posizione di ", r"$y_Q = x_P$"
        ).to_edge(DOWN)
        animation_text[1].set_color(GREEN)
        animation_text[3].set_color(RED)

        function_text_1 = Tex(r"Immaginiamo di fare altri giri, in entrambi i sensi\dots").to_edge(DOWN)
        function_text_2 = Tex(r"\dots il grafico costruito si ripete periodicamente").to_edge(DOWN)

        final_text_1a = Tex(
            r"Otteniamo la \emph{funzione coseno} che associa:", tex_environment="flushleft"
        )
        final_text_1b_left  = Tex(r"a \emph{ogni} numero reale $x$",           tex_environment="center").set_color(GREEN)
        final_text_1b_arrow = Tex(r"$\rightarrow$",                             tex_environment="center")
        final_text_1b_right = Tex(r"il \emph{corrispondente} valore $\cos x$",  tex_environment="center").set_color(RED)
        final_text_1b = VGroup(final_text_1b_left, final_text_1b_arrow, final_text_1b_right).arrange(RIGHT, buff=0.2)

        final_text_2_title  = Tex(r"La funzione $f(x)=\cos x$ ha:",             tex_environment="flushleft")
        final_text_2_item_1 = Tex(r"$\bullet$ dominio: $\mathbb{R}$",           tex_environment="flushleft")
        final_text_2_item_2 = Tex(r"$\bullet$ immagine: $[-1,+1]$",             tex_environment="flushleft")
        final_text_2_item_3 = Tex(r"$\bullet$ periodo: $2\pi$",                 tex_environment="flushleft")
        final_text_2_item_4 = Tex(r"$\bullet$ simmetria: rispetto all'asse $y$", tex_environment="flushleft")

        # ── Axes ───────────────────────────────────────────────────────────────

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
            y_label=r"\cos \alpha",
        )

        extended_axes, extended_x_label, extended_y_label = create_axes(
            x_range=[-2*TAU - 1, 2*TAU + 1, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=16,
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
            y_ticklabels={1: MathTex(r"1"), -1: MathTex(r"-1")},
            x_label=r"x",
            y_label=r"y",
        )

        # ── Example scene objects ──────────────────────────────────────────────

        # α = π/3 → P = (cos π/3, sin π/3) = (0.5, √3/2) in math → (1, √3) in scene
        # complementary = π/2 - π/3 = π/6 → Q = (cos π/6, sin π/6) = (√3/2, 0.5) → (√3, 1)
        ex_angle = PI / 3
        ex_comp  = PI / 2 - ex_angle   # = π/6

        O_example       = Dot([0, 0, 0])
        O_example_label = MathTex(r"O").next_to(O_example, DL, buff=0.1).scale(0.6)
        example_circle  = Circle(radius=2, color=BLUE)

        example_line = Line(
            ORIGIN,
            example_circle.point_from_proportion(ex_angle / TAU),
            color=GREEN,
        )
        example_arc = (
            Sector(radius=0.5, angle=ex_angle, color=GREEN, fill_color=GREEN)
            .set_opacity(0.2)
        )
        example_angle_label = MathTex(r"\alpha").move_to([0.5, 0.25, 0]).scale(0.6)

        P_example       = Dot(example_circle.point_from_proportion(ex_angle / TAU), color=GREEN)
        P_example_label = MathTex(r"P").next_to(P_example, UR, buff=0.1).scale(0.6)

        # Vertical dashed from P down to x-axis → shows x_P = cos α
        P_scene = example_circle.point_from_proportion(ex_angle / TAU)
        example_dashed_x = DashedLine(
            start=P_scene,
            end=[P_scene[0], 0, 0],
            color=RED,
            dash_length=0.1,
        )
        example_cos_label = MathTex(r"\cos\alpha").next_to(
            example_dashed_x, DOWN, buff=0.1
        ).scale(0.6).set_color(RED)

        # Q at complementary angle, line OQ, arc for (π/2 - α), y-dashed
        Q_scene = example_circle.point_from_proportion(ex_comp / TAU)
        example_line_Q = Line(ORIGIN, Q_scene, color=TEAL)
        example_arc_comp = (
            Sector(radius=0.7, angle=ex_comp, color=TEAL, fill_color=TEAL)
            .set_opacity(0.2)
        )
        example_comp_label = MathTex(r"\frac{\pi}{2}-\alpha").move_to([0.95, 0.2, 0]).scale(0.5).set_color(TEAL)
        Q_example       = Dot(Q_scene, color=TEAL)
        Q_example_label = MathTex(r"Q").next_to(Q_example, UR, buff=0.1).scale(0.6).set_color(TEAL)

        # Horizontal dashed from Q left to y-axis → shows y_Q = sin(π/2-α) = cos α
        example_dashed_y = DashedLine(
            start=Q_scene,
            end=[0, Q_scene[1], 0],
            color=RED,
            dash_length=0.1,
        )
        example_sin_comp_label = MathTex(r"\sin\!\left(\tfrac{\pi}{2}\!-\!\alpha\right)").next_to(
            example_dashed_y, UP, buff=0.05
        ).scale(0.55).set_color(RED)

        # ── Construction scene objects ─────────────────────────────────────────

        # y_scale = y_length / (y_max - y_min) = 6/3 = 2, radius = 2 → consistent
        circle = Circle(radius=2, color=BLUE).shift(construction_axes.c2p(0, 0))
        angle  = ValueTracker(0)

        # P at angle α (GREEN) – shown for context
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
        dot_on_circle = Dot(circle.point_from_proportion(0), color=GREEN)
        p_label = always_redraw(lambda: MathTex("P").next_to(dot_on_circle, UR, buff=0.1).scale(0.6))

        # Q at complementary angle π/2 - α (TEAL) – its y-coord = cos α
        def Q_pos():
            a = angle.get_value()
            comp = PI / 2 - a
            return circle.get_center() + 2 * np.array([np.cos(comp), np.sin(comp), 0])
            # equivalently: circle.get_center() + 2 * np.array([np.sin(a), np.cos(a), 0])

        line_Q = always_redraw(lambda: Line(
            circle.get_center(),
            Q_pos(),
            color=TEAL,
            stroke_width=1.5,
        ))
        dot_on_Q = always_redraw(lambda: Dot(Q_pos(), color=TEAL, radius=0.07))
        q_label  = always_redraw(lambda: MathTex("Q").next_to(Q_pos(), UR, buff=0.1).scale(0.6).set_color(TEAL))

        # dot_on_curve traces (α, cos α): same y-coord as Q  [cos α · 2 = Q_y - circle_center_y]
        dot_on_curve = Dot(circle.get_center(), color=RED)
        x_P_label    = always_redraw(lambda: MathTex("y_Q = x_P").next_to(dot_on_curve, RIGHT, buff=0.1).scale(0.6))

        # Horizontal dashed from Q to dot_on_curve (same y-coordinate by construction).
        # Guard against zero-length: at α=0, start==end which crashes DashedLine.
        def _make_dashed():
            s = np.array(Q_pos())
            e = np.array(dot_on_curve.get_center())
            if np.linalg.norm(s - e) < 0.05:
                return VMobject()
            return DashedLine(start=s, end=e, color=GRAY, dash_length=0.1)

        dashed_line = always_redraw(_make_dashed)

        cosine_curve = VMobject(color=RED)

        def update_cosine_curve(mob):
            a     = angle.get_value()
            x_val = construction_axes.c2p(a, 0)[0]
            # cos α in scene coords = circle_center_y + 2*cos α = Q_pos()[1]
            y_val = Q_pos()[1]
            if mob.has_points():
                mob.add_line_to(np.array([x_val, y_val, 0]))
            else:
                mob.set_points([construction_axes.c2p(0, 0), np.array([x_val, y_val, 0])])
            dot_on_circle.move_to(circle.point_from_proportion(a / TAU))
            dot_on_curve.move_to(np.array([x_val, y_val, 0]))

        cosine_curve.add_updater(update_cosine_curve)

        # ── Extended graph objects ─────────────────────────────────────────────

        cosine_function = extended_axes.plot(lambda x: np.cos(x), x_range=(-4*PI, 4*PI), color=RED)

        # ── Animation ─────────────────────────────────────────────────────────

        # Title
        self.play(FadeIn(title, shift=0.15 * UP), run_time=text_fade_time)
        self.wait(read_pause)
        self.play(FadeOut(title), run_time=text_fade_time)

        # Example: introduce point P on the unit circle
        self.play(FadeIn(intro_text, shift=0.15 * UP), run_time=text_fade_time)
        self.play(
            Create(example_axes), Create(O_example), Create(O_example_label),
            Create(example_circle), Write(example_x_label), Write(example_y_label),
        )
        self.play(Create(P_example), Create(P_example_label))
        self.wait(short_pause)
        self.play(Create(example_line), Create(example_arc), Create(example_angle_label))
        self.wait(read_pause)

        # Show x_P = cos α (vertical dashed from P to x-axis)
        self.play(ReplacementTransform(intro_text, definition_text_1))
        self.wait(read_pause)
        self.play(Create(example_dashed_x), Write(example_cos_label))
        self.wait(long_pause)

        # Show complementary angle Q and y_Q = sin(π/2-α) = cos α
        self.play(ReplacementTransform(definition_text_1, definition_text_2))
        self.wait(read_pause)
        self.play(
            Create(example_line_Q), Create(example_arc_comp), Write(example_comp_label),
        )
        self.play(Create(Q_example), Create(Q_example_label))
        self.wait(short_pause)
        self.play(Create(example_dashed_y), Write(example_sin_comp_label))
        self.wait(long_pause)

        example_group = VGroup(
            P_example, P_example_label, example_line, example_arc,
            example_dashed_x, example_cos_label, example_angle_label,
            Q_example, Q_example_label, example_line_Q, example_arc_comp,
            example_dashed_y, example_sin_comp_label, example_comp_label,
            definition_text_2, O_example, O_example_label,
        )
        self.play(*[FadeOut(mob) for mob in example_group])
        self.wait(short_pause)

        # Construction: animate the cosine curve being drawn
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
        # always_redraw objects and empty VMobjects cannot be FadeIn'd reliably:
        # add them directly to the scene instead.
        self.add(cosine_curve, dot_on_circle, dot_on_curve,
                 line_Q, dot_on_Q, q_label, p_label, x_P_label, dashed_line)
        self.wait(short_pause)
        self.play(angle.animate.set_value(TAU), run_time=12, rate_func=smoothererstep)

        cosine_curve.clear_updaters()
        cosine = construction_axes.plot(lambda x: np.cos(x), x_range=(0, TAU), color=RED)
        self.add(cosine)
        self.play(ShowPassingFlash(cosine.copy().set_color(YELLOW), time_width=0.5, run_time=2))
        # The incremental VMobject and always_redraw objects can have degenerate
        # point arrays that crash FadeOut – remove them directly instead.
        x_P_label.clear_updaters()
        dashed_line.clear_updaters()
        self.remove(cosine_curve, dashed_line, x_P_label)
        self.wait(read_pause)

        # Transition to extended axes
        construction_circle_group = VGroup(
            circle, dot_on_circle, dot_on_curve, p_label,
            line, arc, line_Q, dot_on_Q, q_label,
        )
        self.play(
            *[FadeOut(mob) for mob in construction_circle_group],
            ReplacementTransform(animation_text, function_text_1),
        )
        self.wait(read_pause)

        construction_plane_group = VGroup(construction_axes, construction_x_label, construction_y_label, cosine)
        VGroup(extended_axes, extended_x_label, extended_y_label, cosine_function).scale(0.75)

        # Dashed continuations created after the 0.75 scale so c2p is consistent
        continuation_left = DashedVMobject(
            extended_axes.plot(lambda x: np.cos(x), x_range=[-4*PI - 0.8, -4*PI + 0.02], color=RED),
            num_dashes=5, dashed_ratio=0.5,
        )
        continuation_right = DashedVMobject(
            extended_axes.plot(lambda x: np.cos(x), x_range=[4*PI - 0.02, 4*PI + 0.8], color=RED),
            num_dashes=5, dashed_ratio=0.5,
        )

        self.play(construction_plane_group.animate.scale(0.75).move_to(extended_axes.get_center()))
        self.play(
            ReplacementTransform(construction_axes,    extended_axes),
            ReplacementTransform(construction_x_label, extended_x_label),
            ReplacementTransform(construction_y_label, extended_y_label),
            ReplacementTransform(cosine, cosine_function),
            run_time=2,
        )
        self.play(
            ReplacementTransform(function_text_1, function_text_2),
            FadeIn(continuation_left),
            FadeIn(continuation_right),
        )
        self.wait(read_pause)

        # Final section: scale graph up, show definition and properties
        self.play(FadeOut(function_text_2))
        self.wait(short_pause)

        extended_graph = VGroup(
            extended_axes, extended_x_label, extended_y_label,
            cosine_function, continuation_left, continuation_right,
        )
        self.play(
            extended_graph.animate.scale(0.5).move_to(UP * 3.2),
            self.camera.frame.animate.move_to(UP * 1.5),
            run_time=2,
        )
        self.wait(short_pause)

        # "Otteniamo la funzione coseno..."
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

        # "La funzione f(x)=cos x ha: ..."
        final_text_2_title.next_to(extended_graph, DOWN, buff=0.8)
        self.play(Write(final_text_2_title), run_time=text_fade_time)
        self.wait(bullet_pause)

        final_text_2_item_1.next_to(final_text_2_title,  DOWN, buff=0.3, aligned_edge=LEFT)
        final_text_2_item_2.next_to(final_text_2_item_1, DOWN, buff=0.2, aligned_edge=LEFT)
        final_text_2_item_3.next_to(final_text_2_item_2, DOWN, buff=0.2, aligned_edge=LEFT)
        final_text_2_item_4.next_to(final_text_2_item_3, DOWN, buff=0.2, aligned_edge=LEFT)

        # Bullet 1 – dominio: ℝ (x-axis highlight)
        self.play(Write(final_text_2_item_1), run_time=text_fade_time)
        x_axis_highlight = Line(
            extended_axes.c2p(-4*PI, 0), extended_axes.c2p(4*PI, 0),
            color=YELLOW, stroke_width=8,
        )
        self.play(Create(x_axis_highlight), run_time=pulse_time)
        self.wait(highlight_pause)
        self.play(FadeOut(x_axis_highlight), run_time=0.4)
        self.wait(bullet_pause)

        # Bullet 2 – immagine: [−1, +1] (band highlight)
        self.play(Write(final_text_2_item_2), run_time=text_fade_time)
        image_band = Polygon(
            extended_axes.c2p(-4*PI, -1), extended_axes.c2p(4*PI, -1),
            extended_axes.c2p(4*PI,   1), extended_axes.c2p(-4*PI,  1),
            color=YELLOW, fill_opacity=0.15, stroke_width=0,
        )
        image_upper = DashedLine(extended_axes.c2p(-4*PI, 1), extended_axes.c2p(4*PI, 1), color=YELLOW, dash_length=0.12)
        image_lower = DashedLine(extended_axes.c2p(-4*PI,-1), extended_axes.c2p(4*PI,-1), color=YELLOW, dash_length=0.12)
        self.play(FadeIn(image_band), Create(image_upper), Create(image_lower), run_time=pulse_time)
        self.wait(highlight_pause)
        self.play(FadeOut(image_band), FadeOut(image_upper), FadeOut(image_lower), run_time=0.4)
        self.wait(bullet_pause)

        # Bullet 3 – periodo: 2π (cycles expanding outward from centre, then brace)
        self.play(Write(final_text_2_item_3), run_time=text_fade_time)
        cycle_ranges = [(0, TAU), (-TAU, 0), (TAU, 2*TAU), (-2*TAU, -TAU)]
        cycles = [
            extended_axes.plot(lambda x: np.cos(x), x_range=list(r), color=YELLOW, stroke_width=6)
            for r in cycle_ranges
        ]
        for cyc in cycles:
            self.play(Create(cyc), run_time=0.9)
            self.wait(0.4)
        period_brace = Brace(cycles[0], DOWN, color=YELLOW)
        period_label = period_brace.get_tex(r"2\pi").set_color(YELLOW)
        self.play(FadeIn(period_brace), FadeIn(period_label), run_time=pulse_time)
        self.wait(highlight_pause)
        self.play(*[FadeOut(mob) for mob in [*cycles, period_brace, period_label]], run_time=0.5)
        self.wait(bullet_pause)

        # Bullet 4 – simmetria rispetto all'asse y (funzione pari: cos(-x) = cos(x))
        self.play(Write(final_text_2_item_4), run_time=text_fade_time)

        def sym_pair_even(x_val):
            """Two symmetric points (x, cos x) and (-x, cos x) with y-axis as symmetry axis."""
            dot_pos    = Dot(extended_axes.c2p( x_val, np.cos( x_val)), color=YELLOW)
            dot_neg    = Dot(extended_axes.c2p(-x_val, np.cos(-x_val)), color=YELLOW)
            y_axis_dot = Dot(extended_axes.c2p(0, np.cos(x_val)),       color=YELLOW, radius=0.06)
            connector  = DashedLine(dot_pos.get_center(), dot_neg.get_center(), color=YELLOW, dash_length=0.08)
            return VGroup(dot_pos, dot_neg, y_axis_dot, connector)

        for x_sym, fadeout_time in [(PI / 3, 0.5), (2 * PI / 3, 0.6)]:
            pair = sym_pair_even(x_sym)
            dot_pos, dot_neg, y_axis_dot, connector = pair
            self.play(FadeIn(dot_pos), FadeIn(dot_neg), FadeIn(y_axis_dot), Create(connector), run_time=pulse_time)
            self.wait(highlight_pause)
            self.play(FadeOut(pair), run_time=fadeout_time)
            self.wait(short_pause)

        self.wait(long_pause)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(short_pause)
