import turtle
turtle.setup(600, 600, 0, 0)            # Set the size of the window
tina = turtle.Turtle() 
tina.goto(0,0)
radius=40
tina.begin_fill()
tina.circle(radius, steps=30)
tina.end_fill()
tina.penup()
tina.goto(50,50)
tina.pendown()
tina.begin_fill()
tina.circle(radius,steps=20)
tina.end_fill()

turtle.exitonclick()                    # Close the window when we click on it

# Save your progress by checking in your code.