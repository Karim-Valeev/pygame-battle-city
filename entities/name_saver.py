import os

import pygame

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def letter_filler():
    letters = []
    for i in range(65, 91):
        letters.append(chr(i))
    for i in range(97, 123):
        letters.append(chr(i))
    return letters


LETTERS = letter_filler()


class NameSaver:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score

    def draw_text(self, text, font, cntr):
        phrase = font.render(text, 0, WHITE)
        phrase_rect = phrase.get_rect(center=cntr)
        self.screen.blit(phrase, phrase_rect)

    def save(self):
        input_box = pygame.Rect(240, 453, 170, 60)

        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()

        name = ""
        while True:
            self.screen.fill(BLACK)
            self.draw_text("Enter your name using 5 letters:", font, (325, 270))
            pygame.draw.rect(self.screen, WHITE, input_box, 3)

            # Render the current text.
            self.draw_text(name, font, (325, 483))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) == 5:
                        path = os.path.join("scores", "scores.txt")
                        with open(path, "a") as f:
                            f.write(f"{name} - {self.score}\n")
                        return

                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if event.unicode in LETTERS and len(name) < 5:
                            name += event.unicode
            clock.tick(FPS)
