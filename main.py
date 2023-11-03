import settings as stt
import pygame as pg
from scenes import GameScene, SettingsScene


class Game:
    def __init__(self):
        # app stuff
        self.display = stt.DISPLAY

        self.clock = pg.time.Clock()
        self.FPS = stt.FPS

        self.running = True

        self.scenes = {"main menu": "MainMenuScene",
                       "settings": SettingsScene(self.display),
                       "difficulty selection": "DifficultySelectScene",
                       "game": GameScene(self.display),
                       "win screen": "WinScene"}

        self.sfx_volume = 1

        self.current_scene = self.scenes["settings"]

        self.music_menu = pg.mixer.Sound("assets/music/main-menu.wav")
        self.music_in_game = pg.mixer.Sound("assets/music/in-game.wav")
        self.music_HARDMODE_YEAAAH = pg.mixer.Sound("assets/music/hardmode.wav")

    def run(self):
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

    def update(self, dt, mouse_pos, mouse_pressed):
        self.current_scene.update(dt, mouse_pos, mouse_pressed, False)

        if self.current_scene.name == "settings":
            self.sfx_volume = self.current_scene.slider_sfx.value

            for scene in self.scenes.values():
                if isinstance(scene, str) is False:
                    scene.sfx_volume = self.sfx_volume

        if self.current_scene.change_scene:
            prev_scene = self.current_scene
            self.current_scene = self.scenes[self.current_scene.new_scene]
            prev_scene.reset()

    def draw(self, dt):
        self.display.fill("white")

        self.current_scene.draw(dt, self.display)

        pg.display.update()

    def handle_events(self, dt, events, keys_pressed, mouse_pressed, mouse_pos):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

        self.current_scene.handle_events(dt, events, keys_pressed, mouse_pressed, mouse_pos)


i_am_tired_of_writing_long_name_on_these_variables_for_fun = Game()
i_am_tired_of_writing_long_name_on_these_variables_for_fun.run()
