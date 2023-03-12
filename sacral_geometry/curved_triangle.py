from typing import List
from manim import *
from numpy import sin, cos, sqrt


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

        a = PI / 8
        c1 = rotate_about(vs[0], vs[2], a)
        self.add(Dot(c1, color=GREEN_C))

        c2 = rotate_about(vs[1], vs[0], a)
        self.add(Dot(c2, color=RED_C))

        c3 = rotate_about(vs[2], vs[1], a)
        self.add(Dot(c3, color=BLUE_C))

        a2 = TAU / 6 - a / 3
        self.add(Arc(radius=DEFAULT_R, start_angle=a, angle=a2, arc_center=c3))
        self.add(Arc(radius=DEFAULT_R, start_angle=PI / 2 + PI / 6 + a, angle=a2, arc_center=c2))
        self.add(Arc(radius=DEFAULT_R, start_angle=PI + PI / 3 + a, angle=a2, arc_center=c1))


if __name__ == "__main__":
    scene = Scenario()
    scene.render()