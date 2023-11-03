import settings as stt
import pygame as pg
from player import Player
import pymunk as pm
import pymunk.pygame_util as pg_util
from camera import Camera
from game_map import Map
from chaser import Chaser
from timer import Timer


class Game:
    def __init__(self):
        # app stuff
        self.display = stt.DISPLAY

        self.clock = pg.time.Clock()
        self.FPS = stt.FPS

        self.running = True

        self.draw_options = pg_util.DrawOptions(self.display)

        # map
        self.map = Map(1)

        # timer
        self.timer = Timer()

        # main characters (not durk)
        obstacles_collision_type = 7
        player_collision_type = 1
        chaser_collision_type = 2

        self.player = Player(self.map.checkpoints.current_checkpoint.center, player_collision_type)
        self.camera = Camera(self.player.rect.body.position)
        self.chaser = Chaser((self.player.rect.body.position.x,
                              self.player.rect.body.position.y + 200),
                             self.map.array, chaser_collision_type)

        self.player_collision_handlers = [stt.space.add_collision_handler(player_collision_type, obstacles_collision_type + i) for i in range(len(self.map.objects)+4)]
        self.chaser_collision_handlers = [stt.space.add_collision_handler(chaser_collision_type, obstacles_collision_type + i) for i in range(len(self.map.objects)+4)]

        self.bounds = self.map.boundaries

    def run(self):
        while self.running:
            # update some variables
            dt = self.clock.tick(self.FPS)/1000

            keys_pressed = pg.key.get_pressed()
            mouse_pressed = pg.mouse.get_pressed()
            mouse_pos = pg.mouse.get_pos()

            events = pg.event.get()

            # process what just happened
            self.handle_events(dt, events, keys_pressed, mouse_pressed, mouse_pos)
            self.update(dt)
            self.draw(dt)

    def update(self, dt):
        self.player.update(dt)
        self.chaser.update(dt, self.player.rect.body.position)
        stt.space.step(1/self.FPS)

        self.camera.follow(self.player.rect.body.position)

        self.timer.update(dt)

        for handler in self.player_collision_handlers:
            handler.begin = self.player.play_sound

        for handler in self.chaser_collision_handlers:
            handler.begin = self.chaser.play_sound

        stt.debugger.update("fps", str(round(1/dt)))

    def draw(self, dt):
        self.display.fill("white")
        self.camera.clear()

        self.map.draw(self.camera)

        # temp = pg.Surface((stt.cell_size, stt.cell_size), pg.SRCALPHA)
        # temp.fill((0, 255, 127))
        # for cell in self.chaser.path:
        #     cell = list(cell)
        #     self.camera.blit(temp, (cell[1]*stt.cell_size, cell[0]*stt.cell_size))

        self.player.draw(dt, self.camera)
        self.chaser.draw(dt, self.camera)

        self.camera.draw(self.display)

        self.timer.draw(self.display)

        # stt.debugger.draw(self.display)

        pg.display.update()

    def handle_events(self, dt, events, keys_pressed, mouse_pressed, mouse_pos):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

        self.player.handle_events(events, keys_pressed)


i_am_tired_of_writing_long_name_on_these_variables_for_fun = Game()
i_am_tired_of_writing_long_name_on_these_variables_for_fun.run()
