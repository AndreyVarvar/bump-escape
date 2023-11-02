import settings as stt
import pygame as pg
from shape import Circle


class Map:
    def __init__(self):
        self.tyre_image = pg.image.load("assets/images/tire.png").convert_alpha()

        EVERYTHING_WE_NEED_TO_KNOW_ABOUT_THIS_MAP = self.load_map()

    def load_map(self):
        map_layout_image = pg.image.load("assets/images/map.png")
        map_layout_image_size = map_layout_image.get_size()

        map_map = pg.Surface((map_layout_image_size[0] * stt.cell_size, map_layout_image_size[1] * stt.cell_size))

        for x in range(map_layout_image_size[0]):
            for y in range(map_layout_image_size[1]):
                pixel = map_layout_image.get_at((x, y))

                if pixel == (16, 18, 28):
                    map_map.blit(self.tyre_image, ())


        return "map_image", "pymunk_bodies"
