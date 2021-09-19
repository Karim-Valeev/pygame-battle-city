import os
import pygame

from entities.non_game_screen import NonGameScreen

WHITE = (255, 255, 255)


class StatusBar(NonGameScreen):

    def __init__(self, screen, player=None):
        super().__init__(screen)
        if player is None:
            self.highscore = self.calculate_highscore()
        elif player is not None:
            self.enemies_remain = 10 - player.count_enemies_killed
            self.hp = player.hp
            self.score = player.score
            self.font = pygame.font.Font(None, 36)
        else:
            raise AttributeError

    def draw_frame(self):
        status_frame = pygame.Rect(0, 0, 650, 50)
        pygame.draw.rect(self.screen, WHITE, status_frame, 1)

    def draw(self):
        self.draw_frame()
        self.draw_text(f"Enemies: {self.enemies_remain}", self.font, WHITE, (110, 25))
        self.draw_text(f"Score: {self.score}", self.font, WHITE, (325, 25))
        self.draw_text(f"HP: {self.hp}", self.font, WHITE, (550, 25))

    def draw_highscore(self):
        self.draw_frame()
        font = pygame.font.Font(None, 40)
        self.draw_text(f"HIGHSCORE: {self.highscore}", font, WHITE, (325, 25))

    def calculate_highscore(self):
        path = os.path.join('scores', 'scores.txt')
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('XXXXX - 0')

        filesize = os.path.getsize(path)
        if filesize == 0:
            return 0

        with open(path, 'r') as f:
            scores = []
            for line in f:
                score = int(line[8:(len(line) - 1)]) if len(line) < 9 else 0
                scores.append(score)
        return max(scores)
