import pygame as pg


class Slider:
    def __init__(self,
                 rect: pg.Rect,
                 min_value: float,
                 max_value: float,
                 initial_value: float,
                 step: float,
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

        self.value = initial_value
        self.value_rounding_accuracy = value_rounding_accuracy

    def calculate_slider_value(self):
        self.value = self.min_value + round((self.x - self.rail.x)*(self.range / self.rect.width), self.value_rounding_accuracy)
        self.value = max(self.min_value, min(self.max_value, self.value))

    def calculate_slider_pos(self):
        self.x = round(self.x/self.positional_step)*self.positional_step

    def update(self, mouse_pos, mouse_pressed, cursor_busy):
        if not mouse_pressed[0]:
            self.clicked = False
        else:
            if self.clicked:
                self.clamp_rail(mouse_pos)
                self.calculate_slider_pos()
                self.calculate_slider_value()

                self.x = max(self.rail.x, min(self.x, self.rail.x + self.rail.width))  # if the position eve gets out of bounds, it will get corrected here
            else:
                if self.rect.collidepoint(mouse_pos) and not cursor_busy:
                    self.clicked = True

    def clamp_rail(self, mouse_pos):
        self.x = max(self.rail.left, min(mouse_pos[0], self.rail.right))

    def draw(self, surf):
        left_side = pg.Rect(self.rect.x, self.rect.y, self.x - self.rect.x, self.rect.height)
        right_side = pg.Rect(self.x, self.rect.y, self.rect.width - (self.x - self.rect.x), self.rect.height)

        pg.draw.rect(surf, (247, 243, 183), left_side)
        pg.draw.rect(surf, (243, 168, 50), left_side, 4)

        pg.draw.rect(surf, (236, 39, 63), right_side)
        pg.draw.rect(surf, (107, 38, 66), right_side, 4)

        pg.draw.circle(surf, (247, 243, 183), (self.x, self.y), 20)
        pg.draw.circle(surf, (243, 168, 50), (self.x, self.y), 20, 4)
