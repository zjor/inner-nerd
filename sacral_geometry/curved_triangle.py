from typing import List
from manim import *
from numpy import sin, cos, sqrt
from geometry.utils import Point, find_circles_intersection

DEFAULT_SIDE = 2
DEFAULT_R = sqrt(3) / 2 * (2 * DEFAULT_SIDE)


def rotate_about(x: List[float], o: List[float], a: float) -> List[float]:
    _x, _y = x[0] - o[0], x[1] - o[1]
    c, s = cos(a), sin(a)
    _x_ = c * _x - s * _y
    _y_ = s * _x + c * _y
    return [o[0] + _x_, o[1] + _y_, 0]


def get_triangle_vertexes(R: float = DEFAULT_SIDE) -> List[float]:
    vs = []
    for i in range(3):
        a = i * TAU / 3
        vs.append([R * sin(a), R * cos(a), 0])
    return vs


def get_triangle_lines(vs: List[List[float]]):
    lines = []
    for i, j in [(0, 1), (1, 2), (2, 0)]:
        lines.append(Line(start=vs[i], end=vs[j], stroke_color=BLUE_C))
    return lines


class Scenario(Scene):
    def construct(self):
        vs = get_triangle_vertexes()
        lines = get_triangle_lines(vs)
        self.add(*lines)
        # TODO: draw in one direction
        self.add(Arc(radius=DEFAULT_R, start_angle=0, angle=TAU / 6, arc_center=vs[2]))
        self.add(Arc(radius=DEFAULT_R, start_angle=PI, angle=-TAU / 6, arc_center=vs[1]))
        self.add(Arc(radius=DEFAULT_R, start_angle=PI + PI / 3, angle=TAU / 6, arc_center=vs[0]))

        a = PI / 6
        c1 = rotate_about(vs[0], vs[2], a)
        self.add(Dot(c1, color=GREEN_C))

        c2 = rotate_about(vs[1], vs[0], a)
        self.add(Dot(c2, color=RED_C))

        c3 = rotate_about(vs[2], vs[1], a)
        self.add(Dot(c3, color=BLUE_C))

        self.add(*[
            Circle(radius=DEFAULT_R, stroke_color=GREEN_C, stroke_width=1, arc_center=c1),
            Circle(radius=DEFAULT_R, stroke_color=RED_C, stroke_width=1, arc_center=c2),
            Circle(radius=DEFAULT_R, stroke_color=BLUE_C, stroke_width=1, arc_center=c3),
        ])

        for (a, b), v, c in [((c1, c2), vs[0], c3), ((c2, c3), vs[1], c1), ((c3, c1), vs[2], c2)]:
            intersections = find_circles_intersection(Point.from_array(a), Point.from_array(b), DEFAULT_R)
            nearest = Point.from_array(v).find_farthest(intersections)
            self.add(Dot(nearest.to_array(), color=YELLOW))
            self.add(ArcBetweenPoints(
                start=v,
                end=nearest.to_array(),
                radius=DEFAULT_R,
                arc_center=c
            ))



if __name__ == "__main__":
    scene = Scenario()
    scene.render()
