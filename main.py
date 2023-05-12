import os
import random
import pygame
import csv
import pandas as pd


from Display import Display
from Gift import Gift
from Ship import Ship
from World import World

window_width = 1080
window_height = 600
display = Display(window_width, window_height)
window = display.window
border = pygame.Rect(0, 0, window_width, window_height)

CHICKEN_IMAGE = pygame.image.load(os.path.join('Assets', 'kurczak.webp'))
CHICKEN_IMAGE = pygame.transform.scale(CHICKEN_IMAGE, (70, 70))
SPACECRAFT_IMAGE = pygame.image.load(os.path.join('Assets', 'spacecraft.png'))
SPACECRAFT_IMAGE = pygame.transform.scale(SPACECRAFT_IMAGE, (70, 70))
EGG_IMAGE = pygame.image.load(os.path.join('Assets', 'egg.webp'))
EGG_IMAGE = pygame.transform.scale(EGG_IMAGE, (20, 25))


def save_score(row):
    f = open('scores.csv', 'a')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()


def get_max_score():
    max_score = 0
    with open("scores.csv", 'r') as file:
        csv_reader = csv.reader(file, delimiter=':')
        for row in csv_reader:
            if row:
                max_score = max(max_score, int(row[0]))
    return max_score


def main():
    write_to_csv = False
    clock = pygame.time.Clock()
    fps = 60
    is_running = True
    gift_ratio = 100
    enemy_ratio = 40
    world = World(window_height, window_width, display)

    count_frames = 1
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        if count_frames % 2 == 0:
            world.create_star()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_p]:
            is_running = False
        if keys_pressed[pygame.K_ESCAPE]:
            is_running = True

        if is_running:
            count_frames += 1
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                world.ship.move_left()

            if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                world.ship.move_right()

            if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                world.ship.move_up()

            if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
                world.ship.move_down()

            world.collisions()

            if count_frames % enemy_ratio == 0:
                # enemy_ratio = random.randint(100, 500)
                world.spawn_enemy2()

            if count_frames % gift_ratio == 0:
                gift_ratio = random.randint(100, 1000)
                world.spawn_gift()

            pygame.draw.rect(world.display.window, world.background_color, border)

            world.move_enemies()
            world.move_stars()
            world.move_gifts()

            for enemy in world.enemies:
                enemy.bullets_move()
                if enemy.is_alive:
                    if count_frames % enemy.bullet_ratio == 0:
                        enemy.create_bullet()
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                    # pygame.draw.rect(world.display.window, enemy.color, enemy_rect)
                    window.blit(CHICKEN_IMAGE, (enemy_rect.x - 13, enemy_rect.y - 13))
                for bullet in enemy.bullets:
                    window.blit(EGG_IMAGE, (bullet.body.x - 3, bullet.body.y - 3))
                    # pygame.draw.rect(world.display.window, bullet.color, bullet.body)

            i = 0
            while i < len(world.enemies):
                if not world.enemies[i].is_alive and not len(world.enemies[i].bullets):
                    del world.enemies[i]
                    i -= 1
                i += 1

            world.ship.bullets_move()

            if count_frames % world.ship.bullet_ratio == 0:
                world.ship.create_bullet()

            ship_rect = pygame.Rect(world.ship.x, world.ship.y, world.ship.width, world.ship.height)
            # pygame.draw.rect(world.display.window, world.ship.color, ship_rect)
            window.blit(SPACECRAFT_IMAGE, (ship_rect.x - 13, ship_rect.y - 13))

            for bullet in world.ship.bullets:
                pygame.draw.rect(window, bullet.color, bullet.body)

            pygame.font.init()
            x = world.width // 2
            y = 8

            font = pygame.font.Font('freesansbold.ttf', 18)

            text = font.render("SCORE " + str(world.ship.points), True, (255, 255, 255), (8, 17, 53))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            window.blit(text, text_rect)

            x = world.width - 100
            text = font.render("MAX SCORE " + str(get_max_score()), True, (255, 255, 255), (8, 17, 53))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            window.blit(text, text_rect)

            if world.ship.health_points <= 0:
                is_running = False
                write_to_csv = True

            pygame.display.update()

        if not is_running and write_to_csv:
            new_row = [str(world.ship.points)]
            save_score(new_row)
            write_to_csv = False


if __name__ == "__main__":
    main()
