import pygame as pg
from math import acos, dist


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
    x1, y1 = rect.bottomright

    vertices = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

    return vertices


def xor(a, b):
    return not (a and b) and (a or b)


def find_angle_between_points(p1, p2, p3):
    return acos(
        (dist(p2, p1) ** 2 + dist(p2, p3) ** 2 - dist(p1, p3) ** 2)
        / (2 * dist(p1, p2) * dist(p2, p3))
    )


def draw_outline(surf: pg.Surface, thickness):
    outlined_surf = pg.Surface(
        (surf.get_width() + thickness, surf.get_height() + thickness), pg.SRCALPHA
    )

    mask = pg.mask.from_surface(surf)
    mask_surf = mask.to_surface()
    mask_surf.set_colorkey((0, 0, 0))

    for x in range(mask_surf.get_width()):
        for y in range(mask_surf.get_height()):
            if mask_surf.get_at((x, y)) == (255, 255, 255):
                mask_surf.set_at((x, y), (1, 1, 1))

    outlined_surf.blit(mask_surf, (2 * thickness, thickness))
    outlined_surf.blit(mask_surf, (0, thickness))
    outlined_surf.blit(mask_surf, (thickness, 2 * thickness))
    outlined_surf.blit(mask_surf, (thickness, 0))

    outlined_surf.blit(surf, (thickness, thickness))

    return outlined_surf
