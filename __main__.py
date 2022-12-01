#! python

from pymsweeper import *
from utils import clear


def main():

    clear()

    while True:
        inp = main_menu()
        if inp == QUIT:
            break
        elif inp == PLAY:
            play()
        else:
            print("Ceci n'est pas sensé arriver...")

    print("Kenavo !")


if __name__ == "__main__":

    main()

