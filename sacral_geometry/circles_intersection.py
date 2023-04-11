from math import sqrt, sin, cos
from manim import *
from geometry.utils import Point, find_circles_intersection


class Scenario(Scene):
    def __init__(self):
        super().__init__()
        self.a = Point(-0.3, 0.0)
        self.b = Point(0.3, 0.0)
        self.r = 1.5

        self.c1 = Circle(radius=self.r, color=RED).move_to(self.a.to_array())
        self.c2 = Circle(radius=self.r, color=BLUE).move_to(self.b.to_array())

        self.group = VGroup(self.c1, self.c2)
        self.time = ValueTracker(0)
        self.dots = [Dot(), Dot()]

    def _updater(self, _: VGroup) -> None:
        now = self.time.get_value()
        self.a = Point(-0.3 * cos(now), 0.3 * sin(now))
        self.c1.become(Circle(radius=self.r, color=RED).move_to(self.a.to_array()))

        intersections = find_circles_intersection(self.a, self.b, self.r)
        for i, p in enumerate(intersections):
            dot = Dot(point=p.to_array(), color=YELLOW)
            self.dots[i].become(dot)

    def construct(self):
        self.add(self.group)
        self.add(*self.dots)
        self.group.add_updater(self._updater)
        self.play(self.time.animate.set_value(5), run_time=5, rate_func=rate_functions.linear)


if __name__ == "__main__":
    scene = Scenario()

    scene.render()
