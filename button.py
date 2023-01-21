import pygame


class Button:
    def __init__(self, width, height, in_color, active_color):
        self.width = width
        self.height = height
        self.in_color = in_color
        self.active_color = active_color
        self.font = pygame.font.Font('data/arial.ttf', 35)

    def draw(self, x, y, text, scr):
        text_button = self.font.render(text, True, self.in_color)
        pygame.draw.rect(scr, self.active_color, (x, y, self.width, self.height))
        scr.blit(text_button, (x + 15, y + 22))

    def mouse_click(self, x, y, text, scr):
        text_button_1 = self.font.render(text, True, self.in_color)
        text_button_2 = self.font.render(text, True, pygame.Color('Black'))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                scr.blit(text_button_2, (x + 15, y + 22))
                if click[0] == 1:
                    return 1
        else:
            scr.blit(text_button_1, (x + 15, y + 22))
