import numpy as np
from manimlib import *

"""
1. A dot transforms into a line with a dot
2. Group transforms into a square with four dots
3. Four dots are connected with animation
4. More dots appear on the sides of the inner square
5. New dots are connected
6. The process 4-5 is repeated X times
7. The ratio 'p' of the dot location is animated
"""

COLOR = GREEN_E


def zip_to_pairs(items):
    return list(zip(items, items[1:] + [items[0]]))


def build_line_with_a_dot(start, end, p):
    center = start * (1 - p) + end * p
    g = VGroup()
    g += Line(start=start, end=end, color=COLOR)
    g += Circle(arc_center=center, radius=0.05, fill_opacity=1, color=COLOR)
    return g, center


def build_square_group(size, p):
    d = size / 2
    a, b, c, d = np.array((-d, d, 0)), np.array((d, d, 0)), np.array((d, -d, 0)), np.array((-d, -d, 0))

    l1, c1 = build_line_with_a_dot(a, b, p)
    l2, c2 = build_line_with_a_dot(b, c, p)
    l3, c3 = build_line_with_a_dot(c, d, p)
    l4, c4 = build_line_with_a_dot(d, a, p)

    g = VGroup()
    g.add(*[l1, l2, l3, l4])
    return g, [c1, c2, c3, c4]


def inscribe(vertices, p):
    result = []
    for start, end in zip_to_pairs(vertices):
        result.append(start * (1 - p) + end * p)
    return result


def get_vertices(items, p, depth):
    vertices = [items]
    for i in range(depth):
        vertices.append(inscribe(vertices[-1], p))
    return vertices


class InscribedPolygons:

    @staticmethod
    def connect_polygon(vertices):
        g = VGroup()
        for start, end in zip_to_pairs(vertices):
            g += Line(start, end)
        return g

    @staticmethod
    def update_polygon(group, vertices):
        for (start, end), line in zip(zip_to_pairs(vertices), group):
            line.put_start_and_end_on(start, end)

    def __init__(self, bounds, depth=5, p=0.15):
        self.bounds = bounds
        self.depth = depth
        self.vertices = [bounds]
        self.groups = VGroup()
        self.groups.add(InscribedPolygons.connect_polygon(bounds))

        for _ in range(depth):
            self.vertices.append(inscribe(self.vertices[-1], p))
            self.groups.add(InscribedPolygons.connect_polygon(self.vertices[-1]))

    def update_bounds(self):
        self.bounds = [line.get_start() for line in self.groups[0]]
        self.vertices[0] = self.bounds

    def set_p(self, p):
        self.vertices = self.vertices[:1]
        for i in range(self.depth):
            self.vertices.append(inscribe(self.vertices[-1], p))
            InscribedPolygons.update_polygon(self.groups[i + 1], self.vertices[-1])


class Scenario(Scene):
    SQUARE_SIDE = 4.0
    DEPTH = 9

    def play_intro(self) -> Mobject:
        dot = Dot(color=COLOR)
        square = Square(side_length=Scenario.SQUARE_SIDE, color=COLOR)
        self.play(FadeIn(dot))
        self.wait(0.5)
        self.play(ReplacementTransform(dot, target_mobject=square), run_time=2)
        return square

    def play_inscribe_squares(self):
        d = Scenario.SQUARE_SIDE / 2
        corners = [np.array((-1, -1, 0)) * d,
                   np.array((-1, 1, 0)) * d,
                   np.array((1, 1, 0)) * d,
                   np.array((1, -1, 0)) * d]

        p = 0.15
        dots = VGroup(*[Dot(color=BLUE) for _ in range(4)])
        lines = VGroup()
        for _ in range(Scenario.DEPTH):
            corners = inscribe(corners, p)
            for dot, corner in zip(dots, corners):
                dot.move_to(corner)

            self.play(FadeIn(dots), run_time=0.5)

            for start, end in zip_to_pairs(corners):
                line = Line(start, end, color=COLOR)
                self.play(ShowCreation(line), run_time=0.5)
                lines += line

            self.play(FadeOut(dots), run_time=0.5)

    def construct(self):
        box = self.play_intro()
        self.play_inscribe_squares()

        # size = 4
        # d = size / 2
        # bound_vertices = [np.array((-d, -d, 0)), np.array((-d, d, 0)), np.array((d, d, 0)), np.array((d, -d, 0))]
        #
        # p = InscribedPolygons(bound_vertices, 5, 0)
        # self.play(p.groups.move_to, LEFT * 3, run_time=2)
        # p.update_bounds()
        #
        # def update_func(_obj, alpha):
        #     p.set_p(alpha)
        #
        # self.play(UpdateFromAlphaFunc(p.groups, update_func), run_time=3)
