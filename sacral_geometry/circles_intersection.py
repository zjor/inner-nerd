from dataclasses import dataclass
from typing import List
from math import sqrt, sin, cos
from manim import *


@dataclass
class Point:
    x: float
    y: float

    def to_array(self):
        return [self.x, self.y, 0]

    def middle(self, that: Point):
        return Point((self.x + that.x) / 2, (self.y + that.y) / 2)

    def dist2(self, that: Point):
        return (self.x - that.x) ** 2 + (self.y - that.y) ** 2


def find_intersection(a: Point, b: Point, r: float) -> List[Point]:    
    o = a.middle(b)
    l2 = o.dist2(a)

    if l2 > r ** 2:
        return []

    if abs(a.x - b.x) > abs(a.y - b.y):
        alpha = (o.y - a.y) / (o.x - a.x)
        beta = sqrt((r ** 2 - l2) / (1 + alpha ** 2))
        return [
            Point(o.x - alpha * beta, o.y + beta),
            Point(o.x + alpha * beta, o.y - beta),
        ]

    else:
        alpha = (o.x - a.x) / (o.y - a.y)
        beta = sqrt((r ** 2 - l2) / (1 + alpha ** 2))
        return [
            Point(o.x + beta, o.y - alpha * beta),
            Point(o.x - beta, o.y + alpha * beta),
        ]
    


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
        
        intersections = find_intersection(self.a, self.b, self.r)
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
