"""
Lagrangian mechanics simulation: simple pendulum

Scenario:
  [intro]
    - draw a pendulum with helper lines
    - scale down, move left
    - write: Lagrangian mechanics
    - vertical line
    - write: simple pendulum
  [scene]
    - fade in: pendulum on the right
    - write lagrangian, L
    - differentiate
    - derive equations of motion
    - animate pendulum
    - stop, wait & fade out
"""

import numpy as np
from lagrangian_mechanics.solver.ode_solver import solve, integrate_rk4
from manim import *

config.frame_size = (1080, 1080)

L = 2.0
g = 9.81
T = 2 * np.pi * np.sqrt(L / g)

N_STEPS = 1000
SIMULATION_TIME = 1 * T
times = np.linspace(0, SIMULATION_TIME, N_STEPS)

theta = np.pi / 6  # pendulum angle
omega = 0  # pendulum angular velocity


def derivatives(state, step, t, dt):
    [_th, _w] = state
    return [_w, - g / L * np.sin(_th)]


solution = solve(
    np.array([theta, omega]),
    times,
    integrate_rk4,
    derivatives
)

thetas = solution[:, 0]
xs = L * np.sin(thetas)
ys = -L * np.cos(thetas)


class Scenario(MovingCameraScene):

    def play_intro(self):
        _l = 2.0
        _th = np.pi / 6
        _th_ = _th + 0.3
        _origin = (0, 1, 0)
        _end = (-_l * np.sin(_th), 1.0 - _l * np.cos(_th), 0)

        primary_params = {
            "stroke_color": GREEN_B,
            "fill_opacity": 1,
            "fill_color": GREEN_B
        }

        secondary_params = {
            "stroke_color": BLUE_A,
            "stroke_width": 2.0
        }

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
        self.wait(5)

    def construct(self):
        self.play_intro()
        return
        time = ValueTracker(0)

        def updater(_: Mobject):
            step = int(time.get_value() / SIMULATION_TIME * N_STEPS)
            x, y = xs[step], ys[step]
            circle.move_to(np.array([x, y, 0]))
            line.put_start_and_end_on(line.get_start(), end=np.array([x, y, 0]))

        circle = Circle(radius=0.1, color=GREEN_E, fill_opacity=1)
        line = Line(
            start=np.array([0, 0, 0]),
            end=np.array([0, -0.2, 0]),
            stroke_width=2,
            stroke_color=GREEN_E
        )

        circle.add_updater(updater)

        self.camera.frame.set(width=5).move_to([0, -L / 2, 0])

        self.add(circle)
        self.add(line)
        self.add(Line(
            start=[-0.2, 0, 0],
            end=[0.2, 0, 0],
            stroke_width=2,
            stroke_color=GREEN_E
        ))
        self.play(time.animate.set_value(SIMULATION_TIME),
                  run_time=SIMULATION_TIME,
                  rate_func=rate_functions.linear)


if __name__ == "__main__":
    scene = Scenario()

    scene.render()
