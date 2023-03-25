import pygame

from Ship import Ship
from World import World

window_width = 1080
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
border = pygame.Rect(0, 0, window_width, window_height)
ship_width = 46
ship_height = 46
bullet_ratio = 25


def main():
    clock = pygame.time.Clock()
    ship_x_value = (window_width - ship_width) // 2
    ship_y_value = window_height - ship_height - 10
    background_color = (0, 0, 0)
    ship_color = (255, 255, 255)
    enemy_color = (255, 0, 100)
    is_running = True
    fps = 60

    world = World(window_height, window_width)
    ship = Ship(ship_x_value, ship_y_value, ship_height, ship_width, -1, ship_color, world)
    enemy = Ship(0, 0, ship_height, ship_width, 1, enemy_color, world)
    enemy.change_bullet_color((255, 100, 0))

    count_frames = 1
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_p]:
            is_running = False
        if keys_pressed[pygame.K_ESCAPE]:
            is_running = True

        if is_running:
            count_frames += 1
            count_frames %= bullet_ratio
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                ship.move_left()

            if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                ship.move_right()

            if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                ship.move_up()

            if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
                ship.move_down()

            ship.bullets_move()
            enemy.bullets_move()

            if not count_frames:
                ship.create_bullet()
                enemy.create_bullet()

            ship_rect = pygame.Rect(ship.x, ship.y, ship.width, ship.height)
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            pygame.draw.rect(window, background_color, border)
            pygame.draw.rect(window, ship.color, ship_rect)
            pygame.draw.rect(window, enemy.color, enemy_rect)
            for bullet in ship.bullets:
                pygame.draw.rect(window, bullet.color, bullet.body)
            for bullet in enemy.bullets:
                pygame.draw.rect(window, bullet.color, bullet.body)

            pygame.display.update()


if __name__ == "__main__":
    main()
