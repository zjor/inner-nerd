from manim import *
import numpy as np

"""
Scenario:
1. Draw Jin-Jang hieroglyphs
2. Draw the symbol with golden color
3. Flood fill halves
4. Remove the fill
5. Rotate 180 degrees and scale down to match the font height
6. Write "sacral geometry" text
7. Fade-out

Est. impl time: 2h
"""


class JinJangVertices:
    def __init__(self, radius: float):
        self.radius = radius
        self.step = 0.01

    def get_left_half_circle(self):
        vertices = []
        for i in np.arange(-TAU / 2, 0, self.step):
            vertices.append([
                np.sin(i) * self.radius,
                np.cos(i) * self.radius,
                0])
        return vertices

    def get_right_half_circle(self):
        vertices = []
        for i in np.arange(-TAU / 2, 0, self.step):
            vertices.append([
                -np.sin(i) * self.radius,
                np.cos(i) * self.radius,
                0])
        return vertices

    def get_middle_s(self):
        vertices = []
        r_2 = self.radius / 2
        for i in np.arange(0, TAU / 2, self.step):
            vertices.append([np.sin(i) * r_2, np.cos(i) * r_2 + r_2, 0])

        for i in np.arange(0, TAU / 2, self.step):
            vertices.append([-np.sin(i) * r_2, np.cos(i) * r_2 - r_2, 0])
        return vertices

    def get_s_func(self, t: float):
        r_2 = self.radius / 2
        if 0 <= t <= TAU / 2:
            return np.array([np.sin(t) * r_2, np.cos(t) * r_2 + r_2, 0])
        elif TAU / 2 < t <= TAU:
            return np.array([-np.sin(t - TAU / 2) * r_2, np.cos(t - TAU / 2) * r_2 - r_2, 0])
        else:
            raise ValueError(f"t should be between [0, TAU]")

    def get_full_circle(self):
        vertices = []
        for i in np.arange(0, TAU + self.step, self.step):
            vertices.append([
                -np.cos(i + TAU / 4) * self.radius,
                np.sin(i + TAU / 4) * self.radius,
                0
            ])
        return vertices


class Scenario(Scene):
    font = 'Monospace'

    def __init__(
            self,
            radius: float = 4.0,
            primary_font_size: int = 108,
            secondary_font_size: int = 96
    ):
        super().__init__()
        self.radius = radius
        self.secondary_font_size = secondary_font_size
        self.jj_vert = JinJangVertices(radius)

        self.line_conf = {
            "stroke_width": 4,
            "color": YELLOW_B
        }

        r_2 = self.radius / 2
        r_8 = self.radius / 8
        self.top_circle = Circle(radius=r_8, **self.line_conf).move_to(np.array((0.0, r_2, 0.0)))
        self.bottom_circle = Circle(radius=r_8, **self.line_conf).move_to(np.array((0.0, -r_2, 0.0)))
        self.text = Text("陰陽", color=RED, font_size=primary_font_size).move_to(np.array((0.0, -radius * 1.3, 0.0)))

        self.to_fadeout = []
        self.to_remove = []
        self.jj_group: VGroup = None

    def draw_jj_shape(self):
        self.to_remove = [
            Polygon(
                *self.jj_vert.get_full_circle(),
                **self.line_conf
            ),
            ParametricFunction(
                self.jj_vert.get_s_func,
                t_range=np.array([0, TAU]),
                **self.line_conf)
        ]
        for shape in self.to_remove:
            self.play(Create(shape))
        self.play(Create(self.top_circle), Create(self.bottom_circle))
        self.to_remove.extend([self.top_circle, self.bottom_circle])

    def flip_jj_shape(self):
        self.jj_group = VGroup(*[
            Polygon(
                *self.jj_vert.get_full_circle(),
                **self.line_conf
            ),
            ParametricFunction(
                self.jj_vert.get_s_func,
                t_range=np.array([0, TAU]),
                **self.line_conf),
            self.top_circle,
            self.bottom_circle
        ])
        self.play(ApplyMatrix(
            matrix=[[1, 0], [0, -1]],
            mobject=self.jj_group
        ), run_time=2.0)

    def fill_jj_halves(self):
        left_half_poly = Polygon(*[
            *self.jj_vert.get_left_half_circle(),
            *self.jj_vert.get_middle_s()
        ])
        conf_left = {
            "fill_opacity": 1,
            "stroke_width": 0,
            "color": WHITE
        }

        right_half_poly = Polygon(*[
            *self.jj_vert.get_middle_s(),
            *self.jj_vert.get_right_half_circle()
        ])
        conf_right = {
            "fill_opacity": 1,
            "stroke_width": 0,
            "color": GREY_E
        }

        r_2 = self.radius / 2
        r_8 = self.radius / 8
        _top_circle = Circle(radius=r_8, **conf_right).move_to(np.array((0.0, r_2, 0.0)))
        _bottom_circle = Circle(radius=r_8, **conf_left).move_to(np.array((0.0, -r_2, 0.0)))

        self.to_fadeout = [
            _top_circle,
            _bottom_circle,
            Cutout(left_half_poly, self.top_circle, **conf_left),
            Cutout(right_half_poly, self.bottom_circle, **conf_right),
        ]
        self.play(*map(lambda shape: FadeIn(shape), self.to_fadeout))

    def _fade_out(self):
        self.play(*map(lambda shape: FadeOut(shape), self.to_fadeout))
        self.to_fadeout.clear()

    def _remove(self):
        self.remove(*self.to_remove)
        self.to_remove.clear()

    def write_final_message(self):
        self.jj_group.generate_target()
        self.jj_group.target.scale(0.5).shift(2 * UP)

        for obj in self.jj_group.target:
            obj.set(stroke_width=3)

        self.play(MoveToTarget(self.jj_group))

        line1 = Text("Sacral", color=YELLOW_B, font_size=self.secondary_font_size).next_to(self.jj_group.target, DOWN)
        line2 = Text("geometry", color=YELLOW_B, font_size=self.secondary_font_size).next_to(line1, DOWN)

        self.play(Write(line1))
        self.play(Write(line2))

    def construct(self) -> None:
        self.wait(0.5)
        self.draw_jj_shape()
        self.fill_jj_halves()

        self.play(Write(self.text))
        self.to_fadeout.append(self.text)
        self.wait(2.0)

        self._fade_out()
        self._remove()
        self.flip_jj_shape()
        self.write_final_message()
        self.wait(3.0)
        self.play(*[FadeOut(obj) for obj in self.mobjects])
