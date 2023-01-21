import pygame


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font('data/arial.ttf', 35)

    def mouse_click(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                if click[0] == 1:
                    return 1
