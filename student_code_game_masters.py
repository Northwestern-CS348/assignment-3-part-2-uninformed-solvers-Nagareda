from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        peg1 = []
        peg2 = []
        peg3 = []

        disks1 = self.kb.kb_ask(parse_input('fact: (on ?disk peg1)'))
        disks2 = self.kb.kb_ask(parse_input('fact: (on ?disk peg2)'))
        disks3 = self.kb.kb_ask(parse_input('fact: (on ?disk peg3)'))




        if disks1:
            for bindings in disks1:
                for b in bindings.bindings:
                    peg1.append(int(b.constant.element[-1]))
                    peg1.sort()

        if disks2:
            for bindings in disks2:
                for b in bindings.bindings:
                    peg2.append(int(b.constant.element[-1]))
                    peg2.sort()

        if disks3:
            for bindings in disks3:
                for b in bindings.bindings:
                    peg3.append(int(b.constant.element[-1]))
                    peg3.sort()
        new = (tuple(peg1), tuple(peg2), tuple(peg3))
        return new

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        disk = str(movable_statement.terms[0])
        old_peg = str(movable_statement.terms[1])
        new_peg = str(movable_statement.terms[2])







        to_topdisk = parse_input('fact: (top ?disk ' + new_peg + ')')
        tdisk_under = ''

        if new_peg == old_peg:
            return

        if self.isMovableLegal(movable_statement):
            old_on = parse_input('fact: (on ' + disk + ' ' + old_peg + ')')
            self.kb.kb_retract(old_on)

            new_on = parse_input('fact: (on ' + disk + ' ' + new_peg + ')')
            self.kb.kb_assert(new_on)

            fact = self.kb.kb_ask(parse_input("fact: (on ?disk " + old_peg))
            if fact:
                anyleft = True
                array_of_ons = []

                for b in fact:
                    array_of_ons.append(b.bindings[0].constant.element)
                array_of_ons.sort()
                top_dog = array_of_ons[0]

            else:
                anyleft = False

            new_empty = parse_input('fact: (empty ' + new_peg + ')')
            self.kb.kb_retract(new_empty)

            if self.kb.kb_ask(to_topdisk):
                lb = self.kb.kb_ask(to_topdisk)
                tdisk_under = lb[0].bindings[0].constant.element
            t_under = parse_input('fact: (top ' + tdisk_under + ' ' + new_peg + ')')

            self.kb.kb_retract(t_under)

            new_top1 = parse_input('fact: (top ' + disk + ' ' + new_peg + ')')
            self.kb.kb_assert(new_top1)

            old_top = parse_input('fact: (top ' + disk + ' ' + old_peg + ')')
            self.kb.kb_retract(old_top)

            if not anyleft:
                old_empty = parse_input('fact: (empty ' + old_peg + ')')
                self.kb.kb_assert(old_empty)
            else:
                new_top2 = parse_input('fact: (top ' + top_dog + ' ' + old_peg + ')')
                self.kb.kb_assert(new_top2)




    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        r1 = [0, 0, 0]
        r2 = [0, 0, 0]
        r3 = [0, 0, 0]

        row1 = self.kb.kb_ask(parse_input("fact: (coordinate ?X ?pos pos1)"))
        for i in range(len(row1)):
            tile = str(row1[i].bindings[0].constant)
            pos = str(row1[i].bindings[1].constant)
            tile_num = tile[len(tile) - 1]
            pos_num = int(pos[len(pos) - 1])

            if tile_num == "y":
                r1[pos_num - 1] = -1
            else:
                r1[pos_num - 1] = int(tile_num)

        row2 = self.kb.kb_ask(parse_input("fact: (coordinate ?X ?pos pos2)"))
        for i in range(len(row2)):
            tile = str(row2[i].bindings[0].constant)
            pos = str(row2[i].bindings[1].constant)
            tile_num = tile[len(tile) - 1]
            pos_num = int(pos[len(pos) - 1])

            if tile_num == "y":
                r2[pos_num - 1] = -1
            else:
                r2[pos_num - 1] = int(tile_num)

        row3 = self.kb.kb_ask(parse_input("fact: (coordinate ?X ?pos pos3)"))
        for i in range(len(row3)):
            tile = str(row3[i].bindings[0].constant)
            pos = str(row3[i].bindings[1].constant)
            tile_num = tile[len(tile) - 1]
            pos_num = int(pos[len(pos) - 1])

            if tile_num == "y":
                r3[pos_num - 1] = -1
            else:
                r3[pos_num - 1] = int(tile_num)

        t_of_ts = (tuple(r1), tuple(r2), tuple(r3))
        return t_of_ts


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        tile = str(movable_statement.terms[0])
        old_x = str(movable_statement.terms[1])
        old_y = str(movable_statement.terms[2])
        new_x = str(movable_statement.terms[3])
        new_y = str(movable_statement.terms[4])

        old_coord = parse_input("fact: (coordinate " + tile + " " + old_x + " " + old_y + ")")
        self.kb.kb_retract(old_coord)
        old_empty = parse_input("fact: (coordinate empty " + new_x + " "  + new_y + ")")
        self.kb.kb_retract(old_empty)

        new_coord = parse_input("fact: (coordinate " + tile + " " + new_x + " " + new_y + ")")
        self.kb.kb_assert(new_coord)
        new_empty = parse_input("fact: (coordinate empty " + old_x + " " + old_y + ")")
        self.kb.kb_assert(new_empty)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
