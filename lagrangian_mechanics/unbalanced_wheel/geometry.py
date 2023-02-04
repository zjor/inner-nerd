from manim import *
from numpy import sin, cos
from primitives import SegmentedWheel, WheelAxis, CenterOfMass
from lagrangian_mechanics.unbalanced_wheel import Simulation, SIMULATION_TIME, N_STEPS


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


class Geometry:
    def __init__(self, model: Simulation):
        self.model = model
        model.solve_model()

        self.time = ValueTracker(0)
        self.moving_objects = VGroup()
        self.annotations = VGroup()

        R = self.model.params.R
        r = self.model.params.r
        th = self.model.thetas[0]
        x_offset = -6

        self.R = R
        self.r = r
        self.th = th
        self.x_offset = x_offset

        x = model.positions[0] + x_offset

        self.floor = Line(start=np.array((-4, -R, 0)),
                          end=np.array((0, -R, 0)), stroke_width=4, **primary_params)
        self.full_floor = Line(start=np.array((-4, -R, 0)),
                          end=np.array((4, -R, 0)), stroke_width=4, **primary_params)
        self.wheel = SegmentedWheel(radius=R, thickness=0.1, angle=-th,
                                    secondary_color=BLACK, stroke_width=1).move_to([x, 0, 0])
        self.wheel_axis = WheelAxis(radius=(R - 0.1), angle=(th + PI / 4),
                                    stroke_color=BLUE, stroke_width=2).move_to([x, 0, 0])

        x0, y0 = r * sin(th) + x, r * cos(th)
        self.cm = CenterOfMass(radius=0.2, angle=-th, color=YELLOW,
                               stroke_width=2).move_to([x0, y0, 0])

        self.point_of_contact = Circle(radius=0.025, stroke_color=PURE_RED,
                                       fill_color=PURE_RED, fill_opacity=1).move_to(np.array((x, -R, 0)))

        self.moving_objects.add(
            self.wheel,
            self.cm,
            self.point_of_contact,
            self.wheel_axis)

        big_arrow = Arrow(start=ORIGIN, end=[R * cos(0.75 * PI), R * sin(0.75 * PI), 0], buff=0, color=RED, stroke_width=3, max_tip_length_to_length_ratio=0.1).shift([x, 0, 0])
        small_arrow = Arrow(start=[x, 0, 0], end=[x0, y0, 0], buff=0, color=RED, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        self.annotations.add(*[
          big_arrow,
          MathTex(r"R", font_size=36, color=RED).move_to(big_arrow.get_center() + 0.3 * (LEFT + DOWN)),
          small_arrow,
          MathTex(r"r", font_size=36, color=RED).move_to(small_arrow.get_center() + 0.3 * (RIGHT + UP)),
          MathTex(r"m", font_size=36, color=RED).next_to(self.cm, RIGHT),
          MathTex(r"b", font_size=36, color=RED).next_to(self.point_of_contact, DOWN),
          DashedLine(start=ORIGIN, end=[0, R, 0], dash_length=0.2, stroke_color=RED, stroke_width=3).shift([x, 0, 0]),          
          DashedVMobject(Arc(radius=0.3, start_angle=PI / 2, angle=-th, arc_center=[x, 0, 0], stroke_color=RED, stroke_width=3), num_dashes=3),
          MathTex(r"\theta", font_size=36, color=RED).move_to([x + 0.3, 0.5, 0])
        ])

    def _updater(self, _: VGroup) -> None:

        R = self.R
        r = self.r
        x_offset = self.x_offset

        step = int(self.time.get_value() / SIMULATION_TIME * N_STEPS)
        _th = self.model.thetas[step]
        _pos = self.model.positions[step] + x_offset
        _x, _y = r * sin(_th) + _pos, r * cos(_th)
        self.wheel.become(
            SegmentedWheel(radius=R, thickness=0.1, angle=-
                           _th, secondary_color=BLACK, stroke_width=1)
            .move_to([_pos, 0, 0])
        )

        self.wheel_axis.become(
            WheelAxis(radius=(R - 0.1), angle=(_th + PI / 4),
                      stroke_color=BLUE, stroke_width=2).move_to([_pos, 0, 0])
        )

        _cm = CenterOfMass(radius=0.2, angle=-_th, color=YELLOW,
                           stroke_width=2).move_to([_x, _y, 0])
        self.cm.become(_cm)

        self.point_of_contact.move_to(np.array((_pos, -R, 0)))

    def animate(self, scene: Scene):
        self.moving_objects.add_updater(self._updater)

        scene.play(self.time.animate.set_value(SIMULATION_TIME),
                   run_time=SIMULATION_TIME,
                   rate_func=rate_functions.linear)
