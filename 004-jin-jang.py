from manim import *
import numpy as np

"""
Scenario:
1. Draw Jin-Jang hieroglyphs
2. Draw the symbol with golden color
3. Flood fill halves
4. Remove the fill
5. Rotate 180 degrees and scale down to match the font height
6. Write "sacral geometry" text
7. Fade-out

Est. impl time: 2h
"""


class Scenario(Scene):
    font = 'Monospace'
    color = GREEN_E

    def left_half(self) -> ArcPolygonFromArcs:
        r = 1.0
        vertices = []
        for i in np.arange(-TAU / 2, 0, 0.01):
            vertices.append([np.sin(i), np.cos(i), 0])

        r_2 = r / 2
        for i in np.arange(0, TAU / 2, 0.01):
            vertices.append([np.sin(i) * r_2, np.cos(i) * r_2 + r_2, 0])

        for i in np.arange(0, TAU / 2, 0.01):
            vertices.append([-np.sin(i) * r_2, np.cos(i) * r_2 - r_2, 0])

        conf = {
            "fill_opacity": 1,
            "stroke_width": 0,
            "color": RED_A
        }
        poly = Polygon(*vertices, **conf)
        return Cutout(
            poly,
            Circle(radius=r / 8).move_to(np.array((0.0, 0.5, 0.0))),
            **conf)

    def construct(self) -> None:
        self.wait(1.0)

        circle = Circle(radius=1.0, stroke_color=BLUE_C)
        self.play(Create(circle), run_time=2.0)

        top_arc = Arc(start_angle=TAU / 4, angle=-TAU / 2, radius=0.5).set_stroke(BLUE_C)
        top_arc.move_to(np.array((0.25, 0.5, 0.0)))
        self.play(Create(top_arc))

        bottom_arc = Arc(start_angle=TAU / 4, angle=TAU / 2, radius=0.5).set_stroke(BLUE_C)
        bottom_arc.move_to(np.array((-0.25, -0.5, 0.0)))
        self.play(Create(bottom_arc))

        top_circle = Circle(radius=0.125, stroke_color=BLUE_C).move_to(np.array((0.0, 0.5, 0.0)))
        self.play(Create(top_circle))

        bottom_circle = Circle(radius=0.125, stroke_color=BLUE_C).move_to(np.array((0.0, -0.5, 0.0)))
        self.play(Create(bottom_circle))

        poly = self.left_half()
        self.play(FadeIn(poly))
