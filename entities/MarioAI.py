from ..classes.InputAI import InputAI
from .Mario import Mario

class MarioAI(Mario):
    def __init__(self, x, y, level, screen, dashboard, sound, gravity=0.8):
        super(MarioAI, self).__init__(x, y, level, screen, dashboard, sound, gravity)
        self.input = InputAI(self)
