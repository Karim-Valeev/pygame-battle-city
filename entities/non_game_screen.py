class NonGameScreen:
    def __init__(self, screen):
        self.screen = screen

    def draw_text(self, text, font, color, cntr):
        phrase = font.render(text, 0, color)
        phrase_rect = phrase.get_rect(center=cntr)
        self.screen.blit(phrase, phrase_rect)
