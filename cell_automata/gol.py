from dataclasses import dataclass
import random
from typing import List
import numpy as np
from manim import *


@dataclass
class RuleOfLife:
    birth: list[int]
    survival: list[int]


class CommonRules(Enum):
    CLASSIC_B3_S23 = RuleOfLife(birth=[3], survival=[2, 3])
    LABYRINTH_B3_S12345 = RuleOfLife(birth=[3], survival=[1, 2, 3, 4, 5])


class GameOfLife:

    @staticmethod
    def identity(n: int) -> List[List[int]]:
        return [[0] * n for _ in range(n)]

    @staticmethod
    def seed(field: List[List[int]], n: int) -> List[List[int]]:
        random.seed(42)
        for row in range(n):
            for col in range(n):
                field[row][col] = 1 if random.random() > 0.5 else 0
        return field

    @staticmethod
    def seed_manual(field: List[List[int]], n: int) -> List[List[int]]:
        m = n // 2 - 1
        field[m][m] = 1
        field[m - 1][m - 1] = 1
        field[m - 1][m + 1] = 1
        return field

    @staticmethod
    def sum_neighbours(field: List[List[int]], n: int, row: int, col: int):
        s = 0
        if row > 0:
            s += field[row - 1][col]
            if col > 0:
                s += field[row - 1][col - 1]
            if col < n - 1:
                s += field[row - 1][col + 1]
        if col > 0:
            s += field[row][col - 1]
        if col < n - 1:
            s += field[row][col + 1]
        if row < n - 1:
            s += field[row + 1][col]
            if col > 0:
                s += field[row + 1][col - 1]
            if col < n - 1:
                s += field[row + 1][col + 1]
        return s

    def __init__(self, rule: RuleOfLife, n: int = 16) -> None:
        self.n = n
        self.rule = rule
        self.state = GameOfLife.seed_manual(GameOfLife.identity(n), n)

    def evolve(self) -> List[List[int]]:
        next_state = GameOfLife.identity(self.n)
        for row in range(self.n):
            for col in range(self.n):
                neighbours = GameOfLife.sum_neighbours(
                    self.state, self.n, row, col)
                if neighbours in self.rule.birth:
                    next_state[row][col] = 1
                elif neighbours in self.rule.survival and self.state[row][col] == 1:
                    next_state[row][col] = 1
                else:
                    next_state[row][col] = 0
        return next_state


class Scenario(Scene):
    def construct(self):
        n = 48
        dx = 0.175
        gol = GameOfLife(rule=CommonRules.LABYRINTH_B3_S12345.value, n=n)
        pixels = [[None] * n for _ in range(n)]
        for row in range(n):
            for col in range(n):
                props = {
                    "stroke_width": 0,
                    "fill_opacity": gol.state[row][col]
                }
                x, y = (col - n // 2) * dx, (row - n // 2) * dx
                rect = Rectangle(PINK, dx, dx, **props).move_to((x, y, 0))
                pixels[row][col] = rect
                self.add(rect)

        for _ in range(100):
            next_state = gol.evolve()
            animations = []
            for row in range(n):
                for col in range(n):
                    if next_state[row][col] != gol.state[row][col]:
                        rect: VMobject = pixels[row][col]
                        animations.append(
                            rect.animate.set_opacity(next_state[row][col]))
            gol.state = next_state
            if len(animations) > 0:
                self.play(*animations, run_time=0.1)


if __name__ == "__main__":
    scene = Scenario()

    scene.render()


"""
Rules to try:
- 34 Life: This variant of the Game of Life uses the same basic rules, but adds a new birth rule: a dead cell with exactly 3, 4, or 5 neighbors will come to life. This results in more frequent and varied birth patterns, which can lead to interesting and visually pleasing structures.
- Seeds: In this variant, the only birth rule is that a dead cell with exactly 2 or 4 neighbors will come to life. This creates a very sparse pattern, with most cells remaining dead, but the resulting structures can be very intricate and beautiful.
- HighLife: This variant adds a new birth rule, in addition to the standard rule: a dead cell with exactly 3 or 6 neighbors will come to life. This leads to more complex and dynamic patterns, with a greater variety of shapes and behaviors than the standard Game of Life.
- Day and Night: This variant uses the same basic rules as the Game of Life, but adds a new rule for cell survival: a live cell survives if it has 3, 4, 6, or 7 live neighbors. This creates patterns that are more symmetrical and balanced than the standard Game of Life, with shapes that resemble crystals or snowflakes.
"""