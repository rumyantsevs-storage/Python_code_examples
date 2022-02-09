# -*- coding: utf-8 -*-

import pygame
import random
import math

SVGA = (800, 600)
SXGA = (1024, 768)
FHD = (1920, 1080)
CUSTOM = (1800, 900)
RESOLUTION = FHD

FPS = 91

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
SILVER = (192, 192, 192)

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Milling Screensaver")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

trajectory_way = []


class EccentricityAxis:

    def __init__(self, center_x=0.0, center_y=0.0, angle=0.0, eccentricity_radius=1.0):
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle
        self.eccentricity_radius = eccentricity_radius  # 1.0 = 0.01 [mm] (default)
        self.point_x = 0.0
        self.point_y = 0.0
        self.apply_params()

    def apply_params(self):
        self.point_x = self.center_x + self.eccentricity_radius * math.sin(self.angle * (math.pi / 180.0))
        self.point_y = self.center_y + self.eccentricity_radius * math.cos(self.angle * (math.pi / 180.0))


class Plate:

    def __init__(self, start_x=0.0, start_y=0.0, angle=0.0, color=YELLOW):
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle
        self.color = color
        self.points = ()
        self.apply_params()

    def apply_params(self):
        self.points = ((self.start_x + 100.0 * math.sin(self.angle * (math.pi / 180.0)),
                        self.start_y + 100.0 * math.cos(self.angle * (math.pi / 180.0))),
                       (self.start_x + 300.0 * math.sin(self.angle * (math.pi / 180.0)),
                        self.start_y + 300.0 * math.cos(self.angle * (math.pi / 180.0))),
                       (self.start_x + 280.0 * math.sin((self.angle + 15.0) * (math.pi / 180.0)),
                        self.start_y + 280.0 * math.cos((self.angle + 15.0) * (math.pi / 180.0))),
                       (self.start_x + 145.0 * math.sin((self.angle + 30.0) * (math.pi / 180.0)),
                        self.start_y + 145.0 * math.cos((self.angle + 30.0) * (math.pi / 180.0))))


class Mill:

    def __init__(self, center_x=0.0, center_y=0.0, angle=0.0, nplates=4):
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle
        self.nplates = nplates
        self.segment = 360.0 / self.nplates
        self.plates = []

        for i in range(self.nplates):
            plate = Plate(start_x=self.center_x, start_y=self.center_y, angle=i * self.segment)
            self.plates.append(plate)

    def apply_params(self):
        for i in range(self.nplates):
            self.plates[i].start_x = self.center_x
            self.plates[i].start_y = self.center_y
            self.plates[i].angle = self.angle + i * self.segment
            self.plates[i].apply_params()

    def draw_plates(self, color=YELLOW):
        for plate in self.plates:
            pygame.draw.polygon(screen, color,
                                ((plate.points[0][0], plate.points[0][1]),
                                 (plate.points[1][0], plate.points[1][1]),
                                 (plate.points[2][0], plate.points[2][1]),
                                 (plate.points[3][0], plate.points[3][1])))


# Making main cycle

mouse_moves = 0
running = True
while running:
    # Restore default conditions
    trajectory_way.clear()
    screen.fill(BLACK)
    pygame.draw.rect(screen, SILVER, [[0, 0], [RESOLUTION[0], RESOLUTION[1]]])

    # Cut parameters #######################################

    # Tool moving from the left to the right
    from_left_to_right = True  # = random.choice((True, False))
    # Tool Y position
    tool_point_y = RESOLUTION[1] / 2.0  # random.uniform(200.0, RESOLUTION[1] - 200.0)
    # Plate number in tool
    nplates = 4  # random.choice((2, 3, 4, 6, 8, 22))
    # Tool axis runout
    eccentricity = random.uniform(1.0, 5.0)
    # Tool CW revolutions
    clockwise_rotation = True
    # Tool revolution coefficient
    angle_coeff = 2.0  # random.uniform(1.0, 4.0)
    # Tool speed coefficient
    speed_coeff = 0.15  # random.uniform(1.0, 3.0)

    ########################################################

    # Pre-start conditions

    if from_left_to_right:
        tool_point_x = -400
    else:
        tool_point_x = RESOLUTION[0] + 400
        speed_coeff *= -1.0

    tool_point_x = -100

    if clockwise_rotation:
        angle_coeff *= -1.0

    if (speed_coeff >= 3.0) and (angle_coeff <= -3.0):
        angle_coeff = -3.0
    elif (speed_coeff >= 4.0) and (angle_coeff <= -4.0):
        angle_coeff = -4.0
    elif (speed_coeff >= 5.0) and (angle_coeff <= -5.0):
        angle_coeff = -5.0

    # Creating objects
    axis = EccentricityAxis(center_x=tool_point_x, center_y=tool_point_y, angle=0.0, eccentricity_radius=100.0)
    axis1 = EccentricityAxis(center_x=axis.point_x, center_y=axis.point_y, angle=0.0, eccentricity_radius=eccentricity)
    mill = Mill(center_x=axis1.point_x, center_y=axis1.point_x, angle=0.0, nplates=nplates)

    # Making stage cycle
    stage = True
    while stage:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                stage = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_moves += 1
                if mouse_moves > 10:
                    running = False
                    stage = False

        # screen.fill(BLACK)

        # Drawing

        axis.angle -= angle_coeff * 0.125
        axis.center_x += speed_coeff
        axis.apply_params()

        axis1.angle += angle_coeff
        axis1.center_x = axis.point_x
        axis1.center_y = axis.point_y
        axis1.apply_params()

        mill.draw_plates(BLACK)
        mill.angle += angle_coeff
        mill.center_x = axis1.point_x
        mill.center_y = axis1.point_y
        mill.apply_params()
        mill.draw_plates()

        trajectory_way.append((axis1.point_x, axis1.point_y))

        for point in trajectory_way:
            screen.set_at((round(point[0]), round(point[1])), RED)

        if from_left_to_right:
            if axis.center_x > RESOLUTION[0] + 400:
                stage = False
        else:
            if axis.center_x < -400:
                stage = False

        pygame.display.flip()

pygame.quit()
