import settings as stt
import pygame as pg
from player import Player
import pymunk as pm


class Game:
    def __init__(self):
        # app stuff
        self.display = stt.DISPLAY

        self.clock = pg.time.Clock()
        self.FPS = stt.FPS

        self.running = True

        # TEMPORARY!!!
        # self.test = pm.Body()
        # self.test.pos = 100, 100
        # self.test.mass = 1
        # self.poly = pm.Poly.create_box(self.test)

        # stt.space.add(self.test, self.poly)
        # TEMPORARY!!!

        # main characters (not durk)
        # self.player = Player((100, 100))

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
            # self.update(dt)
            self.draw(dt)

    def update(self, dt):
        # self.player.update(dt)
        pass
        # stt.space.step(1/self.FPS)

    def draw(self, dt):
        self.display.fill("white")

        # self.display.blit(pg.transform.scale_by(pg.image.load("assets/images/road.png"), 4), (0, 0))
        #
        # self.player.draw(dt, self.display)
        # pg.draw.circle(self.display, (255, 0, 0), self.test.pos, 20)

        pg.display.update()

    def handle_events(self, dt, events, keys_pressed, mouse_pressed, mouse_pos):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

        # self.player.handle_events(events, keys_pressed)


i_am_tired_of_writing_long_name_on_these_variables_for_fun = Game()
i_am_tired_of_writing_long_name_on_these_variables_for_fun.run()
