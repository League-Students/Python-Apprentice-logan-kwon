import turtle

tina = turtle.Turtle()

screen = turtle.Screen()
screen.setup(500,500)

cam_colors = ["white", "blue", "red", "black", "green"]

def open_cam_1():
    print("CAM 1 OPENED")
    screen.bgcolor(cam_colors[0])
def open_cam_2():
    print("CAM 1 OPENED")
    screen.bgcolor(cam_colors[1])
def open_cam_3():
    print("CAM 1 OPENED")
    screen.bgcolor(cam_colors[2])
def open_cam_1():
    print("CAM 1 OPENED")
    screen.bgcolor(cam_colors[3])
def open_cam_1():
    print("CAM 1 OPENED")
    screen.bgcolor(cam_colors[4])


screen.listen()
screen.onkey(open_cam_1, "1")
screen.onkey(open_cam_2, "2")
screen.onkey(open_cam_3, "3")
screen.onkey(open_cam_4, "4")
screen.onkey(open_cam_5, "5")
turtle.exitonclick()