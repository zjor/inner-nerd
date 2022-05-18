from manimlib import *


class Scenario(Scene):
    font = 'Monospace'
    color = GREEN_E

    def blink_cursor(self, delay=0.4, times=4):
        for i in range(times):
            text = Text('_', font=Scenario.font, color=Scenario.color)
            self.wait(delay)
            self.add(text)
            self.wait(delay)
            self.remove(text)

    def construct(self):
        self.wait(0.5)
        self.blink_cursor()

        phrase = "It all started with a dot"
        for i in range(len(phrase) + 1):
            text = Text(phrase[:i] + '_', font=Scenario.font, color=Scenario.color)
            self.add(text)
            self.wait(0.1)
            if i < len(phrase):
                self.remove(text)

        dot = Circle(radius=0.1, fill_opacity=1, color=Scenario.color)
        dot.set_fill(Scenario.color)

        self.play(Transform(text, target_mobject=dot), run_time=1)
        self.wait(1)
        self.play(FadeOut(text, scale=0.1))
        self.wait(1)

        title = Text("Genesis", font=Scenario.font, color=Scenario.color)
        self.play(FadeIn(title))
        self.wait(1)

        exit_message = Text("to be continued...", font=Scenario.font, color=Scenario.color) \
            .move_to((RIGHT + DOWN) * 3)

        self.play(FadeIn(exit_message))
        self.wait(1.0)

        g = VGroup()
        g.add(*[title, exit_message])
        self.play(FadeOut(g))
        self.wait(1.0)
