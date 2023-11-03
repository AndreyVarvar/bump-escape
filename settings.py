import pygame as pg
import pymunk as pm
from debugger import Debugger

# pygame stuff
pg.init()

D_W, D_H = 640, 800
DISPLAY = pg.display.set_mode((D_W, D_H))
pg.display.set_caption("bumpy escape")

FPS = 60

# pymunk stuff
space = pm.Space()
space.gravity = 0, 0  # top down, no gravity

cell_size = D_W/10

channel_sfx = pg.mixer.Channel(0)

debugger = Debugger()
