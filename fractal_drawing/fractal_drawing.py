# -*- coding: utf-8 -*-

import simple_draw as sd
import pygame

RESOLUTION = (800, 600)

TRUNK_LENGTH = 150
BRANCH_LENGTH = TRUNK_LENGTH * 0.75
INITIAL_ANGLE = 90

sd.caption = 'Fractal Drawing'
sd.resolution = RESOLUTION

pygame.init()


def draw_branches(start_point, angle, length):
    vector = sd.get_vector(start_point=start_point, angle=angle + 30, length=length)
    vector.draw()
    end_point1 = vector.end_point
    vector = sd.get_vector(start_point=start_point, angle=angle - 30, length=length)
    vector.draw()
    end_point2 = vector.end_point
    # элемент хаоса length *= (0.75 - 0.075 + sd.randint(0, 15) * 0.01)
    length *= 0.75
    if length < 3:
        return
    else:
        draw_branches(start_point=end_point1, angle=angle + 30, length=length)
        draw_branches(start_point=end_point2, angle=angle - 30, length=length)


trunk_start_point = sd.get_point(sd.resolution[0] // 2, 0)
trunk_vector = sd.get_vector(start_point=trunk_start_point, angle=INITIAL_ANGLE, length=TRUNK_LENGTH)

trunk_vector.draw()
trunk_end_point = trunk_vector.end_point
draw_branches(start_point=trunk_end_point, angle=INITIAL_ANGLE, length=BRANCH_LENGTH)

sd.pause()
