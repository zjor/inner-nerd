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
from dataclasses import dataclass

import numpy as np
from numpy import sin, cos

from lagrangian_mechanics.solver.ode_solver import solve, integrate_rk4
from manim import *

from primitives import CenterOfMass

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

config.frame_size = (1080, 1080)

SCALE_FACTOR = 1.25

L = 4.0 * SCALE_FACTOR
g = 9.81
T = 2 * np.pi * np.sqrt(L / g)

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

N_STEPS = 8000
SIMULATION_TIME = 5 * T


@dataclass
class UnbalancedWheelParams:
    r: float = 1
    R: float = 2
    m: float = 1
    b: float = 0.8


class UnbalancedWheel:
    def __init__(self, params: UnbalancedWheelParams, initial_th: float = 3 * PI / 5):
        self.params = params
        self.initial_th = initial_th

        self.times = np.linspace(0, SIMULATION_TIME, N_STEPS)
        self.solution = []
        self.thetas = []
        self.positions = []

    def solve_model(self):
        def derivatives(state, step, t, dt):
            r, R, b = self.params.r, self.params.R, self.params.b
            [_th, _w] = state
            return [_w,
                    (g * r * sin(_th) - r * R * _w ** 2 * cos(_th) - _w * b) / (r ** 2 + R ** 2 + 2 * r * R * sin(_th))]

        logging.info("Solving equations...")
        self.solution = solve(
            np.array([self.initial_th, 0]),
            self.times,
            integrate_rk4,
            derivatives
        )
        logging.info(f"Solved: {len(self.solution)} steps")

        self.thetas = self.solution[:, 0]
        self.positions = self.thetas * self.params.R


class Scenario(MovingCameraScene):

    def __init__(self):
        super().__init__()
        self.model = UnbalancedWheel(UnbalancedWheelParams())

    def play_intro(self):
        _l = 2.0
        _th = np.pi / 6
        _th_ = _th + 0.3
        _origin = (0, 1, 0)
        _end = (-_l * np.sin(_th), 1.0 - _l * np.cos(_th), 0)

        group = VGroup()
        group.add(*[
            Line(start=(-0.5, 1.0, 0), end=(0.5, 1.0, 0), **primary_params),
            DashedVMobject(Line(start=(0, 1.2, 0), end=(0, -1.2, 0), **secondary_params), num_dashes=9),
            Line(start=_origin, end=_end, **primary_params),
            Arc(radius=0.5, start_angle=-PI / 2, angle=-_th, arc_center=_origin, **secondary_params),
            DashedVMobject(
                Arc(radius=_l, start_angle=-_th_ - PI / 2, angle=2 * _th_, arc_center=_origin, **secondary_params),
                num_dashes=12
            ),
            Circle(radius=0.2, **primary_params).move_to(_end),
        ])

        primary_font = {
            "font_size": 36,
            "color": GREEN_B
        }

        secondary_font = {
            "font_size": 36,
            "color": BLUE_A
        }

        self.play(FadeIn(group))
        self.play(group.animate.shift(3 * LEFT).scale(0.5))

        text_1 = Text("Lagrangian\nmechanics", **primary_font).next_to(group, direction=RIGHT)
        self.play(Write(text_1))

        line_sep = Line(start=(0, 1, 0), end=(0, -1, 0)).next_to(text_1)
        self.play(Create(line_sep))

        text_2 = Text("Simple\npendulum", **secondary_font).next_to(line_sep, direction=RIGHT)
        self.play(Write(text_2))
        self.wait(3)

    def play_draw_main_scene(self):
        p = self.pendulum
        self.play(Create(p.g_symmetry_line), run_time=0.5)
        self.play(
            FadeIn(*[
                p.g_ceiling,
                p.g_mass,
                p.g_rod
            ]),
            run_time=0.5
        )
        self.play(
            FadeIn(*[
                p.g_angle_arc,
                p.g_trajectory
            ]),
            run_time=0.5
        )
        self.play(
            FadeIn(*[
                p.g_text_theta,
                p.g_text_m,
                p.g_text_l
            ]),
            run_time=0.5
        )

        self.play(p.g_all.animate.scale(SCALE_FACTOR).shift(1.25 * RIGHT + 1.25 * DOWN))
        self.wait(0.5)

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

        text_title = Text("Derivation of the equation of motion", **comment_font) \
            .shift(6 * UP + 4 * LEFT)
        self.play(Write(text_title), run_time=1)

        text_comment1 = Text("1. Lagrangian:", **comment_font) \
            .next_to(text_title, 2 * DOWN) \
            .align_to(text_title, LEFT)
        self.play(Write(text_comment1), run_time=1)
        text_lagrangian = MathTex(r"\mathcal{L} = T - V", **math_font).next_to(text_comment1, RIGHT)
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

        frame = Rectangle(color=RED_C).surround(text_final_eq, dim_to_match=1, stretch=True)
        self.play(Create(frame), run_time=1)
        self.wait(1)

    def animate_pendulum(self):
        self.model.solve_model()

        x_offset = -6

        moving_objects = VGroup()

        R = self.model.params.R
        r = self.model.params.r
        th = self.model.thetas[0]

        floor = Line(start=np.array((-4, -R, 0)), end=np.array((4, -R, 0)), **primary_params)
        wheel = Circle(radius=self.model.params.R).move_to(np.array((x_offset, 0, 0)))

        x0, y0 = r * sin(th) + x_offset, r * cos(th)
        cm = CenterOfMass(radius=0.2, color=YELLOW, stroke_width=2).move_to([x0, y0, 0])

        point_of_contact = Circle(radius=0.05, stroke_color=PURE_RED, fill_color=PURE_RED, fill_opacity=1).move_to(np.array((x_offset, -R, 0)))

        moving_objects.add(wheel, cm, point_of_contact)

        self.add(floor)
        self.add(moving_objects)

        time = ValueTracker(0)

        def updater(_: VGroup) -> None:
            step = int(time.get_value() / SIMULATION_TIME * N_STEPS)
            _th = self.model.thetas[step]
            _pos = self.model.positions[step] + x_offset
            _x, _y = r * sin(_th) + _pos, r * cos(_th)
            wheel.move_to(np.array((_pos, 0, 0)))

            _cm = CenterOfMass(radius=0.2, angle=-_th, color=YELLOW, stroke_width=2).move_to([_x, _y, 0])
            cm.become(_cm)

            point_of_contact.move_to(np.array((_pos, -R, 0)))

        moving_objects.add_updater(updater)

        self.play(time.animate.set_value(SIMULATION_TIME),
                  run_time=SIMULATION_TIME,
                  rate_func=rate_functions.linear)

    def fade_out_all(self):
        self.play(*[FadeOut(obj) for obj in self.mobjects])

    def construct(self):
        # self.play_intro()
        # self.fade_out_all()
        # self.play_draw_main_scene()
        # self.play_draw_equations()
        self.animate_pendulum()
        # self.wait(5)


if __name__ == "__main__":
    scene = Scenario()

    scene.render()
