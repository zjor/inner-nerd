import numpy as np
from manimlib import *

COLOR = GREEN_E


class AnimateByMoving(Scene):

    def construct(self):

        text = Text("Animations #1", color=COLOR)
        self.play(FadeIn(text))
        self.wait()
        self.play(FadeOut(text))

        size = 6
        d = size / 2
        v_line = Line(start=np.array((-d, -d, 0)), end=np.array((-d, d, 0)), color=COLOR)
        h_line = Line(start=np.array((-d, -d, 0)), end=np.array((d, -d, 0)), color=COLOR)
        self.play(FadeIn(VGroup(*[v_line, h_line])))

        frames_count = 100
        dx = size / frames_count

        start = np.array((-d, d, 0))
        end = np.array((-d, -d, 0))

        dot_start = Dot(color=COLOR).move_to(start)
        dot_end = Dot(color=COLOR).move_to(end)
        line = Line(start=start, end=end, color=COLOR)
        self.add(*[dot_start, dot_end, line])

        for i in range(frames_count):
            new_start = start + np.array((0, -dx, 0))
            new_end = end + np.array((dx, 0, 0))

            self.play(
                dot_start.move_to, new_start,
                dot_end.move_to, new_end,
                line.put_start_and_end_on, new_start, new_end,
                run_time=5 / frames_count, rate_func=linear
            )

            if i % 10 == 0 and i > 0:
                self.add(*[
                    Dot(color=GREY_C).move_to(start),
                    Dot(color=GREY_C).move_to(end),
                    Line(start=start, end=end, color=GREY_C)])

            start, end = new_start, new_end

        self.wait(3)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )


class AnimateByUpdateFromFunc(Scene):

    def construct(self):
        size = 6
        d = size / 2
        v_line = Line(start=np.array((-d, -d, 0)), end=np.array((-d, d, 0)), color=COLOR)
        h_line = Line(start=np.array((-d, -d, 0)), end=np.array((d, -d, 0)), color=COLOR)
        self.add(*[v_line, h_line])

        start = np.array((-d, d, 0))
        end = np.array((-d, -d, 0))

        dot_start = Dot(color=COLOR).move_to(start)
        dot_end = Dot(color=COLOR).move_to(end)
        line = Line(start=start, end=end, color=COLOR)
        g = VGroup(*[dot_start, dot_end, line])

        def update_frame(obj, alpha):
            x1 = np.array((-d, d, 0)) * (1 - alpha) + np.array((-d, -d, 0)) * alpha
            x2 = np.array((-d, -d, 0)) * (1 - alpha) + np.array((d, -d, 0)) * alpha
            g[0].move_to(x1)
            g[1].move_to(x2)
            g[2].put_start_and_end_on(x1, x2)

        self.play(UpdateFromAlphaFunc(g, update_frame), run_time=5, rate_func=linear)
