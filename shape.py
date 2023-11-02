import settings as stt
import pymunk as pm
import pygame as pg
import game_math as gm


# this code was stolen from official example online (stealing is the key to success)

class Box:
    def __init__(self, rect: pg.FRect, d=2):
        vertices = gm.get_rect_points_as_polygon(rect)

        for i in range(4):
            segment = pm.Segment(stt.space.static_body, vertices[i], vertices[(i+1) % 4], d)
            segment.elasticity = 1
            segment.friction = 1
            stt.space.add(segment)


class Polygon:
    def __init__(self, pos, vertices, density=0.1):
        self.body = pm.Body(1, 100)
        self.body.position = pos

        shape = pm.Poly(self.body, vertices)
        shape.density = density
        shape.elasticity = 1
        stt.space.add(self.body, shape)


class Rectangle:
    def __init__(self, rect: pg.FRect | pg.Rect):
        self.body = pm.Body()
        self.body.position = rect.center

        shape = pm.Poly.create_box(self.body, rect.size)
        shape.density = 0.1
        shape.elasticity = 1
        shape.friction = 1
        stt.space.add(self.body, shape)


class Circle:
    def __init__(self, pos, radius=50, body_type=pm.Body.DYNAMIC):
        self.body = pm.Body(body_type=body_type)
        self.body.position = pos

        shape = pm.Circle(self.body, radius)

        if body_type != pm.Body.STATIC:
            shape.density = 0.1

        shape.elasticity = 1
        shape.friction = 1

        stt.space.add(self.body, shape)
