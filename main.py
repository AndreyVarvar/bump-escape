import game_math as gm
import settings as stt
import pygame as pg
from player import Player
import pymunk as pm
import pymunk.pygame_util as pg_util
from camera import Camera


class Game:
    def __init__(self):
        # app stuff
        self.display = stt.DISPLAY

        self.clock = pg.time.Clock()
        self.FPS = stt.FPS

        self.running = True

        self.draw_options = pg_util.DrawOptions(self.display)

        # main characters (not durk)
        self.player = Player((100, 100))
        self.camera = Camera((100, 100))

    def run(self):
        while self.running:
            # update some variables
            dt = self.clock.tick(self.FPS) / 1000

            keys_pressed = pg.key.get_pressed()
            mouse_pressed = pg.mouse.get_pressed()
            mouse_pos = pg.mouse.get_pos()

            events = pg.event.get()

            # process what just happened
            self.handle_events(dt, events, keys_pressed, mouse_pressed, mouse_pos)
            self.update(dt)
            self.draw(dt)

    def update(self, dt):
        self.player.update(dt, pg.Rect(0, stt.D_W, 0, stt.D_H))
        stt.space.step(1/self.FPS)

        self.camera.follow(self.player.rect.body.position, pg.Rect(0, stt.D_W, 0, stt.D_H))

    def draw(self, dt):
        self.display.fill("white")
        self.camera.clear()

        road = pg.transform.scale_by(pg.image.load("assets/images/road.png"), 4)

        self.camera.blit(road, (0, 0))
        self.player.draw(dt, self.camera)

        self.camera.draw(self.display)

        pg.display.update()

    def handle_events(self, dt, events, keys_pressed, mouse_pressed, mouse_pos):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

        self.player.handle_events(events, keys_pressed)


i_am_tired_of_writing_long_name_on_these_variables_for_fun = Game()
i_am_tired_of_writing_long_name_on_these_variables_for_fun.run()
