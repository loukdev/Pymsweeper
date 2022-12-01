#! python


import os


def clear():
    os.system("clear")

def get_int(mini, maxi):
    """
    Renvoie un entier compris dans l'intervalle [mini; maxi].

    Demande une nouvelle entrée tant que l'entrée utilisateur est incorrecte.
    """

    if mini > maxi:
        return get_int(maxi, mini)

    try:
        print("> ", end='')
        inp = int(input())
    except ValueError:
        print("Me prends pas pour une bille ! Merci d'entrer un chiffre :")
        return get_int(mini, maxi)

    if not mini <= inp <= maxi:
        print("Par contre, merci d'entrer un chiffre entre", mini, "et", maxi, ":")
        return get_int(mini, maxi)

    return inp

def get_pos(mw, mh, w, h):
    """
    Renvoie un tuple à deux valeurs représentant (dans l'ordre) des coordonnées (x; y).
    mw, w : respectivement, minimum et maximum des valeurs acceptées pour x.
    mh, h : respectivement, minimum et maximum des valeurs acceptées pour y.

    Demande une nouvelle entrée tant que l'entrée utilisateur est incorrecte.
    """

    print("> ", end='')
    inp = input().split(" ")
    if len(inp) < 2:
        print("Bon vas-y, là, je veux deux entiers séparés par un espace, c'est pas compliqué !")
        return get_pos(mw, mh, w, h)

    try:
        x, y = _get_2i_from(inp)
    except ValueError:
        print("Ababravo. Deux entiers, qu'on a dit !")
        return get_pos(mw, mh, w, h)

    if not mw <= x <= w or not mh <= y <= h:
        print(f"Serait-il possible d'avoir des valeurs entre `({mw}, {mh})` et `({w}, {h})` ?")
        return get_pos(mw, mh, wh)

    return x, y

def _get_2i_from(t):
    it = iter(t)

    err, x, y = None, None, None
    while True:
        try:
            x = int(next(it))
            y = int(next(it))
        except ValueError as e:
            err = e
            continue
        except StopIteration:
            break

    if x == None or y == None:
        raise err

    return x, y
