from Bullet import Bullet


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
        self.bullet_height = 30
        self.bullet_width = 10
        self.bullet_color = (0, 195, 255)
        self.bullet_velocity = 10
        self.is_alive = True

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

    def create_bullet(self):
        x = self.x + (self.width - self.bullet_width) // 2
        y = self.y + self.direction * self.bullet_height
        velocity = -self.direction * self.bullet_velocity
        if self.direction == 1:  # down
            y += self.height - self.bullet_height
        bullet = Bullet(x, y, self.bullet_height, self.bullet_width, velocity, self.bullet_color)
        self.bullets.append(bullet)

    def bullets_move(self):
        tmp = []
        for bullet in self.bullets:
            bullet.body.y -= bullet.velocity
            if bullet.body.y >= -bullet.body.height:
                tmp.append(bullet)
        self.bullets = tmp[:]

    def change_bullet_color(self, color):
        self.bullet_color = color
