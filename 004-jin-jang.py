from manimlib import *
import numpy as np


class Scenario(Scene):
    font = 'Monospace'
    color = GREEN_E

    def construct(self) -> None:

        self.wait(1.0)

        circle = Circle(radius=1.0, stroke_color=BLUE_C)
        self.play(ShowCreation(circle), run_time=2.0)

        top_arc = Arc(start_angle=TAU / 4, angle=-TAU / 2, radius=0.5).set_stroke(BLUE_C)
        top_arc.move_to(np.array((0.25, 0.5, 0.0)))
        self.play(ShowCreation(top_arc))

        bottom_arc = Arc(start_angle=TAU / 4, angle=TAU / 2, radius=0.5).set_stroke(BLUE_C)
        bottom_arc.move_to(np.array((-0.25, -0.5, 0.0)))
        self.play(ShowCreation(bottom_arc))

        top_circle = Circle(radius=0.125, stroke_color=BLUE_C).move_to(np.array((0.0, 0.5, 0.0)))
        self.play(ShowCreation(top_circle))

        bottom_circle = Circle(radius=0.125, stroke_color=BLUE_C).move_to(np.array((0.0, -0.5, 0.0)))
        self.play(ShowCreation(bottom_circle))
