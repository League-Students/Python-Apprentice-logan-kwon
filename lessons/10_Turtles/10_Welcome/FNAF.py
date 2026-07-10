import turtle

tina = turtle.Turtle()

screen = turtle.Screen()
screen.setup(500,500)

cam_colors = ["white", "blue", "red", "black", "blue"]

def open_cam_1():
    print("CAM 1 OPENED")
    screen.bgcolor(cam_colors[0])



screen.listen()
screen.onkey(open_cam_1, "1")

turtle.exitonclick()