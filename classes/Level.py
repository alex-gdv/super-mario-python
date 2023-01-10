import json
import pygame
import numpy as np

from .Sprites import Sprites
from .Tile import Tile
from ..entities.Coin import Coin
from ..entities.CoinBrick import CoinBrick
from ..entities.Goomba import Goomba
from ..entities.Mushroom import RedMushroom
from ..entities.Koopa import Koopa
from ..entities.CoinBox import CoinBox
from ..entities.RandomBox import RandomBox

# the number's correspond 
NAME2NUMBER = {"sky":1, "ground":2, "pipe":3, "CoinBox":5, "coinBrick":7, "coin":11, "Koopa":13,
            "Goomba":17, "RandomBox":19, "RedMushroom":23, "Mario":29}
TYPE2NAME = {Goomba:"Goomba", Koopa:"Koopa", RedMushroom:"RedMushroom", Coin:"coin",
            CoinBox:"CoinBox", CoinBrick:"coinBrick", RandomBox:"RandomBox"}

class Level:
    def __init__(self, screen, sound, dashboard):
        self.sprites = Sprites()
        self.dashboard = dashboard
        self.sound = sound
        self.screen = screen
        self.level = None
        self.levelLength = 0
        self.entityList = []

    def moveOnGrid(self, oldX, oldY, newX, newY, num):
        if oldX >= 0 and oldX < self.levelLength and oldY >= 0 and oldY < 16:
            self.levelGrid[oldX][oldY] /= num
        self.updateLevelGrid(newX, newY, num)

    def updateLevelGrid(self, x, y, num):
        if x >= 0 and x < self.levelLength and y >= 0 and y < 16:
            if num == 3:
                self.levelGrid[x][y:] *= num
            elif self.levelGrid[x][y]:
                self.levelGrid[x][y] *= num
            # # with open("level.txt", "w+") as file:
            # print("#################################################################################")
            # for y in range(self.levelGrid.shape[1]):
            #     for x in range(16):# self.levelGrid.shape[0]):
            #         print(str(int(self.levelGrid[x][y])), end="\t")
            #         # file.write(str(int(self.levelGrid[x][y])) + "\t")
            #     print()
            # print("#################################################################################")
            #     # file.write("\n")

    def loadLevel(self, levelname):
        with open("./src/super_mario_python/levels/{}.json".format(levelname)) as jsonData:
            data = json.load(jsonData)
            self.levelLength = data["length"]
            self.levelGrid = np.ones([self.levelLength, 16])
            self.loadLayers(data)
            self.loadObjects(data)
            self.loadEntities(data)

    def loadEntities(self, data):
        try:
            [self.addCoinBox(x, y) for x, y in data["level"]["entities"]["CoinBox"]]
            [self.addGoomba(x, y) for x, y in data["level"]["entities"]["Goomba"]]
            [self.addKoopa(x, y) for x, y in data["level"]["entities"]["Koopa"]]
            [self.addCoin(x, y) for x, y in data["level"]["entities"]["coin"]]
            [self.addCoinBrick(x, y) for x, y in data["level"]["entities"]["coinBrick"]]
            [self.addRandomBox(x, y, item) for x, y, item in data["level"]["entities"]["RandomBox"]]
            for entity in ["CoinBox", "Goomba", "Koopa", "coin", "coinBrick"]:
                for x, y in data["level"]["entities"][entity]:
                    self.updateLevelGrid(x, y, NAME2NUMBER[entity])
            for x, y, _ in data["level"]["entities"]["RandomBox"]:
                self.updateLevelGrid(x, y, NAME2NUMBER["RandomBox"])
        except Exception as e:
            print(str(e))

    def loadLayers(self, data):
        layers = []
        for x in range(*data["level"]["layers"]["sky"]["x"]):
            layers.append(
                (
                        [
                            Tile(self.sprites.spriteCollection.get("sky"), None)
                            for y in range(*data["level"]["layers"]["sky"]["y"])
                        ]
                        + [
                            Tile(
                                self.sprites.spriteCollection.get("ground"),
                                pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                            )
                            for y in range(*data["level"]["layers"]["ground"]["y"])
                        ]
                )
            )
            for y in range(*data["level"]["layers"]["ground"]["y"]):
                self.updateLevelGrid(x, y, NAME2NUMBER["ground"])

        self.level = list(map(list, zip(*layers)))

    def loadObjects(self, data):
        for x, y in data["level"]["objects"]["bush"]:
            self.addBushSprite(x, y)
        for x, y in data["level"]["objects"]["cloud"]:
            self.addCloudSprite(x, y)
        for x, y, z in data["level"]["objects"]["pipe"]:
            self.addPipeSprite(x, y, z)
            self.updateLevelGrid(x, y, NAME2NUMBER["pipe"])
        for x, y in data["level"]["objects"]["sky"]:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None)
        for x, y in data["level"]["objects"]["ground"]:
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("ground"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )
            self.updateLevelGrid(x, y, NAME2NUMBER["ground"])

    def updateEntities(self, cam):
        for entity in self.entityList:
            entity.update(cam)
            gridXCurr = round(entity.rect.x / 32)
            gridYCurr = round(entity.rect.y / 32)
            num = NAME2NUMBER[TYPE2NAME[type(entity)]]
            if (gridXCurr, gridYCurr) != (entity.gridX, entity.gridY):
                self.moveOnGrid(entity.gridX, entity.gridY, gridXCurr, gridYCurr, num)
                entity.updateGridXY(gridXCurr, gridYCurr)
            # if new item spawns
            elif self.levelGrid[gridXCurr][gridYCurr] % num != 0:
                self.moveOnGrid(-1, -1, gridXCurr, gridYCurr, num)
            if entity.alive is None:
                self.entityList.remove(entity)

    def drawLevel(self, camera):
        try:
            for y in range(0, 15):
                for x in range(0 - int(camera.pos.x + 1), 20 - int(camera.pos.x - 1)):
                    if self.level[y][x].sprite is not None:
                        if self.level[y][x].sprite.redrawBackground:
                            self.screen.blit(
                                self.sprites.spriteCollection.get("sky").image,
                                ((x + camera.pos.x) * 32, y * 32),
                            )
                        self.level[y][x].sprite.drawSprite(
                            x + camera.pos.x, y, self.screen
                        )
            self.updateEntities(camera)
        except IndexError:
            return

    def addCloudSprite(self, x, y):
        try:
            for yOff in range(0, 2):
                for xOff in range(0, 3):
                    self.level[y + yOff][x + xOff] = Tile(
                        self.sprites.spriteCollection.get("cloud{}_{}".format(yOff + 1, xOff + 1)), None, )
        except IndexError:
            return

    def addPipeSprite(self, x, y, length=2):
        try:
            # add pipe head
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("pipeL"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("pipeR"),
                pygame.Rect((x + 1) * 32, y * 32, 32, 32),
            )
            # add pipe body
            for i in range(1, length + 20):
                self.level[y + i][x] = Tile(
                    self.sprites.spriteCollection.get("pipe2L"),
                    pygame.Rect(x * 32, (y + i) * 32, 32, 32),
                )
                self.level[y + i][x + 1] = Tile(
                    self.sprites.spriteCollection.get("pipe2R"),
                    pygame.Rect((x + 1) * 32, (y + i) * 32, 32, 32),
                )
        except IndexError:
            return

    def addBushSprite(self, x, y):
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"), None)
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("bush_2"), None
            )
            self.level[y][x + 2] = Tile(
                self.sprites.spriteCollection.get("bush_3"), None
            )
        except IndexError:
            return

    def addCoinBox(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            CoinBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard,
            )
        )

    def addRandomBox(self, x, y, item):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            RandomBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                item,
                self.sound,
                self.dashboard,
                self
            )
        )

    def addCoin(self, x, y):
        self.entityList.append(Coin(self.screen, self.sprites.spriteCollection, x, y))

    def addCoinBrick(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            CoinBrick(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard
            )
        )

    def addGoomba(self, x, y):
        self.entityList.append(
            Goomba(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

    def addKoopa(self, x, y):
        self.entityList.append(
            Koopa(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

    def addRedMushroom(self, x, y):
        self.entityList.append(
            RedMushroom(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

