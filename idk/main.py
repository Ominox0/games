import time
from random import randint
from threading import Thread

import pygame


def tupleMath(t, i, f="*"):
    new = []

    for el in t:
        if f == "*":
            new.append(el * i)

        elif f == "/":
            new.append(el / i)

        elif f == "//":
            new.append(el // i)

        elif f == "-":
            new.append(el - i)

        elif f == "+":
            new.append(el + i)

        elif f == "**":
            new.append(el ** i)

    return tuple(new)


def getDeg(direction):
    if direction == "up":
        return 0

    elif direction == "right":
        return 90

    elif direction == "down":
        return 180

    elif direction == "left":
        return 270

    else:
        return 0
    

def getOpposed(direction):
    if direction == "up":
        return "down"

    elif direction == "right":
        return "left"

    elif direction == "down":
        return "up"

    elif direction == "left":
        return "right"


def getNextDirection(direction):
    if direction == "up":
        return "right"

    elif direction == "right":
        return "down"

    elif direction == "down":
        return "left"

    elif direction == "left":
        return "up"


def getFromDirectionCords(direction):
    if direction == "up":
        return 0, -1

    elif direction == "right":
        return -1, 0

    elif direction == "down":
        return 0, 1

    elif direction == "left":
        return 1, 0


def drawArrowUp(screen, center_x, top_y, bottom_y, offset=5, width=2):
    pygame.draw.line(screen, (255, 255, 255), (center_x, bottom_y), (center_x, top_y), width)

    pygame.draw.line(screen, (255, 255, 255), (center_x, top_y), (center_x - offset, top_y + offset), width)
    pygame.draw.line(screen, (255, 255, 255), (center_x, top_y), (center_x + offset, top_y + offset), width)


class Tile:
    def __init__(self, xy):
        self.xy = xy
        self.direction = "up"
        self.past = None

        self.color = (111, 111, 111)

        self.collide = pygame.Rect(tupleMath(xy, 51), (50, 50))

    def rotate(self):
        self.direction = getNextDirection(self.direction)

    def render(self, screen):
        screen.fill(self.color)

    def onGameTick(self, tiles):
        pass


class FunctionalTile(Tile):
    def __init__(self, xy):
        super().__init__(xy)

        self.itemStorage = {}
        self.itemLimit = 1
        self.itemStack = 8

        self.acceptsInputs = False
        self.acceptsOutputs = True

    def addToStorage(self, item, stack):
        if item in self.itemStorage:
            current = self.itemStorage[item]
            available_space = self.itemStack - current

            if available_space > 0:
                added = min(available_space, stack)
                self.itemStorage[item] += added
                return stack - added
            else:
                return stack
        else:
            if len(self.itemStorage) < self.itemLimit:
                added = min(self.itemStack, stack)
                self.itemStorage[item] = added
                return stack - added
            else:
                return stack

    def getStorage(self, item):
        return self.itemStorage[item]


class OreTile(Tile):
    def __init__(self, xy):
        super().__init__(xy)

        self.color = (203, 203, 203)

        self.type = "iron"


class SellTile(FunctionalTile):
    def __init__(self, xy):
        super().__init__(xy)

        self.color = (50, 255, 70)
        self.acceptsInputs = True

    def addToStorage(self, item, stack):
        if item in self.itemStorage:
            self.itemStorage[item] += stack

        else:
            self.itemStorage[item] = stack

        return 0


class MinerTile(FunctionalTile):
    def __init__(self, xy):
        super().__init__(xy)

    def render(self, screen):
        super().render(screen)

        pygame.draw.rect(screen, (40, 40, 40), (10, 0, 30, 30))

        drawArrowUp(screen, 25, 5, 25)

    def onGameTick(self, tiles):
        self.addToStorage(self.past.type, 1)

        mX, mY = self.xy
        nX, nY = getFromDirectionCords(self.direction)
        pos = mX + nX, mY + nY

        if pos in tiles:
            tileObj = tiles[pos]

            if isinstance(tileObj, FunctionalTile):
                if tileObj.acceptsInputs:

                    amm = self.getStorage(self.past.type)
                    rest = tileObj.addToStorage(self.past.type, amm)

                    self.itemStorage[self.past.type] -= (amm - rest)

                    if self.itemStorage[self.past.type] <= 0:
                        del self.itemStorage[self.past.type]


class ConveyorbeltTile(FunctionalTile):
    def __init__(self, xy):
        super().__init__(xy)

        self.acceptsInputs = True
        self.getNew = True
        self.yOffset = 0

    def render(self, screen):
        super().render(screen)

        pygame.draw.rect(screen, (20, 20, 20), (10, 0, 30, 50))

        if len(self.itemStorage) > 0:
            pygame.draw.rect(screen, (155, 155, 155), (15, 30 - self.yOffset, 20, 20))

        drawArrowUp(screen, 25, 15, 35)

    def addToStorage(self, item, stack):
        if self.getNew:
            return super().addToStorage(item, stack)

        return stack

    def onGameTick(self, tiles):
        mX, mY = self.xy
        nX, nY = getFromDirectionCords(self.direction)
        pos = mX + nX, mY + nY

        if len(self.itemStorage) == 0:
            self.yOffset = 0
            return

        self.yOffset += 15

        if self.yOffset >= 30:
            self.yOffset = 0
            self.getNew = True
        else:
            self.getNew = False

        if not self.getNew:
            return

        if pos in tiles:
            tileObj = tiles[pos]

            if isinstance(tileObj, FunctionalTile):
                if tileObj.acceptsInputs:

                    p = list(self.itemStorage.keys())[0]
                    amm = self.getStorage(p)
                    rest = tileObj.addToStorage(p, amm)

                    self.itemStorage[p] -= (amm - rest)

                    if self.itemStorage[p] <= 0:
                        del self.itemStorage[p]


class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((51 * 10, 51 * 10))
        self.running = True

        self.buttons = {}
        self.tiles = {}

        for i in range(10):
            for j in range(10):
                pos = i, j
                if randint(0, 10) == 1:
                    self.tiles[pos] = OreTile(pos)
                elif randint(0, 20) == 1:
                    self.tiles[pos] = SellTile(pos)
                else:
                    self.tiles[pos] = Tile(pos)

        Thread(target=self.onGameTIck).start()
        self.run()

        pygame.font.quit()
        pygame.quit()

    def onGameTIck(self):
        while self.running:
            timeStart = time.time()

            for tile in self.tiles:
                tileObj = self.tiles[tile]
                tileObj.onGameTick(self.tiles)

            diff = time.time() - timeStart

            time.sleep(1 - diff)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                elif event.type == pygame.MOUSEBUTTONUP:
                    for tile in self.tiles:
                        tileObj = self.tiles[tile]
                        if tileObj.collide.collidepoint(event.pos):
                            if event.button == 1:
                                if type(tileObj) is Tile:
                                    self.tiles[tile] = ConveyorbeltTile(tile)
                                    self.tiles[tile].past = tileObj

                                elif type(tileObj) is OreTile:
                                    self.tiles[tile] = MinerTile(tile)
                                    self.tiles[tile].color = tileObj.color
                                    self.tiles[tile].past = tileObj

                                else:
                                    tileObj.rotate()

                            elif event.button == 3:
                                if tileObj.past is not None:
                                    self.tiles[tile] = tileObj.past

                            break

            self.screen.fill((0, 0, 0))

            for tile in self.tiles:
                tileObj = self.tiles[tile]

                surf = pygame.Surface((50, 50))
                tileObj.render(surf)

                newSurf = pygame.transform.rotate(surf, getDeg(tileObj.direction))

                self.screen.blit(newSurf, tupleMath(tile, 51))

            pygame.display.update()


if __name__ == '__main__':
    Main()
