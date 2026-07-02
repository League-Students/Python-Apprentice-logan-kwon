import turtle
tina = turtle.Turtle()                          # Tell Python we want to work 
turtle.setup(600, 600, 0, 0)
tina.pendown()            # Set the size of the window
tina = turtle.Turtle()                  # Create a turtle named tina
def make_side(x=0, y=0):
    tina.left(36)
    tina.forward(100)
make_side
tina.pencolor("blue")
make_side
tina.pencolor("green")
make_side
tina.pencolor("purple")
make_side
tina.pencolor("yellow")

turtle.exitonclick()                    # Close the window when we click on it