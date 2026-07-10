import turtle

tina = turtle.Turtle()

screen = turtle.Screen()
screen.setup(500,500)

cam_colors = ["red", "black", "green", "white", "blue"]

def open_cam_1():
    print("cam 1 open11")



screen.listen()
screen.onkey(open_cam_1, "1")

turtle.exitonclick()