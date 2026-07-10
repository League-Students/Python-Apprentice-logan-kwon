import turtle

tina = turtle.Turtle()

screen = turtle.Screen()
screen.setup(500,500)

cam_colors = ["red", "black", "green", "white", "blue"]

def open_cam_1():
    print("CAM 1 OPENED")



screen.listen()
screen.onkey(open_cam_1, "1")

turtle.exitonclick()