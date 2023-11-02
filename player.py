import settings as stt
import pygame as pg
from math import radians as rad, sin, cos, sqrt, degrees as deg, pi
import pymunk as pm
from shape import Rectangle
import game_math as gm


class Player:
    def __init__(self, pos):
        self.pos = pg.Vector2(pos)

        self.image = pg.transform.scale_by(pg.image.load("assets/images/kart.png"), 3)
        self.rotation = 90  # degrees

        self.movement = {"forward": False, "backward": False, "left-turn": False, "right-turn": False}

        self.speed = 0
        self.acceleration = 5

        # PHYSICS YEAAH BABYYY
        image_size = self.image.get_size()
        player_physcis_rect = pg.FRect((self.pos.x - image_size[0]/2, self.pos.y - image_size[1]/2), image_size)
        self.rect = Rectangle(player_physcis_rect)

        self.rotation_speed = pi  # radians

        self.current_image = self.get_image()

    def update(self, *args):
        dt = args[0]
        bounds = args[1]

        # update the image
        self.current_image = self.get_image()

        # change position based on movement
        velocity_vector = pg.Vector2(self.rect.body.velocity)
        looking = pg.Vector2(cos(rad(self.rotation)), -sin(rad(self.rotation)))
        if self.rect.body.velocity.length > 0:
            self.rect.body.velocity = pm.Vec2d(*list(pg.Vector2.lerp(velocity_vector.normalize(), looking, 0.01) * self.rect.body.velocity.length))

        if self.movement["forward"]:
            pulling_force = (10**5 * cos(rad(self.rotation)),
                             10**5 * -sin(rad(self.rotation)))  # don't ask why this exact number

            self.rect.body.apply_force_at_local_point(pulling_force)

        if self.movement["backward"]:
            self.speed += self.acceleration * dt

            pulling_force = (10**5 * -cos(rad(self.rotation)),
                             10**5 * sin(rad(self.rotation)))  # don't ask why this exact number

            self.rect.body.apply_force_at_local_point(pulling_force)

        # rotate or SPIN
        if gm.xor(self.movement["right-turn"], self.movement["left-turn"]):
            angle_change = self.rotation_speed * dt

            if self.movement["left-turn"]:
                angle_change = -angle_change

            self.rect.body.angular_velocity += angle_change

        self.rect.body.angular_velocity /= 1.01

        if self.rotation < 0:
            self.rotation += 360
        elif self.rotation >= 360:
            self.rotation -= 360

        # make sure player doesn't get out of bounds
        boundaries = {"top": False, "bottom": False, "left": False, "right": False}

        if self.rect.body.position.x < bounds.left:
            self.rect.body.position = pm.Vec2d(bounds.left, self.rect.body.position.y)
            self.rect.body.velocity = (0, self.rect.body.velocity.y)
            boundaries["left"] = True
        elif self.rect.body.position.x > bounds.right:
            self.rect.body.position = pm.Vec2d(bounds.right, self.rect.body.position.y)
            self.rect.body.velocity = (0, self.rect.body.velocity.y)
            boundaries["right"] = True

        if self.rect.body.position.y < bounds.top:
            self.rect.body.position = pm.Vec2d(self.rect.body.position.x, bounds.top)
            self.rect.body.velocity = (self.rect.body.velocity.x, 0)
            boundaries["top"] = True
        elif self.rect.body.position.y > bounds.bottom:
            self.rect.body.position = pm.Vec2d(self.rect.body.position.x, bounds.bottom)
            self.rect.body.velocity = (self.rect.body.velocity.x, 0)
            boundaries["bottom"] = True

        stt.debugger.update("player_pos", str(self.rect.body.position))
        stt.debugger.update("player_uhh", str(boundaries))
        stt.debugger.update("player_angle", str(self.rect.body.angle))

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
