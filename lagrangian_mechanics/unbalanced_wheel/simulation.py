import logging
import numpy as np
from numpy import pi as PI, sin, cos
from lagrangian_mechanics.unbalanced_wheel.params import ModelParams, N_STEPS, SIMULATION_TIME, g
from lagrangian_mechanics.solver.ode_solver import solve, integrate_rk4


class Simulation:
    def __init__(self, params: ModelParams, initial_th: float = 3 * PI / 5):
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
