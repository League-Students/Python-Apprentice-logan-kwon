import turtle

tina = turtle.Turtle()
tina.shape("turtle")3
screen = turtle.Screen()
screen.setup(600,600)

cam_colors = ["white", "blue", "red", "black", "green"]

def open_cam_1():
    print("CAM 1 OPENED")
    screen.bgcolor(cam_colors[0])
def open_cam_2():
    print("CAM 2 OPENED")
    screen.bgcolor(cam_colors[1])
def open_cam_3():
    print("CAM 3 OPENED")
    screen.bgcolor(cam_colors[2])
def open_cam_4():
    print("CAM 4 OPENED")
    screen.bgcolor(cam_colors[3])
def open_cam_5():
    print("CAM 5 OPENED")
    screen.bgcolor(cam_colors[4])
def exit_cam():
    print("CAM EXITED")
    screen.bgcolor("yellow")
screen.listen()
screen.onkey(open_cam_1, "1")
screen.onkey(open_cam_2, "2")
screen.onkey(open_cam_3, "3")
screen.onkey(open_cam_4, "4")
screen.onkey(open_cam_5, "5")
screen.onkey(exit_cam, "0")
turtle.exitonclick()
