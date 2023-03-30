from numpy import sin
from manim import *



class Scenario(Scene):
    def construct(self):
        for i in range(256):
            radius = 2 * (1 - i / 255)
            v = i / 255
            color = rgb_to_color([v] * 3)
            c = Circle(radius=radius, color=color, fill_color=color).move_to([-3, 3, 0])
            self.add(c)

            v = 1 / (256 - i)
            color = rgb_to_color([v] * 3)
            c = Circle(radius=radius, color=color, fill_color=color, stroke_color=color).move_to([0, 0, 0])
            self.add(c)

            v = sin(i / 255 * PI / 2)
            color = rgb_to_color([v] * 3)
            c = Circle(radius=radius, color=color, fill_color=color).move_to([3, -3, 0])
            self.add(c)


if __name__ == "__main__":
    config.frame_size = (1080, 1080)
    scene = Scenario()

    scene.render()
