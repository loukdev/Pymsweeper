#! python


from utils import *
from data import *


QUIT = 0
PLAY = 1

MAP_W = 8
MAP_H = 8

def main_menu():
    print("Menu principal :\n",
          QUIT, ". Quitter.\n",
          PLAY, ". Jouer.\n", sep='', end='')

    return get_int(0, 1)

def play():

    grid = Grid(MAP_W, MAP_H, 10)

    clear()
    print("Zzzé parti, zé partiiiii !! Hum. Pardon. Voici la carte, vierge pour l'instant (normal, c'est le début de partie) :")
    print(grid)
    print("Indiquer la position de la case à dévoiler sous la forme \"x y\", où x et y sont deux entiers, respectivement la colonne et la ligne.")
    print("Pour quitter la partie prématurément, indiquer un -1 dans la position (par exemple : \"-1 0\").")

    stop = won = False
    while not stop:

        pos = get_pos(-1, -1, MAP_W, MAP_H)
        if pos[0] < 0 or pos[1] < 0:
            print("On abandonne la partie ? Abadakor... Bombadakor.\n")
            break

        clear()

        mined = grid.reveal_at(pos)
        if mined:
            print("Et boooom ! C'était une mine... dommage, vous êtes mort-e ! C'est bête, hein. Heureusement que ce n'est qu'un jeu.")
            grid.fix()
            stop = True
        elif grid.is_cleared():
            print("Oyeah, toutes les cases vides ont été découvertes, c'est la victoire !!")
            won = stop = True

        print(grid)

    print("Appuyer sur <Entrée> pour revenir au menu principal...", end='')
    input()
    clear()

