from manim import *

class Node(VGroup):
    def __init__(self, lable, position=ORIGIN, next=None, **kwargs):
        super().__init__(**kwargs)
        self.lable = lable
        self.position = position
        self.next = next

        self.circle = Square(side_length=1, color=BLUE, fill_opacity=0.5)
        self.lable_text = Text(lable, font_size=24).move_to(self.position)

        self.lable_text.move_to(self.circle.get_center())

        self.add(self.circle, self.lable_text)
        self.move_to(self.position)

    def drawArrow(self):
        if self.next:
            start = self.get_center()
            end = self.next.get_center()

            arrow = Arrow(start=start, end=end, color=WHITE, stroke_width=0.5)
            arrow.tip_length = 0.01
            return arrow
        return None


class LinkedListScene(Scene):
    def construct(self):

        nodes_names = ["1", "2", "3", "4", "5"]
        nodes = []

        # Automatic positioning with spacing
        spacing = 2  # Adjust spacing as needed
        total_width = spacing * (len(nodes_names) - 1)
        start_position = ORIGIN - RIGHT * total_width / 2

        for i, name in enumerate(nodes_names):
            position = start_position + RIGHT * i * spacing
            node = Node(lable=name, position=position)
            nodes.append(node)

            if i > 0:
                nodes[i-1].next = node

        arrows = [node.drawArrow() for node in nodes if node.next]

        self.play(*[Create(node) for node in nodes])
        self.wait(1)

        for arrow in arrows:
            if arrow:
                self.play(Create(arrow))

        self.wait(1)