from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
#from manim_voiceover.services.azure import AzureService

def get_positions(vgroup):
    return [obj.get_center() for obj in vgroup]

def get_bottom_positions(vgroup):
     return [obj.get_bottom() for obj in vgroup]

def reverse_node_animation(scene, nodeGroup):
        #scene.play(*[obj. animate.shift(UP*2.5) for obj in scene.mobjects]) # This is important, it shifts all objects from one place to another.
        
        reverseGroup = nodeGroup.copy()
        # self.add(reverseGroup)
        
       # reverseGroup = VGroup(*reversed(reverseGroup)).arrange(buff=1)

        center = ORIGIN

        positions =  get_positions(nodeGroup) #[node.get_center() for node in nodeGroup]  # get positions of all elements.

        move_to_positions = [position + DOWN * 3.5 for position in positions]


        point = NodePointer(start=positions[0]+DOWN*2, end = positions[0]+DOWN*0.5, pointerName="Temp")
        # point = ArrowTip(start=positions[0]+DOWN*2, end = positions[0]+DOWN*0.5, pointerName="Temp")
        text = Text(text="Temp", font_size=24)
        text.set_opacity(0.5)
        text.move_to(positions[0]+LEFT*2)
        scene.add(text)

        scene.play(text.animate.move_to(positions[0]+DOWN*2).set_fill(opacity=1.0))

        scene.remove(text)
        scene.add(point)


        bottomPositions = get_bottom_positions(nodeGroup)

        with scene.voiceover(text = "Now we can iterate through all nodes using a loop to get to the last node") as tracker:
             for p in positions: 
                  scene.play(point.animate.move_to(p+DOWN*1.2))


        with scene.voiceover(text="The most obvious and easiest way to do this is to just create a separate pointer like this and keep appending five, and then four, and then 3 and so on") as tracker : 
            #scene.wait(tracker.duration)
            for node, position, pointerPosition in zip(reversed(reverseGroup), move_to_positions, reversed(positions)): 
                    scene.play(point.animate.move_to(pointerPosition+DOWN*1.2 ))
                    square = Square().surround(node)
                    scene.play(Create(square))
                    scene.play(node.animate.move_to(position), run_time=0.5, wait=True)  #run_time is important because that's what makes it feel like animating
                    scene.remove(square)      



        #self.play(reverseGroup.animate.move_to(ORIGIN ))
  
        with scene.voiceover(text = "This is also a naive and intuitive approach because that is how you can reverse a linkedList as well") as tracker:
                scene.wait(tracker.duration)
    

#keeping scale between 0 to 1.
class Node(VMobject):
    def __init__(self, side_length=2, nodeColor=BLUE, scale=0.1, nodeOpacity=0.5, nodeData = "1", **kwargs):
        super().__init__(**kwargs)
        self.side_length = side_length
        self.nodeColor = nodeColor
        self.nodeOpacity = nodeOpacity
        self.nodeData = nodeData
        self.scaleFactor = scale
        self.draw_node()
        
    def draw_node(self):
        self.squareNode = Square(side_length= self.side_length)
        self.squareNode.set_fill(color= self.nodeColor, opacity = self.nodeOpacity)
        self.add(self.squareNode) 
        nodeData = Text(self.nodeData, color=WHITE,font_size=20*self.side_length)
        nodePointer = Text("next*", color=WHITE,font_size=15*self.side_length)

        nodeData.move_to(self.squareNode.get_center()+UP*(0.2/self.side_length))  #moving up a little in the box
        nodePointer.move_to(self.squareNode.get_center()+DOWN*(0.2/self.side_length))  #moving up a little in the box
        line = Line(start=self.squareNode.get_left(), end=self.squareNode.get_right())
        self.add(nodeData, nodePointer, line)
        # arrow = Arrow(stroke_width=50,start=self.squareNode.get_right()+DOWN*0.2, end=self.squareNode.get_left(), color=BLUE, buff=0)
        # self.add(arrow)

# pointerDirection= "left | right | center" - default to center
class NodePointer(VMobject):
        def __init__(self, start=ORIGIN, end=ORIGIN, color=BLUE, pointerDirection="center", pointerNameSize=24, pointerName = "head", **kwargs):
            super().__init__(**kwargs)
            self.start = start
            self.end = end
            self.color = color
            self.direction = pointerDirection
            self.pointerName = pointerName
            self.nameSize = pointerNameSize
            self.pointer = Text(text=self.pointerName, font_size=self.nameSize)
            self.pointer.move_to(self.start)
            if self.direction == "center":
                arrow = Arrow(start=self.pointer.get_center(), end=self.end, color=self.color) 
                self.add(self.pointer, arrow)
            elif self.direction == "left":
                arrow = Arrow(start=self.pointer.get_left(), end=self.end, color=self.color) 
                self.add(self.pointer, arrow) 
            else:
                arrow = Arrow(start=self.pointer.get_right(), end=self.end, color=self.color)
                self.add(self.pointer, arrow) 
            

        def getPointerText(self):
             return self.pointer
        

def add_last_node_arrow(scene, arrows, nodeGroup):
        nullText = Text("NULL", font_size=24 )
        nullText.next_to(nodeGroup[-1], nodeGroup[-1].get_center() , buff=0.5)

        nullArrow = Arrow(start=nodeGroup[-1].get_right()+DOWN*0.2, end=nullText.get_left() , color=BLUE, buff=0)
        arrows.add(nullArrow)   #To add the last arrow
        scene.add(arrows)
        return nullText

def getNodeGroup():
    nodeGroup = VGroup(
           Node(side_length=0.9, nodeColor= BLUE, nodeOpacity=0.5, nodeData="1"),
           Node(side_length=0.9, nodeColor= BLUE, nodeOpacity=0.5, nodeData="2"),
           Node(side_length=0.9, nodeColor= BLUE, nodeOpacity=0.5, nodeData="3"),
           Node(side_length=0.9, nodeColor= BLUE, nodeOpacity=0.5, nodeData="4"),
           Node(side_length=0.9, nodeColor= BLUE, nodeOpacity=0.5, nodeData="5"),
       )
    nodeGroup.arrange(buff=1)
    return nodeGroup

class ReverseLinkedList(VoiceoverScene):
    def construct(self):
        
        # self.camera.frame_width = 6
        # self.camera.frame_height= 10

        self.set_speech_service(GTTSService(lang="en", tld="com"))  #, create_subcaption=False)
        #self.set_speech_service(AzureService(voice="en-US-AiralNeural", style="newscast-casual"))

        

        # listGroup = VGroup( node, node2, node3 ,node4, node5).arrange( buff=1)  # To create a group, above way is a diff way
        #self.add(nodeGroup)

        
        nodeGroup = VGroup(
           Node(side_length=1,scale=0.2, nodeColor= BLUE, nodeOpacity=0.5, nodeData="1"),
           Node(side_length=1,scale=0.2, nodeColor= BLUE, nodeOpacity=0.5, nodeData="2"),
           Node(side_length=1,scale=0.2, nodeColor= BLUE, nodeOpacity=0.5, nodeData="3"),
           Node(side_length=1,scale=0.2, nodeColor= BLUE, nodeOpacity=0.5, nodeData="4"),
           Node(side_length=1,scale=0.2, nodeColor= BLUE, nodeOpacity=0.5, nodeData="5"),
       )
        nodeGroup.arrange(buff=1)

        arrows = VGroup()  
        for i in range(len(nodeGroup) - 1):
            arrow = Arrow(stroke_width=35,start=nodeGroup[i].get_right()+DOWN*0.2, end=nodeGroup[i+1].get_left(), color=BLUE, buff=0)
            arrows.add(arrow)


        for node in nodeGroup:
             self.play(FadeIn(node, run_time=0.4))

        headPointer = NodePointer(start =nodeGroup[0].get_left()+LEFT*1.8, end = nodeGroup[0].get_left(), pointerDirection="right", pointerName= "Head*")

        # headText = Text("Head*", font_size=24)
        # headTextPosition = nodeGroup[0].get_center()+LEFT*1.8
        # headText.move_to(headTextPosition)

        # arrow = Arrow(stroke_width=35, start=headText.get_right(), end=nodeGroup[0].get_left(), color=BLUE)
        # self.add(arrow)
 
        with self.voiceover(text="In this question we need to reverse a singly linked list and we are given a head of that linked list") as tracker: 
            self.play(FadeIn(arrows))
            self.play(FadeIn(headPointer))
            square = Rectangle(color=YELLOW).surround(headPointer.getPointerText())
            self.wait(tracker.duration/10*5)  # 30 seconds / 100
            self.play(Create(square))
            #self.remove(square)
        

        with self.voiceover(text="For example, this represents a singly linked list of node objects from one to five") as tracker: 
            self.wait(tracker.duration)
            #self.play(FadeIn(nodeGroup, run_time=2))
            #self.play(FadeIn(nullptrText))
    


 

        # self.play(*[obj. animate.shift(UP*2.5) for obj in self.mobjects]) # This is important, it shifts all objects from one place to another.



        #reverse_node_animation(self, nodeGroup)
        
        
        reverseGroup =  VGroup(*reversed(nodeGroup))  #.arrange( buff=1) 
        reverseGroup.arrange(buff=1)

 
        with self.voiceover(text="We simply need to reverse this list from five to one like this") as tracker: 
            self.play(ReplacementTransform(nodeGroup, reverseGroup) , run_time=2)
            
       

        reverseGroup = VGroup(*reversed(nodeGroup)).arrange(buff=1)

        with self.voiceover(text = "Let me reverse it back to original linked list") as tracker:
             self.play(ReplacementTransform(reverseGroup, nodeGroup))
             self.wait(tracker.duration)


        nullptrText = add_last_node_arrow(self, arrows, nodeGroup)
        # self.add(nullptrText)
        self.play(*[obj. animate.shift(UP*2.5) for obj in self.mobjects])

        with self.voiceover(text="Now before we start coding the solution, let us think how we can solve this. Let's suppose this is our complete list") as tracker : 
            self.play(FadeIn(nullptrText))
            self.wait(tracker.duration)
            
        
        reverse_node_animation(self, nodeGroup) #need to pass reverse group here

        

        self.wait(1)

        