#! python

from pymsweeper import *
from utils import clear


def main():

    clear()

    while True:
        inp = main_menu()
        if inp == M_QUIT:
            break
        elif inp == M_PLAY:
            play()
        elif inp == M_RULS:
            show_rules()
        else:
            print("Ceci n'est pas sensé arriver...")

    print("Kenavo !")


if __name__ == "__main__":

    main()
