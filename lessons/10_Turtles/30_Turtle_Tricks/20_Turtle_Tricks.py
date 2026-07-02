
import turtle                           # Tell Python we want to work with the turtle
turtle.setup(600, 600, 0, 0)            # Set the size of the window
tina = turtle.Turtle()                  # Create a turtle named tina

... # Your code here
def make_side(x=0,y=0):
    tina.left(36)
    tina.forward(50)
make_side
tina.pencolor("blue")
make_side
tina.pencolor("green")
make_side
tina.pencolor("purple")
make_side
tina.pencolor("yellow")
make_side
turtle.exitonclick()                    # Close the window when we click on it