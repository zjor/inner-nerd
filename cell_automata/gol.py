import random
from typing import List
import numpy as np
from manim import *


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

    def __init__(self, n: int = 16) -> None:
        self.n = n        
        self.state = GameOfLife.seed(GameOfLife.identity(n), n)

    def evolve(self) -> List[List[int]]:
        next_state = GameOfLife.identity(self.n)
        for row in range(self.n):
            for col in range(self.n):
                x = GameOfLife.sum_neighbours(self.state, self.n, row, col)
                if x == 3:
                    next_state[row][col] = 1
                elif x in [2, 3] and self.state[row][col] == 1:
                    next_state[row][col] = 1
                else:
                    next_state[row][col] = 0
        return next_state

    
class Scenario(Scene):
    def construct(self):
        n = 32
        dx = 0.175
        gol = GameOfLife(n)
        pixels = [[None] * n for _ in range(n)]
        for row in range(n):
            for col in range(n):
                props = {
                    "stroke_width": 0,
                    "fill_opacity": gol.state[row][col]
                }
                x, y = (col - n // 2) * dx, (row - n // 2) * dx
                rect = Rectangle(BLUE_C, dx, dx, **props).move_to((x, y, 0))
                pixels[row][col] = rect
                self.add(rect)
        
        for _ in range(50):
            next_state = gol.evolve()
            animations = []
            for row in range(n):
                for col in range(n):
                    if next_state[row][col] != gol.state[row][col]:
                        rect: VMobject = pixels[row][col]
                        animations.append(rect.animate.set_opacity(next_state[row][col]))            
            gol.state = next_state
            if len(animations) > 0:
                self.play(*animations, run_time=0.5)
                    




if __name__ == "__main__":
    scene = Scenario()

    scene.render()
