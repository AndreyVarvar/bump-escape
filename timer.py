import settings as stt
import pygame as pg


class Timer:
    def __init__(self):
        self.time = 0

        self.label = pg.image.load("assets/images/label.png")
        self.numbers = pg.image.load("assets/images/numbers.png")

    def update(self, dt):
        self.time += dt

    def draw(self, surf):
        image = pg.transform.scale_by(self.get_image(), 3)
        surf.blit(image, (10, 10))

    def get_image(self):
        # self.time is in seconds
        seconds = self.time
        stt.debugger.update("time", str(self.time))
        minutes = seconds // 60
        hours = minutes // 60  # HOW LONG HAVE YOU BEEN PLAYING?????

        minutes -= hours * 60
        seconds -= minutes * 60 + hours * 3600

        # get numbers image
        time_board = self.label.copy().convert_alpha()

        hours_image = self.get_number(int(hours))
        minutes_image = self.get_number(int(minutes))
        seconds_image = self.get_number(int(seconds))

        # slap them onto the time board
        time_board.blit(hours_image, (2, 6))
        time_board.blit(minutes_image, (24, 6))
        time_board.blit(seconds_image, (44, 6))

        return time_board

    def get_number(self, n):
        numbers = pg.Surface((17, 16), pg.SRCALPHA)

        if len(str(n)) == 1:
            numbers.blit(self.numbers.subsurface(pg.Rect(0, 0, 8, 16)), (0, 0))
            numbers.blit(self.numbers.subsurface(pg.Rect(n * 8, 0, 8, 16)), (9, 0))
        else:
            numbers.blit(
                self.numbers.subsurface(pg.Rect(int(str(n)[0]) * 8, 0, 8, 16)), (0, 0)
            )
            numbers.blit(
                self.numbers.subsurface(pg.Rect(int(str(n)[1]) * 8, 0, 8, 16)), (9, 0)
            )

        return numbers
