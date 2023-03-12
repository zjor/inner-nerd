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
from primitives import LAGRANGIAN_RAYLEIGH
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
        self.play(Write(t1), run_time=6)

    def play_draw_main_scene(self):
        self.play(FadeIn(*[
            self.geometry.floor,
            self.geometry.moving_objects
        ]))
        self.play(FadeIn(self.geometry.annotations))
        self.write_problem_description()
        self.wait(4)
        self.play(FadeOut(*self.to_hide))
        self.to_hide.clear()

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
        self.play(Write(txt_1), run_time=1)

        txt_2 = MathTex(r"v_x=\dot{\theta}rsin\theta+\dot{\theta}R", **math_font) \
            .next_to(txt_1, 2 * DOWN) \
            .align_to(txt_1, LEFT)
        self.play(Write(txt_2), run_time=1)
        self.wait(0.5)

        txt_3 = MathTex(r"v_y=-\dot{\theta}rcos\theta", **math_font) \
            .next_to(txt_2, DOWN) \
            .align_to(txt_2, LEFT)
        self.play(Write(txt_3), run_time=1)
        self.wait(0.5)

        txt_4 = MathTex(r"v^2=\dot{\theta}^2(r^2+R^2+2rRsin\theta)", **math_font) \
            .next_to(txt_3, DOWN) \
            .align_to(txt_3, LEFT)
        self.play(Write(txt_4), run_time=1)
        self.wait(0.5)

        txt_5 = MathTex(r"T=\frac{1}{2}m\dot{\theta}^2(r^2+R^2+2rRsin\theta)", **math_font) \
            .next_to(txt_4, DOWN) \
            .align_to(txt_4, LEFT)
        self.play(Write(txt_5), run_time=1)
        self.wait(1)

        # Potential energy section
        txt_6 = Text("2. Potential energy", **comment_font) \
            .move_to(6.5 * UP + LEFT)
        self.play(Write(txt_6), run_time=1)

        txt_7 = MathTex(r"V=mg(R+rcos\theta)", **math_font) \
            .next_to(txt_6, 2 * DOWN) \
            .align_to(txt_6, LEFT)
        self.play(Write(txt_7), run_time=1)
        self.wait(0.5)

        # Rayleigh energy dissipation function
        txt_8 = Text("3. Rayleigh dissipation", **comment_font) \
            .next_to(txt_7, 2 * DOWN) \
            .align_to(txt_7, LEFT)
        self.play(Write(txt_8), run_time=1)
        self.wait(0.5)

        txt_9 = MathTex(r"D=\frac{1}{2}{\dot{\theta}^2}b", **math_font) \
            .next_to(txt_8, 2 * DOWN) \
            .align_to(txt_8, LEFT)
        self.play(Write(txt_9), run_time=1)
        self.wait(1)

        # Deriving equations of motion
        txt_10 = Text("4. Equations of motion", **comment_font) \
          .move_to(6.5 * UP + 3 * RIGHT)
        self.play(Write(txt_10), run_time=1)

        txt_11 = MathTex(r"\mathcal{L}=\frac{1}{2}m\dot{\theta}^2(r^2+R^2+2rRsin\theta)-\\-mg(R+rcos\theta)", **math_font) \
            .next_to(txt_10, 2 * DOWN) \
            .align_to(txt_10, LEFT)
        self.play(Write(txt_11), run_time=1)
        self.wait(0.5)

        txt_12 = MathTex(LAGRANGIAN_RAYLEIGH, **math_font) \
            .next_to(txt_11, DOWN) \
            .align_to(txt_11, LEFT)
        self.play(Write(txt_12), run_time=1)
        self.wait(0.5)

        f = r"\frac{\partial\mathcal{L}}{\partial\dot\theta}=m\dot\theta(r^2+R^2+2rRsin\theta)"
        txt_13 = MathTex(f, **math_font) \
            .next_to(txt_12, DOWN) \
            .align_to(txt_12, LEFT)
        self.play(Write(txt_13), run_time=1)
        self.wait(0.5)

        f = r"\frac{d}{dt}\left(\frac{\partial \mathcal{L}}{\partial\dot{\theta}}\right)=m\ddot\theta(r^2+R^2+2rRsin\theta)+\\+2rRm{{\theta}^2}cos\theta"
        txt_14 = MathTex(f, **math_font) \
            .next_to(txt_13, DOWN) \
            .align_to(txt_13, LEFT)
        self.play(Write(txt_14), run_time=2)
        self.wait(0.5)

        f = r"\frac{\partial \mathcal{L}}{\partial\theta}=rRm{\dot\theta^2}cos\theta+mgrsin\theta"
        txt_15 = MathTex(f, **math_font) \
            .next_to(txt_14, DOWN) \
            .align_to(txt_14, LEFT)
        self.play(Write(txt_15), run_time=1)
        self.wait(0.5)

        f = r"\ddot\theta(r^2+R^2+2rRsin\theta)+rR{\dot\theta^2}cos\theta-\\-grsin\theta+\dot{\theta}\frac{b}{m}=0"
        txt_16 = MathTex(f, **math_font) \
            .next_to(txt_15, DOWN) \
            .align_to(txt_15, LEFT)
        self.play(Write(txt_16), run_time=2)
        self.wait(0.5)
        self.to_hide.extend([
          txt_1, txt_2, txt_3, txt_4, txt_5, txt_6, txt_7, txt_8,
          txt_9, txt_10, txt_11, txt_12, txt_13, txt_14, txt_15, txt_16
        ])

        f = r"""
\begin{cases}
\ddot\theta=\frac{grsin\theta-rR{\dot\theta^2}cos\theta-\dot{\theta}\frac{b}{m}}{r^2+R^2+2rRsin\theta},\\
x={\theta}R
\end{cases}
        """
        text_final_eq = MathTex(f, **math_font_large) \
            .next_to(txt_16, 1.2 * DOWN) \
            .align_to(txt_16, LEFT)
        self.play(Write(text_final_eq), run_time=3)
        self.wait(0.5)

        frame = Rectangle(color=RED_C).surround(
            text_final_eq, dim_to_match=1, stretch=True)
        self.play(Create(frame), run_time=1)
        self.wait(0.5)

        g = VGroup(text_final_eq, frame)
        self.play(g.animate.move_to([0, -4, 0]))
        self.wait(1)

        self.play(FadeOut(self.geometry.annotations, *self.to_hide))
        self.play(self.geometry.floor.animate.become(self.geometry.full_floor))
        self.wait(1)


    def animate_pendulum(self):
        self.geometry.animate(self)

    def fade_out_all(self):
        self.play(*[FadeOut(obj) for obj in self.mobjects])

    def construct(self):
        self.play_intro()
        self.fade_out_all()
        self.play_draw_main_scene()
        self.play_draw_equations()
        self.animate_pendulum()
        self.wait(5)


if __name__ == "__main__":
    scene = Scenario()

    scene.render()
