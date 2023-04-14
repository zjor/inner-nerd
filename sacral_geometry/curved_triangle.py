"""
Scenario:
- three dots fade in
- three dots get connected into a triangle
- triangle sides bends into arcs
- draw helper circles with a dashed line
- draw helper arcs which are the trajectories for the helper centers
- triangle vertices rotates, each about next the neighbour vertex, with circles
- main shape appears; with central circle
- helper shapes disappear
- internal shape starts pulsating
- fade out the scene
"""

from typing import List
from manim import *
from numpy import sin, cos, sqrt
from geometry.utils import Point, find_circles_intersection

DEFAULT_SIDE = 4
DEFAULT_R = sqrt(3) / 2 * (2 * DEFAULT_SIDE)

PRIMARY_COLOR = YELLOW
SECONDARY_COLOR = BLUE


def rotate_about(x: List[float], o: List[float], a: float) -> List[float]:
    _x, _y = x[0] - o[0], x[1] - o[1]
    c, s = cos(a), sin(a)
    _x_ = c * _x - s * _y
    _y_ = s * _x + c * _y
    return [o[0] + _x_, o[1] + _y_, 0]


def get_triangle_vertexes(R: float = DEFAULT_SIDE) -> List[List[float]]:
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
    def __init__(self):
        super().__init__()
        self.time = ValueTracker(0.01)
        self.vs = get_triangle_vertexes()

        self.helper_circles = [
            DashedVMobject(
                Circle(radius=DEFAULT_R, stroke_color=SECONDARY_COLOR, stroke_width=1),
                num_dashes=128).move_to(v)
            for v in self.vs
        ]

        self.group = VGroup(*[
            # 0..2; helper circles center dots
            *[Dot() for _ in range(3)],

            # 3..5; helper circles
            *self.helper_circles,

            # 6..8; intersection marks
            Dot(), Dot(), Dot(),

            # 9..11
            ArcBetweenPoints(start=ORIGIN, end=ORIGIN, angle=0, color=PRIMARY_COLOR),
            ArcBetweenPoints(start=ORIGIN, end=ORIGIN, angle=0, color=PRIMARY_COLOR),
            ArcBetweenPoints(start=ORIGIN, end=ORIGIN, angle=0, color=PRIMARY_COLOR),
        ])

    def _updater(self, _: VGroup) -> None:
        vs = self.vs
        angle = self.time.get_value()

        # moving helper circles centers
        c1 = rotate_about(vs[0], vs[2], angle)
        c2 = rotate_about(vs[1], vs[0], angle)
        c3 = rotate_about(vs[2], vs[1], angle)

        opacity = 1
        if PI / 16 < angle < 3 * PI / 24:
            opacity = 20.372 * angle - 3
        elif angle >= 3 * PI / 24:
            opacity = 0

        print(angle, opacity)

        self.group[0].become(Dot(c1, color=SECONDARY_COLOR, radius=0.05).set_opacity(opacity))
        self.group[1].become(Dot(c2, color=SECONDARY_COLOR, radius=0.05).set_opacity(opacity))
        self.group[2].become(Dot(c3, color=SECONDARY_COLOR, radius=0.05).set_opacity(opacity))

        # moving helper circles themselves
        self.group[3].become(
            DashedVMobject(Circle(radius=DEFAULT_R, stroke_color=SECONDARY_COLOR, stroke_width=1),
                           num_dashes=128).move_to(c1))
        self.group[4].become(
            DashedVMobject(Circle(radius=DEFAULT_R, stroke_color=SECONDARY_COLOR, stroke_width=1),
                           num_dashes=128).move_to(c2))
        self.group[5].become(
            DashedVMobject(Circle(radius=DEFAULT_R, stroke_color=SECONDARY_COLOR, stroke_width=1),
                           num_dashes=128).move_to(c3))

        # moving arcs
        for i, ((a, b), v, c) in enumerate([((c1, c2), vs[0], c3), ((c2, c3), vs[1], c1), ((c3, c1), vs[2], c2)]):
            intersections = find_circles_intersection(Point.from_array(a), Point.from_array(b), DEFAULT_R)
            nearest = Point.from_array(v).find_farthest(intersections)
            self.group[6 + i].become(Dot(nearest.to_array(), color=PRIMARY_COLOR))
            self.group[9 + i].become(ArcBetweenPoints(
                start=v,
                end=nearest.to_array(),
                radius=DEFAULT_R,
                arc_center=c,
                stroke_color=PRIMARY_COLOR,
            ))

    def construct(self):
        vs = self.vs

        # Fade in triangle vertices
        self.play(FadeIn(*[
            Dot(v, color=PRIMARY_COLOR, radius=0.05) for v in vs
        ]))

        # Draw triangle sides
        lines = [
            Line(start=vs[i], end=vs[j], stroke_color=PRIMARY_COLOR) for i, j in [(0, 1), (1, 2), (2, 0)]
        ]

        self.play(*[Create(line) for line in lines])

        # Draw helper circles
        self.play(*[FadeIn(c) for c in self.helper_circles])

        # Bend triangle sides to arcs
        self.play(*[
            lines[0].animate.become(
                Arc(radius=DEFAULT_R, start_angle=0, angle=TAU / 6, arc_center=vs[2],
                    stroke_color=PRIMARY_COLOR)).reverse_points(),
            lines[2].animate.become(
                Arc(radius=DEFAULT_R, start_angle=PI, angle=-TAU / 6, arc_center=vs[1], stroke_color=PRIMARY_COLOR)),
            lines[1].animate.become(
                Arc(radius=DEFAULT_R, start_angle=PI + PI / 3, angle=TAU / 6, arc_center=vs[0],
                    stroke_color=PRIMARY_COLOR).reverse_points()),
        ])

        self.add(self.group)
        self.group.add_updater(self._updater)

        self.play(self.time.animate.set_value(PI / 8), run_time=2.5, rate_func=rate_functions.linear)

        self.wait(0.5)


if __name__ == "__main__":
    import sys

    print(sys.version)
    config.frame_size = (1080, 1080)
    scene = Scenario()
    scene.render()
