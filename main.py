import pygame

width = 600
height = 800
fps = 60
window = pygame.display.set_mode((width, height))
border = pygame.Rect(0, 0, 600, 800)


def main():
    clock = pygame.time.Clock()
    x_value = 277

    bullets = []
    c = 1
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        c += 1
        c %= 25
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            x_value -= 5
            x_value = max(5, x_value)

        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            x_value += 5
            x_value = min(549, x_value)

        ship = pygame.Rect(x_value, 750, 46, 46)

        pygame.draw.rect(window, (0, 0, 0), border)

        tmp = []
        for bullet in bullets:
            bullet.y -= 10
            if bullet.y >= -20:
                tmp.append(bullet)
            pygame.draw.rect(window, (0, 191, 255), bullet)
        bullets = tmp[:]

        if not c:
            bullets.append(pygame.Rect(x_value + 23 - 5, 720, 10, 30))

        pygame.draw.rect(window, (255, 255, 255), ship)

        pygame.display.update()


if __name__ == "__main__":
    main()
