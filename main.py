from folumo.config import config

from minerGame.main import Main as MG_M
from cardsGame.main import Main as CG_M
from cardsGame.textLike import main as CG_MT


def main():
    con = config()
    con.registerAttribute("game", "minerGame")
    con.save()

    v = con.get("game")

    {
        "minerGame": MG_M,
        "cardsGame": CG_M,
        "cardsGameT": CG_MT
    }[v]()


if __name__ == '__main__':
    main()
