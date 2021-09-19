import pygame
from .name_saver import NameSaver
from .non_game_screen import NonGameScreen

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 64)
RED = (255, 0, 0)


def letter_filler():
    LETTERS = []
    for i in range(65, 91):
        LETTERS.append(chr(i))
    for i in range(97, 123):
        LETTERS.append(chr(i))
    return LETTERS


class EndingScreen(NonGameScreen):
    def __init__(self, screen, win, score):
        super().__init__(screen)
        self.screen = screen
        self.win = win
        self.score = score
        self.cursor_for_YN = 0
        self.clock = pygame.time.Clock()

    def start(self):
        font1 = pygame.font.Font(None, 40)
        font2 = pygame.font.Font(None, 35)
        if self.win:
            ending_phrase = "VICTORY!"
            color = GREEN
        else:
            ending_phrase = "GAME OVER!"
            color = RED

        while True:
            self.screen.fill(BLACK)

            self.draw_text(ending_phrase, font1, color, (325, 212))

            question = "Do you want to save your name?"
            self.draw_text(
                question,
                font2,
                WHITE,
                (325, 375),
            )

            self.draw_text(
                "YES",
                font2,
                WHITE,
                (250, 538),
            )
            self.draw_text(
                "NO",
                font2,
                WHITE,
                (400, 538),
            )

            if self.cursor_for_YN == 0:
                cursor_frame = pygame.Rect(198, 508, 105, 60)
            else:
                cursor_frame = pygame.Rect(348, 508, 105, 60)

            pygame.draw.rect(self.screen, WHITE, cursor_frame, 3)

            pygame.display.update()

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                elif i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_LEFT:
                        if self.cursor_for_YN == 1:
                            self.cursor_for_YN = 0
                    elif i.key == pygame.K_RIGHT:
                        if self.cursor_for_YN == 0:
                            self.cursor_for_YN = 1
                    elif i.key == pygame.K_RETURN:
                        if self.cursor_for_YN == 0:
                            ns = NameSaver(self.screen, self.score)
                            ns.save()
                        return

            self.clock.tick(FPS)
