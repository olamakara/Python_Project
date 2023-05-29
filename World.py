import os.path
import random
from Gift import Gift
import pygame
from Gift import GiftType
from Ship import BulletType
from Ship import Ship
from enum import Enum

MAX_SPEED = 30
MAX_BULLET_VELOCITY = 25
MIN_BULLET_RATIO = 10
COIN_IMAGE = pygame.image.load(os.path.join('Assets', 'coin.png'))
COIN_IMAGE = pygame.transform.scale(COIN_IMAGE, (40, 40))
pygame.mixer.init()
pygame.mixer.Channel(1).set_volume(0.1)
pygame.mixer.Channel(0).set_volume(0.2)
pygame.mixer.Channel(4).set_volume(0.1)
pygame.mixer.Channel(1).play(pygame.mixer.Sound('Assets/main_sound.mp3'))


# pygame.mixer.music.load('Assets/chicken_sound.mp3')


def collide(rect1, rect2):
    rect1_left = rect1.x
    rect1_top = rect1.y
    rect1_right = rect1.x + rect1.width
    rect1_bottom = rect1.y + rect1.height
    rect2_left = rect2.x
    rect2_top = rect2.y
    rect2_right = rect2.x + rect2.width
    rect2_bottom = rect2.y + rect2.height

    if (rect2_bottom > rect1_top > rect2_top or rect2_bottom > rect1_bottom > rect2_top) and \
            (rect2_left < rect1_left < rect2_right or rect2_left < rect1_right < rect2_right):
        return 1
    return 0


class MapSideType(Enum):
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4


class GamePhase(Enum):
    ENEMIES1 = 1
    ENEMIES2 = 2
    BOSS = 3
    BONUS = 4


class World:
    def __init__(self, height, width, display):
        self.height = height
        self.width = width
        self.enemies = []
        self.gifts = []
        self.boss = None
        self.display = display
        self.gift_width = 20
        self.gifts_height = 20
        self.ship_width = 46
        self.ship_height = 46
        self.gift_height = 20
        self.gift_width = 20
        self.star_width = 2
        self.star_height = 2
        self.star_color = (255, 255, 255)
        self.ship_x_value = (width - self.ship_width) // 2
        self.ship_y_value = height - self.ship_height - 10
        self.background_color = (8, 17, 53)
        self.background_stars = []
        self.ship_color = (255, 255, 255)
        self.enemy_color = (255, 0, 100)
        self.ship = Ship(self.ship_x_value, self.ship_y_value, self.ship_height, self.ship_width, -1, self.ship_color, self)
        self.ship.bullet_type = BulletType.ONE
        self.ship.bullet_height = 10
        self.ship.bullet_width = 10
        self.ship.bullet_ratio = 25
        self.ship.bullet_velocity = 10
        self.enemy_velocity = 3
        self.coins = []
        self.coin_height = 31
        self.coin_width = 31
        self.game_phase = GamePhase.ENEMIES1
        self.enemy_wave = 30
        self.bonus_wave = 50
        self.boss_health_points = 50

    def collisions(self):
        boss_rect = pygame.Rect(self.boss.x, self.boss.y, self.boss.width, self.boss.height)
        ship_rect = pygame.Rect(self.ship.x, self.ship.y, self.ship.width, self.ship.height)
        boss = self.boss
        i = 0
        while i < len(self.enemies):
            enemy = self.enemies[i]
            if enemy.is_alive:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if collide(enemy_rect, ship_rect):
                    # pygame.mixer.music.play()
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Assets/chicken_sound.mp3'))
                    enemy.is_alive = False
                    self.ship.points += enemy.award
                    self.ship.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    self.ship.health_points -= 1
            i += 1

        i, j = 0, 0
        while i < len(self.ship.bullets):
            j = 0
            bullet = self.ship.bullets[i]
            while j < len(self.enemies):
                enemy = self.enemies[j]
                if enemy.is_alive:
                    if collide(bullet.body, pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                        # pygame.mixer.music.play()
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('Assets/chicken_sound.mp3'))
                        del self.ship.bullets[i]
                        enemy.is_alive = False
                        self.ship.points += enemy.award
                        # enemies[j].color = (1, 1, 1)
                        i -= 1
                        j -= 1
                        break
                j += 1
            if (self.game_phase == GamePhase.BOSS):
                if boss.is_alive and collide(bullet.body, boss_rect):
                    self.boss.health_points -= 1
                    print(self.boss.health_points)
                    if self.boss.health_points <= 0:
                        self.boss.is_alive = False
                    del self.ship.bullets[i]
                    i -= 1
            i += 1

        i = 0
        for enemy in self.enemies:
            while i < len(enemy.bullets):
                bullet = enemy.bullets[i]
                # bullet.color = (255, 255, 255)
                if collide(bullet.body, ship_rect):
                    del enemy.bullets[i]
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('Assets/splash_sound.mp3'))
                    self.ship.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    self.ship.health_points -= 1
                    i -= 1
                i += 1
            i = 0
        if (self.game_phase == GamePhase.BOSS):
            if boss.is_alive and collide(boss_rect, ship_rect):
                boss.health_points -= 1
                self.ship.health_points -= 1
                if boss.health_points <= 0:
                    boss.is_alive = False
                if self.ship.health_points <= 0:
                    self.ship.is_alive = False

        i = 0
        while i < len(boss.bullets):
            bullet = boss.bullets[i]
            if collide(bullet.body, ship_rect):
                del boss.bullets[i]
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('Assets/splash_sound.mp3'))
                self.ship.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.ship.health_points -= 1
                i -= 1
            i += 1
        i = 0

        while i < len(self.gifts):
            if collide(self.gifts[i].body, ship_rect):
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('Assets/gift_sound.mp3'))
                self.upgrade_ship(self.gifts[i])
                del self.gifts[i]
                i -= 1
            i += 1

        if (self.game_phase == GamePhase.BONUS):
            i = 0
            while i < len(self.coins):
                if collide(self.coins[i][0], ship_rect):
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('Assets/gift_sound.mp3'))
                    self.ship.points += 100
                    del self.coins[i]
                    i -= 1
                i += 1

    def upgrade_ship(self, gift):
        print(gift.gift_type)
        if gift.gift_type == GiftType.SPEED and self.ship.x_velocity < MAX_SPEED:
            self.ship.x_velocity += gift.value
            self.ship.y_velocity += gift.value

        elif gift.gift_type == GiftType.BULLET_VELOCITY and self.ship.bullet_velocity < MAX_BULLET_VELOCITY:
            self.ship.bullet_velocity += gift.value

        elif gift.gift_type == GiftType.BULLET_COLOR:
            self.ship.bullet_color = gift.value

        elif gift.gift_type == GiftType.BULLET_RATIO and self.ship.bullet_ratio > MIN_BULLET_RATIO:
            self.ship.bullet_ratio -= gift.value

        elif gift.gift_type == GiftType.WEAPON_UPGRADE:
            self.ship.upgrade_bullet_type()

    def spawn_gift(self):

        value = 1
        # gift_type = random.randint(1, 5)
        gift_type = random.choice(list(GiftType))
        img = ''
        if gift_type == GiftType.SPEED:
            value = random.randint(1, 3)
            img = 'gift_speed.webp'
        elif gift_type == GiftType.BULLET_VELOCITY:
            value = random.randint(1, 5)
            img = 'gift_bullet_velocity.webp'
        elif gift_type == GiftType.BULLET_COLOR:
            value = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
            img = 'gift_color.webp'
        elif gift_type == GiftType.BULLET_RATIO:
            value = random.randint(1, 5)
            img = 'gift_bullet_ratio.webp'
        elif gift_type == GiftType.WEAPON_UPGRADE:
            value = 1
            img = 'gift_weapon.webp'

        x = random.randint(0, self.width - self.gift_width)
        velocity = random.randint(2, 8)
        gift_image = pygame.image.load(os.path.join('Assets', img))
        gift_image = pygame.transform.scale(gift_image, (35, 35))
        gift = Gift(x, self.gift_height, self.gift_height, self.gift_width, velocity, value, gift_type, self,
                    gift_image)
        self.gifts.append(gift)

    def spawn_random_enemy(self):
        while True:
            tmp_x = random.randint(0, self.width - self.ship_width)
            tmp_y = random.randint(0, self.height // 2)
            flag = True
            for enemy in self.enemies:
                if collide(enemy, pygame.Rect(tmp_x, tmp_y, self.ship_width, self.ship_height)):
                    flag = False
                    break
            if flag:
                new_enemy = Ship(tmp_x, tmp_y, self.ship_height, self.ship_width, 1, self.enemy_color, self)
                # new_enemy.bullet_velocity = 5
                # new_enemy.bullet_ratio = self.
                new_enemy.bullet_color = (255, 100, 0)
                self.enemies.append(new_enemy)
                break

    def spawn_enemy1(self):
        enemy = Ship(10, 10, self.ship_height, self.ship_width, 1, self.enemy_color, self)
        enemy.change_bullet_color((255, 100, 0))
        enemy.bullet_ratio = random.randint(200, 250)
        self.enemies.append(enemy)

    def create_star(self):
        new_star = pygame.Rect(random.randint(0, self.width), -self.height, self.star_width, self.star_height)
        self.background_stars.append([new_star, random.randint(2, 12)])

    def create_coin(self):
        new_coin = pygame.Rect(random.randint(0, self.width), -self.height, self.coin_width, self.coin_height)
        self.coins.append([new_coin, random.randint(2, 7)])

    def move_stars(self):
        tmp = []
        for star in self.background_stars:
            star[0].y += star[1]
            if star[0].y <= self.height:
                tmp.append(star)
                pygame.draw.rect(self.display.window, self.star_color, star[0])

        self.background_stars = tmp[:]

    def move_coins(self):
        tmp = []
        for coin in self.coins:
            coin[0].y += coin[1]
            if coin[0].y <= self.height:
                tmp.append(coin)
                # pygame.draw.rect(self.display.window, (0,255,0), coin[0])
                self.display.window.blit(COIN_IMAGE, (coin[0].x - 5, coin[0].y - 5))
        self.coins = tmp[:]

    def move_gifts(self):
        tmp = []
        for gift in self.gifts:
            if gift.move():
                tmp.append(gift)
                # pygame.draw.rect(self.display.window, gift.color, gift.body)
                self.display.window.blit(gift.img, (gift.body.x - 9, gift.body.y - 9))
        self.gifts = tmp[:]

    def move_enemy1(self, enemy):
        if (enemy.y // 150) % 2 == 0:
            if enemy.x > self.display.width - 2 * enemy.width:
                enemy.x_velocity = 0
                enemy.y_velocity = self.enemy_velocity
            else:
                enemy.x_velocity = self.enemy_velocity
                enemy.y_velocity = 0
        else:
            if enemy.x < 2 * enemy.width:
                enemy.x_velocity = 0
                enemy.y_velocity = self.enemy_velocity
            else:
                enemy.x_velocity = -self.enemy_velocity
                enemy.y_velocity = 0
        enemy.x += enemy.x_velocity
        enemy.y += enemy.y_velocity
        if enemy.y >= self.display.height:
            enemy.is_alive = False

    def spawn_enemy2(self):

        map_side = random.choice(list(MapSideType))
        while map_side == MapSideType.BOTTOM:
            map_side = random.choice(list(MapSideType))
        x, y = 0, 0
        x_velocity, y_velocity = random.randint(1, 5), random.randint(0, 3)
        if map_side == MapSideType.LEFT:
            x = -self.ship_width
            y = random.randint(0, 0.25 * self.height)
        elif map_side == MapSideType.TOP:
            x = random.randint(-self.ship_width, self.width + self.ship_width)
            y = -self.ship_height
            x_velocity = random.randint(-5, 5)
            y_velocity = random.randint(1, 3)
        elif map_side == MapSideType.RIGHT:
            x = self.width
            y = random.randint(0, 0.25 * self.height)
            x_velocity = -x_velocity

        enemy = Ship(x, y, self.ship_height, self.ship_width, 1, self.enemy_color, self)
        enemy.change_bullet_color((255, 100, 0))
        enemy.bullet_ratio = random.randint(200, 250)
        enemy.x_velocity = x_velocity
        enemy.y_velocity = y_velocity
        self.enemies.append(enemy)

    def move_enemy2(self, enemy):
        enemy.x += enemy.x_velocity
        enemy.y += enemy.y_velocity
        if enemy.y >= self.height or enemy.y < -enemy.height or enemy.x > self.width or enemy.x < -enemy.width:
            enemy.is_alive = False

    def move_enemies1(self):
        for enemy in self.enemies:
            self.move_enemy1(enemy)

    def move_enemies2(self):
        for enemy in self.enemies:
            self.move_enemy2(enemy)

    def create_boss(self):
        width = 150
        height = 120
        self.boss = Ship((self.width - width) // 2, height, height, width, 1, (255, 0, 0), self)
        self.boss.award = 1000
        self.boss.health_points = self.boss_health_points
        self.boss.bullet_type = BulletType.THREE_WIDE
        self.boss.bullet_velocity = 1
        self.boss.bullet_ratio = 80

    def change_boss_velocity(self, map_side):
        x_velocity, y_velocity = random.randint(1, 5), random.randint(0, 3)
        if map_side == MapSideType.BOTTOM:
            y_velocity = -y_velocity
        elif map_side == MapSideType.TOP:
            x_velocity = random.randint(-5, 5)
            y_velocity = random.randint(1, 3)
        elif map_side == MapSideType.RIGHT:
            y = random.randint(0, 0.25 * self.height)
            x_velocity = -x_velocity
        self.boss.x_velocity = x_velocity
        self.boss.y_velocity = y_velocity

    def move_boss(self):
        boss = self.boss
        boss.x += boss.x_velocity
        boss.y += boss.y_velocity
        if boss.y >= self.height - 3 * boss.height:
            self.change_boss_velocity(MapSideType.BOTTOM)
        elif boss.y < 40:
            self.change_boss_velocity(MapSideType.TOP)
        elif boss.x > self.width - boss.width - 40:
            self.change_boss_velocity(MapSideType.RIGHT)
        elif boss.x < 40:
            self.change_boss_velocity(MapSideType.LEFT)

    def change_phase(self):
        phase = self.game_phase
        if phase == GamePhase.ENEMIES1:
            self.game_phase = GamePhase.ENEMIES2
        elif phase == GamePhase.ENEMIES2:
            self.game_phase = GamePhase.BOSS
        elif phase == GamePhase.BOSS:
            self.game_phase = GamePhase.BONUS
        elif phase == GamePhase.BONUS:
            self.game_phase = GamePhase.ENEMIES1
