from super_mario_python.classes.InputAI import InputAI
from super_mario_python.entities.Mario import Mario

class MarioAI(Mario):
    def __init__(self, x, y, level, screen, dashboard, sound, gravity=0.8):
        super(MarioAI, self).__init__(x, y, level, screen, dashboard, sound, gravity)
        self.input = InputAI(self)
