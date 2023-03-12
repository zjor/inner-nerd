from typing import List
from manim import *
import random

N_SIDES = 8
DX = 0.75
COLORS = [RED_C, BLUE_C, GRAY_B, GREEN_C, YELLOW_C, PINK, GOLD_C, TEAL_C]

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)


def rotate(d):
    if d == RIGHT:
        return DOWN
    elif d == DOWN:
        return LEFT
    elif d == LEFT:
        return UP
    else:
        return RIGHT


def generate_spiral(n: int):
    m = [[0] * n for _ in range(n)]
    coordinates = []

    i = 1
    x = (n // 2 - 1, n // 2 - 1)
    m[x[0]][x[1]] = i
    direction = RIGHT
    coordinates.append(x)

    for side in [2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 8]:
        steps_remaining = side - 1
        while steps_remaining > 0:
            steps_remaining -= 1
            i += 1
            x = (x[0] + direction[0], x[1] + direction[1])
            m[x[0]][x[1]] = i
            coordinates.append(x)

        direction = rotate(direction)

    return m, coordinates


class Scenario(Scene):
    def construct(self):
        self.wait(1)

        blocks = [[None] * N_SIDES for _ in range(N_SIDES)]
        _, seq = generate_spiral(N_SIDES)

        for r in range(N_SIDES):
            for c in range(N_SIDES):
                x = (c - N_SIDES // 2) * DX
                y = (r - N_SIDES // 2) * DX
                color = random.choice(COLORS)
                rect = Rectangle(color=color, width=DX, height=DX,
                                 fill_opacity=0, stroke_width=0).move_to((x, y, 0))
                blocks[r][c] = rect
                self.add(rect)

        i, j = 0, -10
        while j < N_SIDES ** 2:
            x, y = seq[i]
            rect: VMobject = blocks[y][x]
            animations = []
            animations.append(rect.animate.set_opacity(1))

            if j >= 0:
                x, y = seq[j]
                rect: VMobject = blocks[y][x]
                animations.append(rect.animate.set_opacity(0))
            self.play(*animations, run_time=0.1)
            i += 1
            if i >= N_SIDES ** 2:
                i = N_SIDES ** 2 - 1
            j += 1

        self.wait(1)


if __name__ == "__main__":
    scene = Scenario()
    scene.render()
