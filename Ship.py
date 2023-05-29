import pygame

from Bullet import Bullet
from enum import Enum






class BulletType(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    THREE_WIDE = 4


class Ship:
    def __init__(self, x, y, height, width, direction, color, world):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.direction = direction  # -1 - up, 1 - down
        self.x_velocity = 5
        self.y_velocity = 5
        self.color = color
        self.bullets = []
        self.world = world
        self.bullet_height = 20
        self.bullet_width = 15
        self.bullet_color = (255, 0, 0)
        self.bullet_velocity = 3
        self.is_alive = True
        self.health_points = 3
        self.points = 0
        self.award = 100
        self.bullet_ratio = 80
        self.bullet_type = BulletType.ONE

    def move_left(self):
        self.x -= self.x_velocity
        self.x = max(self.x_velocity, self.x)

    def move_right(self):
        self.x += self.x_velocity
        self.x = min(self.world.width - self.width - 5, self.x)

    def move_up(self):
        self.y -= self.x_velocity
        self.y = max(self.y_velocity, self.y)

    def move_down(self):
        self.y += self.x_velocity
        self.y = min(self.world.height - self.height - 5, self.y)

    def upgrade_bullet_type(self):
        if self.bullet_type == BulletType.ONE:
            self.bullet_type = BulletType.TWO
        elif self.bullet_type == BulletType.TWO:
            self.bullet_type = BulletType.THREE
        elif self.bullet_type == BulletType.THREE:
            self.bullet_type = BulletType.THREE_WIDE

    def create_bullet(self):

        y = self.y + self.direction * self.bullet_height
        x = self.x + (self.width - self.bullet_width) // 2
        velocity = -self.direction * self.bullet_velocity

        if self.bullet_type == BulletType.ONE:

            if self.direction == 1:  # down
                y += self.height - self.bullet_height
            bullet = Bullet(x, y, self.bullet_height, self.bullet_width, 0, velocity, self.bullet_color)
            self.bullets.append(bullet)

        elif self.bullet_type == BulletType.TWO:

            x1 = x - self.bullet_width
            x2 = x + self.bullet_width

            if self.direction == 1:  # down
                y += self.height - self.bullet_height
            bullet = Bullet(x1, y, self.bullet_height, self.bullet_width, 0, velocity, self.bullet_color)
            self.bullets.append(bullet)
            bullet = Bullet(x2, y, self.bullet_height, self.bullet_width, 0, velocity, self.bullet_color)
            self.bullets.append(bullet)

        elif self.bullet_type == BulletType.THREE:

            x1 = x - self.bullet_width - 8
            x2 = x + self.bullet_width + 8

            if self.direction == 1:  # down
                y += self.height - self.bullet_height
            bullet = Bullet(x1, y, self.bullet_height, self.bullet_width, 0, velocity, self.bullet_color)
            self.bullets.append(bullet)
            bullet = Bullet(x2, y, self.bullet_height, self.bullet_width, 0, velocity, self.bullet_color)
            self.bullets.append(bullet)
            bullet = Bullet(x, y, self.bullet_height, self.bullet_width, 0, velocity, self.bullet_color)
            self.bullets.append(bullet)

        elif self.bullet_type == BulletType.THREE_WIDE:

            x1 = x - self.bullet_width - 8
            x2 = x + self.bullet_width + 8

            if self.direction == 1:  # down
                y += self.height - self.bullet_height
            bullet = Bullet(x1, y, self.bullet_height, self.bullet_width, -3, velocity, self.bullet_color)
            self.bullets.append(bullet)
            bullet = Bullet(x2, y, self.bullet_height, self.bullet_width, 3, velocity, self.bullet_color)
            self.bullets.append(bullet)
            bullet = Bullet(x, y, self.bullet_height, self.bullet_width, 0, velocity, self.bullet_color)
            self.bullets.append(bullet)



    def bullets_move(self):
        tmp = []
        for bullet in self.bullets:
            bullet.body.y -= bullet.velocity_y
            bullet.body.x += bullet.velocity_x
            if bullet.body.y <= -bullet.body.height or bullet.body.y > self.world.height:
                pass
            elif bullet.body.x <= -bullet.body.width or bullet.body.x > self.world.width:
                pass
            else:
                tmp.append(bullet)
        self.bullets = tmp

    def change_bullet_color(self, color):
        self.bullet_color = color
