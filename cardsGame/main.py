import random
from typing import Type

from cardsGame.cards import *
import pygame


class gameClass:
    def __init__(self):
        self.playerHp = 15_000
        self.enemyHp = 15_000

        self.cardsBot: dict[int, None | MonsterCard] = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
        }
        self.cardsBotGone: list[Cards] = []
        self.cardsBotHand: list[Type[Cards]] = []
        self.botDeck: list[Type[Cards]] = [
            Elemental_CCard, Elemental_LCard,
            Elemental_FA2Card, Elemental_WCard,
            LightningStrikeCard, AncientRelic_FlamingSwordCard,
            Elemental_EarthCard, Elemental_ETCard,
            Elemental_ETCard, AncientRelic_WKCard,
            Elemental_FACard, Elemental_FAECard,
            ElementalUnionCard, EarthquakeCard, TheMindReaderCard
        ]

        self.cardsPlayer: dict[int, None | MonsterCard] = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
        }
        self.cardsPlayerGone: list[Cards] = []
        self.cardsPlayerHand: list[Cards] = []
        self.playerDeck: list[Type[Cards]] = [
            SpaceFighter_006Card, SpaceFighter_09Card,
            SpaceArmour_MSCard, SpaceArmour_MTCard,
            SpaceArmour_MLCard, BasicSpacePilotCard,
            BasicSpaceMarineCard, SpaceArmour_MHCard,
            SpaceArmour_MCCard, SpaceArmour_MACard,
            LightningStrikeCard, AncientRelic_TSCard,
            AncientRelic_WKCard, AncientRelic_FlamingSwordCard,
            FriendInACanCard
        ]

        self.turn = "player"

        self.round = 1

        self.StartGame()

    def summonPlayerCard(self, hand):
        for card in self.cardsPlayer:
            if self.cardsPlayer[card] is None:
                targX = hand.xy[0]
                hand.xy = card, 1
                self.cardsPlayer[card] = hand

                del self.cardsPlayerHand[targX]

                for cardHand in self.cardsPlayerHand:
                    x, y = cardHand.xy

                    if cardHand.xy[0] > targX:
                        cardHand.xy = x - 1, y
                break

    def summonBotCard(self, hand):
        pass

    def StartGame(self):
        playerCards = random.sample(self.playerDeck, 5)

        x = 0
        for c in playerCards:
            self.cardsPlayerHand.append(c(self, (x, 2)))

            x += 1

        botCards = random.sample(self.botDeck, 5)
        self.cardsBotHand.extend(botCards)

    def NextTurn(self):
        self.turn = "player" if self.turn == "bot" else "bot"

    def removeCardPos(self, pos):
        X, Y = pos

        if Y == 0:
            deck = self.cardsBot
            deckGone = self.cardsBotGone
        else:
            deck = self.cardsPlayer
            deckGone = self.cardsPlayerGone

        card = deck[X]
        deck[X] = None

        deckGone.append(card)

    def botTurn(self):
        l1 = [v for k, v in self.cardsBot.items() if v is not None]
        l2 = [v for k, v in self.cardsPlayer.items() if v is not None]
        if len(l1) == 0:
            self.botPlaceCards()
            self.NextTurn()
            return

        attacker = random.choice(l1)
        target = random.choice(l2)

        ability = attacker.abilities["normal"][0]
        attacker.attackF(ability, target)
        self.NextTurn()

    def botPlaceCards(self):
        pass


def aboutCard(card: Cards):
    surface = pygame.Surface((200, 120))
    surface.fill((40, 40, 40))
    font = pygame.font.SysFont(None, 24)

    hp_text = font.render(f"ATK: {getattr(card, 'attack', 'N/A')}", True, (255, 255, 255))
    defence_text = font.render(f"DEF: {getattr(card, 'defence', 'N/A')}", True, (255, 255, 255))
    desc_text = font.render(card.desc, True, (200, 200, 200))

    surface.blit(hp_text, (10, 10))
    surface.blit(defence_text, (10, 40))
    surface.blit(desc_text, (10, 70))

    return surface


class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.widthGame = 1400 + 30
        self.width = self.widthGame + 400
        self.height = 51 * 17 + 10

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True

        self.font32 = pygame.font.SysFont(None, 32)
        self.font = pygame.font.SysFont(None, 36)
        self.font64 = pygame.font.SysFont(None, 64)

        self.buttons = {}

        self.player: dict[str, None | MonsterCard] = {
            "attacker": None,
            "victim": None,
            "hand": None,
        }

        self.game = gameClass()
        self.run()
        pygame.font.quit()
        pygame.quit()

    def render1(self):
        surf = pygame.Surface((self.widthGame, 248 + (15 * 2)))
        surf.fill((30, 60, 90))

        txt = self.font.render("Your Hand", True, (255, 255, 255))
        surf.blit(txt, (15, 0))

        self.screen.blit(surf, (0, self.height - surf.get_height()))

    def render2(self):

        surf = pygame.Surface((400, self.height))
        surf.fill((20, 20, 20))

        hand = self.player["hand"]

        if hand is not None:
            self.renderHandDataAndActions(surf, hand)

        self.screen.blit(surf, (self.widthGame, 0))

    def renderHandDataAndActions(self, surf, hand):
        text0 = self.font64.render("ACTIONS", True, (255, 255, 255))

        if isinstance(hand, MonsterCard):
            buttonRect1 = pygame.draw.rect(surf, (50, 50, 50), (138, 90, 124, 44))
            text1 = self.font.render("Summon", True, (255, 255, 255))
            surf.blit(text1, (148, 100))  # centered X
            self.buildButton(buttonRect1.topleft, buttonRect1.size, hand, self.addCard)

        elif isinstance(hand, SupportCard):
            targ = self.player["attacker"]

            if hand.isEquiptAble:
                if targ is None:
                    text1 = self.font.render("Select attacker to apply this card", True, (255, 255, 255))

                else:
                    text1 = self.font.render("Apply this card to selected attacker?", True, (255, 255, 255))

                surf.blit(text1, (400 - (text1.get_width()) / 2, 100))  # centered X


        surf.blit(text0, (95, 5))  # centered X

    def addCard(self, hand):
        self.player["hand"] = None
        self.game.summonPlayerCard(hand)

    def buildButton(self, xy, wh, pkg, function):
        x, y = xy
        self.buttons[((x + self.widthGame, y), wh, pkg)] = function

    def run(self):
        while self.running:
            for button in self.buttons.copy():
                del self.buttons[button]

            extraBlit = []
            self.screen.fill((0, 0, 0))

            self.render1()
            self.render2()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = event.pos
                    for (xy, wh, dataPkg) in self.buttons:
                        if pygame.Rect(xy, wh).collidepoint(pos):
                            if dataPkg is not None:
                                self.buttons[(xy, wh, dataPkg)](dataPkg)
                            else:
                                self.buttons[(xy, wh, dataPkg)]()

                elif event.type == pygame.KEYUP:
                    if event.key != pygame.K_RETURN:
                        break

                    if self.game.turn == "player":
                        cardObj = self.player["attacker"]
                        target = self.player["victim"]

                        if cardObj is None or target is None:
                            continue

                        ability = cardObj.abilities["normal"][0]

                        cardObj.attackF(ability, target)

                        self.game.NextTurn()

                        self.player["attacker"] = None
                        self.player["victim"] = None

            if self.game.turn == "bot":
                pygame.time.delay(500)
                self.game.botTurn()

            pos = pygame.mouse.get_pos()
            press = pygame.mouse.get_pressed()

            pX, pY = pos
            part = "b"
            for l in ["b", self.game.cardsBot.values(), "p", self.game.cardsPlayer.values(), "h", self.game.cardsPlayerHand]:
                if l in ["b", "p", "h"]:
                    part = l
                    continue

                for card in l:
                    if card is None:
                        continue

                    if card.collision.collidepoint(pos):
                        if press[0]:
                            if part == "p":
                                self.player["attacker"] = card
                            elif part == "b":
                                self.player["victim"] = card
                            elif part == "h":
                                self.player["hand"] = card
                        tooltip = aboutCard(card)
                        sW, sH = tooltip.get_size()

                        extraBlit.append((tooltip, (pX - (sW / 2), pY)))

                        pygame.draw.rect(self.screen, (255, 155, 0), (tupleMath(card.collision.topleft, 5, "-"), tupleMath(card.collision.size, 10, "+")))

            c = self.player["attacker"]
            if c is not None:
                pygame.draw.rect(self.screen, (0, 255, 155), (tupleMath(c.collision.topleft, 5, "-"), tupleMath(c.collision.size, 10, "+")))

            c = self.player["victim"]
            if c is not None:
                pygame.draw.rect(self.screen, (255, 0, 0), (tupleMath(c.collision.topleft, 5, "-"), tupleMath(c.collision.size, 10, "+")))

            for card in self.game.cardsBot.values():
                if card is None:
                    continue
                card.render(self.screen)

            for card in self.game.cardsPlayer.values():
                if card is None:
                    continue
                card.render(self.screen)

            for card in self.game.cardsPlayerHand:
                if card is None:
                    continue
                card.render(self.screen)

            for (surf, pos) in extraBlit:
                self.screen.blit(surf, pos)

            pygame.display.update()


if __name__ == '__main__':
    Main()
