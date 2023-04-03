import pygame
from enum import Enum

class GiftType(Enum):
    SPEED = 1
    BULLET_SPEED = 2
    BULLET_COLOR = 3
    BULLET_RATIO = 4
    WEAPON_UPGRADE = 5


class Gift:
    def __init__(self, x, y, height, width, velocity, value, gift_type, world):
        self.body = pygame.Rect(x, y, width, height)
        self.velocity = velocity
        self.value = value
        self.gift_type = GiftType(gift_type)
        self.world = world
        self.color = (255, 190, 20)

    def move(self):
        self.body.y += self.velocity
        if self.body.y > self.world.height:
            return 0
        return 1
