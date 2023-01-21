import os
import sys
import pygame
import random
from button import Button

pygame.init()
pygame.mixer.init()

FPS = 60
WIDTH = 900
HEIGHT = 600

state = 'start'
timer = 10
frame = 0

speed_d = 0
x = 3
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
sound_win = pygame.mixer.Sound('data/win.wav')

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

BUTTON = Button(205, 75)

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
    global volume, sound
    text_game = ["Flying duck"]

    ok = True

    fon = load_image('fon.png')
    screen.blit(fon, (0, 0))

    screen.blit(icon_game, (370, 10))
    screen.blit(start_button, (165, 140))
    screen.blit(options_button, (165, 240))
    screen.blit(exit_button, (165, 340))

    font1 = pygame.font.Font('data/arial.ttf', 65)
    text_coord = 100
    for line in text_game:
        string_rendered = font1.render(line, True, pygame.Color('Black'))
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

            act = BUTTON.mouse_click(325, 220)
            act1 = BUTTON.mouse_click(325, 320)
            act2 = BUTTON.mouse_click(325, 420)

            if act == 1:
                return
            if act1 == 1:
                what()
            if act2 == 1:
                terminate()

        pygame.display.flip()
        clock.tick(FPS)


def what():
    global sound
    intro_text = ["Суть данной игры проста, набрать как можно больше очков.",
                  "игра заканчивается при достижении 500 очков.",
                  "У вас всего 3 жизни и они не восполняемы, ",
                  "когда жизни заканчиваются, игра соответственно тоже.",
                  "каждые 10 очков игра ускоряется и становится сложнее играть.",
                  "",
                  "",
                  "В игре спрятанна пасхалка :)",
                  "Кнопка complexity - выбрать уровень сложности!"]

    text = ["Вкл/Выкл музыку m,"
            "уменьшить '-' увеличить '+' громкость",
            "Для прыжков используйте ЛКМ"]

    ok = True

    fon = load_image('fon.png')
    complexity_button = load_image('complexity.png')

    screen.blit(fon, (0, 0))
    screen.blit(back_button, (342, 430))
    screen.blit(complexity_button, (140, 275))

    font = pygame.font.Font('data/arial.ttf', 18)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    text_coord = 270
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('Black'))
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sound = not sound
                    if sound:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > 321 and x < 495 and y > 358 and y < 408:
                    change_complexity()
                    ok = False
                if x > 362 and x < 456 and y > 450 and y < 496:
                    start_screen()
                    ok = False

        pygame.display.flip()
        clock.tick(FPS)


def easy_lvl():
    global x
    x = 4


def normal_lvl():
    global x
    x = 10


def hard_lvl():
    global x
    x = 15


def change_complexity():
    text_game = ["Выбор сложности"]

    ok = True

    fon = load_image('fon.png')
    easy = load_image('easy.png')
    normal = load_image('normal.png')
    hard = load_image('hard.png')
    screen.blit(fon, (0, 0))
    screen.blit(easy, (350, 150))
    screen.blit(normal, (350, 240))
    screen.blit(hard, (350, 340))

    font1 = pygame.font.Font('data/arial.ttf', 38)
    text_coord = 100
    for line in text_game:
        string_rendered = font1.render(line, True, pygame.Color('Black'))
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
                if x > 371 and x < 463 and y > 168 and y < 217:
                    easy_lvl()
                    ok = False
                    what()
                if x > 371 and x < 463 and y > 260 and y < 304:
                    normal_lvl()
                    ok = False
                    what()
                if x > 371 and x < 463 and y > 361 and y < 407:
                    hard_lvl()
                    ok = False
                    what()

            pygame.display.flip()
            clock.tick(FPS)


def read_record():
    with open('data/record.txt') as f:
        return f.readline()


def write_record(r):
    with open('data/record.txt', 'w') as f:
        f.write(str(r))


def game_over(score):
    pygame.mixer.music.stop()
    img = load_image('gameover.png')
    text = font.render('Жизни: 0', 1, pygame.Color(0, 0, 0))

    screen.blit(text, (WIDTH - 170, 10))
    screen.blit(img, (300, 150))
    screen.blit(end_button, (350, 350))

    r = read_record()
    font_game_over = pygame.font.Font('data/arial.ttf', 20)
    text = font_game_over.render(f'record: {r} score {score}', True, (0, 0, 0))

    screen.blit(text, (285, 330))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > 370 and x < 463 and y > 371 and y < 415:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def win(score):
    pygame.mixer.music.stop()
    img = load_image('win.png')
    text = font.render(f'Очки: {score}', 1, pygame.Color(0, 0, 0))

    screen.blit(text, (10, 10))
    screen.blit(img, (250, 180))
    screen.blit(end_button, (350, 350))

    r = read_record()
    font_game_over = pygame.font.Font('data/arial.ttf', 20)
    text = font_game_over.render(f'record: {r} score {score}', True, (0, 0, 0))

    screen.blit(text, (285, 330))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > 370 and x < 463 and y > 371 and y < 415:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


flappy_bird = load_image('flappy bird.png', -1)
player_image = load_image('player.png', -1)
player_image_secret = load_image('player_secret.png', -1)

start_button = load_image('start_button.png')
back_button = load_image('back.png')
end_button = load_image('end_button.png')
options_button = load_image('options_button.png')
exit_button = load_image('exit_button.png')

icon_game = load_image('icon_game.png')
icon_game = pygame.transform.scale(icon_game, (128, 128))

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
    speed_p = x + score // 10  # скорость уточки усложняющаяся

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

    elif state == 'win':
        sound_win.play()
        write_record(score)
        win(score)

    elif state == 'play':
        if click:
            boost_d = - 2  # управляемость
        else:
            boost_d = 0

        position_d += speed_d
        speed_d = (speed_d + boost_d + 1) * 0.98
        player.y = position_d

        if len(pipe) == 0 or pipe[len(pipe) - 1].x < WIDTH - 200:
            pipe.append(pygame.Rect(WIDTH, 0, 52, pos_p - size_p // 2))
            pipe.append(pygame.Rect(WIDTH, pos_p + size_p // 2, 52, HEIGHT - pos_p + size_p // 2))

            pos_p += random.randint(-100, 100)
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
            sound_die.play()
            if state == 'game over':
                if score > int(record):
                    write_record(score)
                game_over(score)

    else:
        position_d += speed_d
        speed_d = (speed_d + boost_d + 1) * 0.98
        player.y = position_d

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

    if score > 500:
        state = 'win'

    if score >= 50 and score <= 200:  # замена персонажа при достижении очков, так называемый рейдж мод
        image_secret = player_image_secret.subsurface(34 * int(frame), 0, 34, 24)
        image_secret = pygame.transform.rotate(image_secret, -speed_d * 2)
        screen.blit(image_secret, player)

    if score >= 200:  # пасхалка, отсылка на оригинальную версию flappy bird
        flappy = flappy_bird.subsurface(34 * int(frame), 0, 34, 24)
        flappy = pygame.transform.rotate(flappy, -speed_d * 2)
        screen.blit(flappy, player)

    text2 = font.render('Очки: ' + str(score), 1, pygame.Color(0, 0, 0))
    screen.blit(text2, (10, 10))

    text1 = font.render('Жизни: ' + str(lives), 1, pygame.Color(0, 0, 0))
    screen.blit(text1, (WIDTH - 170, 10))

    pygame.display.update()
    clock.tick(FPS)

terminate()
