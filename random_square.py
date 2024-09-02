from manim import *
import random


# This class constructs a visual for linkedlist in a memory 

class RandomSquares(Scene):
    def construct(self):
        # Define the size of the squares
        square_size = 1
        # Define the area dimensions (in Manim units)
        width = 8 
        height = 6
        
        # Initialize an empty list to hold the squares
        squares = []
        positions = []  # To store the positions of the squares

        def does_overlap(square1, square2):
            # Check if two squares overlap
            return (square1.get_left()[0] < square2.get_right()[0] and
                    square1.get_right()[0] > square2.get_left()[0] and
                    square1.get_bottom()[1] < square2.get_top()[1] and
                    square1.get_top()[1] > square2.get_bottom()[1])

        # Generate squares
        while len(squares) < 4:
            # Generate random position
            x = random.uniform(-width/2 + square_size/2, width/2 - square_size/2)
            y = random.uniform(-height/2 + square_size/2, height/2 - square_size/2)
            
            # Create a square at the random position
            new_square = Square(side_length=square_size).move_to([x, y, 0])
            
            # Check for overlaps with existing squares
            overlap = False
            for existing_square in squares:
                if does_overlap(new_square, existing_square):
                    overlap = True
                    break
            
            # If no overlap, add the new square to the list
            if not overlap:
                squares.append(new_square)
                positions.append(new_square.get_center())

        # Add all squares to the scene
        for square in squares:
            self.add(square)

        # Create arrows connecting the squares
        for i in range(len(positions)):
            start_point = positions[i]
            end_point = positions[(i + 1) % len(positions)]  # Connect to the next square
            
            # Create an arrow from the start to end point
            arrow = Arrow(start=start_point, end=end_point, buff=0.1)
            self.play(Create(arrow))

        self.wait(2)  # Pause to view the result