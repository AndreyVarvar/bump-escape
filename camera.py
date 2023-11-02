import settings as stt
import pygame as pg


class Camera:
    def __init__(self, pos):
        self.frame = pg.Surface((stt.D_W, stt.D_H), pg.SRCALPHA)
        self.rect = pg.FRect(pos, self.frame.get_size())

    def follow(self, pos, bounds):
        self.rect.bottomright = pos

        if self.rect.width < bounds.width:
            self.rect.centerx = bounds.centerx
        elif self.rect.left < bounds.left:
            self.rect.left = bounds.left
        elif self.rect.right > bounds.right:
            self.rect.right = bounds.right

        if self.rect.height < bounds.height:
            self.rect.centery = bounds.centery
        elif self.rect.top < bounds.top:
            self.rect.top = bounds.top
        elif self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom

        print(self.rect)

    def draw(self, surf):
        surf.blit(self.frame, (0, 0))

    def blit(self, surf, pos):
        self.frame.blit(surf, (pos[0]-self.rect.centerx, pos[1]-self.rect.centery))

    def clear(self):
        self.frame.fill("white")
