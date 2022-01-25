# -*- coding: utf-8 -*-

import pygame
import simple_draw as sd
from random import randint
from pprint import pprint

RESOLUTION_FHD = (1920, 1080)
RESOLUTION_CUSTOM = (1600, 900)

RANDOM_LOW = 0
RANDOM_HIGH = 6
SQUARE_SIDE = 100

sd.resolution = RESOLUTION_FHD

pygame.init()
pygame.mouse.set_visible(False)


def color_number(number=0):
    color_list = [
        # (192, 192, 192),
        # sd.COLOR_DARK_RED,
        # sd.COLOR_YELLOW,
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (255, 0, 255),
    ]

    # i = 0
    # for _ in range(256):
    #     color_list.append((i, i, i))
    #     i += 1

    return color_list[number]


matrix = []
subarray = []
past_subarray = []

past_number = RANDOM_HIGH + 1
for j in range(0, sd.resolution[1] + 1, SQUARE_SIDE):
    index_i = 0
    for i in range(0, sd.resolution[0] + 1, SQUARE_SIDE):
        random_number = randint(RANDOM_LOW, RANDOM_HIGH)
        if past_subarray == []:
            while random_number == past_number:
                random_number = randint(RANDOM_LOW, RANDOM_HIGH)
        else:
            while (random_number == past_number) or (random_number == past_subarray[index_i]):
                    random_number = randint(RANDOM_LOW, RANDOM_HIGH)
        subarray.append(random_number)
        past_number = random_number
        index_i += 1
    matrix.append(subarray)
    past_subarray = subarray
    subarray = []

index_j = 0
for j in range(sd.resolution[1] // SQUARE_SIDE + 1):
    index_i = 0
    for i in range(sd.resolution[0] // SQUARE_SIDE + 1):
        print(matrix[j][i], end=' ')
        sd.square(left_bottom=sd.Point(index_i, index_j), side=SQUARE_SIDE, color=color_number(matrix[j][i]))
        index_i += SQUARE_SIDE
    print()
    index_j += SQUARE_SIDE

mouse_moves = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_moves += 1
            if mouse_moves > 3:
                running = False

pygame.quit()
