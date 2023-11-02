import settings as stt
import pygame as pg


def clamp(n, min_n, max_n):
    if n < min_n:
        return min_n
    if n > max_n:
        return max_n

    return n


def convert_pos(pos):
    return pos[0], -pos[1]


def get_rect_points_as_polygon(rect: pg.FRect | pg.Rect):
    x0, y0 = convert_pos(rect.topleft)
    x1, y1 = convert_pos(rect.bottomright)

    vertices = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

    return vertices


def xor(a, b):
    return not (a and b) and (a or b)
