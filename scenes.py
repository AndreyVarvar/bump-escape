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
from consts import colors


class BaseScene:
    def __init__(self, name):
        self.name = name
        self.change_scene = False
        self.new_scene = name  # do not change

        self.sfx_volume = 1

        self.has_background = False

    def check_change(self, *args):
        pass

    def reset(self):
        self.new_scene = self.name
        self.change_scene = False

    def handle_events(self, *args):
        pass


class MainMenuScene(BaseScene):
    def __init__(self, display, font):
        super().__init__("main menu")

        self.display = display
        self.font = font

        self.button_play = Button(
            pg.Rect(120, 275, 400, 100),
            colors["green"],
            colors["dark-green"],
            colors["light-green"],
            colors["green"],
            "Play",
            True,
            5,
            self.font,
            "assets/sfx/bump.ogg",
            self.sfx_volume,
            5,
        )

        self.button_settings = Button(
            pg.Rect(120, 400, 400, 100),
            colors["tangerine"],
            colors["brown"],
            colors["orange"],
            colors["tangerine"],
            "Settings",
            True,
            5,
            self.font,
            "assets/sfx/bump.ogg",
            self.sfx_volume,
            5,
        )

    def update(self, *args):
        dt = args[0]
        mouse_pos = args[1]
        mouse_pressed = args[2]
        sfx_volume = args[3]

        if sfx_volume != self.sfx_volume:
            self.sfx_volume = sfx_volume

        self.button_play.update(mouse_pos, mouse_pressed, stt.cursor, self.sfx_volume)
        self.button_settings.update(
            mouse_pos, mouse_pressed, stt.cursor, self.sfx_volume
        )

        if self.button_play.clicked:
            self.change_scene = True
            self.new_scene = "difficulty selection"

        elif self.button_settings.clicked:
            self.change_scene = True
            self.new_scene = "settings"

    def draw(self, *args):
        dt = args[0]
        surf = args[1]

        self.button_play.draw(surf)
        self.button_settings.draw(surf)

    def reset(self):
        self.new_scene = self.name
        self.change_scene = False

        self.button_play.clicked = False
        self.button_settings.clicked = False


class SettingsScene(BaseScene):
    def __init__(self, display, font):
        super().__init__("settings")

        self.display = display

        self.slider_sfx = Slider(
            rect=pg.Rect(120, 120, 400, 20),
            min_value=0,
            max_value=1,
            initial_value=1,
            slide_sound_path="assets/sfx/bump.ogg",
            sfx_volume=self.sfx_volume,
            step=0.1,
        )

        self.font = font
        self.text_sfx = self.font.render("SFX", 5, True)
        self.text_sfx_pos = ((stt.D_W - self.text_sfx.get_width()) // 2, 70)

        self.slider_music = Slider(
            rect=pg.Rect(120, 220, 400, 20),
            min_value=0,
            max_value=1,
            initial_value=1,
            slide_sound_path="assets/sfx/bump.ogg",
            sfx_volume=self.sfx_volume,
            step=0.1,
        )

        self.music_volume = 1

        self.text_music = self.font.render("music", 5, True)
        self.text_music_pos = ((stt.D_W - self.text_sfx.get_width()) // 2, 170)

        self.button_exit = Button(
            pg.Rect(20, 20, 100, 50),
            colors["cyan"],
            colors["dark-cyan"],
            colors["light-cyan"],
            colors["cyan"],
            "Back",
            True,
            5,
            self.font,
            "assets/sfx/bump.ogg",
            self.sfx_volume,
        )

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
        sfx_volume = args[3]

        if sfx_volume != self.sfx_volume:
            self.sfx_volume = sfx_volume

        self.slider_sfx.update(mouse_pos, mouse_pressed, stt.cursor, self.sfx_volume)
        self.slider_music.update(mouse_pos, mouse_pressed, stt.cursor, self.sfx_volume)

        self.music_volume = self.slider_music.value

        self.button_exit.update(mouse_pos, mouse_pressed, stt.cursor, self.sfx_volume)

        self.sfx_volume = self.slider_sfx.value

        if self.button_exit.clicked is True:
            self.new_scene = "main menu"
            self.change_scene = True

    def reset(self):
        self.change_scene = False
        self.new_scene = self.name

        self.button_exit.clicked = False


class DifficultySelectScene(BaseScene):
    def __init__(self, display, font):
        super().__init__("difficulty selection")

        self.display = display
        self.font = font

        self.selected_difficulty = 1

        self.button_easy = Button(
            pg.Rect(70, 275, 500, 100),
            colors["green"],
            colors["dark-green"],
            colors["light-green"],
            colors["green"],
            "Ez-easy",
            True,
            5,
            self.font,
            "assets/sfx/bump.ogg",
            self.sfx_volume,
            5,
        )

        self.button_hard = Button(
            pg.Rect(70, 400, 500, 105),
            colors["tangerine"],
            colors["brown"],
            colors["orange"],
            colors["tangerine"],
            "HARDCODE-YEAH",
            True,
            5,
            self.font,
            "assets/sfx/bump.ogg",
            self.sfx_volume,
            5,
        )

    def update(self, *args):
        dt = args[0]
        mouse_pos = args[1]
        mouse_pressed = args[2]
        sfx_volume = args[3]

        if sfx_volume != self.sfx_volume:
            self.sfx_volume = sfx_volume

        self.button_easy.update(mouse_pos, mouse_pressed, stt.cursor, self.sfx_volume)
        self.button_hard.update(mouse_pos, mouse_pressed, stt.cursor, self.sfx_volume)

    def draw(self, *args):
        dt = args[0]
        surf = args[1]

        self.button_easy.draw(surf)
        self.button_hard.draw(surf)

        if self.button_easy.clicked:
            self.selected_difficulty = 1
            self.change_scene = True
            self.new_scene = "game"
        elif self.button_hard.clicked:
            self.selected_difficulty = 2
            self.change_scene = True
            self.new_scene = "game"

    def reset(self):
        self.new_scene = self.name
        self.change_scene = False

        self.button_easy.clicked = False
        self.button_hard.clicked = False


class GameScene(BaseScene):
    def __init__(self, display):
        super().__init__("game")

        # app stuff
        self.display = display

        self.clock = pg.time.Clock()

        self.draw_options = pg_util.DrawOptions(self.display)

        # how hard it is to play
        self.difficulty = 1

        # map
        self.map = Map(1)

        # timer
        self.timer = Timer()

        # YEEEEE
        self.has_background = True

        # main characters (not durk)
        obstacles_collision_type = 7
        player_collision_type = 1
        chaser_collision_type = 2

        self.player = Player(
            self.map.checkpoints.current_checkpoint.center, player_collision_type
        )
        self.camera = Camera(self.player.rect.body.position)
        self.chaser = Chaser(
            (self.player.rect.body.position.x, self.player.rect.body.position.y + 200),
            self.map.array,
            chaser_collision_type,
            self.difficulty,
        )

        self.player_collision_handlers = [
            stt.space.add_collision_handler(
                player_collision_type, obstacles_collision_type + i - 3
            )
            for i in range(len(self.map.objects) + 4)
        ]
        self.chaser_collision_handlers = [
            stt.space.add_collision_handler(
                chaser_collision_type, obstacles_collision_type + i - 3
            )
            for i in range(len(self.map.objects) + 4)
        ]

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

        if self.player.rect.body.position.y <= 100:
            self.change_scene = True
            self.new_scene = "win screen"

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
        self.player.handle_events(events, keys_pressed)

    def reset(self):
        self.new_scene = self.name
        self.change_scene = False

        # timer
        self.timer = Timer()

        player_collision_type = 1
        chaser_collision_type = 2

        self.player = Player(
            self.map.checkpoints.current_checkpoint.center, player_collision_type
        )
        self.camera = Camera(self.player.rect.body.position)
        self.chaser = Chaser(
            (self.player.rect.body.position.x, self.player.rect.body.position.y + 200),
            self.map.array,
            chaser_collision_type,
        )


class WinScene(BaseScene):
    def __init__(self, display, font):
        super().__init__("win screen")

        self.display = display
        self.font = font

        self.label = pg.Surface((100, 100))

        self.text = self.font.render("CONGRATS!", 6, True)
        self.text2 = self.font.render("You beat the game!", 4, True)
        self.text3 = self.font.render("btw the game was made in 2 days...", 4, True)

    def update(self, *args):
        pass

    def update_label(self, label):
        self.label = pg.transform.scale_by(label, 5)

    def draw(self, *args):
        self.display.fill("white")

        self.display.blit(self.label, ((stt.D_W - self.label.get_width()) // 2, 200))

        self.display.blit(self.text, ((stt.D_W - self.text.get_width()) // 2, 500))
        self.display.blit(self.text2, ((stt.D_W - self.text2.get_width()) // 2, 550))
        self.display.blit(self.text3, ((stt.D_W - self.text3.get_width()) // 2, 600))
