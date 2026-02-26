# SineConstruction.py
# Animation that demonstrates the construction of the sine function using Manim.

from manim import *


class SineConstruction(MovingCameraScene):
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

        title = Tex(r"La funzione seno").scale(1.25)

        intro_text = Tex(
            r"Consideriamo un ", r"punto $P$", " sulla ", r"circonferenza goniometrica"
        ).to_edge(DOWN)
        intro_text[1].set_color(GREEN)
        intro_text[3].set_color(BLUE)

        definition_text_1 = Tex(
            r"Chiamiamo ", r"angolo $\alpha$", r" l'angolo tra l'asse $x$ e il raggio $OP$"
        ).to_edge(DOWN)
        definition_text_1[1].set_color(GREEN)

        definition_text_2 = Tex(
            r"L'ordinata di $P$ è detta ", r"\emph{seno}",
            r" dell'angolo $\alpha$: ", r"$y_P = \sin \alpha$"
        ).to_edge(DOWN)
        definition_text_2[1].set_color(RED)
        definition_text_2[3].set_color(RED)

        animation_text = Tex(
            r"Variamo ora l'angolo ", r"$\alpha$",
            r" e registriamo la posizione di ", r"$y_P$"
        ).to_edge(DOWN)
        animation_text[1].set_color(GREEN)
        animation_text[3].set_color(RED)

        function_text_1 = Tex(r"Immaginiamo di fare altri giri, in entrambi i sensi\dots").to_edge(DOWN)
        function_text_2 = Tex(r"\dots il grafico costruito si ripete periodicamente").to_edge(DOWN)

        final_text_1a = Tex(
            r"Otteniamo la \emph{funzione seno} che associa:", tex_environment="flushleft"
        )
        final_text_1b_left  = Tex(r"a \emph{ogni} numero reale $x$",          tex_environment="center").set_color(GREEN)
        final_text_1b_arrow = Tex(r"$\rightarrow$",                            tex_environment="center")
        final_text_1b_right = Tex(r"il \emph{corrispondente} valore $\sin x$", tex_environment="center").set_color(RED)
        final_text_1b = VGroup(final_text_1b_left, final_text_1b_arrow, final_text_1b_right).arrange(RIGHT, buff=0.2)

        final_text_2_title  = Tex(r"La funzione $f(x)=\sin x$ ha:",           tex_environment="flushleft")
        final_text_2_item_1 = Tex(r"$\bullet$ dominio: $\mathbb{R}$",          tex_environment="flushleft")
        final_text_2_item_2 = Tex(r"$\bullet$ immagine: $[-1,+1]$",            tex_environment="flushleft")
        final_text_2_item_3 = Tex(r"$\bullet$ periodo: $2\pi$",                tex_environment="flushleft")
        final_text_2_item_4 = Tex(r"$\bullet$ simmetria: rispetto all'origine", tex_environment="flushleft")

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
            y_label=r"\sin \alpha",
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

        O_example       = Dot([0, 0, 0])
        O_example_label = MathTex(r"O").next_to(O_example, DL, buff=0.1).scale(0.6)
        example_circle  = Circle(radius=2, color=BLUE)
        example_angle   = ValueTracker(PI / 3)
        example_line    = Line(
            example_circle.get_center(),
            example_circle.point_from_proportion(example_angle.get_value() / TAU),
            color=GREEN,
        )
        example_arc = (
            Sector(radius=0.5, angle=example_angle.get_value(), color=GREEN, fill_color=GREEN)
            .set_opacity(0.2)
            .shift(example_circle.get_center())
        )
        P_example       = Dot(example_circle.point_from_proportion(example_angle.get_value() / TAU), color=GREEN)
        P_example_label = MathTex(r"P").next_to(P_example, UR, buff=0.1).scale(0.6)
        example_dashed_line = DashedLine(
            start=P_example.get_center(),
            end=[P_example.get_x(), 0, 0],
            color=RED,
            dash_length=0.1,
        )
        example_angle_label  = MathTex(r"\alpha").move_to([0.5, 0.25, 0]).scale(0.6)
        example_dashed_label = MathTex(r"\sin\alpha").next_to(example_dashed_line, RIGHT, buff=0.1).scale(0.6)

        # ── Construction scene objects ─────────────────────────────────────────

        circle = Circle(radius=2, color=BLUE).shift(construction_axes.c2p(0, 0))
        angle  = ValueTracker(0)
        line   = always_redraw(lambda: Line(
            circle.get_center(),
            circle.point_from_proportion(angle.get_value() / TAU),
            color=GREEN,
        ))
        arc = always_redraw(lambda:
            Sector(radius=0.5, angle=angle.get_value(), color=GREEN, fill_color=GREEN)
            .shift(circle.get_center())
            .set_opacity(0.2)
        )

        sine_curve    = VMobject(color=RED)
        dot_on_circle = Dot(circle.point_from_proportion(0), color=GREEN)
        dot_on_curve  = Dot(circle.get_center(), color=RED)
        p_label   = always_redraw(lambda: MathTex("P").next_to(dot_on_circle, UR, buff=0.1).scale(0.6))
        y_p_label = always_redraw(lambda: MathTex("y_P").next_to(dot_on_curve, RIGHT, buff=0.1).scale(0.6))
        dashed_line = always_redraw(lambda: DashedLine(
            start=dot_on_circle.get_center(),
            end=dot_on_curve.get_center(),
            color=GRAY,
            dash_length=0.1,
        ))

        def update_sine_curve(mob):
            new_point = circle.point_from_proportion(angle.get_value() / TAU)
            x_val = construction_axes.c2p(angle.get_value(), 0)[0]
            y_val = new_point[1]
            if mob.has_points():
                mob.add_line_to(np.array([x_val, y_val, 0]))
            else:
                mob.set_points([construction_axes.c2p(0, 0), np.array([x_val, y_val, 0])])
            dot_on_circle.move_to(new_point)
            dot_on_curve.move_to(np.array([x_val, y_val, 0]))

        sine_curve.add_updater(update_sine_curve)

        # ── Extended graph objects ─────────────────────────────────────────────

        sine_function = extended_axes.plot(lambda x: np.sin(x), x_range=(-4*PI, 4*PI), color=RED)

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
        self.play(Create(example_line))
        self.play(ReplacementTransform(intro_text, definition_text_1))
        self.wait(read_pause)
        self.play(Create(example_arc), Create(example_angle_label))
        self.wait(long_pause)
        self.play(ReplacementTransform(definition_text_1, definition_text_2))
        self.wait(read_pause)
        self.play(Create(example_dashed_line), Create(example_dashed_label))
        self.wait(long_pause)

        example_group = VGroup(
            P_example, P_example_label, example_line, example_arc,
            example_dashed_line, example_dashed_label, definition_text_2,
            example_angle_label, O_example, O_example_label,
        )
        self.play(*[FadeOut(mob) for mob in example_group])
        self.wait(short_pause)

        # Construction: animate the sine curve being drawn
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
        self.play(*[FadeIn(mob) for mob in [sine_curve, dot_on_circle, dot_on_curve, p_label, y_p_label, dashed_line]])
        self.wait(short_pause)
        self.play(angle.animate.set_value(TAU), run_time=12, rate_func=smoothererstep)

        sine_curve.clear_updaters()
        sine = construction_axes.plot(lambda x: np.sin(x), x_range=(0, TAU), color=RED)
        self.add(sine)
        self.play(ShowPassingFlash(sine.copy().set_color(YELLOW), time_width=0.5, run_time=2))
        self.play(FadeOut(sine_curve), FadeOut(y_p_label), FadeOut(dashed_line))
        self.wait(read_pause)

        # Transition to extended axes
        construction_circle_group = VGroup(circle, dot_on_circle, dot_on_curve, p_label, line, arc)
        self.play(
            *[FadeOut(mob) for mob in construction_circle_group],
            ReplacementTransform(animation_text, function_text_1),
        )
        self.wait(read_pause)

        construction_plane_group = VGroup(construction_axes, construction_x_label, construction_y_label, sine)
        VGroup(extended_axes, extended_x_label, extended_y_label, sine_function).scale(0.75)

        # Dashed continuations created after the 0.75 scale so c2p is consistent
        continuation_left = DashedVMobject(
            extended_axes.plot(lambda x: np.sin(x), x_range=[-4*PI - 0.8, -4*PI + 0.02], color=RED),
            num_dashes=5, dashed_ratio=0.5,
        )
        continuation_right = DashedVMobject(
            extended_axes.plot(lambda x: np.sin(x), x_range=[4*PI - 0.02, 4*PI + 0.8], color=RED),
            num_dashes=5, dashed_ratio=0.5,
        )

        self.play(construction_plane_group.animate.scale(0.75).move_to(extended_axes.get_center()))
        self.play(
            ReplacementTransform(construction_axes,    extended_axes),
            ReplacementTransform(construction_x_label, extended_x_label),
            ReplacementTransform(construction_y_label, extended_y_label),
            ReplacementTransform(sine, sine_function),
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
            sine_function, continuation_left, continuation_right,
        )
        self.play(
            extended_graph.animate.scale(0.5).move_to(UP * 3.2),
            self.camera.frame.animate.move_to(UP * 1.5),
            run_time=2,
        )
        self.wait(short_pause)

        # "Otteniamo la funzione seno..."
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

        # "La funzione f(x)=sin x ha: ..."
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
            extended_axes.plot(lambda x: np.sin(x), x_range=list(r), color=YELLOW, stroke_width=6)
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

        # Bullet 4 – simmetria rispetto all'origine (two symmetric pairs)
        self.play(Write(final_text_2_item_4), run_time=text_fade_time)

        def sym_pair(x_val):
            """Return a VGroup showing two symmetric points connected through the origin."""
            dot_pos    = Dot(extended_axes.c2p( x_val, np.sin( x_val)), color=YELLOW)
            dot_neg    = Dot(extended_axes.c2p(-x_val, np.sin(-x_val)), color=YELLOW)
            origin_dot = Dot(extended_axes.c2p(0, 0), color=YELLOW, radius=0.06)
            connector  = DashedLine(dot_pos.get_center(), dot_neg.get_center(), color=YELLOW, dash_length=0.08)
            return VGroup(dot_pos, dot_neg, origin_dot, connector)

        for x_sym, fadeout_time in [(PI / 3, 0.5), (5 * PI / 3, 0.6)]:
            pair = sym_pair(x_sym)
            dot_pos, dot_neg, origin_dot, connector = pair
            self.play(FadeIn(dot_pos), FadeIn(dot_neg), FadeIn(origin_dot), Create(connector), run_time=pulse_time)
            self.wait(highlight_pause)
            self.play(FadeOut(pair), run_time=fadeout_time)
            self.wait(short_pause)

        self.wait(long_pause)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(short_pause)