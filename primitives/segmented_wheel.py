from manim import *
from numpy import sin, cos


class SegmentedWheel(VGroup):
    def __init__(self,
                 radius: float = 1,
                 thickness: float = 0.01,
                 angle: float = 0,
                 n_segments: int = 16,
                 primary_color: str = BLUE,
                 secondary_color: str = GREEN,
                 **kwargs):
        super().__init__(**kwargs)
        th = TAU / n_segments
        for i in range(n_segments):
            color = primary_color if i % 2 == 0 else secondary_color
            sector = AnnularSector(
                inner_radius=(radius - thickness),
                outer_radius=radius,
                angle=th,
                start_angle=(angle + th * i),
                stroke_color=primary_color,
                fill_color=color,
                **kwargs
            )
            self.add(sector)


class WheelAxis(VGroup):
    def __init__(self, radius: float = 1, angle: float = 0, dash_length=0.3, **kwargs):
        super().__init__(**kwargs)
        s, c = sin(angle), cos(angle)
        self.add(DashedLine(
            start=[s * radius, c * radius, 0],
            end=[-s * radius, -c * radius, 0],
            dash_length=dash_length,
            **kwargs))

        s, c = sin(angle + PI / 2), cos(angle + PI / 2)
        self.add(DashedLine(
            start=[s * radius, c * radius, 0],
            end=[-s * radius, -c * radius, 0],
            dash_length=dash_length,
            **kwargs))
