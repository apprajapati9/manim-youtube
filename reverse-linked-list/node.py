from manim import *

class Node(VGroup):
    def __init__(self, label, position=ORIGIN, next=None, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.position = position
        self.next = next

        self.circle = Square(side_length=1, color=BLUE, fill_opacity=0.5)
        self.label_text = Text(label, font_size=24).move_to(self.position)

        self.label_text.move_to(self.circle.get_center())

        self.add(self.circle, self.label_text)
        self.move_to(self.position)

    def drawArrow(self):
        if self.next:
            start = self.circle.get_center() + RIGHT * 0.2
            end = self.next.circle.get_left() + RIGHT * 0.2

            arrow = Arrow(start=start, end=end, color=WHITE, stroke_width=0.5)
            arrow.tip_length = 0.1  # Smaller arrow tip
            arrow.scale(0.5)  # Shorten the arrow
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
            node = Node(label=name, position=position)
            nodes.append(node)

            if i > 0:
                nodes[i-1].next = node

        arrows = [node.drawArrow() for node in nodes if node.next]

        # Create and display the nodes and arrows
        self.play(*[Create(node) for node in nodes])
        if arrows:
            self.play(*[Create(arrow) for arrow in arrows if arrow])

        # Display the title
        text = Text(text="Reverse a singly linked list", font_size=36)
        text.to_edge(UP)
        self.play(Write(text))

        self.wait(1)

        # Create a group for nodes and arrows
        all_elements = VGroup(*nodes, *arrows)

        # Push the whole group up
        self.play(all_elements.animate.shift(UP * 2))
        self.wait(1)

        # Duplicate each node and place on top of the original
        reversed_nodes = []
        for node in nodes:
            duplicate = Node(label=node.label, position=node.position)
            # Stack directly above the original node
            duplicate.move_to(node.position + UP * 2)
            reversed_nodes.append(duplicate)
            self.add(duplicate)

        # Calculate the center position for reversed nodes
        reversed_total_width = spacing * (len(nodes_names) - 1)
        reversed_start_position = ORIGIN - RIGHT * reversed_total_width / 2

        # Animate moving the reversed nodes from the top to the center in reverse order
        for i, node in enumerate(reversed(reversed_nodes)):
            target_position = reversed_start_position + RIGHT * i * spacing

            # Highlight the original node being duplicated
            original_node = nodes[len(nodes) - 1 - i]
            self.play(
                original_node.circle.animate.set_color(YELLOW),  # Highlight the original node
                node.animate.move_to(target_position)  # Move the duplicate to the center
            )

            # Reset the original node color after the move
            self.play(original_node.circle.animate.set_color(BLUE))

        # Fix the next pointers for reversed nodes
        for i in range(len(reversed_nodes) - 1):
            reversed_nodes[i].next = reversed_nodes[i + 1]

        # Draw arrows for the newly centered reversed nodes
        reversed_arrows = [node.drawArrow() for node in reversed_nodes if node.next]
        if reversed_arrows:
            self.play(*[Create(arrow) for arrow in reversed_arrows if arrow])

        self.wait(1)
 