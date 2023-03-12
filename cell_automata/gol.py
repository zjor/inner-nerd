from typing import List
import numpy as np
from manim import *

colors = [
    GREEN_C, BLUE_C, YELLOW_C, MAROON_C
]

class Scenario(Scene):
    def construct(self):
        cells: List[Rectangle] = []
        i = 0
        for x in range(2):
            for y in range(2):
                rect = Rectangle(width=1, height=1, fill_color=colors[i], fill_opacity=0, stroke_color=BLACK).move_to((x, y, 0))
                cells.append(rect)
                i += 1
                self.add(rect)

        for j in range(5):
          for i in range(4):
              self.play(cells[i].animate.set_opacity(1), run_time=0.3)

          for i in range(4):
              self.play(cells[i].animate.set_opacity(0), run_time=0.3)

            


if __name__ == "__main__":
    scene = Scenario()

    scene.render()
