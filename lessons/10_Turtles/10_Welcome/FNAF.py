import turtle

tina = turtle.Turtle()

screen = turtle.Screen()
screen.setup(500,500)

cam_colors = ["red", "black", "green", "white", "blue"]

screen.listen()
screen.onkey(open_cam_1, "1")
turtle.exitonclick()