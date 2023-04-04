import random

import pygame

from Gift import Gift
from Ship import Ship
from World import World

window_width = 1080
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
border = pygame.Rect(0, 0, window_width, window_height)
ship_width = 46
ship_height = 46
gift_height = 20
gift_width = 20
star_width = 2
star_height = 2
star_color = (255, 255, 255)


def collide(bullet_rect, ship_rect):
    bullet_left = bullet_rect.x
    bullet_top = bullet_rect.y
    bullet_right = bullet_rect.x + bullet_rect.width
    bullet_bottom = bullet_rect.y + bullet_rect.height
    ship_left = ship_rect.x
    ship_top = ship_rect.y
    ship_right = ship_rect.x + ship_rect.width
    ship_bottom = ship_rect.y + ship_rect.height

    if (ship_bottom > bullet_top > ship_top or ship_bottom > bullet_bottom > ship_top) and\
       (ship_left < bullet_left < ship_right or ship_left < bullet_right < ship_right):
        return 1
    # if ((bullet_left >= ship_right or bullet_right <= ship_left) and (bullet_top <= ship_bottom or bullet_bottom >= ship_top)):
    #
    #     return 0
    return 0


def collisions(enemies, ship, gifts):
    ship_rect = pygame.Rect(ship.x, ship.y, ship.width, ship.height)
    i = 0
    while i < len(enemies):
        enemy = enemies[i]
        if enemy.is_alive:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if collide(enemy_rect, ship_rect):
                enemy.is_alive = False
                ship.points += enemy.award
                ship.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                return enemies, ship, gifts
        i += 1

    i, j = 0, 0
    while i < len(ship.bullets):
        j = 0
        while j < len(enemies):
            bullet = ship.bullets[i]
            enemy = enemies[j]
            if enemy.is_alive:
                if collide(bullet.body, pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                    del ship.bullets[i]
                    enemy.is_alive = False
                    ship.points += enemy.award
                    # enemies[j].color = (1, 1, 1)
                    i -= 1
                    j -= 1
                    break
            j += 1
        i += 1

    i = 0
    for enemy in enemies:
        while i < len(enemy.bullets):
            bullet = enemy.bullets[i]
            if collide(bullet.body, ship_rect):
                del enemy.bullets[i]
                ship.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                return enemies, ship, gifts
                # i -= 1
            i += 1

    i = 0
    while i < len(gifts):
        if collide(gifts[i].body, ship_rect):
            del gifts[i]
            i -= 1
        i += 1
    return enemies, ship, gifts


def spawn_gift(gifts, world):

    value = 1
    gift_type = random.randint(1, 5)
    if gift_type == 1:
        value = random.randint(1, 3)
    if gift_type == 2:
        value = random.randint(1, 5)
    if gift_type == 3:
        value = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
    if gift_type == 4:
        value = random.randint(1, 20)
    if gift_type == 5:
        value = 1
    x = random.randint(0, window_width - gift_width)
    velocity = random.randint(2, 8)
    gift = Gift(x, -gift_height, gift_height, gift_width, velocity, value, gift_type, world)
    gifts.append(gift)
    return gifts


def main():
    clock = pygame.time.Clock()
    ship_x_value = (window_width - ship_width) // 2
    ship_y_value = window_height - ship_height - 10
    background_color = (8, 17, 53)
    ship_color = (255, 255, 255)
    enemy_color = (255, 0, 100)
    is_running = True
    fps = 60
    gift_ratio = 100
    enemy_ratio = 450

    world = World(window_height, window_width)
    ship = Ship(ship_x_value, ship_y_value, ship_height, ship_width, -1, ship_color, world)
    enemy = Ship(100, 100, ship_height, ship_width, 1, enemy_color, world)
    enemy.change_bullet_color((255, 100, 0))
    enemies = [enemy]
    gifts = []
    background_stars = []

    count_frames = 1
    while True:

        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        if count_frames % 2 == 0:
            new_star = pygame.Rect(random.randint(0, window_width), -star_height, star_width, star_height)
            background_stars.append([new_star, random.randint(2, 12)])

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_p]:
            is_running = False
        if keys_pressed[pygame.K_ESCAPE]:
            is_running = True

        if is_running:
            count_frames += 1
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                ship.move_left()

            if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                ship.move_right()

            if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                ship.move_up()

            if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
                ship.move_down()

            enemies, ship, gifts = collisions(enemies, ship, gifts)

            if count_frames % enemy_ratio == 0:
                enemy_ratio = random.randint(100, 500)
                while True:
                    tmp_x = random.randint(0, window_width - ship_width)
                    tmp_y = random.randint(0, window_height // 2)
                    flag = True
                    for enemy in enemies:
                        if collide(enemy, pygame.Rect(tmp_x, tmp_y, ship_width, ship_height)):
                            flag = False
                            break
                    if flag:
                        new_enemy = Ship(tmp_x, tmp_y, ship_height, ship_width, 1, enemy_color, world)
                        new_enemy.bullet_velocity = 5
                        new_enemy.bullet_ratio = 50
                        new_enemy.bullet_color = (255, 100, 0)
                        enemies.append(new_enemy)
                        break

            if count_frames % gift_ratio == 0:
                gifts = spawn_gift(gifts, world)
                gift_ratio = random.randint(100, 1000)

            pygame.draw.rect(window, background_color, border)

            tmp = []
            for star in background_stars:
                star[0].y += star[1]
                if star[0].y <= world.height:
                    tmp.append(star)
                    pygame.draw.rect(window, star_color, star[0])
            background_stars = tmp[:]

            tmp = []
            for gift in gifts:
                if gift.move():
                    tmp.append(gift)
                    pygame.draw.rect(window, gift.color, gift.body)
            gifts = tmp[:]

            for enemy in enemies:
                enemy.bullets_move()
                if enemy.is_alive:
                    if count_frames % enemy.bullet_ratio == 0:
                        enemy.create_bullet()
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                    pygame.draw.rect(window, enemy.color, enemy_rect)
                for bullet in enemy.bullets:
                    pygame.draw.rect(window, bullet.color, bullet.body)

            i = 0
            while i < len(enemies):
                if not enemies[i].is_alive and not len(enemies[i].bullets):
                    del enemies[i]
                    i -= 1
                i += 1

            ship.bullets_move()

            if count_frames % ship.bullet_ratio == 0:
                ship.create_bullet()
                # enemy.create_bullet()

            ship_rect = pygame.Rect(ship.x, ship.y, ship.width, ship.height)
            # enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            # pygame.draw.rect(window, background_color, border)
            pygame.draw.rect(window, ship.color, ship_rect)
            # pygame.draw.rect(window, enemy.color, enemy_rect)
            for bullet in ship.bullets:
                pygame.draw.rect(window, bullet.color, bullet.body)
            # for bullet in enemy.bullets:
            #     pygame.draw.rect(window, bullet.color, bullet.body)

            pygame.font.init()
            x = world.width // 2
            y = 8

            font = pygame.font.Font('freesansbold.ttf', 18)
            text = font.render(str(ship.points), True, (255, 255, 255), (8, 17, 53))
            textRect = text.get_rect()
            textRect.center = (x, y)
            window.blit(text, textRect)

            pygame.display.update()


if __name__ == "__main__":
    main()
