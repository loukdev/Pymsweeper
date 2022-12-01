#! python


import random as rand
from utils import clear


class Box:

    C_MINE = '*'
    C_UNKN = ' '
    C_FLAG = '!'
    C_POSS = '?'
    C_WFLA = 'x'

    def __init__(self):
        self.reset()

    def refresh(self):
        self.count = 0
        self.hidden = True
        self.flagged = False

    def reset(self):
        self.refresh()
        self.mined = False

    @property
    def revealed(self):
        return not self.hidden
    @revealed.setter
    def revealed(self, v):
        if isinstance(v, bool):
            self.hidden = not v

    def __str__(self):
        if self.hidden:
            c = Box.C_UNKN
        elif self.mined:
            c = Box.C_MINE
        elif self.flagged:
            c = Box.C_WFLA
        else:
            c = str(self.count)
        return c

class Grid:

    _DEBUG = False

    def __init__(self, w, h, nmines):
        self.set_dim(w, h, nmines)

        self._new_grid()
        self._lay_mines()


    def __repr__(self):
        w = self._w

        s = f'reste : {self._rem_clr}\n'
        s += '    '
        tmp = ' '.join( [str(i) for i in range(w)] )
        l = len(tmp)
        s += tmp + '\n'
        s += '   '
        s += ''.join( ['-' for _ in range(l)] ) + '-\n'

        i = 0
        for b in self._grid:
            if self._DEBUG: hid = b.hidden ; b.hidden = False

            if i%w == 0:
                s += f"{i//w} |"
            s += f" {b}"
            if i%w == w-1:
                s += '\n'
            i += 1

            if self._DEBUG: b.hidden = hid

        return s

    @property
    def nmines(self):
        """
        @property pour obtenir le nombre de mines.
        """
        return self._n
    @nmines.setter
    def nmines(self, n):
        """
        @property.setter pour mettre à jour le nombre de mines. Contrôle les valeurs.
        """
        if not isinstance(n, int):
            raise TypeError("Number of mines must be an `int`.")

        w, h = self._w, self._h

        self._n = w*h - 2 if n > w*h - 2 else (1 if n < 1 else n)
        self._rem_clr = w*h - self._n

    def set_dim(self, w, h, nmines=None):
        """
        Redéfinis les dimensions : la largeur et la hauteur, optionnellement le nombre de mines.
        """
        if w*h < 4:
            raise ValueError("Grid must contain at least 4 boxes (w * h must be >=4).")

        self._w, self._h = w, h
        self._l = w*h

        if nmines != None:
            self.nmines = nmines
 
    def get_at(self, x, y):
        """
        Renvoie un objet `Box` représentant la case à la position indiquée.
        """

        return self._grid[y*self._w + x]


    def refresh(self):
        """
        Réinitialise la carte en gardant ses dimensions et l'emplacement des mines.
        """

        self._rem_clr = self._l - self._n

        for b in self._grid:
            b.refresh()

    def reset(self, w, h, nmines):
        """
        Réinitialise la carte avec de nouveaux emplacements de mines.
        """
        self._lay_mines()

    def reveal_at(self, pos):
        """
        Renvoie True si la case à la position indiquée est minée, False sinon. `pos` doit être de type `(int, int)`.

        Révèle la case à la position indiquée. Si la case n'est pas minée et qu'elle n'a pas de mine ajdacente, lance une révélation récursive à partir de la position indiquée.
        """

        if not isinstance(pos, tuple) or isinstance(pos, tuple) and len(pos) < 2 or \
           not isinstance(pos[0], int) or not isinstance(pos[1], int):
            raise ValueError("Need `(int, int)` as argument.")

        x, y = pos[0], pos[1]
        if x < 0 or y < 0:
            raise ValueError("Coordinates cannot be negative.")

        box = self.get_at(x, y)

        # If box is not mined, starting recursive revealing
        # (and updating number of remaining boxes to reveal):
        if not box.mined:
            self._start_rec_reveal(x, y)
        else: # Else, simply revealing it:
            box.revealed = True

        return box.mined

    def is_cleared(self):
        """
        Renvoie `True` si la grille a été complètement révélée.
        """
        return self._rem_clr == 0


    def fix(self):
        """
        Révèle toutes les mines and montre les drapeaux erronés.
        """

        for b in self._grid:
            if b.mined: b.revealed = True

    def _new_grid(self):
        """
        Crée une nouvelle grille avec les dimensions courantes.
        """
        self._grid = [Box() for n in range(self._l)]

    def _lay_mines(self):
        """
        Pose des mines aléatoirement et supprime les anciennes.
        """
        # Create index list of future mined boxes :
        plist = [_ for _ in range(self._l)]

        # Number of mines
        n = self._n
        while n > 0:
            # Mine one random box :
            i = rand.choice(plist)
            self._grid[i].mined = True

            plist.remove(i)
            n -= 1

        # Demine remaining boxes :
        for i in plist:
            self._grid[i].mined = False

        # Update adjacent mines for all boxes :
        for i in range(self._l):
            self._count_at(i)


    def _start_rec_reveal(self, x, y):
        """
        Commence une révélation récursive en partant de la case à la position (x, y).

        Révèle la case courante. Si la case n'a pas de mine adjacente, continue la révélation récursive vers toutes les cases adjacentes.
        """
 
        box = self.get_at(x, y)
        # If already revealed, no need to start any reveal again :
        if box.revealed:
            return

        self._reveal(box)

        # Starting recursive revealing to all adjacent boxes.
        # No checking needed, it's done into self._rec_reveal_to.
        if box.count == 0:
            # Index of current box to reveal:
            i = y*self._w + x
            self._rec_reveal_to(i, -1, -1)
            self._rec_reveal_to(i,  0, -1)
            self._rec_reveal_to(i,  1, -1)

            self._rec_reveal_to(i, -1,  0)
            # self._grid[i] <=> (i,  0,  0)
            self._rec_reveal_to(i, +1,  0)

            self._rec_reveal_to(i, -1, +1)
            self._rec_reveal_to(i,  0, +1)
            self._rec_reveal_to(i,  1, +1)

    def _rec_reveal_to(self, i, ow, oh):
        """
        Continue une révélation récursive de la case i vers les offset indiqués.
        Les offsets `ow` et `oh` donnent la direction vers laquelle on est envoyée, et ne permettent d'avancer que d'un pas à la fois. Quelles que soient les valeurs envoyées, leur effet sera toujours dans l'intervalle [-1; 1].
        """

        #clear()
        #print(f"i: {i}; ow: {ow}; oh:{oh}")
        #print(self, "En attente...", sep='\n')

        w, h = self._w, self._h
        x, y = i%w + ow, i//w + oh

         # If it brings us off the grid, we stop now.
        if not (0 <= x < w) or \
           not (0 <= y < h):
            return

        # Recalculating index of current box:
        i += self._w*oh + ow

        box = self.get_at(x, y)
        # If already revealed or mined, no need to continue:
        if box.revealed or box.mined:
            return

        #print(f"Processing at {i} ({x}; {y})... ", end='')
        #input()

        self._reveal(box)

        # T = Top, B = Bottom, L = Left, R = Right.
        # If no adjacent mine, then we continue recursive revealing:
        if box.count == 0:
            # if currently going T or L
            if oh < 0 or ow < 0:
                self._rec_reveal_to(i, -1, -1) # going to TL
            # if currently going T
            if oh < 0:
                self._rec_reveal_to(i,  0, -1) # going to T
            # if currently going T or R
            if oh < 0 or ow > 0:
                self._rec_reveal_to(i, +1, -1) # going to TR

            # if currently going L
            if ow < 0:
                self._rec_reveal_to(i, -1,  0) # going to L
            # not going again on current box
            #   self._rec_reveal_to(i,  0,  0)
            # if currently going R
            if ow > 0:
                self._rec_reveal_to(i, +1,  0) # going to R

            # if currently going B or L
            if oh > 0 or ow < 0:
                self._rec_reveal_to(i, -1, +1) # going to BL
            # if currently going B
            if oh > 0:
                self._rec_reveal_to(i,  0, -1) # going to B
            # if currently going B or R
            if oh > 0 or ow > 0:
                self._rec_reveal_to(i, +1, +1) # going to BR

    def _reveal(self, box):
        box.revealed = True
        self._rem_clr -= 1

    def _count_at(self, i):
        """
        Met à jour le nombre de mines de l'objet `Box` à position indiquée.
        """

        w, h = self._w, self._h
        x, y = i%w, i//w

        box = self.get_at(x, y)
        box.count = 0

        # L = left ; R = right ; T = top ; B = bottom
        # Looking at the T line
        if y > 0:
            # Looking at the TL
            if x > 0 and self._grid[i-w-1].mined:
                box.count += 1
            # Looking at the T
            if self._grid[i-w].mined:
                box.count += 1
            # Looking at the TR
            if x < w-1 and self._grid[i-w+1].mined:
                box.count += 1

        # Looking at the current line
        # Looking at the L
        if x > 0 and self._grid[i-1].mined:
            box.count += 1
        # Looking at the R
        if x < w-1 and self._grid[i+1].mined:
            box.count += 1

        # Looking at the B line
        if y < h-1:
            # Looking at the BL
            if x > 0 and self._grid[i+w-1].mined:
                box.count += 1
            # Looking at the B
            if self._grid[i+w].mined:
                box.count += 1
             # Looking at the BR
            if x < w-1 and self._grid[i+w+1].mined:
                box.count += 1

