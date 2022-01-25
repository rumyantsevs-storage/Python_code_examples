# -*- coding: utf-8 -*-

import pygame
import random

SVGA = (800, 600)
FHD = (1920, 1080)
RESOLUTION = FHD

WIDTH = 800
HEIGHT = 600
FPS = 60

PIXEL_SIDE = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("White Noize")
clock = pygame.time.Clock()


class Quad(pygame.sprite.Sprite):

    def __init__(self, pos_x=0, pos_y=0, PIXEL_SIDE_x=100, PIXEL_SIDE_y=100, color=WHITE):
        pygame.sprite.Sprite.__init__(self)
        self.PIXEL_SIDE_x = PIXEL_SIDE_x
        self.PIXEL_SIDE_y = PIXEL_SIDE_y
        self.image = pygame.Surface((self.PIXEL_SIDE_x, self.PIXEL_SIDE_y))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x + PIXEL_SIDE_x // 2, pos_y + PIXEL_SIDE_y // 2)

    def change_color(self):
        new_color = random.randint(0, 255)
        self.color = (new_color, new_color, new_color)
        self.image.fill(self.color)

    def update(self):
        self.change_color()


all_sprites = pygame.sprite.Group()

for j in range(0, RESOLUTION[1] + 1, PIXEL_SIDE):
    for i in range(0, RESOLUTION[0] + 1, PIXEL_SIDE):
        quad = Quad(pos_x=i, pos_y=j)
        all_sprites.add(quad)

pygame.mouse.set_visible(False)
mouse_moves = 0
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_moves += 1
            if mouse_moves > 3:
                running = False

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
