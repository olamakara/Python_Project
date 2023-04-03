import pygame
from enum import Enum


class GiftType(Enum):
    SPEED = 1
    BULLET_SPEED = 2
    BULLET_COLOR = 3
    WEAPON_UPGRADE = 4


class Gift:
    def __init__(self, x, y, height, width, velocity, value, gift_type):
        self.body = pygame.Rect(x, y, width, height)
        self.velocity = velocity
        self.value = value
        self.gift_type = GiftType(gift_type)
