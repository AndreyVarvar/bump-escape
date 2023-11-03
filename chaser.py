import settings as stt
import pygame as pg
import pymunk as pm
from math import cos, sin, degrees as deg, pi, dist

from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder


class Chaser:
    def __init__(self, pos, map_array, collision_type, difficulty=1):
        self.grid = Grid(matrix=map_array)
        self.matrix_size = (len(map_array[0]), len(map_array))

        self.finder = DijkstraFinder()

        self.radius = stt.cell_size//2 - 5

        self.difficulty = difficulty

        self.image = pg.transform.scale(pg.image.load("assets/images/roomba.png"), (self.radius*2, self.radius*2)).convert_alpha()

        self.body = pm.Body(body_type=pm.Body.DYNAMIC)
        self.body.position = pos
        self.circ = pm.Circle(self.body, self.radius)
        self.circ.density = 0.1
        self.circ.elasticity = 1
        self.circ.friction = 1

        self.circ.collision_type = collision_type

        stt.space.add(self.body, self.circ)

        self.collision_sound = pg.mixer.Sound("assets/sfx/bump.ogg")


        self.prev_player_pos = (0, 0)
        self.prev_chase_pos = (1, 1)

        self.circ.body.angular_velocity = 0

        self.path = []

        self.sfx_volume = 1

    def find_path(self, player_pos):
        player_pos_in_matrix = (int(player_pos[1] // stt.cell_size),
                                int(player_pos[0] // stt.cell_size))
        chaser_pos_in_matrix = (int(self.circ.body.position.y // stt.cell_size),
                                int(self.circ.body.position.x // stt.cell_size))

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

    def update(self, dt, player_pos, sfx_volume):
        self.path = self.find_path(player_pos)
        self.sfx_volume = sfx_volume

        next_cell_pos = list(self.path[1 if len(self.path) >= 2 else 0])
        next_cell = pg.Rect(next_cell_pos[1] * stt.cell_size, next_cell_pos[0] * stt.cell_size, stt.cell_size, stt.cell_size)

        looking = pm.Vec2d(-sin(self.circ.body.angle), cos(self.circ.body.angle))  # the trigonometric functions are swapped, because instead of calculating angle from positive x-axis, pymunk calculates it from positive y-axis
        target = pm.Vec2d(self.circ.body.position.x - next_cell.centerx, self.circ.body.position.y - next_cell.centery)

        # for some reason angle on vectors is calculated from negative x-axis... WHAT IS GOING ON
        looking_ang = looking.angle + pi
        target_ang = target.angle + pi

        if self.circ.body.angle < 0:
            self.circ.body.angle += 2*pi
        elif self.circ.body.angle >= 2*pi:
            self.circ.body.angle -= 2*pi

        # rotate towards target location
        power = 10
        if abs(looking_ang - target_ang) < pi:
            power = 3

        if looking_ang < target_ang:
            self.circ.body.angular_velocity = power
        else:
            self.circ.body.angular_velocity = -power

        if abs(looking_ang - target_ang) < pi/8:
            self.circ.body.apply_force_at_local_point((0, -self.difficulty*10**5))
        else:
            self.circ.body.velocity = pm.Vec2d(self.circ.body.velocity.x//1.2, self.circ.body.velocity.y//1.2)

        # debugging
        # stt.debugger.update("next_cell", str(next_cell))
        # stt.debugger.update("path_len", str(len(self.path)))
        # stt.debugger.update("roomba_pos", str(self.circ.body.position))
        # stt.debugger.update("roomba_angle", str(self.circ.body.angle))
        # stt.debugger.update("looking_vector", str(looking))
        # stt.debugger.update("target_vector", str(target))
        # stt.debugger.update("looking_angle", str(looking_ang))
        # stt.debugger.update("target_angle", str(target_ang))

    def draw(self, dt, camera):
        image = pg.transform.rotate(self.image, deg(-self.circ.body.angle))
        image_rect = image.get_rect(center=self.circ.body.position)

        camera.blit(image, image_rect)

    @staticmethod
    def find_turns(path):
        if len(path) >= 2:
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
        else:
            return path

    def play_sound(self, arbiter, space, data):
        player_pos = self.prev_player_pos[0]*stt.cell_size, self.prev_player_pos[1]*stt.cell_size
        volume = -dist(player_pos, self.circ.body.position)/(5*stt.cell_size) + 1

        if volume < 0:
            volume = 0
        self.collision_sound.set_volume(volume*self.sfx_volume)
        self.collision_sound.play()
        return True
