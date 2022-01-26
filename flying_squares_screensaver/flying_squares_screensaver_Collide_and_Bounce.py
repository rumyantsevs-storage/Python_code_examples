# -*- coding: utf-8 -*-

import pygame
import random
from math import fabs

SVGA = (800, 600)
FHD = (1920, 1080)
RESOLUTION = FHD

FPS = 91

OBJ_SIDE = 300
OBJ_COUNT = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)


def color(color_id=0):
    colors = [WHITE, RED, GREEN, BLUE, YELLOW, PINK]
    return colors[color_id]


pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Flying Squares (Collide and Bounce)")
clock = pygame.time.Clock()


class Square(pygame.sprite.Sprite):
    id = -1
    collided1 = collided2 = None

    def __init__(self, pos_x=RESOLUTION[0] / 2, pos_y=RESOLUTION[1] / 2, side_x=0.0, side_y=0.0, angle=0.0,
                 color=WHITE):
        pygame.sprite.Sprite.__init__(self)
        Square.id += 1
        self.id = Square.id
        self.side_x = side_x
        self.side_y = side_y
        self.image = pygame.Surface((self.side_x, self.side_y))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.angle = angle
        self.speed_x = self.speed_y = 0
        self.max_speed = 10.0
        self.ready_to_collide = True

    def change_color(self):
        new_color = color(random.randint(0, 3))
        while self.color == new_color:
            new_color = color(random.randint(0, 3))
        self.color = new_color
        self.image.fill(self.color)

    def collide_with_object(self, side_of_collide=None):
        if side_of_collide == 'Top':
            self.angle = 180.0 - self.angle
            self.change_color()
            self.ready_to_collide = False
        elif side_of_collide == 'Bottom':
            self.angle = 180.0 - self.angle
            self.change_color()
            self.ready_to_collide = False
        if side_of_collide == 'Right':
            self.angle = 180.0 - self.angle + 180.0
            self.change_color()
            self.ready_to_collide = False
        elif side_of_collide == 'Left':
            self.angle = 180.0 - self.angle + 180.0
            self.change_color()
            self.ready_to_collide = False

    def update(self):
        if self.angle < 0:
            self.angle = 360.0 + self.angle

        if self.angle >= 360.0:
            self.angle -= 360.0

        if self.angle <= 90.0:
            self.speed_x = self.max_speed - 0.111111 * self.angle
            self.speed_y = 0.111111 * self.angle * -1.0
        elif self.angle <= 180.0:
            self.speed_x = 0.111111 * (self.angle - 90.0) * -1.0
            self.speed_y = (self.max_speed - 0.111111 * (self.angle - 90.0)) * -1.0
        elif self.angle <= 270.0:
            self.speed_x = (self.max_speed - 0.111111 * (self.angle - 180.0)) * -1.0
            self.speed_y = 0.111111 * (self.angle - 180.0)
        elif self.angle <= 360.0:
            self.speed_x = 0.111111 * (self.angle - 270.0)
            self.speed_y = self.max_speed - 0.111111 * (self.angle - 270.0)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # print(self.speed_x, self.speed_y)
        # print(self.rect.x)

        if self.rect.x < 0.0:
            self.angle = 180.0 - self.angle
            self.change_color()
            self.ready_to_collide = True
        elif self.rect.x > (RESOLUTION[0] - self.side_x):
            self.angle = 180.0 - self.angle
            self.change_color()
            self.ready_to_collide = True

        if self.rect.y < 0.0:
            self.angle = 180.0 - self.angle + 180.0
            self.change_color()
            self.ready_to_collide = True
        elif self.rect.y > (RESOLUTION[1] - self.side_y):
            self.angle = 180.0 - self.angle + 180.0
            self.change_color()
            self.ready_to_collide = True

        if (self.ready_to_collide == True) and (Square.collided1 == self.id):
            self.collide_with_object()


all_sprites = pygame.sprite.Group()

# start_angles = [25.0, 30.0, 35.0, 40.0, 45.0, 50.0]

for obj in range(OBJ_COUNT):
    square = Square(pos_x=random.randint(OBJ_SIDE, RESOLUTION[0] - OBJ_SIDE - 1),
                    pos_y=random.randint(OBJ_SIDE, RESOLUTION[1] - OBJ_SIDE - 1), side_x=OBJ_SIDE, side_y=OBJ_SIDE,
                    angle=random.randrange(25, 55, 5), color=color(random.randint(0, 3)))
    all_sprites.add(square)

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
    if len(all_sprites.sprites()) > 1:
        j = 0
        for another in all_sprites.sprites():
            i = 0
            for current in all_sprites.sprites():
                if (current.id != another.id) and current.rect.colliderect(another):
                    Square.collided1 = current.id
                    Square.collided2 = another.id
                    if (fabs(current.rect.y - another.rect.y) < OBJ_SIDE) and (current.rect.x > another.rect.x):
                        current.collide_with_object(side_of_collide='Bottom')
                        # another.collide_with_object(side_of_collide='Top')
                    elif (fabs(current.rect.y - another.rect.y) < OBJ_SIDE) and (current.rect.x < another.rect.x):
                        current.collide_with_object(side_of_collide='Top')
                        # another.collide_with_object(side_of_collide='Bottom')
                    elif (fabs(current.rect.x - another.rect.x) < OBJ_SIDE) and (current.rect.y > another.rect.y):
                        current.collide_with_object(side_of_collide='Right')
                        # another.collide_with_object(side_of_collide='Left')
                    elif (fabs(current.rect.x - another.rect.x) < OBJ_SIDE) and (current.rect.y < another.rect.y):
                        current.collide_with_object(side_of_collide='Left')
                        # another.collide_with_object(side_of_collide='Right')
                    # print('collided', current.id, another.id)
                else:
                    pass  # print('no collide')
                i += 1
            j += 1

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
