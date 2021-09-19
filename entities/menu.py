import pygame

from entities.non_game_screen import NonGameScreen

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Menu(NonGameScreen):
    def __init__(self, screen, status_bar):
        super().__init__(screen)
        self.cursor = 0
        self.screen = screen
        self.sb = status_bar
        self.font = pygame.font.Font(None, 36)

    def start(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill(BLACK)
            self.sb.draw_highscore()

            if self.cursor == 0:
                cursor_frame = pygame.Rect(240, 240, 170, 60)
            else:
                cursor_frame = pygame.Rect(240, 453, 170, 60)

            pygame.draw.rect(self.screen, WHITE, cursor_frame, 3)

            self.draw_text("START", self.font, WHITE, (325, 270))
            self.draw_text("QUIT", self.font, WHITE, (325, 483))

            pygame.display.update()

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                elif i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_UP:
                        if self.cursor == 1:
                            self.cursor = 0
                    elif i.key == pygame.K_DOWN:
                        if self.cursor == 0:
                            self.cursor = 1
                    elif i.key == pygame.K_RETURN:
                        if self.cursor == 0:
                            return True
                        else:
                            exit()

            clock.tick(FPS)
