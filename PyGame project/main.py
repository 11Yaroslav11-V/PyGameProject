import os
import sys
import pygame

pygame.init()

FPS = 60
WIDTH = 900
HEIGHT = 600
STATE = 'start'
SPEED_D = 0
BOOST_D = 0

pygame.display.set_caption("flying duck")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

obstacle_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
opponent_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

player = pygame.Rect(WIDTH // 3, HEIGHT // 2, 50, 50)


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

    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 64)
    text_coord = 220
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('Pink'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 320
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def game_screen():
    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def what():
    intro_text = ["Для прыжков используйте клавишу SPACE или ЛКМ"]

    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 245
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('Pink'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Player(pygame.sprite.Sprite):
    player_image = load_image('player.png', -1)

    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = Player.player_image

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 3
        self.rect.y = HEIGHT // 2

        self.state = STATE
        self.boost_d = BOOST_D
        self.speed_d = SPEED_D

        self.start_position = (self.rect.x, self.rect.y)
        self.rect.topleft = self.start_position

    def update(self):
        press = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        click = press[0] or keys[pygame.K_SPACE]

        if self.state == 'start':
            if click:
                self.state = 'play'

            self.rect.y += (HEIGHT // 2 - self.rect.y) * 0.1
            player.y = self.rect.y
        elif self.state == 'play':
            if click:
                self.boost_d = -2
            else:
                self.boost_d = 0

            self.rect.y += self.speed_d
            self.speed_d = (self.speed_d + self.speed_d + 1) * 0.98
            player.y = self.rect.y

            if player.top < 0 or player.bottom > HEIGHT:
                self.state = 'fall'
        elif self.state == 'fall':
            self.state = ' start'
        else:
            pass


start_screen()
game_screen()
what()
terminate()
