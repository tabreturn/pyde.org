from pyp5js import *


def setup():
    createCanvas(640, 360)


def draw():
    background(127)
    noStroke()

    for i in range(0, height, 20):
        fill(129, 206, 15)
        rect(0, i, width, 10)
        fill(255)
        rect(i, 0, 10, height)

