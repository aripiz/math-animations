# KeplerLaws.py
# Animation that introduces and visualizes Kepler's three laws with Manim.

from manim import *


class KeplerLaws(MovingCameraScene):
    def construct(self):

        # ── Timing constants ──────────────────────────────────────────────────
        text_fade_time = 1.4
        short_pause    = 1.0
        read_pause     = 3.0
        long_pause     = 4.0

        # ── Helpers ───────────────────────────────────────────────────────────

        def ellipse_point(a, b, t, center=ORIGIN):
            return center + np.array([a * np.cos(t), b * np.sin(t), 0.0])

        def solve_kepler_equation(mean_anomaly, eccentricity, iterations=8):
            """Newton solve for eccentric anomaly: M = E - e*sin(E)."""
            E = mean_anomaly
            for _ in range(iterations):
                E -= (E - eccentricity * np.sin(E) - mean_anomaly) / (
                    1 - eccentricity * np.cos(E)
                )
            return E

        def make_swept_sector(a, b, E_start, E_end, center, focus_point, color):
            """Filled polygon: focus → arc from E_start to E_end → focus."""
            pts = [ellipse_point(a, b, t, center=center) for t in np.linspace(E_start, E_end, 60)]
            return Polygon(
                focus_point, *pts,
                color=color, fill_color=color, fill_opacity=0.40, stroke_width=1.5,
            )

        def make_area_updater(sector_holder, a, b, E_start, center, focus, color):
            """Returns an updater that redraws the swept sector as E_tracker grows."""
            def updater(mob, E_tracker=None):
                E_end = E_tracker.get_value()
                if E_end <= E_start:
                    mob.become(VMobject())
                    return
                new_sector = make_swept_sector(a, b, E_start, E_end, center, focus, color)
                mob.become(new_sector)
            return updater

        # ── Text blocks ───────────────────────────────────────────────────────

        title = Tex(r"Le tre leggi di Keplero").scale(1.25)

        def law_tex(*parts):
            t = Tex(*parts, font_size=38)
            t.to_edge(DOWN)
            return t

        law_1_text = law_tex(
            r"Ogni pianeta percorre un'orbita ellittica attorno al Sole", r"\\",
            r"che si trova in uno dei due fuochi dell'ellisse.",
        )
        law_2_text = law_tex(
            r"Il segmento che collega il pianeta al Sole", r"\\",
            r"copre sul piano dell'orbita aree uguali in tempi uguali.",
        )
        law_3_text = law_tex(
            r"Il rapporto tra il quadrato del periodo orbitale e il cubo del semiasse maggiore", r"\\",
            r"dell'orbita è una costante uguale per tutti i pianeti del sistema solare.",
        )

        def law_header(text):
            h = Tex(text, font_size=40)
            h.to_edge(UP)
            rect = SurroundingRectangle(
                h, color=WHITE,
                fill_color=BLACK, fill_opacity=1,
                corner_radius=0.12, buff=0.22, stroke_width=1.5,
            )
            return VGroup(rect, h)

        law_1_header = law_header(r"Prima legge")
        law_2_header = law_header(r"Seconda legge")
        law_3_header = law_header(r"Terza legge")

        # ── Scene vertical offset ─────────────────────────────────────────────
        SCENE_UP = UP * 0.7

        # ── Intro ─────────────────────────────────────────────────────────────
        self.play(FadeIn(title, shift=0.15 * UP), run_time=text_fade_time)
        self.wait(read_pause)
        self.play(FadeOut(title), run_time=text_fade_time)

        # ==================================================================
        # LAW 1 — Elliptical orbit, Sun at one focus
        # ==================================================================
        a1   = 2.8
        b1   = 1.8
        c1   = np.sqrt(a1**2 - b1**2)
        e1   = c1 / a1
        ctr1 = SCENE_UP

        orbit1 = ParametricFunction(
            lambda t: ellipse_point(a1, b1, t, center=ctr1),
            t_range=[0, TAU], color=BLUE,
        )

        foc1_pos = ctr1 + RIGHT * c1
        foc2_pos = ctr1 + LEFT  * c1

        focus_1       = Dot(foc1_pos, color=YELLOW, radius=0.10)
        focus_2       = Dot(foc2_pos, color=GRAY,   radius=0.07)
        sun           = Dot(foc1_pos, color=YELLOW, radius=0.12)
        center        = Dot(ctr1, color=GRAY, radius=0.05)
        focus_1_label = MathTex(r"F_1", font_size=28).next_to(focus_1, UP, buff=0.12)
        focus_2_label = MathTex(r"F_2", font_size=28).next_to(focus_2, UP, buff=0.12)
        sun_label     = Tex(r"Sole", font_size=26).next_to(sun, DOWN, buff=0.18)

        semi_a_line = DashedLine(
            ctr1 + LEFT * a1, ctr1 + RIGHT * a1, color=GRAY, stroke_width=1.0
        )
        semi_b_line = DashedLine(
            ctr1 + DOWN * b1, ctr1 + UP * b1, color=GRAY, stroke_width=1.0
        )
        a_label = MathTex(r"a", font_size=28).next_to(ctr1 + RIGHT * (a1 * 0.5), DOWN, buff=0.12)
        b_label = MathTex(r"b", font_size=28).next_to(ctr1 + UP    * (b1 * 0.5), LEFT, buff=0.12)

        peri1_pos = ctr1 + RIGHT * a1
        aph1_pos  = ctr1 + LEFT  * a1
        peri1_dot = Dot(peri1_pos, color=WHITE, radius=0.05)
        aph1_dot  = Dot(aph1_pos,  color=WHITE, radius=0.05)
        peri1_lbl = Tex(r"Perielio", font_size=22).next_to(peri1_pos, UR, buff=0.10)
        aph1_lbl  = Tex(r"Afelio",   font_size=22).next_to(aph1_pos,  UL, buff=0.10)

        t1      = ValueTracker(0.0)
        planet1 = always_redraw(lambda: Dot(
            ellipse_point(a1, b1, t1.get_value(), center=ctr1),
            color=GREEN, radius=0.08,
        ))
        radius_line1 = always_redraw(lambda: Line(
            sun.get_center(),
            planet1.get_center(),
            color=GREEN, stroke_width=2,
        ))
        planet1_label = Tex(r"Pianeta", font_size=24)
        planet1_label.add_updater(lambda m: m.next_to(planet1, UP, buff=0.08))

        self.play(FadeIn(law_1_header), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(law_1_text, shift=0.15 * UP), run_time=2.2)
        self.wait(read_pause)

        self.play(Create(orbit1), run_time=2)
        self.play(
            FadeIn(semi_a_line), FadeIn(semi_b_line),  FadeIn(center),
            Write(a_label), Write(b_label),
            run_time=1.4,
        )
        self.play(
            FadeIn(focus_1), FadeIn(focus_2),
            Write(focus_1_label), Write(focus_2_label),
            FadeIn(peri1_dot), FadeIn(aph1_dot),
            Write(peri1_lbl), Write(aph1_lbl),
            run_time=1.4,
        )
        self.play(FadeIn(sun), Write(sun_label), run_time=1.0)
        self.wait(short_pause)

        self.play(
            FadeOut(semi_a_line), FadeOut(semi_b_line), FadeOut(center),
            FadeOut(a_label), FadeOut(b_label),
            FadeOut(focus_2), FadeOut(focus_2_label),
            FadeOut(focus_1_label),
            FadeOut(sun_label),
            run_time=0.8,
        )

        self.play(FadeIn(planet1), Create(radius_line1), Write(planet1_label), run_time=1.0)
        self.play(t1.animate.set_value(TAU), run_time=10, rate_func=linear)
        self.wait(long_pause)

        law1_group = VGroup(
            orbit1, focus_1, sun, planet1, radius_line1, planet1_label,
            peri1_dot, aph1_dot, peri1_lbl, aph1_lbl,
        )

        # ==================================================================
        # LAW 2 — Equal areas in equal times
        # ==================================================================
        self.play(
            FadeOut(law1_group),
            FadeOut(law_1_text),
            FadeOut(law_1_header),
            run_time=1.0,
        )
        self.play(FadeIn(law_2_header), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(law_2_text, shift=0.15 * UP), run_time=2.2)
        self.wait(read_pause)

        ctr2     = ctr1
        sun2_pos = ctr2 + RIGHT * c1

        orbit2   = ParametricFunction(
            lambda t: ellipse_point(a1, b1, t, center=ctr2),
            t_range=[0, TAU], color=BLUE,
        )
        sun2     = Dot(sun2_pos, color=YELLOW, radius=0.12)
        sun2_lbl = Tex(r"Sole", font_size=26).next_to(sun2, LEFT, buff=0.16)
        self.play(Create(orbit2), FadeIn(sun2), Write(sun2_lbl), run_time=1.6)
        self.wait(0.4)
        self.play(FadeOut(sun2_lbl), run_time=0.5)

        focus_pos = sun2.get_center()

        peri2_pos = ctr2 + RIGHT * a1
        aph2_pos  = ctr2 + LEFT  * a1
        peri2_dot = Dot(peri2_pos, color=WHITE, radius=0.05)
        aph2_dot  = Dot(aph2_pos,  color=WHITE, radius=0.05)
        peri2_lbl = Tex(r"Perielio", font_size=22).next_to(peri2_pos, DOWN, buff=0.12)
        aph2_lbl  = Tex(r"Afelio",   font_size=22).next_to(aph2_pos,  UP,   buff=0.12)

        v_max_arrow = Arrow(
            peri2_pos, peri2_pos + UP * 0.70,
            buff=0, color=YELLOW, stroke_width=2, max_tip_length_to_length_ratio=0.18,
        )
        v_min_arrow = Arrow(
            aph2_pos, aph2_pos + DOWN * 0.40,
            buff=0, color=YELLOW, stroke_width=2, max_tip_length_to_length_ratio=0.18,
        )
        v_max_label = MathTex(r"\vec{v}_{\max}", font_size=24, color=YELLOW).next_to(v_max_arrow.get_tip(), RIGHT, buff=0.08)
        v_min_label = MathTex(r"\vec{v}_{\min}", font_size=24, color=YELLOW).next_to(v_min_arrow.get_tip(), LEFT,  buff=0.08)

        self.play(
            FadeIn(peri2_dot), FadeIn(aph2_dot),
            Write(peri2_lbl), Write(aph2_lbl),
            GrowArrow(v_max_arrow), GrowArrow(v_min_arrow),
            Write(v_max_label), Write(v_min_label),
            run_time=1.2,
        )
        self.wait(0.4)

        time_tracker = ValueTracker(0.0)
        arc_dt = 4.0

        timer_label2 = Tex(r"Tempo:", font_size=30)
        timer_value2 = DecimalNumber(0.0, num_decimal_places=1, font_size=30, color=WHITE)
        timer_value2.add_updater(lambda m: m.set_value(time_tracker.get_value()))
        timer_unit2  = MathTex(r"\Delta t", font_size=30, color=WHITE)

        timer_row2 = VGroup(timer_label2, timer_value2, timer_unit2)
        timer_row2.arrange(RIGHT, buff=0.20)
        timer_value2.align_to(timer_label2[0][0], DOWN)
        timer_unit2.align_to(timer_label2[0][0], DOWN)
        timer_row2.next_to(law_2_header, DOWN, buff=0.38)
        timer_row2.to_edge(LEFT, buff=0.50)
        self.play(FadeIn(timer_row2), run_time=0.8)

        DM         = 0.70
        M_starts   = [0.15, PI / 2, PI - DM / 2]
        arc_colors = [BLUE, ORANGE, GREEN]
        arc_names  = [r"A_1", r"A_2", r"A_3"]

        E_tracker = ValueTracker(solve_kepler_equation(M_starts[0], e1))
        planet2 = always_redraw(lambda: Dot(
            ellipse_point(a1, b1, E_tracker.get_value(), center=ctr2),
            color=RED, radius=0.09,
        ))
        rv2 = always_redraw(lambda: Line(
            focus_pos, planet2.get_center(), color=RED, stroke_width=2,
        ))
        self.play(FadeIn(planet2), Create(rv2), run_time=0.8)

        static_areas          = VGroup()
        area_labels_on_sector = VGroup()

        for i, (M_s, col, aname) in enumerate(zip(M_starts, arc_colors, arc_names)):
            E_start = solve_kepler_equation(M_s,      e1)
            E_end   = solve_kepler_equation(M_s + DM, e1)
            E_tracker.set_value(E_start)
            time_tracker.set_value(0.0)

            live_area = VMobject()
            def _upd(mob, _es=E_start, _c=col):
                E_cur = E_tracker.get_value()
                if E_cur <= _es + 1e-4:
                    mob.become(VMobject())
                    return
                mob.become(make_swept_sector(a1, b1, _es, E_cur, ctr2, focus_pos, _c))
            live_area.add_updater(_upd)
            self.add(live_area)

            self.play(
                E_tracker.animate.set_value(E_end),
                time_tracker.animate.set_value(arc_dt),
                run_time=arc_dt, rate_func=linear,
            )
            live_area.clear_updaters()
            frozen = make_swept_sector(a1, b1, E_start, E_end, ctr2, focus_pos, col)
            self.remove(live_area)
            self.add(frozen)
            static_areas.add(frozen)

            E_mid   = (E_start + E_end) / 2
            arc_mid = ellipse_point(a1, b1, E_mid, center=ctr2)
            lbl_pos = focus_pos + 0.62 * (arc_mid - focus_pos)
            area_lbl = MathTex(aname, font_size=30, color=col)
            area_lbl.move_to(lbl_pos)
            self.play(FadeIn(area_lbl), run_time=0.4)
            area_labels_on_sector.add(area_lbl)
            self.wait(0.4)

        equal_text = MathTex(
            r"\Delta t_1 = \Delta t_2 = \Delta t_3",
            r"\;\Leftrightarrow \;",
            r"A_1 = A_2 = A_3",
            font_size=34,
        )
        equal_text.next_to(orbit2, DOWN, buff=0.45)

        self.play(Write(equal_text), run_time=1.8)
        self.play(Indicate(equal_text, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.wait(long_pause)

        law2_group = VGroup(
            orbit2, sun2, planet2, rv2,
            static_areas, area_labels_on_sector,
            timer_row2, equal_text,
            peri2_dot, aph2_dot, peri2_lbl, aph2_lbl,
            v_max_arrow, v_min_arrow, v_max_label, v_min_label,
        )

        # ==================================================================
        # LAW 3 — T² ∝ a³  (three real planetary orbits)
        # ==================================================================
        self.play(
            FadeOut(law2_group),
            FadeOut(law_2_text),
            FadeOut(law_2_header),
            run_time=1.2,
        )
        self.play(FadeIn(law_3_header), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(law_3_text, shift=0.15 * UP), run_time=2.2)
        self.wait(read_pause)

        # Real planetary data (AU, Earth-years)
        planets_data = [
            # (name,  a [AU],  T [yr],  color)
            (r"Terra",  1.000,  1.000, BLUE),
            (r"Marte",  1.524,  1.881, RED),
            (r"Giove",  5.203, 11.862, ORANGE),
        ]

        # Jupiter's orbital period = 11.86 scene-seconds; others scale proportionally
        JUP_PERIOD_SC  = 11.86
        period_scale   = JUP_PERIOD_SC / 11.862          # ≈ 1.0 s per Earth-year
        period_terra   = planets_data[0][2] * period_scale  # ≈ 1.00 s
        period_marte   = planets_data[1][2] * period_scale  # ≈ 1.88 s
        period_giove   = planets_data[2][2] * period_scale  # ≈ 11.86 s

        # Jupiter → 1.9 scene units; same visual eccentricity for all orbits
        AU_to_scene = 1.9 / 5.203
        e3_scene    = 0.30

        sun3_pos = SCENE_UP + LEFT * 3.0 + DOWN * 0.2
        sun3     = Dot(sun3_pos, color=YELLOW, radius=0.14)
        sun3_lbl = Tex(r"Sole", font_size=24).next_to(sun3, DR, buff=0.10)

        orbits3       = VGroup()
        planets3      = VGroup()
        radius_lines3 = VGroup()
        orbit_labels  = VGroup()
        global_t      = ValueTracker(0.0)

        # Precompute per-planet scene geometry for later reuse (braces)
        planet_geom = []   # list of (a_sc, b_sc, c_sc, center, period_sc)

        for pname, a_au, T_yr, col in planets_data:
            a_sc      = a_au * AU_to_scene
            b_sc      = a_sc * np.sqrt(1 - e3_scene**2)
            c_sc      = a_sc * e3_scene
            center    = sun3_pos + RIGHT * c_sc
            period_sc = T_yr * period_scale
            planet_geom.append((a_sc, b_sc, c_sc, center, period_sc))

            orbit = ParametricFunction(
                lambda t, aa=a_sc, bb=b_sc, cc=center: ellipse_point(aa, bb, t, center=cc),
                t_range=[0, TAU], color=col, stroke_width=1.8,
            )
            orbits3.add(orbit)

            omega = TAU / period_sc
            phase = 0.3 * a_au
            planet = always_redraw(
                lambda aa=a_sc, bb=b_sc, cc=center, om=omega, ph=phase, ccol=col: Dot(
                    ellipse_point(aa, bb, om * global_t.get_value() + ph, center=cc),
                    color=ccol, radius=0.08,
                )
            )
            rline = always_redraw(
                lambda aa=a_sc, bb=b_sc, cc=center, om=omega, ph=phase, ccol=col: Line(
                    sun3_pos,
                    ellipse_point(aa, bb, om * global_t.get_value() + ph, center=cc),
                    color=ccol, stroke_width=1.0, stroke_opacity=0.5,
                )
            )
            planets3.add(planet)
            radius_lines3.add(rline)

            if pname == r"Terra":
                lbl_anchor = center + LEFT * a_sc
                lbl = Tex(pname, font_size=30, color=col)
                lbl.next_to(np.array([lbl_anchor[0], lbl_anchor[1], 0]), LEFT, buff=0.14)
            else:
                top_pos = center + UP * b_sc
                lbl = Tex(pname, font_size=30, color=col)
                lbl.next_to(np.array([top_pos[0], top_pos[1], 0]), UP, buff=0.12)
            orbit_labels.add(lbl)

        # ── Elapsed-time counter — same layout and position as Law 2 ──
        # Value displayed in T_Terra units

        timer_label3 = Tex(r"Tempo:", font_size=30)
        timer_value3 = DecimalNumber(0.0, num_decimal_places=2, font_size=30, color=WHITE)
        timer_value3.add_updater(lambda m: m.set_value(global_t.get_value() / period_terra))
        timer_unit3  = MathTex(r"T_{\text{Terra}}", font_size=30, color=WHITE)

        timer_row3 = VGroup(timer_label3, timer_value3, timer_unit3)
        timer_row3.arrange(RIGHT, buff=0.20)
        timer_value3.align_to(timer_label3[0][0], DOWN)
        timer_unit3.align_to(timer_label3[0][0], UP)
        timer_row3.next_to(law_3_header, DOWN, buff=0.38)
        timer_row3.to_edge(LEFT, buff=0.50)

        # ── Right-side verification panel (pre-built, rows revealed one by one) ──
        panel_title = Tex(r"Confrontiamo per i diversi pianeti $T^2/a^3$:", font_size=30)
        panel_subtitle = Tex(
            r"1 yr è un \textit{anno terrestre}\\ 1 au è la \textit{distanza media Terra-Sole}",
            font_size=30,
        )

        panel_rows = VGroup()
        for pname, a_au, T_yr, col in planets_data:
            ratio_val = round(T_yr**2 / a_au**3, 2)
            row = MathTex(
                rf"\text{{{pname}}}: \;"
                rf"\frac{{\left({T_yr:.2f}\,\text{{yr}}\right)^2}}"
                rf"{{\left({a_au:.2f}\,\text{{au}}\right)^3}}"
                rf"\approx {ratio_val:.2f}\,\text{{yr}}^2/\text{{au}}^3",
                font_size=26, color=col,
            )
            panel_rows.add(row)
        panel_rows.arrange(DOWN, buff=0.38, aligned_edge=LEFT)

        panel_block = VGroup(panel_title, panel_subtitle, panel_rows)
        panel_block.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        panel_block.to_edge(RIGHT, buff=0.50)
        panel_block.align_to(orbits3, UP).shift(DOWN * 0.1)

        # Show panel title and subtitle before orbiting starts
        self.play(FadeIn(sun3), Write(sun3_lbl), run_time=1.0)
        self.play(Create(orbits3), run_time=2.5)
        self.play(FadeIn(orbit_labels), run_time=1.2)
        self.play(FadeIn(planets3), FadeIn(radius_lines3), run_time=1.0)
        self.play(FadeIn(timer_row3), run_time=0.8)
        self.wait(short_pause)

        self.play(Write(panel_title), run_time=1.0)
        self.play(Write(panel_subtitle), run_time=1.0)
        self.wait(0.5)

        # ── Main loop: orbit until each planet's first completion ──
        prev_t = 0.0
        for i, (pname, a_au, T_yr, col) in enumerate(planets_data):
            a_sc, b_sc, c_sc, center, period_sc = planet_geom[i]
            run_time = period_sc - prev_t

            # Animate planets until this planet completes its first orbit
            self.play(
                global_t.animate.set_value(period_sc),
                run_time=run_time, rate_func=linear,
            )

            # ── Highlight completed orbit ──
            orbit_hl = ParametricFunction(
                lambda t, aa=a_sc, bb=b_sc, cc=center: ellipse_point(aa, bb, t, center=cc),
                t_range=[0, TAU], color=YELLOW, stroke_width=3.5,
            )

            # ── Brace for semi-major axis of this orbit ──
            right_tip  = center + RIGHT * a_sc
            ctr_dot    = Dot(center, color=GRAY, radius=0.05)
            brace      = BraceBetweenPoints(center, right_tip, direction=DOWN)
            brace_lbl  = brace.get_tex(r"a")

            # Show highlight + brace + indicate timer simultaneously
            self.play(
                Create(orbit_hl),
                FadeIn(brace), FadeIn(ctr_dot), Write(brace_lbl),
                Indicate(timer_row3, color=YELLOW, scale_factor=1.3),
                run_time=1.0,
            )
            self.wait(0.6)

            # Show the data row for this planet
            self.play(Write(panel_rows[i]), run_time=1.2)
            self.wait(0.6)

            # Remove highlight and brace before continuing
            self.play(
                FadeOut(orbit_hl),
                FadeOut(brace), FadeOut(ctr_dot), FadeOut(brace_lbl),
                run_time=0.6,
            )

            prev_t = period_sc

        self.wait(read_pause)

        # ── Summary formula ──
        formula_law = MathTex(r"\dfrac{T^2}{a^3} = \text{costante}", font_size=34)
        formula_law.next_to(orbits3, DOWN, buff=0.38)

        self.play(FadeIn(formula_law, shift=0.1 * UP), run_time=1.4)
        self.play(Indicate(formula_law, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.wait(long_pause)

        # ── Outro ─────────────────────────────────────────────────────────────
        self.play(FadeOut(law_3_text), run_time=0.8)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.6)
        self.wait(short_pause)