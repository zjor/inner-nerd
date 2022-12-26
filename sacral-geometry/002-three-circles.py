from manim import *
import numpy as np


def distance(p1, p2):
    return np.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2 +
        (p1[2] - p2[2]) ** 2
    )


def get_vertices(radius, start_angle, center, n):
    vertices = []
    for i in range(0, n):
        vertices.append(np.array([
            np.cos(start_angle + i * TAU / n) * radius,
            np.sin(start_angle + i * TAU / n) * radius,
            0
        ]) + np.array(center))
    return vertices


class Scenario(Scene):
    def construct(self):
        alpha = 3 * PI / 2
        scale = 2.0
        r = 2 / np.sqrt(3) * scale
        root_vertices = get_vertices(r, alpha, (0, 0, 0), 3)

        root_centers = []
        for (i, j) in zip([0, 1, 2], [1, 2, 0]):
            root_centers.append([
                (root_vertices[i][0] + root_vertices[j][0]) / 2,
                (root_vertices[i][1] + root_vertices[j][1]) / 2,
                (root_vertices[i][2] + root_vertices[j][2]) / 2,
            ])

        for i in range(0, 3):
            self.add(Circle(radius=scale, stroke_color=BLUE).move_to(root_centers[i]))
            self.add(Circle(radius=0.01).move_to(root_centers[i]))

        # dashed hexagon
        hex_vertices = get_vertices(r, alpha, (0, 0, 0), 6)
        self.add(DashedVMobject(Polygon(*hex_vertices), num_dashes=36))
        for i in range(0, 3):
            self.add(DashedVMobject(
                Line(start=[0, 0, 0], end=hex_vertices[i * 2 + 1], stroke_color=BLUE),
                num_dashes=7))

        # inner hexagons
        for i in range(0, 3):
            inner_hex_vertices = get_vertices(scale, -PI / 3 + TAU / 3 * i, root_centers[i], 6)
            self.add(Polygon(*inner_hex_vertices))
            self.add(Polygon(*[
                hex_vertices[2 * i + 1],
                inner_hex_vertices[0], inner_hex_vertices[1]
            ]))

        outer_r = scale * (1 + 1 / np.sqrt(3))
        self.add(Circle(radius=outer_r))
        self.add(DashedVMobject(Circle(radius=(outer_r + 0.3)), num_dashes=96))
