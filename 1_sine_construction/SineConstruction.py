# Script to create an animation that demonstrates the construction of a sine function using Manim library.

from manim import *

class SineConstruction(MovingCameraScene):
    def construct(self):

        # Axes setup
        def create_axes(x_range, y_range, x_length=10, y_length=6, color=WHITE, x_ticklabels=None, y_ticklabels=None, x_label=None, y_label=None):
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

        # Title and texts
        title = Tex(r"La funzione seno").scale(1.25)
        intro_text = Tex(r"Consideriamo un ", r"punto $P$", " sulla ", r"circonferenza unitaria").to_edge(DOWN)
        intro_text[1].set_color(GREEN)
        intro_text[3].set_color(BLUE)

        definition_text_1 = Tex(r"Chiamiamo ", r"angolo $\alpha$", " l'angolo tra l'asse $x$ e il raggio $OP$").to_edge(DOWN) 
        definition_text_1[1].set_color(GREEN)

        definition_text_2 = Tex(r"L'ordinata di $P$ è detta ", r"\emph{seno}", r" dell'angolo $\alpha$: ", r"$y_P = \sin \alpha$").to_edge(DOWN)
        definition_text_2[1].set_color(RED)
        definition_text_2[3].set_color(RED)

        animation_text = Tex(r"Variamo ora l'angolo ", r"$\alpha$"," e registriamo la posizione di ",  r"$y_P$").to_edge(DOWN)
        animation_text[1].set_color(GREEN)
        animation_text[3].set_color(RED)

        function_text_1 = Tex(r"Immaginiamo di fare altri giri, in entrambi i sensi\dots").to_edge(DOWN)
        function_text_2 = Tex(r"\dots il grafico costruito si ripete periodicamente").to_edge(DOWN)

        final_text_1 = Tex(r"Otteniamo la funzione seno.", tex_environment="flushleft")
        final_text_2 = Tex(
            r"""
            La funzione $f(x) = \sin x$ ha:
                \begin{itemize}
                    \item dominio $\mathbb{R}$
                    \item immagine $[-1,+1]$
                    \item periodo $2\pi$
                \end{itemize}
            """, tex_environment="flushleft")

        # Create example axes
        example_axes, example_x_label, example_y_label = create_axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            x_ticklabels={1: MathTex(r"1"), -1: MathTex(r"-1")},
            y_ticklabels={1: MathTex(r"1"), -1: MathTex(r"-1")},
            x_label=r"x",
            y_label=r"y"
        )

        # Create construction axes
        construction_axes, construction_x_label, construction_y_label = create_axes(
            x_range=[0, TAU+0.5, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            x_ticklabels={PI/2: MathTex(r"\frac{\pi}{2}"), PI: MathTex(r"\pi"), 3*PI/2: MathTex(r"\frac{3\pi}{2}"), TAU: MathTex(r"2\pi")},
            y_ticklabels={1: MathTex(r"1"), -1: MathTex(r"-1")},
            x_label=r"\alpha",
            y_label=r"\sin \alpha"
        )

        # Create extended axes
        extended_axes, extended_x_label, extended_y_label = create_axes(
            x_range=[-2*TAU-1, 2*TAU+1, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=16,
            x_ticklabels={
                -4 * PI: MathTex(r"-4\pi"),
                -3 * PI: MathTex(r"-3\pi"),
                -2 * PI: MathTex(r"-2\pi"),
                -PI: MathTex(r"-\pi"),
                0: MathTex(r"0"),
                PI: MathTex(r"\pi"),
                2 * PI: MathTex(r"2\pi"),
                3 * PI: MathTex(r"3\pi"),
                4 * PI: MathTex(r"4\pi"),
            },
            y_ticklabels={1: MathTex(r"1"), -1: MathTex(r"-1")},
            x_label=r"x",
            y_label=r"y"
        )

        # Create the circle
        circle = Circle(radius=2, color=BLUE).shift(construction_axes.c2p(0, 0))

        # Create the angle
        angle = ValueTracker(0)
        line = always_redraw(lambda: Line(circle.get_center(), circle.point_from_proportion(angle.get_value() / TAU), color=GREEN))
        arc = always_redraw(lambda: Sector(radius=0.5, angle=angle.get_value(), color=GREEN, fill_color=GREEN).shift(circle.get_center()).set_opacity(0.2))

        # Create the sine curve
        sine_curve = VMobject(color=RED)
        dot_on_circle = Dot(color=GREEN)
        dot_on_curve = Dot(color=RED)

        # Labels for points
        p_label = always_redraw(lambda: MathTex("P").next_to(dot_on_circle, UR, buff=0.1).scale(0.7))
        y_p_label = always_redraw(lambda: MathTex("y_P").next_to(dot_on_curve, RIGHT, buff=0.1).scale(0.7))

        # Create dashed line connecting P to y_P
        dashed_line = always_redraw(lambda: DashedLine(
            start=dot_on_circle.get_center(),
            end=dot_on_curve.get_center(),
            color=GRAY,
            dash_length=0.1
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

        # Create the example points
        O_example = Dot([0,0,0])
        O_example_label = MathTex(r"O").next_to(O_example, DL, buff=0.1).scale(0.7)
        example_circle = Circle(radius=2, color=BLUE)
        example_angle = ValueTracker(PI/4)
        example_line = always_redraw(lambda: Line(example_circle.get_center(), example_circle.point_from_proportion(example_angle.get_value() / TAU), color=GREEN))
        example_arc = Sector(radius=0.5, angle=example_angle.get_value(), color=GREEN, fill_color=GREEN).set_opacity(0.2).shift(example_circle.get_center())

        P_example = Dot(example_circle.point_from_proportion(example_angle.get_value() / TAU), color=GREEN)
        P_example_label = MathTex(r"P").next_to(P_example, UR, buff=0.1).scale(0.7)
        dashed_line_example = DashedLine(
            start=P_example.get_center(),
            end=Dot(point=[P_example.get_x(),0,0]).get_center(),
            color=RED,
            dash_length=0.1
        )

        example_angle_label = MathTex(r"\alpha").next_to(example_arc, 0.2*RIGHT, buff=0.1).scale(0.7)

        # Create the complete sine function
        sine_function = extended_axes.plot(lambda x: np.sin(x), x_range=(-20,20), color=RED)

        # Animation
        # Animate the title
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title), run_time=1.5) 

        # Animate the example
        self.play(Write(intro_text))
        self.play(Create(example_axes), Create(O_example),Create(O_example_label), Create(example_circle), Write(example_x_label), Write(example_y_label))
        self.play(Create(P_example), Create(P_example_label))
        self.wait(1)
        self.play(Create(example_line))
        self.play(ReplacementTransform(intro_text, definition_text_1))
        self.wait(1)
        self.play(Create(example_arc), Create(example_angle_label))
        self.wait(3)
        self.play(ReplacementTransform(definition_text_1, definition_text_2))
        self.wait(1)
        self.play(Create(dashed_line_example))
        self.wait(3)

        example_group = VGroup(P_example, P_example_label,example_line,example_arc, dashed_line_example, definition_text_2, example_angle_label, O_example, O_example_label)

        self.play(*[FadeOut(mob) for mob in example_group])

        self.play([
            ReplacementTransform(example_axes, construction_axes),
            ReplacementTransform(example_x_label, construction_x_label),
            ReplacementTransform(example_y_label, construction_y_label),
            ReplacementTransform(example_circle, circle)
        ], run_time=2)

        # Animate the construction
        self.play(Write(animation_text))
        sine_construction = VGroup(line, arc, sine_curve, dot_on_circle, dot_on_curve, p_label, y_p_label, dashed_line)
        self.play(*[FadeIn(mob)for mob in sine_construction])
        self.play(angle.animate.set_value(TAU), run_time=11, rate_func=smoothererstep)
        sine_curve.clear_updaters()
        sine = construction_axes.plot(lambda x: np.sin(x), x_range=(0,TAU), color=RED)
        self.add(sine)
        self.play(ShowPassingFlash(sine.copy().set_color(YELLOW), time_width=0.5, run_time=2))

        self.play(
            FadeOut(sine_curve),
            FadeOut(y_p_label),
            FadeOut(dashed_line), 
        )
        
        self.wait(2)

        # Remove circle and points
        construction_circle_group = VGroup(circle, dot_on_circle, dot_on_curve, p_label, line, arc)
        self.play(
            *[FadeOut(mob) for mob in construction_circle_group],
            ReplacementTransform(animation_text, function_text_1),
        )
        self.wait(2)
        construction_plane_group = VGroup(construction_axes, construction_x_label, construction_y_label, sine)
        extended_plane_group = VGroup(extended_axes, extended_x_label, extended_y_label, sine_function).scale(0.75)

        self.play(construction_plane_group.animate.scale(0.75).move_to(construction_axes.c2p(PI, 0)))
        self.play([
            ReplacementTransform(construction_axes, extended_axes),
            ReplacementTransform(construction_x_label, extended_x_label),
            ReplacementTransform(construction_y_label, extended_y_label),
            ReplacementTransform(sine,sine_function),
        ], run_time=2)
        self.play(ReplacementTransform(function_text_1, function_text_2))
        self.wait(3) 

        # Show final result
        self.play( *[FadeOut(mob)for mob in self.mobjects])
        self.play(Write(final_text_1))
        self.wait(1)
        self.play(FadeOut(final_text_1)) 
        self.play(Write(final_text_2), run_time=3)
        self.wait(3)
        self.play(*[FadeOut(mob)for mob in self.mobjects])