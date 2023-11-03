import pygame as pg
from consts import colors


class Slider:
    def __init__(self,
                 rect: pg.Rect,
                 min_value: float,
                 max_value: float,
                 initial_value: float,
                 step: float,
                 slide_sound_path: str,
                 sfx_volume: float,
                 value_rounding_accuracy=5
                 ):
        self.min_value = min_value
        self.max_value = max_value
        self.range = self.max_value - self.min_value
        self.rect = rect
        self.step = step
        self.rail = rect.inflate(0, -0.8 * rect.height)
        self.x, self.y = rect.x + rect.width*(initial_value/self.range), rect.centery  # position of the knob
        self.height = int(rect.width * 0.075)
        self.clicked = False
        self.positional_step = self.rail.width / (self.range / self.step)

        self.prev_x = self.x

        self.slide_sound = pg.mixer.Sound(slide_sound_path)
        self.sfx_volume = sfx_volume
        self.slide_sound.set_volume(0.2*sfx_volume)

        self.value = initial_value
        self.value_rounding_accuracy = value_rounding_accuracy

    def calculate_slider_value(self) -> None:
        self.value = self.min_value + round((self.x - self.rail.x)*(self.range / self.rect.width), self.value_rounding_accuracy)
        self.value = max(self.min_value, min(self.max_value, self.value))

    def calculate_slider_pos(self) -> None:
        self.x = round(self.x/self.positional_step)*self.positional_step

    def update(self, mouse_pos, mouse_pressed, cursor, sfx_volume=None) -> None:
        if sfx_volume is not None:
            if sfx_volume != self.sfx_volume:
                self.sfx_volume = sfx_volume
                self.slide_sound.set_volume(0.2*sfx_volume)

        if not mouse_pressed[0]:
            self.clicked = False
        else:
            if self.clicked:
                self.clamp_rail(mouse_pos)
                self.calculate_slider_pos()
                self.calculate_slider_value()

                self.x = max(self.rail.x, min(self.x, self.rail.x + self.rail.width))  # if the position eve gets out of bounds, it will get corrected here

                if self.x != self.prev_x:
                    self.slide_sound.play()
                    self.prev_x = self.x
            else:
                if self.rect.collidepoint(mouse_pos) and not cursor.busy:
                    cursor.busy = True
                    self.clicked = True

    def clamp_rail(self, mouse_pos) -> None:
        self.x = max(self.rail.left, min(mouse_pos[0], self.rail.right))

    def draw(self, surf) -> None:
        left_side = pg.Rect(self.rect.x, self.rect.y, self.x - self.rect.x, self.rect.height)
        right_side = pg.Rect(self.x, self.rect.y, self.rect.width - (self.x - self.rect.x), self.rect.height)

        pg.draw.rect(surf, colors["banana"], left_side)
        pg.draw.rect(surf, colors["orange"], left_side, 4)

        pg.draw.rect(surf, colors["dark-red"], right_side)
        pg.draw.rect(surf, colors["very-dark-red"], right_side, 4)

        pg.draw.circle(surf, colors["banana"], (self.x, self.y), 20)
        pg.draw.circle(surf, colors["orange"], (self.x, self.y), 20, 4)
