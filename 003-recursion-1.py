import numpy as np
from math import sqrt
from manimlib import *

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


def get_triangle_tips(side):
    return [
        np.array((-1, -1, 0)) * side / 2,
        np.array((1, -1, 0)) * side / 2,
        np.array((0, sqrt(3) / 2, 0)) * side / 2]


def get_square_tips(side):
    d = side / 2
    return [np.array((-1, -1, 0)) * d,
            np.array((-1, 1, 0)) * d,
            np.array((1, 1, 0)) * d,
            np.array((1, -1, 0)) * d]


def move_tips(tips, offset):
    for tip in tips:
        tip += offset
    return tips


def build_triangle(side, color):
    """
    The default Triangle() method fails with "NameError: name 'DEGREES' is not defined"
    :return: VGroup of lines forming a triangle and coordinates of the tips
    """
    tips = get_triangle_tips(side)
    g = VGroup()
    for start, end in zip_to_pairs(tips):
        g += Line(start, end, color=color)
    return g, tips


def build_polygon(tips, color):
    g = VGroup()
    for start, end in zip_to_pairs(tips):
        g += Line(start, end, color=color)
    return g


class InscribedPolygons:

    @staticmethod
    def connect_polygon(vertices, color):
        g = VGroup()
        for start, end in zip_to_pairs(vertices):
            g += Line(start, end, color=color)
        return g

    @staticmethod
    def update_polygon(group, vertices):
        for (start, end), line in zip(zip_to_pairs(vertices), group):
            line.put_start_and_end_on(start, end)

    def __init__(self, bounds, depth=5, p=0.15, color=COLOR):
        self.bounds = bounds
        self.depth = depth
        self.vertices = [bounds]
        self.groups = VGroup()
        self.groups.add(InscribedPolygons.connect_polygon(bounds, color))

        for _ in range(depth):
            self.vertices.append(inscribe(self.vertices[-1], p))
            self.groups.add(InscribedPolygons.connect_polygon(self.vertices[-1], color))

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
        tips = get_square_tips(Scenario.SQUARE_SIDE)

        p = 0.15
        dots = VGroup(*[Dot(color=BLUE) for _ in range(4)])
        lines = VGroup()
        for i in range(Scenario.DEPTH):
            tips = inscribe(tips, p)
            for dot, tip in zip(dots, tips):
                dot.move_to(tip)
            runtime_base = (Scenario.DEPTH - i) / Scenario.DEPTH
            self.play(FadeIn(dots), run_time=0.3 * runtime_base)

            for start, end in zip_to_pairs(tips):
                line = Line(start, end, color=COLOR)
                self.play(ShowCreation(line), run_time=0.4 * runtime_base)
                lines += line

            self.play(FadeOut(dots), run_time=0.2 * runtime_base)
        self.wait(1)
        self.play(FadeOut(lines))

    def play_inscribed_polygons(self):
        box_tips = move_tips(get_square_tips(Scenario.SQUARE_SIDE), LEFT * 2.5)
        inscribed_boxes = InscribedPolygons(box_tips, depth=Scenario.DEPTH, p=0, color=COLOR)

        tri_tips = move_tips(get_triangle_tips(Scenario.SQUARE_SIDE), RIGHT * 2.5)
        inscribed_tri = InscribedPolygons(tri_tips, depth=Scenario.DEPTH, p=0, color=BLUE)
        
        def get_update_func(obj, direction):
            def update_func(_obj, alpha):
                p = alpha if direction > 0 else 1 - alpha
                obj.set_p(p)
            return update_func
        
        self.play(UpdateFromAlphaFunc(inscribed_boxes.groups, get_update_func(inscribed_boxes, 1)), run_time=3)
        self.wait(0.5)
        self.play(UpdateFromAlphaFunc(inscribed_tri.groups, get_update_func(inscribed_tri, -1)), run_time=3)
        self.wait(0.5)
        self.play(UpdateFromAlphaFunc(inscribed_tri.groups, get_update_func(inscribed_tri, 1)), run_time=3)
        self.wait(0.5)
        self.play(UpdateFromAlphaFunc(inscribed_boxes.groups, get_update_func(inscribed_boxes, -1)), run_time=3)

    def play_outro(self):
        self.wait(1.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def construct(self):
        box = self.play_intro()
        self.play_inscribe_squares()

        self.play(box.move_to, LEFT * 2.5, run_time=0.5)

        tri_tips = move_tips(get_triangle_tips(Scenario.SQUARE_SIDE), RIGHT * 2.5)
        tri = build_polygon(tri_tips, BLUE)
        
        self.play(FadeIn(tri), run_time=0.5)
        self.wait(0.5)
        self.remove(box)
        self.play_inscribed_polygons()
        self.play_outro()
