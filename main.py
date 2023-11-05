import settings as stt
import pygame as pg
from scenes import (
    GameScene,
    SettingsScene,
    MainMenuScene,
    DifficultySelectScene,
    WinScene,
)
from font import Font
from consts import colors

import pymunk
import pathfinding

import asyncio
import _cffi_backend  # this is needed for the webbuild


class Game:
    def __init__(self):
        # app stuff
        self.display = stt.DISPLAY

        self.clock = pg.time.Clock()
        self.FPS = stt.FPS

        self.running = True

        self.font = Font(
            "assets/fonts/da_font.png",
            colors["letter-end"],
            colors["offset-indicator"],
            1,
        )

        self.scenes = {
            "main menu": MainMenuScene(self.display, self.font),
            "settings": SettingsScene(self.display, self.font),
            "difficulty selection": DifficultySelectScene(self.display, self.font),
            "game": GameScene(self.display),
            "win screen": WinScene(self.display, self.font),
        }

        self.sfx_volume = 1

        self.current_scene = self.scenes["main menu"]

        self.music_volume = 1

        self.music_menu = pg.mixer.Sound("assets/music/main-menu.wav")
        self.music_in_game = pg.mixer.Sound("assets/music/in-game.wav")
        self.music_HARDMODE_YEAAAH = pg.mixer.Sound("assets/music/hardmode.wav")
        self.currently_playing = "menu music"

        self.road = pg.transform.scale_by(pg.image.load("assets/images/road.png"), 4)

    async def run(self):
        while self.running:
            # update some variables
            dt = self.clock.tick(self.FPS) / 1000

            keys_pressed = pg.key.get_pressed()
            mouse_pressed = pg.mouse.get_pressed()
            mouse_pos = pg.mouse.get_pos()

            events = pg.event.get()

            # process what just happened
            self.update(dt, mouse_pos, mouse_pressed)
            self.draw(dt)
            self.handle_events(dt, events, keys_pressed, mouse_pressed, mouse_pos)

            await asyncio.sleep(0)

    def update(self, dt, mouse_pos, mouse_pressed):
        self.current_scene.update(dt, mouse_pos, mouse_pressed, self.sfx_volume)
        stt.cursor.update(mouse_pressed)

        if self.current_scene.name != "game":
            if self.currently_playing != "menu music":
                self.currently_playing = "menu music"
                stt.channel_music.stop()

            if not stt.channel_music.get_busy():
                stt.channel_music.play(self.music_menu)
        elif self.current_scene.difficulty == 1:
            if self.currently_playing != "in-game music":
                self.currently_playing = "in-game music"
                stt.channel_music.stop()

            if not stt.channel_music.get_busy():
                stt.channel_music.play(self.music_in_game, -1)
        else:
            if self.currently_playing != "HARDCODE RAAH":
                self.currently_playing = "HARDCODE RAAH"
                stt.channel_music.stop()

            if not stt.channel_music.get_busy():
                stt.channel_music.play(self.music_HARDMODE_YEAAAH, -1)

        if self.current_scene.name == "settings":
            self.sfx_volume = self.current_scene.sfx_volume
            for scene in self.scenes.values():
                scene.sfx_volume = self.sfx_volume

            if self.music_volume != self.current_scene.music_volume:
                self.music_volume = self.current_scene.music_volume

                self.music_menu.set_volume(self.music_volume)
                self.music_in_game.set_volume(self.music_volume)
                self.music_HARDMODE_YEAAAH.set_volume(self.music_volume)

        elif self.current_scene.name == "difficulty selection":
            self.scenes["game"].difficulty = self.current_scene.selected_difficulty

        if self.current_scene.change_scene:
            self.scenes["win screen"].update_label(
                self.scenes["game"].timer.get_image()
            )
            prev_scene = self.current_scene
            self.current_scene = self.scenes[self.current_scene.new_scene]
            prev_scene.reset()

    def draw(self, dt):
        self.display.fill("white")

        if self.current_scene.has_background is False:
            self.display.blit(self.road, (0, 0))
            self.display.blit(self.road, (0, 640))

        self.current_scene.draw(dt, self.display)

        pg.display.update()

    def handle_events(self, dt, events, keys_pressed, mouse_pressed, mouse_pos):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

        self.current_scene.handle_events(
            dt, events, keys_pressed, mouse_pressed, mouse_pos
        )


i_am_tired_of_writing_long_name_on_these_variables_for_fun = Game()
asyncio.run(i_am_tired_of_writing_long_name_on_these_variables_for_fun.run())
