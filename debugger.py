import pygame as pg


class Debugger:
    def __init__(self):
        self.text = dict()
        self.font = pg.font.SysFont("haha no", 30)

    def update(self, description: str, text: str):
        self.text[description] = text

    def draw(self, surf):
        for i, description in enumerate(self.text.keys()):
            text_surf = self.font.render(description + ": " + self.text[description], True, (127, 0, 0))
            surf.blit(text_surf, (10, 10 + i*40))
