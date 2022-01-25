# -*- coding: utf-8 -*-

import simple_draw as sd
from random import random, randint
import pygame

WINDOW = (1600, 900)
FHD = (1920, 1080)
RESOLUTION = FHD

NUMBER_OF_SNOWFLAKES = 20

sd.resolution = RESOLUTION
sd.background_color = (0, 0, 0)

pygame.init()
pygame.mouse.set_visible(False)


class Snowflake:
    counter = -1

    def __init__(self, x, y, length, color, factor_a, factor_b, factor_c, speed, wind):
        self.x = x
        self.y = y
        self.past_x = self.past_y = None
        self.length = length
        self.color = color
        self.factor_a = factor_a
        self.factor_b = factor_b
        self.factor_c = factor_c
        self.speed = speed
        self.wind = wind
        Snowflake.counter += 1
        self.id = Snowflake.counter  # print('Снежинка № {} создана'.format(self.id))

    def draw(self):
        self.past_x, self.past_y = self.x, self.y
        center = sd.Point(self.past_x, self.past_y)
        sd.snowflake(center=center, length=self.length, color=sd.background_color, factor_a=self.factor_a,
                     factor_b=self.factor_b, factor_c=self.factor_c)
        self.x *= self.wind
        self.y -= self.speed
        center = sd.Point(self.x, self.y)
        sd.snowflake(center=center, length=self.length, color=self.color, factor_a=self.factor_a,
                     factor_b=self.factor_b, factor_c=self.factor_c)

    def __del__(self):
        pass  # print('Снежинка № {} растаяла'.format(self.id))


snowfall = []


def make_snowflake():
    white_bright = randint(242, 254)
    snowflake = Snowflake(x=randint(-120, sd.resolution[0] + 20), y=sd.resolution[1] + 70 + randint(-50, 720),
                          length=randint(30, 95), color=(white_bright, white_bright, white_bright), factor_a=random(),
                          factor_b=random(), factor_c=randint(1, 179), speed=randint(4, 12),
                          wind=float('1.00' + str(randint(1, 3))))
    snowfall.append(snowflake)


for _ in range(NUMBER_OF_SNOWFLAKES):
    make_snowflake()

mouse_moves = 0
running = True
while running:
    i = 0
    while i < NUMBER_OF_SNOWFLAKES:
        snowfall[i].draw()
        if snowfall[i].y < -170:
            snowfall.pop(i)
            make_snowflake()
        i += 1
    # print('Длина списка снежинок: {}'.format(len(snowfall)))
    sd.sleep(0.005)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_moves += 1
            if mouse_moves > 3:
                running = False

pygame.quit()
