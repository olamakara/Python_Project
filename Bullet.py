import pygame


class Bullet:
    def __init__(self, x, y, height, width, velocity_x, velocity_y, color):
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.body = pygame.Rect(x, y, width, height)  # body.x/body.y
