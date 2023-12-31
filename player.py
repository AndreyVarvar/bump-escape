import settings as stt
import pygame as pg
from math import sin, cos, degrees as deg, pi
import pymunk as pm
from shape import Rectangle
import game_math as gm


class Player:
    def __init__(self, pos, collision_type):
        self.pos = pg.Vector2(pos)

        self.image = pg.transform.scale_by(pg.image.load("assets/images/kart.png"), 2.8)
        self.rotation = 90  # degrees

        self.movement = {
            "forward": False,
            "backward": False,
            "left-turn": False,
            "right-turn": False,
        }

        self.prev_velocity = pm.Vec2d(0, 0)

        self.collision_sound = pg.mixer.Sound("assets/sfx/bump.ogg")

        # PHYSICS YEAAH BABYYY
        image_size = self.image.get_size()
        player_physcis_rect = pg.FRect(
            (self.pos.x - image_size[0] / 2, self.pos.y - image_size[1] / 2), image_size
        )
        self.rect = Rectangle(player_physcis_rect)

        self.rect.shape.collision_type = collision_type

        self.rotation_speed = pi  # radians

        self.current_image = self.get_image()

        self.sfx_volume = 1

    def update(self, *args):
        dt = args[0]
        self.sfx_volume = args[1]

        # update the image
        self.current_image = self.get_image()

        # change position based on movement
        if self.movement["forward"]:
            self.rect.body.apply_force_at_local_point((0, -(10**5) * 1.5))

        if self.movement["backward"]:
            self.rect.body.apply_force_at_local_point((0, 10**5 * 1.5))

        # rotate or SPIN
        if gm.xor(self.movement["right-turn"], self.movement["left-turn"]):
            angle_change = self.rotation_speed * dt

            if self.movement["left-turn"]:
                angle_change = -angle_change

            self.rect.body.angular_velocity += angle_change

        self.rect.body.angular_velocity /= 1.01

        if self.rect.body.angle < 0:
            self.rect.body.angle += 2 * pi
        elif self.rect.body.angle >= 2 * pi:
            self.rect.body.angle -= 2 * pi

        stt.debugger.update("player_pos", str(self.rect.body.position))
        stt.debugger.update("player_angle", str(self.rect.body.angle))
        # stt.debugger.update("player_velocity", str((round(self.rect.body.velocity[0], 2), round(self.rect.body.velocity[1], 2))))
        # stt.debugger.update("angle_vector", str(self.rect.body.rotation_vector))
        # stt.debugger.update("looking", str(looking))

    def draw(self, *args):
        dt = args[0]
        surf = args[1]

        image_rect = self.current_image.get_rect(center=self.rect.body.position)

        surf.blit(self.current_image, image_rect)

    def handle_events(self, *args):
        events = args[0]
        keys_pressed = args[1]

        self.movement["forward"] = keys_pressed[pg.K_w] or keys_pressed[pg.K_UP]
        self.movement["backward"] = keys_pressed[pg.K_s] or keys_pressed[pg.K_DOWN]
        self.movement["left-turn"] = keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]
        self.movement["right-turn"] = keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT]

    def get_image(self):
        image = pg.transform.rotate(self.image, -deg(self.rect.body.angle))

        return image

    def play_sound(self, arbiter, space, data):
        self.collision_sound.set_volume(
            (1 - (1 / ((self.rect.body.kinetic_energy / (5 * 10**7)) + 1)))
            * self.sfx_volume
        )
        self.collision_sound.play()
        return True
