from manim import *

class PointerTip(Scene):
    def construct(self, arrowDirection):
        arrowTip = ArrowTip()

        cirlce=  Circle()
        
        self.add(arrowTip)