class Cursor:
    def __init__(self):
        self.busy = False

    def update(self, mouse_pressed):
        if not mouse_pressed[0]:
            self.busy = False
