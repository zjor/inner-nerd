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

SCALE_FACTOR = 1.25

L = 4.0 * SCALE_FACTOR
g = 9.81
T = 2 * np.pi * np.sqrt(L / g)

N_STEPS = 8000
SIMULATION_TIME = 8 * T
times = np.linspace(0, SIMULATION_TIME, N_STEPS)

theta = -PI / 6  # pendulum angle
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


class SimplePendulum:
    def __init__(self, initial_angle: float = PI / 6, l: float = 4.0, r: float = 0.3):
        self.rod_start = np.array((0, l / 2, 0))

        _th = initial_angle
        _th_ = _th + 0.15
        self.rod_end = np.array((-l * np.sin(_th), l / 2 - l * np.cos(_th), 0))
        self.g_rod = Line(start=self.rod_start, end=self.rod_end, **primary_params)
        self.g_mass = Circle(radius=r, **primary_params).move_to(self.rod_end)

        self.g_ceiling = Line(start=self.rod_start + 0.5 * LEFT, end=self.rod_start + 0.5 * RIGHT, **primary_params)
        self.g_symmetry_line = DashedVMobject(
            Line(start=(0, l / 2 + 0.2, 0), end=(0, -(l / 2 + 0.2), 0), **secondary_params),
            num_dashes=12
        )
        self.g_angle_arc = Arc(radius=0.5, start_angle=-PI / 2, angle=-_th, arc_center=self.rod_start,
                               **secondary_params)
        self.g_trajectory = DashedVMobject(
            Arc(radius=l, start_angle=-_th_ - PI / 2, angle=2 * _th_, arc_center=self.rod_start, **secondary_params),
            num_dashes=12
        )
        self.g_trajectory.set_z_index(self.g_mass.z_index - 1)
        self.g_text_theta = MathTex(r"\theta", **drawing_symbols_params).next_to(self.g_angle_arc, RIGHT)
        self.g_text_l = MathTex(r"l", **drawing_symbols_params) \
            .move_to((self.rod_start + self.rod_end) / 2 + LEFT / 2)
        self.g_text_m = MathTex(r"m", **drawing_symbols_params).next_to(self.g_mass, DOWN)

        self.g_symbols = VGroup(*[
            self.g_text_theta,
            self.g_text_l,
            self.g_text_m
        ])

        self.g_all = VGroup(*[
            self.g_rod,
            self.g_mass,
            self.g_ceiling,
            self.g_symmetry_line,
            self.g_angle_arc,
            self.g_trajectory,
            *self.g_symbols
        ])


class Scenario(MovingCameraScene):

    def __init__(self):
        super().__init__()
        self.pendulum = SimplePendulum()

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
        self.play(FadeOut(self.pendulum.g_symbols), run_time=0.5)

        time = ValueTracker(0)

        ox, oy, _ = self.pendulum.g_rod.get_start()

        def mass_updater(circle: Mobject) -> None:
            step = int(time.get_value() / SIMULATION_TIME * N_STEPS)
            x, y = xs[step] + ox, ys[step] + oy
            circle.move_to(np.array([x, y, 0]))

        def rod_updater(rod: Mobject) -> None:
            step = int(time.get_value() / SIMULATION_TIME * N_STEPS)
            x, y = xs[step] + ox, ys[step] + oy
            rod.put_start_and_end_on(rod.get_start(), end=np.array([x, y, 0]))

        def arc_updater(arc: Arc) -> None:
            step = int(time.get_value() / SIMULATION_TIME * N_STEPS)
            new_arc = Arc(radius=arc.radius * SCALE_FACTOR, start_angle=arc.start_angle, angle=thetas[step],
                          arc_center=np.array((ox, oy, 0)), **secondary_params)
            arc.become(new_arc)

        self.pendulum.g_mass.add_updater(mass_updater)
        self.pendulum.g_rod.add_updater(rod_updater)
        self.pendulum.g_angle_arc.add_updater(arc_updater)

        self.play(time.animate.set_value(SIMULATION_TIME),
                  run_time=SIMULATION_TIME,
                  rate_func=rate_functions.linear)

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
