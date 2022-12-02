class InputAI:
    def __init__(self, entity):
        self.entity = entity
        self.receivedInput = False
    
    def receiveInput(self, input):
        self.input = input
        self.receivedInput = True

    def move(self, direction, jumping, boost):
        self.entity.traits["goTrait"].direction = direction
        self.entity.traits['jumpTrait'].jump(jumping)
        self.entity.traits['goTrait'].boost = boost
    
    def checkForInput(self):
        if self.receivedInput:
            self.receivedInput = False
            if self.input == 0:
                self.move(0, False, False)
            elif self.input == 1:
                self.move(-1, False, False)
            elif self.input == 2:
                self.move(-1, True, False)
            elif self.input == 3:
                self.move(-1, True, True)
            elif self.input == 4:
                self.move(1, False, False)
            elif self.input == 5:
                self.move(1, True, False)
            elif self.input == 6:
                self.move(1, True, True)
            elif self.input == 7:
                self.move(0, True, False)
            elif self.input == 8:
                self.move(-1, False, True)
            elif self.input == 9:
                self.move(1, False, True)
