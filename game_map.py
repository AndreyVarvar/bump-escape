import settings as stt
import pygame as pg


class Map:
    def __init__(self):
        EVERYTHING_WE_NEED_TO_KNOW_ABOUT_THIS_MAP = self.load_map()

    def load_map(self):
        map_layout_image = pg.image.load("assets/images/map.png")
        map_layout_image_size = map_layout_image.get_size()
        map_map = pg.Surface((map_layout_image_size[0], map_layout_image_size[1]))
