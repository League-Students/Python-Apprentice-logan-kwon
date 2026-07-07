"""
# 20_Crazy_Spiral.py

Make your own crazy spiral with a pattern like
in 10_Flaming_Ninja_Star.py, but use what you've learned about loops

uid: zfzMbyH7
name: Crazy Spiral
"""

... # Copy code to make a turtle and set up the window
import turtle
t = turtle.Turtle() # Create a turtle named t
t.pendown()
# 1) Complete make_a_shape() to make the turtle move in some pattern. 
# For instance, you can make it go left 30 degrees, then forward 50 pixels, 
# then right 60 degrees, then forward 100 pixels. Make any shape you like.

def make_a_shape(t):    
    t.forward(30)
    t.left(60)
    t.forward(10)
    t.right(20)
    t.forward(2000)
# 2) Call make_a_shape() in a loop to make the turtle draw a spiral.
# For instance, you can call make_a_shape() 100 times to make a spiral with 100 shapes.
# The second ... in the for loop should be the number of shapes you want to make,
# for example 100, or a list of numbers.

num_shapes = 30

for i in range(100):
    make_a_shape(t)
    t.right(360/num_shapes)

turtle.exitonclick()