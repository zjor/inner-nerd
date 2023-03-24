from dataclasses import dataclass
from typing import List
from math import sqrt
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

    def construct(self):
        a = Point(-0.3, 0.0)
        b = Point(0.3, 0.0)
        r = 1.5
        c1 = Circle(radius=r, color=RED).move_to(a.to_array())
        c2 = Circle(radius=r, color=BLUE).move_to(b.to_array())
        self.add(c1, c2)

        intersections = find_intersection(a, b, r)
        for p in intersections:
            self.add(Dot(point=p.to_array(), color=YELLOW))


if __name__ == "__main__":
    scene = Scenario()

    scene.render()
