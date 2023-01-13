import os
import sys
import pygame

pygame.init()

FPS = 60
WIDTH = 900
HEIGHT = 600

pygame.display.set_caption("flying duck")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

position_d = HEIGHT // 2
speed_d = 0
boost_d = 0
player = pygame.Rect(WIDTH // 3, position_d, 50, 50)


def terminate():
    pygame.quit()
    sys.exit()


state = 'start'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if state == 'start':
        if click:
            state = 'play'

        position_d += (HEIGHT // 2 - position_d) * 0.1
        player.y = position_d
    elif state == 'play':
        if click:
            boost_d = -2
        else:
            boost_d = 0

        position_d += speed_d
        speed_d = (speed_d + boost_d + 1) * 0.98
        player.y = position_d

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'
    elif state == 'fall':
        state = ' start'
    else:
        pass

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, pygame.Color('green'), player)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
