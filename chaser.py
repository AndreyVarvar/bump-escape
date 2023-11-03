import settings as stt
import pygame as pg
from shape import Circle
import pymunk as pm
import game_math as gm
from math import cos, sin, degrees as deg, radians as rad, pi, dist

from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder


class Chaser:
    def __init__(self, pos, map_array):
        self.grid = Grid(matrix=map_array)
        self.matrix_size = (len(map_array[0]), len(map_array))

        self.finder = DijkstraFinder()

        self.image = pg.transform.scale_by(pg.image.load("assets/images/roomba.png"), 2).convert_alpha()

        image_size = self.image.get_size()
        self.rect = Circle((pos[0] - image_size[0] // 2, pos[1]), stt.cell_size//2-10)

        self.prev_player_pos = (0, 0)
        self.prev_chase_pos = (1, 1)

        self.rect.body.angular_velocity = 0

        self.path = []

    def find_path(self, player_pos):
        player_pos_in_matrix = (int(player_pos[1] // stt.cell_size),
                                int(player_pos[0] // stt.cell_size))
        chaser_pos_in_matrix = (int(self.rect.body.position.y // stt.cell_size),
                                int(self.rect.body.position.x // stt.cell_size))

        if self.prev_chase_pos != chaser_pos_in_matrix or self.prev_player_pos != player_pos_in_matrix:
            self.grid.cleanup()

            self.prev_chase_pos = chaser_pos_in_matrix
            self.prev_player_pos = player_pos_in_matrix

            start = self.grid.node(*chaser_pos_in_matrix)
            end = self.grid.node(*player_pos_in_matrix)

            path, runs = self.finder.find_path(start, end, self.grid)
            # i don't need 'runs' variable
            stt.debugger.update("path", "calculating")

            path = self.find_turns(path)
            return path
        else:
            stt.debugger.update("path", "not calculating")
            return self.path

    def update(self, dt, player_pos):
        self.path = self.find_path(player_pos)

        next_cell_pos = list(self.path[1])
        next_cell = pg.Rect(next_cell_pos[1] * stt.cell_size, next_cell_pos[0] * stt.cell_size, stt.cell_size, stt.cell_size)

        looking = pm.Vec2d(-sin(self.rect.body.angle), cos(self.rect.body.angle))  # the trigonometric functions are swapped, because instead of calculating angle from positive x-axis, pymunk calculates it from positive y-axis
        target = pm.Vec2d(self.rect.body.position.x - next_cell.centerx, self.rect.body.position.y - next_cell.centery)

        # for some reason angle on vectors is calculated from negative x-axis... WHAT IS GOING ON
        looking_ang = looking.angle + pi
        target_ang = target.angle + pi

        if self.rect.body.angle < 0:
            self.rect.body.angle += 2*pi
        elif self.rect.body.angle >= 2*pi:
            self.rect.body.angle -= 2*pi

        # rotate towards target location
        power = 10
        if abs(looking_ang - target_ang) < pi:
            power = 3

        if looking_ang < target_ang:
            self.rect.body.angular_velocity = power
        else:
            self.rect.body.angular_velocity = -power

        if abs(looking_ang - target_ang) < pi/8:
            self.rect.body.apply_force_at_local_point((0, -5*10**5))
        else:
            self.rect.body.velocity = pm.Vec2d(self.rect.body.velocity.x//1.2, self.rect.body.velocity.y//1.2)

        # debugging
        stt.debugger.update("next_cell", str(next_cell))
        stt.debugger.update("path_len", str(len(self.path)))
        stt.debugger.update("roomba_pos", str(self.rect.body.position))
        stt.debugger.update("roomba_angle", str(self.rect.body.angle))
        stt.debugger.update("looking_vector", str(looking))
        stt.debugger.update("target_vector", str(target))
        stt.debugger.update("looking_angle", str(looking_ang))
        stt.debugger.update("target_angle", str(target_ang))

    def draw(self, dt, camera):
        image = pg.transform.rotate(self.image, deg(-self.rect.body.angle))
        image_rect = image.get_rect(center=self.rect.body.position)

        camera.blit(image, image_rect)

    @staticmethod
    def find_turns(path):
        prev_cells = [list(path[0]), list(path[1])]
        turns = [path[0]]
        for node in path[2:-1]:
            cell = list(node)
            cell_prev = prev_cells[1]
            cell_prev_prev = prev_cells[0]

            if cell[0] == cell_prev[0] == cell_prev_prev[0] or cell[1] == cell_prev[1] == cell_prev_prev[1]:
                prev_cells.pop(0)
                prev_cells.append(list(node))
            else:
                turns.append(prev_cells[1])
                prev_cells.pop(0)
                prev_cells.append(list(node))

        turns.append(path[-1])

        return turns
