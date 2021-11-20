from vpython import *
from vpython.rate_control import rate
import copy
from vpython.vpython import *
from vpython.vpython import vector, mag, canvas

from random import random
from typing import Dict

devMode = False
energyLoosesRate = 0.15
side = 50.0
table_width = 230  # 129
table_height = 5
table_lenght = 130  # 142
thinkness = 5
r = 5
ballMas = 1
balls = []
walls = dict()
coordinates_objects = []
side = side - thinkness * 0.5 - r
maxTime = 100

def set_visible_coordinate_system(is_visible):
    for obj in coordinates_objects:
        obj.visible = is_visible

def initialize_coordinate_system():
    x_box = box(pos=vector(0, 0, 0), size=vector(300, 10, 10), color=color.purple)
    x_label = label(pos=x_box.size / 2, text="X", xoffset=-10,
                    yoffset=-10, space=0,
                    height=16, border=4,
                    font='sans', color=color.white)
    y_box = box(pos=vector(0, 0, 0), size=vector(10, 300, 10), color=color.cyan)
    y_label = label(pos=y_box.size / 2, text="Y", xoffset=-10,
                    yoffset=-10, space=0,
                    height=16, border=4,
                    font='sans', color=color.white)

    z_box = box(pos=vector(0, 0, 0), size=vector(10, 10, 300), color=color.white)
    z_label = label(pos=z_box.size / 2, text="Z", xoffset=-10,
                    yoffset=-10, space=0,
                    height=16, border=4,
                    font='sans', color=color.white)
    coordinates_objects.append(x_label)
    coordinates_objects.append(x_box)
    coordinates_objects.append(y_box)
    coordinates_objects.append(y_label)
    coordinates_objects.append(z_box)
    coordinates_objects.append(z_label)



def initializeWalls(walls_dict: Dict[str, box]):
    wallFloor = box(pos=vector(0, 0, 0), size=vector(table_width, table_height, table_lenght),
                    color=color.green)
    walls_dict["floor"] = wallFloor
    wallLeft = box(pos=vector(((-table_width / 2) - table_height / 2), table_height, 0),
                   size=vector(table_height, table_height, table_lenght), color=color.red)
    walls_dict["left"] = wallLeft
    wallRight = box(pos=vector(((+table_width / 2) + table_height / 2), table_height, 0),
                    size=vector(table_height, table_height, table_lenght), color=color.red)
    walls_dict["right"] = wallRight
    wallBack = box(pos=vector(0, table_height, -table_lenght / 2 - table_height / 2),
                   size=vector(table_width, table_height, table_height), color=color.red)
    walls_dict["back"] = wallBack
    wallFront = box(pos=vector(0, table_height, table_lenght / 2 + table_height / 2),
                    size=vector(table_width, table_height, table_height), color=color.red)
    walls_dict["front"] = wallFront


def devPrint(s):
    if devMode:
        print(s)


def initializeBalls(balls):
    devPrint("work in begin:  initializeBalls")
    retainLenght = 50
    balls.append(sphere(color=color.green, radius=r, make_trail=True, retain=retainLenght))
    balls.append(sphere(color=color.yellow, radius=r, make_trail=True, retain=retainLenght))
    balls.append(sphere(color=color.purple, radius=r, make_trail=True, retain=retainLenght))
    balls.append(sphere(color=color.black, radius=r, make_trail=True, retain=retainLenght))
    balls.append(sphere(color=color.white, radius=r, make_trail=True, retain=retainLenght))
    balls.append(sphere(color=color.green, radius=r, make_trail=True, retain=retainLenght))
    balls.append(sphere(color=color.yellow, radius=r, make_trail=True, retain=retainLenght))
    balls.append(sphere(color=color.purple, radius=r, make_trail=True, retain=retainLenght))
    balls.append(sphere(color=color.black, radius=r, make_trail=True, retain=retainLenght))
    initializePos(balls)
    initializeVelocity(balls)
    initializeMass(balls, ballMas)


def initializePos(balls):
    for i in range(len(balls)):
        if not devMode:
            while True:
                x_pos = random() * table_width * .8 - table_width / 2.5
                y_pos = table_height + r / 2
                z_pos = random() * table_lenght * .8 - table_lenght / 2.5
                balls[i].pos = vector(x_pos, y_pos, z_pos)
                isCollision = False
                for j, ball in enumerate(balls):
                    if j == i:
                        continue
                    isCollision = checkForCollisionTwoBalls(balls[i], balls[j])
                if not isCollision:
                    break
        else:
            if len(balls) == 2:
                balls[0].pos = vector(-10, table_height + r / 2, 0)
                balls[1].pos = vector(10, table_height + r / 2, 0)
            else:
                raise Exception("Only 2 balls supported in devMode")


#
#
def moveBalls(balls, g, dt):
    for ball in balls:
        ball.pos = ball.pos + (ball.v / ball.mass) * dt
        # ball.v.y = ball.v.y + g * dt


#
#
def handleCollisionWithWalls(balls, table_lenght, table_width):
    for ball in balls:
        border_x = table_width / 2 - r
        border_z = table_lenght / 2 - r
        if not (border_x > ball.pos.x > -border_x):
            ball.v.x = -ball.v.x
            handleTeleportX(ball, border_x)
            ball.v = ball.v * (1 - energyLoosesRate)

        # if not (side > ball.pos.y > -side):
        #    ball.v.y = -ball.v.y
        #    handleTeleportY(ball, side)
        #    ball.v = ball.v * (1 - energyLoosesRate)

        if not (border_z > ball.pos.z > -border_z):
            ball.v.z = -ball.v.z
            handleTeleportZ(ball, border_z)
            ball.v = ball.v * (1 - energyLoosesRate)


#

def checkForCollisionTwoBalls(b1, b2):
    return (b1.radius + b2.radius) > mag(b1.pos - b2.pos)


def simpleCollisionHandler(b1, b2):
    b1.v = - b1.v
    b2.v = - b2.v
    pass


#
def initializeVelocity(balls):
    for i in range(len(balls)):
        if not devMode:
            randNumberX = random() * side
            randNumberY = 0
            randNumberZ = random() * side
            balls[i].v = vector(randNumberX, randNumberY, randNumberZ)
        else:
            randNumberX = random() * side
            randNumberY = 0
            randNumberZ = random() * side
            balls[i].v = vector(randNumberX, randNumberY, randNumberZ)


def initializeMass(balls, ballMas):
    for b in balls:
        b.mass = ballMas


def handleTeleportX(ball, side):
    if ball.pos.x > side:
        ball.pos.x = side
        devPrint("teleport to:" + str(side))

    if ball.pos.x < -side:
        ball.pos.x = -side
        devPrint("teleport to:" + str(side))


def handleTeleportY(ball, side):
    if ball.pos.y > side:
        ball.pos.y = side
        devPrint("teleport to:" + str(side))
    if ball.pos.y < -side:
        ball.pos.y = -side
        devPrint("teleport to:" + str(side))


def handleTeleportZ(ball, side):
    if ball.pos.z > side:
        ball.pos.z = side
        devPrint("teleport to:" + str(side))
    if ball.pos.z < -side:
        ball.pos.z = -side
        devPrint("teleport to:" + str(side))


# def devPrintX(ball):
#    print(str(side) + " > " + str(ball.pos.x) + " >" + str(-side))


def calculateNewVelocity(b1, b2):
    massRatio = (2 * b2.mass) / (b1.mass + b2.mass)
    lenghtDiff = (b1.pos - b2.pos)
    velocityDiff = (b1.v - b2.v)
    posDiff = b1.pos - b2.pos
    toSubtrack = ((massRatio / lenghtDiff.mag2) * velocityDiff.dot(posDiff) * posDiff)
    b1.v = b1.v - toSubtrack
    return b1


def handleCollisionBetweenTwoBalls(b1, b2):
    # b1Old = b1.clone()
    b1Old = copy.deepcopy(b1)
    b1 = calculateNewVelocity(b1, b2)
    b2 = calculateNewVelocity(b2, b1Old)
    pass


def handleColisionsWithBalls(balls):
    ballsLen = len(balls)
    for i in range(0, ballsLen - 1):
        for j in range(i + 1, ballsLen):
            if checkForCollisionTwoBalls(balls[i], balls[j]):
                devPrint("ColisionDetect: " + str("[") + str(i) + " : " + str(j) + "]")
                handleCollisionBetweenTwoBalls(balls[i], balls[j])

    pass


#
#
def moveWhile():
    t = 0
    dt = 0.01
    g = -10

    initialize_coordinate_system()
    scene = canvas.get_selected()
    camera_pos = scene.camera.pos
    camera_pos.y = camera_pos.y + 50
    camera_pos.z = camera_pos.z - 20
    scene.camera.pos = camera_pos
    initializeWalls(walls)
    initializeBalls(balls)
    set_visible_coordinate_system(False)
    while True:
        rate(330)
        moveBalls(balls, g, dt)
        handleCollisionWithWalls(balls, table_lenght, table_width)
        handleColisionsWithBalls(balls)
        t = t + dt


# MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN
if __name__ == '__main__':
    moveWhile()

# MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN
