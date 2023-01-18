import os
import sys
import pygame
from random import randint

pygame.init()
pygame.mixer.init()

FPS = 60
WIDTH = 900
HEIGHT = 600

state = 'start'
timer = 10
frame = 0

speed_d = 0
boost_d = 0
position_d = 0

speed_p = 3
size_p = 200
pos_p = HEIGHT // 2

font = pygame.font.Font('data/arial.ttf', 24)

pygame.mixer.music.load('data/music.mp3')
volume = 0.1
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

sound_die = pygame.mixer.Sound('data/die.wav')
sound_hit = pygame.mixer.Sound('data/hit.wav')

sound = True

lives = 3
score = 0

pygame.display.set_caption("flying duck")
icon = pygame.image.load('data/icon.png')
pygame.display.set_icon(icon)


screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 3, HEIGHT // 2, 34, 24)

pipe = []
background = []
scores = []

background.append(pygame.Rect(0, 0, 297, 600))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Играть",
                  "Как играть?",
                  "Выход"]

    text_game = ["Flying duck"]

    ok = True

    fon = load_image('fon.png')
    screen.blit(fon, (0, 0))
    font1 = pygame.font.Font(None, 64)
    text_coord = 220
    for line in intro_text:
        string_rendered = font1.render(line, True, pygame.Color('Red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 320
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    font2 = pygame.font.Font('data/arial.ttf', 65)
    text_coord = 100
    for line in text_game:
        string_rendered = font2.render(line, True, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 190
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while ok:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                ok = False
                if x > 323 and x < 581 and y > 290 and y < 320:
                    what()
                elif x > 322 and x < 472 and y > 343 and y < 379:
                    terminate()
                else:
                    print('Игра началась')

        pygame.display.flip()
        clock.tick(FPS)


def what():
    intro_text = ["Для прыжков используйте ЛКМ",
                  "Назад"]

    text = ["Вкл/Выкл музыку m,"
            "уменьшить '-' увеличить '+' громкость"]

    ok = True

    fon = load_image('fon.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 245
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('Red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    text_coord = 200
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('Red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while ok:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > 18 and x < 103 and y > 294 and y < 315:
                    start_screen()
                    ok = False

        pygame.display.flip()
        clock.tick(FPS)


def read_record():
    with open('data/record.txt') as f:
        return f.readline()


def write_record(r):
    with open('data/record.txt', 'w') as f:
        f.write(str(r))


def game_over(score):
    img = load_image('gameover.png')
    screen.blit(img, (300, 150))
    r = read_record()
    font_game_over = pygame.font.Font('data/arial.ttf', 20)
    text = font_game_over.render(f'record: {r} score {score}', True, (0, 0, 0))
    screen.blit(text, (285, 330))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


player_image_secret = load_image('player_secret.png', -1)
flappy_bird = load_image('flappy bird.png', -1)
player_image = load_image('player.png', -1)
pipe_bot = load_image('pipe_bottom.png', -1)
pipe_top = load_image('pipe_top.png', -1)


start_screen()
fon_game = load_image('fon_game.png')
running = True
while running:
    record = read_record()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                sound = not sound
                if sound:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_KP_MINUS:
                volume -= 0.1
                pygame.mixer.music.set_volume(volume)
            if event.key == pygame.K_KP_PLUS:
                volume += 0.1
                pygame.mixer.music.set_volume(volume)

    press = pygame.mouse.get_pressed()
    click = press[0]

    if timer > 0:
        timer -= 1

    frame = (frame + 0.2) % 4
    speed_p = 3 + score // 10

    for i in range(len(background) - 1, -1, -1):
        bg = background[i]
        bg.x -= speed_p // 2

        if bg.right < 0:
            background.remove(bg)

        if background[len(background) - 1].right <= WIDTH:
            background.append(pygame.Rect(background[len(background) - 1].right, 0, 297, 600))

    for i in range(len(pipe) - 1, -1, -1):
        elem = pipe[i]
        elem.x -= speed_p

        if elem.right < 0:
            pipe.remove(elem)
            if elem in scores:
                scores.remove(elem)

    if state == 'start':
        if click and timer == 0 and len(pipe) == 0:
            state = 'play'
        position_d += (HEIGHT // 2 - position_d) * 0.1
        player.y = position_d

    elif state == 'play':
        if click:
            boost_d = - 2
        else:
            boost_d = 0

        position_d += speed_d
        speed_d = (speed_d + boost_d + 1) * 0.98
        player.y = position_d

        if len(pipe) == 0 or pipe[len(pipe) - 1].x < WIDTH - 200:
            pipe.append(pygame.Rect(WIDTH, 0, 52, pos_p - size_p // 2))
            pipe.append(pygame.Rect(WIDTH, pos_p + size_p // 2, 52, HEIGHT - pos_p + size_p // 2))

            pos_p += randint(-100, 100)
            if pos_p < size_p:
                pos_p = size_p
            elif pos_p > HEIGHT - size_p:
                pos_p = HEIGHT - size_p

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        for elem in pipe:
            if player.colliderect(elem):
                state = 'fall'

            if elem.right < player.left and elem not in scores:
                scores.append(elem)
                score += 1

    elif state == 'fall':
        speed_d, boost_d = 0, 0
        pos_p = HEIGHT // 2
        if lives > 1:
            sound_hit.play()

        lives -= 1
        if lives > 0:
            state = 'start'
            timer = 60
        else:
            state = 'game over'
            pygame.mixer.music.stop()
            sound_die.play()
            if state == 'game over':
                if score > int(record):
                    write_record(score)
                game_over(score)

    else:
        position_d += speed_d
        speed_d = (speed_d + boost_d + 1) * 0.98
        player.y = position_d

        if timer == 0:
            running = False

    screen.fill((0, 0, 0))
    for bg in background:
        screen.blit(fon_game, bg)

    for elem in pipe:
        if elem.y == 0:
            rect = pipe_top.get_rect(bottomleft=elem.bottomleft)
            screen.blit(pipe_top, rect)
        else:
            rect = pipe_bot.get_rect(topleft=elem.topleft)
            screen.blit(pipe_bot, rect)

    image = player_image.subsurface(34 * int(frame), 0, 34, 24)
    image = pygame.transform.rotate(image, -speed_d * 2)
    screen.blit(image, player)

    if score >= 50 and score <= 70:  # замена персонажа при достижении очков
        image_secret = player_image_secret.subsurface(34 * int(frame), 0, 34, 24)
        image_secret = pygame.transform.rotate(image_secret, -speed_d * 2)
        screen.blit(image_secret, player)

    if score >= 200 and score <= 300:  # пасхалка, отсылка на оригинальную версию flappy bird
        flappy = flappy_bird.subsurface(34 * int(frame), 0, 34, 24)
        flappy = pygame.transform.rotate(flappy, -speed_d * 2)
        screen.blit(flappy, player)

    text = font.render('Очки: ' + str(score), 1, pygame.Color(0, 0, 0))
    screen.blit(text, (10, 10))

    text = font.render('Жизни: ' + str(lives), 1, pygame.Color(0, 0, 0))
    screen.blit(text, (WIDTH - 170, 10))

    pygame.display.update()
    clock.tick(FPS)

terminate()