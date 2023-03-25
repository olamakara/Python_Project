import pygame


class Bullet:
    def __init__(self, x, y, height, width, velocity, color):
        self.velocity = velocity
        self.color = color
        self.body = pygame.Rect(x, y, width, height)  # body.x/body.y
