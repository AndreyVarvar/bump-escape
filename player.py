import settings as stt
import pygame as pg
from math import radians as rad, sin, cos
from game_math import clamp
import pymunk as pm


class Player:
    def __init__(self, pos):
        self.pos = pg.Vector2(pos)

        self.image = pg.transform.scale_by(pg.image.load("assets/images/kart.png"), 3)
        self.rotation = 90  # degrees

        self.movement = {"forward": False, "backward": False, "left-turn": False, "right-turn": False}

        self.current_image = self.get_image()

        self.speed = pg.Vector2()
        self.acceleration = 5
        self.max_speed = 100

        # PHYSICS YEAAH BABYYY
        self.rect = pm.Body()
        self.rect.position = self.pos.x, -self.pos.y  # because y-axis is inverted in pygame and not in pymunk space

        self.poly = pm.Poly.create_box(self.rect)
        self.poly.mass = 100

        stt.space.add(self.rect, self.poly)

        self.rotation_speed = 1

    def update(self, *args):
        dt = args[0]

        # update the image
        self.current_image = self.get_image()

        # change position based on movement
        if self.movement["forward"] is True:
            self.speed.x += cos(rad(self.rotation)) * self.acceleration * dt
            self.speed.y -= sin(rad(self.rotation)) * self.acceleration * dt

        if self.movement["backward"] is True:
            self.speed.x -= cos(rad(self.rotation)) * self.acceleration * dt
            self.speed.y += sin(rad(self.rotation)) * self.acceleration * dt

        if (self.movement["forward"] is True and self.movement["backward"] is True) or (self.movement["forward"] is False and self.movement["backward"] is False):
            self.speed.x /= 1.1
            self.speed.y /= 1.1

        self.speed.clamp_magnitude_ip(self.max_speed) if self.speed.magnitude() > 0 else "uhh"

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        # rotate or SPIN
        if self.movement["left-turn"] is True:
            self.rotation += self.speed.magnitude() * self.rotation_speed

        if self.movement["right-turn"] is True:
            self.rotation -= self.speed.magnitude() * self.rotation_speed


        if self.rotation < 0:
            self.rotation += 360
        elif self.rotation >= 360:
            self.rotation -= 360

    def draw(self, *args):
        dt = args[0]
        surf = args[1]

        image_rect = self.current_image.get_rect(center=self.pos)

        surf.blit(self.current_image, image_rect)

    def handle_events(self, *args):
        events = args[0]
        keys_pressed = args[1]

        self.movement["forward"] = keys_pressed[pg.K_w] or keys_pressed[pg.K_UP]
        self.movement["backward"] = keys_pressed[pg.K_s] or keys_pressed[pg.K_DOWN]
        self.movement["left-turn"] = keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]
        self.movement["right-turn"] = keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT]

    def get_image(self):
        image = pg.transform.rotate(self.image, self.rotation-90)

        return image
