import settings as stt
import pygame as pg
from shape import Circle
import pymunk as pm
from shape import Box


class Checkpoints:
    def __init__(self):
        self.checkpoints: list[pg.Rect]
        self.checkpoints = []
        self.current_checkpoint = None

    def add_checkpoint(self, checkpoint: pg.Rect):
        self.checkpoints.append(checkpoint)

    def update(self, player_pos):
        for checkpoint in self.checkpoints:
            if checkpoint.collidepoint(player_pos):
                self.current_checkpoint = checkpoint
                return  # terminate the process


class Map:
    def __init__(self):
        self.tyre_image = pg.transform.scale(pg.image.load("assets/images/tire.png"), (stt.cell_size, stt.cell_size)).convert_alpha()
        self.checkpoint_image = pg.transform.scale(pg.image.load("assets/images/checkpoint.png"), (stt.cell_size, stt.cell_size)).convert_alpha()
        self.road_image = pg.transform.scale_by(pg.image.load("assets/images/road.png"), 4).convert_alpha()

        EVERYTHING_WE_NEED_TO_KNOW_ABOUT_THIS_MAP = self.load_map()

        self.map, self.objects, self.checkpoints, self.boundaries, self.array = EVERYTHING_WE_NEED_TO_KNOW_ABOUT_THIS_MAP

    def draw(self, camera):
        camera.blit(self.map, (0, 0))

    def load_map(self):
        map_layout_image = pg.image.load("assets/images/map.png")
        map_layout_image_size = map_layout_image.get_size()

        map_map = pg.Surface((map_layout_image_size[0] * stt.cell_size, map_layout_image_size[1] * stt.cell_size), pg.SRCALPHA)
        objects = []
        checkpoints = Checkpoints()
        map_array = []

        bounds_rect = pg.FRect(0, 0, stt.D_W,map_layout_image_size[1] * stt.cell_size - 20)

        bounds = Box(bounds_rect)

        for i in range(int(map_map.get_height()/self.road_image.get_height())):
            map_map.blit(self.road_image, (0, i*self.road_image.get_height()))

        for x in range(map_layout_image_size[0]):
            map_array_row = []

            for y in range(map_layout_image_size[1]):
                pixel = map_layout_image.get_at((x, y))

                if pixel == (16, 18, 28):
                    map_map.blit(self.tyre_image, (stt.cell_size*x, stt.cell_size*y))
                    objects.append(Circle((stt.cell_size*(x+0.5), stt.cell_size*(y+0.5)), stt.cell_size/2, pm.Body.STATIC))
                    map_array_row.append(0)

                elif pixel == (255, 255, 255):
                    map_map.blit(self.checkpoint_image, (stt.cell_size * x, stt.cell_size * y))
                    checkpoints.add_checkpoint(pg.Rect(x*stt.cell_size, y*stt.cell_size, stt.cell_size, stt.cell_size))
                    map_array_row.append(1)

                else:
                    map_array_row.append(1)

            map_array.append(map_array_row)

        checkpoints.current_checkpoint = pg.Rect(stt.D_W//2 - stt.cell_size//2, map_layout_image_size[1]*stt.cell_size-stt.D_H//2, stt.cell_size, stt.cell_size)

        return map_map, objects, checkpoints, bounds, map_array
