"""
Lagrangian mechanics simulation: an un balanced wheel

A mass (m) is attached to a weightless wheel of a radius (R),
the distance between the mass and the center of a wheel is (r),
(if r == R we face Θ'' -> inf, when Θ -> pi)
initial angle of a wheel is Θ, friction coefficient is (b)

Eq. of motion: Θ''(r^2 + R^2 + 2rRsinΘ) + rRΘ^2cosΘ - grsinΘ + Θ'b/m = 0

Scenario:
  [intro]
    - fade in: logo & 'Lagrangian mechanics'
    - vertical line
    - write: unbalanced wheel
  [scene]
    - fade in: unbalanced wheel
    - fade in: notation
    - write lagrangian, L, D-function
    - differentiate
    - derive equations of motion
    - animate the wheel
    - wait until motion stops, pause
"""
import logging

import numpy as np

from lagrangian_mechanics.unbalanced_wheel import ModelParams, Simulation, Geometry
from manim import *


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

config.frame_size = (1080, 1080)


primary_params = {
    "stroke_color": GREEN_B,
    "fill_opacity": 1,
    "fill_color": GREEN_B
}

secondary_params = {
    "stroke_color": BLUE_C,
    "stroke_width": 2.0
}

drawing_symbols_params = {
    "color": RED_C,
    "font_size": 36
}


class Scenario(MovingCameraScene):

    def __init__(self):
        super().__init__()
        self.model = Simulation(ModelParams())
        self.geometry = Geometry(self.model)
        self.to_hide = []

    def play_intro(self):
        _l = 2.0
        _th = np.pi / 6
        _th_ = _th + 0.3
        _origin = (0, 1, 0)
        _end = (-_l * np.sin(_th), 1.0 - _l * np.cos(_th), 0)

        group = VGroup()
        group.add(*[
            Line(start=(-0.5, 1.0, 0), end=(0.5, 1.0, 0), **primary_params),
            DashedVMobject(Line(start=(0, 1.2, 0), end=(
                0, -1.2, 0), **secondary_params), num_dashes=9),
            Line(start=_origin, end=_end, **primary_params),
            Arc(radius=0.5, start_angle=-PI / 2, angle=-
                _th, arc_center=_origin, **secondary_params),
            DashedVMobject(
                Arc(radius=_l, start_angle=-_th_ - PI / 2, angle=2 *
                    _th_, arc_center=_origin, **secondary_params),
                num_dashes=12
            ),
            Circle(radius=0.2, **primary_params).move_to(_end),
        ])
        group.shift(3 * LEFT).scale(0.5)

        primary_font = {
            "font_size": 36,
            "color": GREEN_B
        }

        secondary_font = {
            "font_size": 36,
            "color": BLUE_A
        }

        text_1 = Text("Lagrangian\nmechanics", **
                      primary_font).next_to(group, direction=RIGHT)
        self.play(FadeIn(group, text_1))

        line_sep = Line(start=(0, 1, 0), end=(0, -1, 0)).next_to(text_1)
        self.play(Create(line_sep))

        text_2 = Text("Unbalanced\nwheel", **
                      secondary_font).next_to(line_sep, direction=RIGHT)
        self.play(Write(text_2))
        self.wait(1.5)

    def write_problem_description(self):
        text = """A mass m is attached to a weightless wheel
of a radius R, the distance between the mass 
and the center of the wheel is r,
initial angle of the wheel is Θ, 
the friction coefficient is b."""
        t2c = {
          '[7:8]': RED,
          '[55:56]': RED,
          '[120:121]': RED,
          '[153:154]': RED,
          '[185:186]': RED,
        }
        t1 = Text(text, t2c=t2c, color=GREEN_B, font="Consolas", font_size=24, line_spacing=1.5).next_to(self.geometry.moving_objects, RIGHT)
        self.to_hide.append(t1)
        self.play(Write(t1), run_time=3)

    def play_draw_main_scene(self):
        self.play(FadeIn(*[
            self.geometry.floor,
            self.geometry.moving_objects
        ]))
        self.play(FadeIn(self.geometry.annotations))
        self.write_problem_description()
        self.wait(1)
        self.play(FadeOut(self.geometry.annotations, *self.to_hide))
        self.play(self.geometry.floor.animate.become(self.geometry.full_floor))

    def play_draw_equations(self):
        comment_font = {
            "font_size": 24,
            "color": GREEN_B
        }

        math_font = {
            "font_size": 28,
            "color": BLUE_B
        }

        math_font_large = {
            "font_size": 36,
            "color": BLUE_B
        }

        # Kinetic energy section
        txt_1 = Text("1. Kinetic energy", **comment_font) \
            .move_to(6.5 * UP + 5.5 * LEFT)
        self.play(Write(txt_1), run_time=0.5)

        txt_2 = MathTex(r"v_x=\dot{\theta}rsin\theta+\dot{\theta}R", **math_font) \
            .next_to(txt_1, 2 * DOWN) \
            .align_to(txt_1, LEFT)
        self.play(Write(txt_2), run_time=0.5)

        txt_3 = MathTex(r"v_y=-\dot{\theta}rcos\theta", **math_font) \
            .next_to(txt_2, DOWN) \
            .align_to(txt_2, LEFT)
        self.play(Write(txt_3), run_time=0.5)

        txt_4 = MathTex(r"v^2=\dot{\theta}^2(r^2+R^2+2rRsin\theta)", **math_font) \
            .next_to(txt_3, DOWN) \
            .align_to(txt_3, LEFT)
        self.play(Write(txt_4), run_time=0.5)

        txt_5 = MathTex(r"T=\frac{1}{2}m\dot{\theta}^2(r^2+R^2+2rRsin\theta)", **math_font) \
            .next_to(txt_4, DOWN) \
            .align_to(txt_4, LEFT)
        self.play(Write(txt_5), run_time=0.5)

        # Potential energy section
        txt_6 = Text("2. Potential energy", **comment_font) \
            .move_to(6.5 * UP + LEFT)
        self.play(Write(txt_6), run_time=0.5)

        txt_7 = MathTex(r"V=mg(R+rcos\theta)", **math_font) \
            .next_to(txt_6, 2 * DOWN) \
            .align_to(txt_6, LEFT)
        self.play(Write(txt_7), run_time=0.5)

        # Reileygh energy dissipation function
        txt_8 = Text("3. Reileygh dissipation", **comment_font) \
            .next_to(txt_7, 2 * DOWN) \
            .align_to(txt_7, LEFT)
        self.play(Write(txt_8), run_time=0.5)

        txt_9 = MathTex(r"D=\frac{1}{2}{\dot{\theta}^2}b", **math_font) \
            .next_to(txt_8, 2 * DOWN) \
            .align_to(txt_8, LEFT)
        self.play(Write(txt_9), run_time=0.5)

        # Deriving equations of motion
        txt_10 = Text("4. Equations of motion", **comment_font) \
          .move_to(6.5 * UP + 3 * RIGHT)
        self.play(Write(txt_10), run_time=0.5)

        txt_11 = MathTex(r"\mathcal{L}=\frac{1}{2}m\dot{\theta}^2(r^2+R^2+2rRsin\theta)-\\-mg(R+rcos\theta)", **math_font) \
            .next_to(txt_10, 2 * DOWN) \
            .align_to(txt_10, LEFT)
        self.play(Write(txt_11), run_time=0.5)


        LE_LaTeX = \
            r"\frac{d}{dt}\left(\frac{\partial \mathcal{L}}{\partial\dot{\theta}}\right)-\frac{\partial \mathcal{L}}{\partial\theta}+\frac{\partial D}{\partial{\dot\theta}}=0"
        txt_12 = MathTex(LE_LaTeX, **math_font) \
            .next_to(txt_11, DOWN) \
            .align_to(txt_11, LEFT)
        self.play(Write(txt_12), run_time=0.5)


        return

        text_comment1 = Text("1. Lagrangian:", **comment_font) \
            .next_to(text_title, 2 * DOWN) \
            .align_to(text_title, LEFT)
        self.play(Write(text_comment1), run_time=1)
        text_lagrangian = MathTex(
            r"\mathcal{L} = T - V", **math_font).next_to(text_comment1, RIGHT)
        self.play(Write(text_lagrangian), run_time=1)

        text_t = MathTex(r"T = m\frac{(\dot{\theta}l)^2}{2},\;kinetic\;energy", **math_font) \
            .next_to(text_lagrangian, DOWN) \
            .align_to(text_comment1, LEFT)
        self.play(Write(text_t), run_time=1)

        text_v = MathTex(r"V = mgl(1 - cos\theta),\;potential\;energy", **math_font) \
            .next_to(text_t, DOWN) \
            .align_to(text_t, LEFT)
        self.play(Write(text_v), run_time=1)

        self.wait(3)

        text_comment2 = Text("2. Plugging into the Lagrange's equation:", **comment_font) \
            .next_to(text_v, 2 * DOWN) \
            .align_to(text_v, LEFT)
        self.play(Write(text_comment2), run_time=1)

        LE_LaTeX = \
            r"\frac{d}{dt}\left(\frac{\partial \mathcal{L}}{\partial\dot{\theta}}\right)-\frac{\partial \mathcal{L}}{\partial\theta}=0"
        text_le = MathTex(LE_LaTeX, **math_font) \
            .next_to(text_comment2, DOWN) \
            .align_to(text_comment2, LEFT)
        self.play(Write(text_le), run_time=1)

        text_le_1 = MathTex(r"\frac{\partial \mathcal{L}}{\partial\dot{\theta}}=ml^2\dot\theta^2", **math_font) \
            .next_to(text_le, DOWN) \
            .align_to(text_le, LEFT)
        self.play(Write(text_le_1), run_time=1)

        text_le_2 = MathTex(
            r"\frac{d}{dt}\left(\frac{\partial \mathcal{L}}{\partial\dot{\theta}}\right)=ml^2\ddot\theta", **math_font) \
            .next_to(text_le_1, DOWN) \
            .align_to(text_le_1, LEFT)
        self.play(Write(text_le_2), run_time=1)

        text_le_3 = MathTex(r"\frac{\partial \mathcal{L}}{\partial\theta}=-mglsin\theta", **math_font) \
            .next_to(text_le_2, DOWN) \
            .align_to(text_le_2, LEFT)
        self.play(Write(text_le_3), run_time=1)

        self.wait(2)

        text_le_4 = MathTex(r"ml^2\ddot\theta+mglsin\theta=0", **math_font) \
            .next_to(text_le_3, 2 * DOWN) \
            .align_to(text_le_3, LEFT)
        self.play(Write(text_le_4), run_time=1)

        self.wait(1)

        text_final_eq = MathTex(r"\ddot\theta+\frac{g}{l}sin\theta=0", **math_font_large) \
            .next_to(text_le_3, 2 * DOWN) \
            .align_to(text_le_3, LEFT)

        self.play(text_le_4.animate.become(text_final_eq), run_time=2)

        frame = Rectangle(color=RED_C).surround(
            text_final_eq, dim_to_match=1, stretch=True)
        self.play(Create(frame), run_time=1)
        self.wait(1)

    def animate_pendulum(self):
        self.geometry.animate(self)

    def fade_out_all(self):
        self.play(*[FadeOut(obj) for obj in self.mobjects])

    def construct(self):
        # self.play_intro()
        # self.fade_out_all()
        # self.play_draw_main_scene()
        self.play_draw_equations()
        # self.animate_pendulum()
        # self.wait(5)


if __name__ == "__main__":
    scene = Scenario()

    scene.render()
