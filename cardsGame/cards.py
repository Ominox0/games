import pygame
from functools import lru_cache


@lru_cache()
def load(path):
    return pygame.image.load(path)


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


def sized(img, size):
    return pygame.transform.scale(img, size)


class Cards:
    def __init__(self, gameItself, xy):
        self.game = gameItself
        self.xy = xy
        self.size = tupleMath((85, 124), 2)
        self.sizeSupport = (85, 124)
        self.support = None
        self.mainImgPath = None

        self.attack = 100
        self.defence = 100
        self.desc = ""
        self.cost = 0

        self.collision = pygame.Rect(0, 0, 0, 0)

    def getAttack(self):
        return self.attack

    def render(self, screen):
        X, Y = self.xy
        X *= 170 + 30
        Y *= 300
        X += 25
        Y += 25

        self.collision = pygame.Rect(X, Y, *self.size)

        if self.mainImgPath is None:
            pygame.draw.rect(screen, (111, 111, 111), (X, Y, *self.size))
        else:
            img = sized(load(self.mainImgPath), self.size)
            screen.blit(img, (X, Y))

        if self.support is not None:
            img = sized(self.support.render(), self.sizeSupport)
            screen.blit(img, (X + 100, Y + 150))


class MonsterCard(Cards):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.basicAbilityCODEX = [
            "basicDamage",
            "healPlayer",
            "healEnemy",
            "destroyCard",
        ]
        self.abilities = {}

    def attackF(self, ability, target):
        if ability == "basicDamage":
            target.defence -= self.getAttack()
            if target.defence <= 0:
                self.game.removeCardPos(target.xy)
            print(f"{self} dealt {self.getAttack()} to {target}")
        elif ability == "healPlayer":
            self.game.playerHp += 100
            print(f"Player healed for {100}")
        elif ability == "healEnemy":
            self.game.enemyHp += 100
            print(f"Enemy healed for {100}")


class SupportCard(Cards):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)

        self.isEquiptAble = False

    def onApply(self, mainCard):
        pass


class BabyAnkiCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BabyAnki.png"

        self.attack = 1600
        self.defence = 1800

        self.desc = "All Dinosaur type monsters gain 200atk"


class BabyBlackDragonlordCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BabyBlackDragonlord.png"

        self.attack = 1500
        self.defence = 1200

        self.desc = "Summons a dragon from your used cards pile"


class BabyT_RexosCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BabyT_Rexos.png"

        self.attack = 1700
        self.defence = 800

        self.desc = "While on field all dinosaur types can attack twice per turn"


class BasicSpaceMarineCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BasicSpaceMarine.png"

        self.attack = 1600
        self.defence = 1800

        self.desc = "Summons also and a Space Armour from your deck"


class BasicSpacePilotCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BasicSpacePilot.png"

        self.attack = 1200
        self.defence = 1900

        self.desc = "Summons also and a Space Armour from your deck"


class BlackLightningDragoonCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/blackLightningDragoon.png"

        self.attack = 3000
        self.defence = 2500

        self.desc = "When sent to used cards pile you can summon new dragon but its stats will be 0atk/def"


class BoomSaurusCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BoomSaurus.png"

        self.attack = 1200
        self.defence = 1800

        self.desc = "Summon this card on your opponent side and pay 4 mana to destory all monster cards"


class CrocoIsADinoCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/CrocoIsADino.png"

        self.attack = 2500
        self.defence = 200

        self.desc = "This card gains 300atk/def for each Dinosaur type in the field"


class dragonlordOfLostLandCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/dragonlordOfLostLand.png"

        self.attack = 2300
        self.defence = 2800

        self.desc = "Discard 2 dragon type monster to get this; all dragons get 500atk more and attack twice, the turn they are summoned"


class fireDragonEggCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/fireDragonEgg.png"

        self.attack = 0
        self.defence = 0

        self.desc = "Send this card to used cards pile and get a dragon in return"


class FlameDragonCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/FlameDragon.png"

        self.attack = 800
        self.defence = 1000

        self.desc = "Can inflict 500dmg to opponent for 1 mana"


class iceDragonEggCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/iceDragonEgg.png"

        self.attack = 0
        self.defence = 0

        self.desc = "Send this card to used cards pile and get a dragon in return"


class iceDragonlordCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/iceDragonlord.png"

        self.attack = 2800
        self.defence = 3000

        self.desc = "Discard 1 card or discard this card on the end of the turn"


class JurassicTerritoryCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/JurassicTerritory.png"

        self.desc = "All dinosaur monster get 500atk/def and 1st time they are sent tu used cards pile"
        self.cost = 2


class MetamorphosisCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/Metamorphosis.png"

        self.desc = "Send one monster to used cards pile and get same type in return"
        self.cost = 4


class SpaceArmour_MCCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/SpaceArmour_MC.png"

        self.desc = "Equipted monster has 500def more opponents cant use monster abilities on the turn they summon it"
        self.isEquiptAble = True


class SpaceArmour_MHCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/SpaceArmour_MH.png"

        self.desc = ""


class SpaceArmour_MLCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/SpaceArmour_ML.png"

        self.desc = "Equipted monster gains 500def and attacks all monsters at once"
        self.isEquiptAble = True


class SpaceArmour_MTCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/SpaceArmour_MT.png"

        self.desc = "Equipted monster can attack twice, any dmg dealt to it is doubled"
        self.isEquiptAble = True


class T_AnkiloCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/T_Ankilo.png"

        self.attack = 1800
        self.defence = 2000

        self.desc = "Can summon one more dinosaur monster"


class TheBraveKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/TheBraveKnight.png"

        self.attack = 2500
        self.defence = 2000

        self.desc = "Can pay 2 mana for each card you want to remove"


class UndeadBladeCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/UndeadBlade.png"

        self.desc = "Equipt on a zombie type card for 1 mana and it will get 500atk boost + it can attack 2 times this turn"


class UndeadElStakorCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/UndeadElStakor.png"

        self.attack = 1000
        self.defence = 0

        self.desc = "Once this card is sent to used cards deck you get 1 rat token"


class UndeadGoblinCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/UndeadGoblin.png"

        self.attack = 800
        self.defence = 500

        self.desc = "When this cards gets sent to used cards you can summon one free zombie card except for undead goblin"


class undeadRideCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/undeadRide.png"

        self.attack = 800
        self.defence = 1000

        self.desc = "Discard 1 zombie type card to summon this card"


class zombieCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/zombie.png"

        self.attack = 1000
        self.defence = 800

        self.desc = "Can be brought back from used cards for 2 mana"


class ZombieChimeraCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/ZombieChimera.png"

        self.attack = 2800
        self.defence = 2500

        self.desc = "Can be summoned by destroying 2 zombie cards"


class ZombiePartyCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/ZombieParty.png"

        self.desc = "Summons 3 zombies for cost of 4 mana"
        self.cost = 4


class ZomieDragonlordCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/ZomieDragonlord.png"

        self.attack = 2800
        self.defence = 0

        self.desc = "When this card goes to used cards it summons as many zombie type monster as possible (1 zombie per 1 mana)"


class AncientRelic_FlamingSwordCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/AncientRelic_FlamingSword.png"

        self.desc = "Equipted monster gains 1500atk and 800def"
        self.isEquiptAble = True


class SpaceArmour_MACard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/SpaceArmour_MA.png"

        self.desc = "Equipted monster gains 1000def"
        self.isEquiptAble = True


class AncientRelic_TSCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/AncientRelic_TS.png"

        self.desc = "Summon any monster from used cards pile"
        self.cost = 5


class AncientRelic_WKCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/AncientRelic_WK.png"

        self.isEquiptAble = True

        self.desc = "equipted monster gains 300atk/def if a monster gets sent to used cards pile than this ability cant be activated next round"


class CanAndBottleGangCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/CanAndBottleGang.png"

        self.attack = 2100
        self.defence = 1800

        self.desc = "When this card is sent to your used cards pile add one card with Can in its name"


class ElementalEnergyCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/ElementalEnergy.png"

        self.attack = 1500
        self.defence = 1600

        self.desc = "While this monster is on the field all your Elemental monsters gain 300atk while opponent's monsters lose 300atk"


class ElementalUnionCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/ElementalUnion.png"

        self.desc = "By paying 1 mana you can add from your deck to your hand one Elemental monster"
        self.cost = 1


class Elemental_ACard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_A.png"

        self.attack = 1800
        self.defence = 1500

        self.desc = "While this card is on the field other Elemental monsters gain 300atk/def"


class Elemental_EarthCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_Earth.png"

        self.attack = 1000
        self.defence = 2500

        self.desc = "While this card is on the field all Elemental monsters on your field gain 500def"


class Elemental_FACard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_FA.png"

        self.attack = 2000
        self.defence = 1800

        self.desc = "While this card is on the field other Elemental monsters gain 300atk/def"


class Elemental_FAECard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_FAE.png"

        self.attack = 2500
        self.defence = 2000

        self.desc = "While this card is on the field other Elemental monsters gain 300atk/def"


class EMP_generatorCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/EMP_generator.png"

        self.desc = "Can be used once every 3 rounds, costs 2 mana, and disables all mechanical cards for 1 round"
        self.cost = 2


class FriendInACanCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/FriendInACan.png"

        self.desc = "By paying 3 mana summons 3 1000atk/def friend tokens"


class Friend_TokenCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Friend_Token.png"

        self.attack = 1000
        self.defence = 1000

        self.desc = "Just a red gremlin duet"


class JuiceSlimeCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/JuiceSlime.png"

        self.attack = 1800
        self.defence = 1500

        self.desc = "When this card is summoned you can add one card with Can in its name"


class SpaceArmour_MSCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/SpaceArmour_MS.png"

        self.isEquiptAble = True

        self.desc = "The equipped monster gains 1500def and it can attack all monsters on the field"

    def canApplyOnCard(self, card):
        pass

class SpaceFighter_006Card(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/SpaceFighter_006.png"

        self.attack = 1500
        self.defence = 2000

        self.desc = "On summon of this card equipt from your used cards pile one Space Armour card to this card"


class SpaceFighter_09Card(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/SpaceFighter_09.png"

        self.attack = 1200
        self.defence = 1600

        self.desc = "When this card is summoned you can add from your deck to the hand 1 monster from your deck to your hand with Space in its name"


class TheMindReaderCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/TheMindReader.png"

        self.desc = "By paying 3 mana send one random card from their hand to their used cards pile"
        self.cost = 3


class UndeadSkeletonKingCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/UndeadSkeletonKing.png"

        self.attack = 2500
        self.defence = 2000

        self.desc = "When this card is sent to your used cards pile you can add from your used cards pile up to 3 Zombie type monsters to your hand"


class ZombieKidCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/ZombieKid.png"

        self.attack = 1000
        self.defence = 800

        self.desc = "When this card is sent to your used cards pile you can summon it back by paying 1 mana bit it's stats are 0 atk/def"


class ZombieKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/ZombieKnight.png"

        self.attack = 1200
        self.defence = 1600

        self.desc = "Just a zombie kid with armour; extra protection I guess?"


class Elemental_ETCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_ET.png"

        self.attack = 500
        self.defence = 2000

        self.desc = "When this card is summoned you can summon 1 Elemental monster from your used cards pile"


class Elemental_FA2Card(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_FA2.png"

        self.attack = 1500
        self.defence = 1500

        self.desc = "By paying 5 mana you can summon two Elemental monsters from your hand"
        self.cost = 5


class Elemental_LCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_L.png"

        self.attack = 1500
        self.defence = 1500

        self.desc = "By paying 5 mana you can destroy 2 cards on opponents field"
        self.cost = 5


class Elemental_WCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_W.png"

        self.attack = 1500
        self.defence = 1500

        self.desc = "By paying 4 mana destroy one card on your opponents side of the field"
        self.cost = 4


class LightningStrikeCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/LightningStrike.png"

        self.desc = "By paying 10 mana and discarding 2 cards destroy all cards on both player fields"
        self.cost = 10


class BlackKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BlackKnight.png"

        self.attack = 1800
        self.defence = 1500

        self.desc = "On summon of this card you can add one Spell card from your used card"


class BOOMTurtleCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BOOMTurtle.png"

        self.attack = 500
        self.defence = 2500

        self.desc = "For 3 mana destroy one monster on field"
        self.cost = 3


class EarthquakeCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/Earthquake.png"

        self.desc = "Pay 2 mana; destroy one monster on your opponents field with highest Def"
        self.cost = 2


class Elemental_CCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/Elemental_C.png"

        self.attack = 1500
        self.defence = 1500

        self.desc = "Pay 2 mana; all your Elemental monsters gain 500atk/def"


class KnightHorseCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/KnightHorse.png"

        self.attack = 1500
        self.defence = 2000

        self.desc = "Once per turn you can summon one Knight monster from y our hand to your side of the field"


class RatTokenCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/RatToken.png"

        self.attack = 100
        self.defence = 500

        self.desc = "Just a chill Rat"


class RocketTurtleCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/RocketTurtle.png"

        self.attack = 500
        self.defence = 2500

        self.desc = "For 2 mana summon one Turtle monster from your hand"
        self.cost = 2


class TurtleBadgeCard(SupportCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.mainImgPath = "cardsGame/assets/TurtleBadge.png"

        self.desc = ""
        self.cost = 1

        self.desc = "For 1 mana add from your deck 1 Turtle monster to your hand"


class NeonThePurpleKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/NeonThePurpleKnight.png"

        self.attack = 1800
        self.defence = 1500

        self.desc = "Can summon knight for 3 mana from hand or used cards pile"


class ArthurTheEmeraldKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/ArthurTheEmeraldKnight.png"

        self.attack = 2300
        self.defence = 1900

        self.desc = "Can summon knight for 4 mana from hand or used cards pile"


class SeamaryTheSapphireKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/SeamaryTheSapphireKnight.png"

        self.attack = 2000
        self.defence = 1500

        self.desc = "Can summon a spell card when not your turn for double the price"


class BlakkTheObsidianKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/BlakkTheObsidianKnight.png"

        self.attack = 1500
        self.defence = 1000

        self.desc = "draws 2 cards and than discard 1"


class LancelotTheDragonKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/LancelotTheDragonKnight.png"

        self.attack = 2200
        self.defence = 1800

        self.desc = "Once per turn can pay 4 mana for a spell card from used cards pile; only this round"


class FelgrandTheGoldenKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/FelgrandTheGoldenKnight.png"

        self.attack = 2000
        self.defence = 1500

        self.desc = "1st time monsters would get destroyed"


class RosemaryTheRedbloodKnightCard(MonsterCard):
    def __init__(self, gameItself, xy):
        super().__init__(gameItself, xy)
        self.abilities["normal"] = [self.basicAbilityCODEX[0]]
        self.mainImgPath = "cardsGame/assets/RosemaryTheRedbloodKnight.png"

        self.attack = 2000
        self.defence = 1500

        self.desc = "Can pay 4 mana for a knight monster from your hand"
