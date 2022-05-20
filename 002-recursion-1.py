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


def zip_pairs(items):
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


def inscribe_square(vertices, p):
    result = []
    for start, end in zip_pairs(vertices):
        result.append(start * (1 - p) + end * p)
    return result


class Scenario(Scene):

    def construct(self):
        dot = Circle(radius=0.05, fill_opacity=1, color=COLOR)
        dot.set_fill(COLOR)
        self.play(FadeIn(dot))

        p = 0.15

        line_and_dot_group, _ = build_line_with_a_dot(np.array((-2, 0, 0)), np.array((2, 0, 0)), p)
        self.play(Transform(dot, target_mobject=line_and_dot_group))
        self.play(FadeOut(dot))

        square_group, next_vertices = build_square_group(4, p)
        self.play(FadeIn(square_group))

        for start, end in zip_pairs(next_vertices):
            self.play(ShowCreation(Line(start=start, end=end, color=COLOR)), run_time=0.4)

        for i in range(15):
            next_vertices = inscribe_square(next_vertices, p)
            g = VGroup()
            for v in next_vertices:
                g += Circle(arc_center=v, radius=0.05, fill_opacity=1, color=COLOR)
            self.play(FadeIn(g), run_time=0.4 / (i + 1))

            for start, end in zip_pairs(next_vertices):
                self.play(ShowCreation(Line(start=start, end=end, color=COLOR)), run_time=0.4 / (i + 1))

