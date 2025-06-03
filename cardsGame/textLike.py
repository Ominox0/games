from cardsGame.main import gameClass, SupportCard, MonsterCard


def showAndGetCard(l, text, askRet, t2="\nIndex: >>> "):
    print(text)
    for i, c in enumerate(l):
        print(f"{i} | {c.__class__.__name__} - {c.__class__.__bases__[0].__name__}")

    if askRet:
        ind = input(t2)

        return l[int(ind)]


def isEmpty(l):
    return not any(x is not None for x in l)


def main():
    gC = gameClass()

    print("\nYou play 1st (cannot attack 1st round)")
    print("Game starts!\n")

    while True:
        while True:
            c = showAndGetCard(gC.cardsPlayerHand, "Your hand", True)

            if isinstance(c, SupportCard):
                if isEmpty(gC.cardsPlayer.values()) and c.isEquiptAble:
                    print("This card cannot be equipped; your deck is empty and this card is equitable")
                if not isEmpty(gC.cardsPlayer.values()) and not c.isEquiptAble:
                    c2 = showAndGetCard(gC.cardsPlayerHand, "Select monster to equipt this card", True)

                    if isinstance(c, MonsterCard):
                        c2.support = c

            if input("End phase? >>> ") == "yes":
                break

            print("info: 'My deck', 'My hand', 'My udp', 'Opponent deck'")
            action = input("Show info: >>>")

            if action == "My deck":
                showAndGetCard(list(gC.cardsPlayer.values()), "Your deck", False)

            elif action == "My hand":
                showAndGetCard(list(gC.cardsPlayerHand), "Your deck", False)

            elif action == "My udp":
                showAndGetCard(list(gC.cardsPlayerGone), "Your udp", False)

            elif action == "Opponent deck":
                showAndGetCard(list(gC.cardsBot.values()), "Opponent deck", False)

            print("\n")

