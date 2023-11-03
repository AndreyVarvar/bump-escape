import settings as stt
import pygame as pg
from player import Player
import pymunk.pygame_util as pg_util
from camera import Camera
from game_map import Map
from chaser import Chaser
from timer import Timer
from slider import Slider
from button import Button
from font import Font


class BaseScene:
    def __init__(self, name):
        self.name = name
        self.change_scene = False
        self.new_scene = name  # do not change

        self.sfx_volume = 1

    def check_change(self, *args):
        pass

    def reset(self):
        self.new_scene = self.name
        self.change_scene = False


class SettingsScene(BaseScene):
    def __init__(self, display):
        super().__init__("settings")

        self.display = display

        self.slider_sfx = Slider(rect=pg.Rect(120, 120, 400, 20),
                                 min_value=0,
                                 max_value=1,
                                 initial_value=1,
                                 step=0.1)

        self.font = Font("assets/fonts/da_font.png", pg.Color(43, 15, 84), pg.Color(255, 218, 69), 1)
        self.text_sfx = self.font.render("SFX", 5, True)
        self.text_sfx_pos = ((stt.D_W - self.text_sfx.get_width()) // 2, 70)


        self.slider_music = Slider(rect=pg.Rect(120, 220, 400, 20),
                                   min_value=0,
                                   max_value=1,
                                   initial_value=1,
                                   step=0.1)

        self.text_music = self.font.render("music", 5, True)
        self.text_music_pos = ((stt.D_W - self.text_sfx.get_width()) // 2, 170)

        self.button_exit = Button(pg.Rect(20, 20, 100, 50),
                                  (0, 139, 139),
                                  (30, 65, 68),
                                  (109, 234, 214),
                                  (30, 65, 68),
                                  "Back",
                                  True,
                                  5,
                                  self.font)

    def draw(self, *args):
        dt = args[0]
        surf = args[1]

        surf.blit(self.text_sfx, self.text_sfx_pos)
        self.slider_sfx.draw(surf)

        surf.blit(self.text_music, self.text_music_pos)
        self.slider_music.draw(surf)

        self.button_exit.draw(surf)

    def update(self, *args):
        dt = args[0]
        mouse_pos = args[1]
        mouse_pressed = args[2]
        cursor_busy = args[3]

        self.slider_sfx.update(mouse_pos, mouse_pressed, cursor_busy)
        self.slider_music.update(mouse_pos, mouse_pressed, cursor_busy)

        self.button_exit.update(mouse_pos, mouse_pressed)

        if self.button_exit.clicked is True:
            self.new_scene = "main menu"
            self.change_scene = True

    def handle_events(self, *args):
        pass


class GameScene(BaseScene):
    def __init__(self, display):
        super().__init__("game")

        # app stuff
        self.display = display

        self.clock = pg.time.Clock()

        self.draw_options = pg_util.DrawOptions(self.display)

        self.quit = False

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

        self.player_collision_handlers = [stt.space.add_collision_handler(player_collision_type, obstacles_collision_type + i - 3) for i in range(len(self.map.objects) + 4)]
        self.chaser_collision_handlers = [stt.space.add_collision_handler(chaser_collision_type, obstacles_collision_type + i - 3) for i in range(len(self.map.objects) + 4)]

        self.bounds = self.map.boundaries

    def update(self, *args):
        dt = args[0]

        self.player.update(dt, self.sfx_volume)
        self.chaser.update(dt, self.player.rect.body.position, self.sfx_volume)

        stt.space.step(dt)

        self.camera.follow(self.player.rect.body.position)

        self.timer.update(dt)

        for handler in self.player_collision_handlers:
            handler.begin = self.player.play_sound

        for handler in self.chaser_collision_handlers:
            handler.begin = self.chaser.play_sound

        stt.debugger.update("fps", str(round(1 / dt)))

    def draw(self, *args):
        dt = args[0]

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

    def handle_events(self, dt, events, keys_pressed, mouse_pressed, mouse_pos):
        for event in events:
            if event.type == pg.QUIT:
                self.quit = True

        self.player.handle_events(events, keys_pressed)

    def reset(self):
        self.new_scene = self.name
        self.change_scene = False

        # timer
        self.timer = Timer()

        player_collision_type = 1
        chaser_collision_type = 2

        self.player = Player(self.map.checkpoints.current_checkpoint.center, player_collision_type)
        self.camera = Camera(self.player.rect.body.position)
        self.chaser = Chaser((self.player.rect.body.position.x,
                              self.player.rect.body.position.y + 200),
                             self.map.array, chaser_collision_type)
