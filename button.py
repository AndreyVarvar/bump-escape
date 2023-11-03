import settings as stt
import pygame as pg
from font import Font
import game_math as gm


class Button:
    def __init__(self,
                 rect: pg.Rect,
                 primary_color: pg.Color | tuple[int, int, int],
                 secondary_color: pg.Color | tuple[int, int, int],
                 hover_primary_color: pg.Color | tuple[int, int, int],
                 hover_secondary_color: pg.Color | tuple[int, int, int],
                 text: str,
                 outline_text: bool,
                 corner_radius: int,
                 font: Font,
                 text_scale=3):

        self.rect = rect
        self.color = primary_color
        self.outline_color = secondary_color

        self.hover_color = hover_primary_color
        self.hover_outline_color = hover_secondary_color

        self.corner_radius = corner_radius

        self.font = font
        self.text = self.font.render(text, text_scale, outline_text)
        self.text_pos = (self.rect.x + (self.rect.width - self.text.get_width())/2,
                         self.rect.y + (self.rect.height - self.text.get_height())/2)

        self.hovered = False
        self.clicked = False

    def update(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True

            if mouse_pressed[0]:
                self.clicked = True
            else:
                self.clicked = False
        else:
            self.hovered = False

    def draw(self, surf):
        color1 = self.hover_color if gm.xor(self.hovered, self.clicked) else self.color
        color2 = self.hover_outline_color if gm.xor(self.hovered, self.clicked) else self.outline_color
        pg.draw.rect(surf, color1, self.rect, 0, self.corner_radius)
        pg.draw.rect(surf, color2, self.rect, 4, self.corner_radius)

        surf.blit(self.text, self.text_pos)
