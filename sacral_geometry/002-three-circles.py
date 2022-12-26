from manim import *
import numpy as np
from scene_utils import WithIntroScenario


def distance(p1, p2):
    return np.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2 +
        (p1[2] - p2[2]) ** 2
    )


def get_vertices(radius, start_angle, center, n) -> list:
    vertices = []
    for i in range(0, n):
        vertices.append(np.array([
            np.cos(start_angle + i * TAU / n) * radius,
            np.sin(start_angle + i * TAU / n) * radius,
            0
        ]) + np.array(center))
    return vertices


PRIMARY_COLOR = "#FFCD03"
SECONDARY_COLOR = "#CFA600"
PRIMARY_THICKNESS = 2.0
SECONDARY_THICKNESS = 1.0

pcpt_conf = {
    "stroke_color": PRIMARY_COLOR,
    "stroke_width": PRIMARY_THICKNESS
}

scst_conf = {
    "stroke_color": SECONDARY_COLOR,
    "stroke_width": SECONDARY_THICKNESS
}


class Scenario(WithIntroScenario):
    def __init__(self):
        super().__init__()

    def construct(self):
        self.into()

        self.wait(0.5)

        alpha = 3 * PI / 2
        scale = 3.0
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
            self.play(Create(Circle(radius=scale, **pcpt_conf).move_to(root_centers[i])), run_time=1)

        # dashed hexagon
        hex_vertices = get_vertices(r, alpha, (0, 0, 0), 6)
        self.play(Create(DashedVMobject(Polygon(*hex_vertices, **scst_conf), num_dashes=36)), run_time=1)

        lines_to_center = []
        for i in range(0, 3):
            lines_to_center.append(Create(DashedVMobject(
                Line(start=[0, 0, 0], end=hex_vertices[i * 2 + 1], **scst_conf),
                num_dashes=7)))
        self.play(*lines_to_center)

        # inner hexagons
        for i in range(0, 3):
            inner_hex_vertices = get_vertices(scale, -PI / 3 + TAU / 3 * i, root_centers[i], 6)
            self.play(Create(Polygon(*inner_hex_vertices, **scst_conf)))
            self.play(Create(Polygon(*[
                hex_vertices[2 * i + 1],
                inner_hex_vertices[0], inner_hex_vertices[1]
            ], **scst_conf)))

        outer_r = scale * (1 + 1 / np.sqrt(3))
        self.play(Create(Circle(radius=outer_r, **pcpt_conf)))
        outer_r2 = outer_r + 0.3
        self.play(Create(DashedVMobject(Circle(radius=outer_r2, **scst_conf), num_dashes=96)))

        satellites: list = list(map(lambda x: (x, 0.1), get_vertices(outer_r2, 0, (0, 0, 0), 4)))
        satellites.extend(map(lambda x: (x, 0.05), get_vertices(outer_r2, PI / 12, (0, 0, 0), 4)))
        satellites.extend(map(lambda x: (x, 0.05), get_vertices(outer_r2, - PI / 12, (0, 0, 0), 4)))
        sat_anim = []
        for s in satellites:
            sat_anim.append(
                FadeIn(Circle(radius=s[1], fill_color=PRIMARY_COLOR, fill_opacity=1, **pcpt_conf).move_to(s[0])))
        self.play(*sat_anim)
