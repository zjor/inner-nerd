from manim import *
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL


class CenterOfMass(VGroup):
    def __init__(self, radius: float = 1, angle: float = 0, color: str = WHITE, **kwargs):
        super().__init__(**kwargs)
        circle = Circle(radius=radius, stroke_color=color, **kwargs)
        sector_a = AnnularSector(
            inner_radius=0, outer_radius=radius, angle=PI / 2, start_angle=angle, fill_color=color)
        sector_b = AnnularSector(
            inner_radius=0, outer_radius=radius, angle=PI / 2, start_angle=(angle + PI), fill_color=color)
        self.add(circle, sector_a, sector_b)
