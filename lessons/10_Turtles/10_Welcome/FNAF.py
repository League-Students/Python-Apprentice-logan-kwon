import turtle
import time

tina = turtle.Turtle()
tina.shape("turtle")
tina_path = [1,2,4,5]
tina_progress = 0
cam_num = 0

screen = turtle.Screen()
screen.setup(600,600)

def move_tina():
    global tina_progress
    tina_progress += 1
    show_animatronics()
    screen.ontimer(move_tina,2000)
    

cam_colors = ["white", "blue", "red", "gray", "green"]

def show_animatronics():
    global cam_num
    if(cam_num == tina_path[tina_progress]):
        tina.showturtle()
    else:
        tina.hideturtle()


def open_cam_1():
    global cam_num
    cam_num = 1
    print("CAM 1 OPENED")
    screen.bgcolor(cam_colors[0])
    show_animatronics()
def open_cam_2():
    global cam_num
    cam_num = 2
    print("CAM 2 OPENED")
    screen.bgcolor(cam_colors[1])
    show_animatronics()
def open_cam_3():
    global cam_num
    cam_num = 3
    print("CAM 3 OPENED")
    screen.bgcolor(cam_colors[2])
    show_animatronics()
def open_cam_4():
    global cam_num
    cam_num = 4
    print("CAM 4 OPENED")
    screen.bgcolor(cam_colors[3])
    show_animatronics()
def open_cam_5():
    global cam_num
    cam_num = 5
    print("CAM 5 OPENED")
    screen.bgcolor(cam_colors[4])
    show_animatronics()
def exit_cam():
    print("CAM EXITED")
    screen.bgcolor("yellow")
    show_animatronics()

exit_cam()

screen.listen()
screen.onkey(open_cam_1, "1")
screen.onkey(open_cam_2, "2")
screen.onkey(open_cam_3, "3")
screen.onkey(open_cam_4, "4")
screen.onkey(open_cam_5, "5")
screen.onkey(exit_cam, "0")

screen.ontimer(move_tina, 2000)

turtle.exitonclick()
