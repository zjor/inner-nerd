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


def find_intersection(a: Point, b: Point, r: float) -> List[Point]:
    # TODO: handle dist(a, b) > 2 * r
    o = Point((a.x + b.x) / 2, (a.y + b.y) / 2)
    l2 = (o.x - a.x) ** 2 + (o.y - a.y) ** 2

    if abs(a.x - b.x) > abs(a.y - b.y):
      alpha = (o.y - a.y) / (o.x - a.x) 
    else:
      alpha = (o.x - a.x) / (o.y - a.y) 

    beta = sqrt((r ** 2 - l2) / (1 + alpha ** 2))        
    return [
        Point(o.x - alpha * beta, o.y + beta),
        Point(o.x + alpha * beta, o.y - beta),
    ]
    

class Scenario(Scene):
    def construct(self):
        a = Point(-0.5, -0.1)
        b = Point(0.5, 0.2)
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