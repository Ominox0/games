import time
from random import randint, uniform
from threading import Thread

import pygame


class OreDataC:
    def __init__(self, rarity, name, color):
        self.rarity = rarity  # 1 in X
        self.name = name
        self.color = color


oreData = {
    "coal": OreDataC(10, "coal", (55, 55, 55)),
    "copper": OreDataC(20, "copper", (200, 50, 50)),
    "iron": OreDataC(20, "iron", (155, 155, 155)),
    "sulfur": OreDataC(45, "sulfur", (190, 209, 19)),
    "titanium": OreDataC(25, "titanium", (79, 99, 95)),
    "ruby": OreDataC(35, "ruby", (255, 77, 109)),
    "plasteel ": OreDataC(50, "plasteel ", (167, 217, 216)),
    "uranium ": OreDataC(70, "uranium ", (104, 130, 113)),
    "tungsten ": OreDataC(35, "tungsten ", (94, 93, 93)),
    "gold": OreDataC(80, "gold", (255, 249, 89)),
    "silver": OreDataC(65, "silver", (227, 227, 227)),
    "jade": OreDataC(40, "jade", (151, 217, 137)),
    "salt": OreDataC(15, "salt", (237, 237, 237)),
    "silicon": OreDataC(65, "silicon", (166, 166, 166)),
    "erz des kaisers": OreDataC(100, "erz des kaisers", (185, 140, 212))
}


def choose_ore_by_rarity():
    weighted_ores = []
    for ore_name, ore in oreData.items():
        weight = 1 / max(ore.rarity, 1)
        weighted_ores.append((ore_name, weight))

    total_weight = sum(weight for _, weight in weighted_ores)
    pick = uniform(0, total_weight)
    current = 0
    for ore_name, weight in weighted_ores:
        current += weight
        if pick <= current:
            return ore_name


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

        elif f == "":
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


def getColorFromType(cType):
    return oreData[cType].color


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

        self.type = choose_ore_by_rarity()
        self.color = getColorFromType(self.type)


class SellTile(FunctionalTile):
    def __init__(self, xy):
        super().__init__(xy)

        self.color = (50, 255, 70)
        self.acceptsInputs = True

    def addToStorage(self, item, stack):
        print(item, stack)
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
        self.itemLimit = 99  # allow multiple item types
        self.colorOre = {}
        self.yOffset = 0
        self.getNew = True

    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(screen, (20, 20, 20), (10, 0, 30, 50))

        # draw each ore, spread them horizontally for visibility
        i = 0
        for ore, amount in self.itemStorage.items():
            if amount <= 0: continue
            color = getColorFromType(ore)
            x_offset = 15 + (i % 2) * 12
            y_offset = 30 - self.yOffset + (i // 2) * 12
            pygame.draw.rect(screen, color, (x_offset, y_offset, 10, 10))
            i += 1

        drawArrowUp(screen, 25, 15, 35)

    def addToStorage(self, item, stack):
        # set the color for this ore type if not already set
        if item not in self.colorOre:
            self.colorOre[item] = getColorFromType(item)
        return super().addToStorage(item, stack)

    def onGameTick(self, tiles):
        mX, mY = self.xy
        nX, nY = getFromDirectionCords(self.direction)
        pos = mX + nX, mY + nY

        if len(self.itemStorage) == 0:
            self.yOffset = 0
            return

        # simulate movement visually
        self.yOffset += 5

        if self.yOffset >= 30:
            self.yOffset = 0
            self.getNew = True
        else:
            self.getNew = False

        if not self.getNew:
            return

        if pos not in tiles:
            return

        tileObj = tiles[pos]
        if not isinstance(tileObj, FunctionalTile) or not tileObj.acceptsInputs:
            return  # don't remove items if we can't transfer

        # Try to transfer each type of ore
        any_transferred = False
        to_remove = []
        for ore in list(self.itemStorage.keys()):
            amount = self.itemStorage[ore]
            if amount <= 0:
                to_remove.append(ore)
                continue

            rest = tileObj.addToStorage(ore, amount)
            transferred = amount - rest

            if transferred > 0:
                self.itemStorage[ore] -= transferred
                any_transferred = True

            if self.itemStorage[ore] <= 0:
                to_remove.append(ore)

        for ore in to_remove:
            del self.itemStorage[ore]

        # Stop movement if nothing was transferred
        if not any_transferred:
            self.yOffset = 0
            self.getNew = False



class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        W, H = 30, 20

        self.screen = pygame.display.set_mode((51 * W, 51 * H))
        self.running = True

        self.buttons = {}
        self.tiles = {}

        for i in range(W):
            for j in range(H):
                pos = i, j
                if randint(0, 20) == 1:
                    self.tiles[pos] = OreTile(pos)
                elif randint(0, 30) == 1:
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

            time.sleep(0.1 - diff)

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
