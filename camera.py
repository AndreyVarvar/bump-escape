import settings as stt
import pygame as pg


class Camera:
    def __init__(self, pos):
        self.frame = pg.Surface((stt.D_W, stt.D_H), pg.SRCALPHA)
        frame_size = self.frame.get_size()
        self.rect = pg.FRect((-stt.D_W//2, pos[1]-frame_size[1]//2), self.frame.get_size())

    def follow(self, pos):
        self.rect.bottom = pos[1]  # i don't understand myself why bottomright

        if self.rect.bottom > 23250:
            self.rect.bottom = 23250

    def draw(self, surf):
        surf.blit(self.frame, (0, 0))

    def blit(self, surf, pos):
        self.frame.blit(surf, (pos[0]-self.rect.x - self.rect.width//2, pos[1]-self.rect.y - self.rect.height//2))

    def clear(self):
        self.frame.fill("white")
