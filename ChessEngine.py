import numpy as np

# position = (Ligne, Colonne)
num2Letter = "abcdefgh"
Letter2num = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
num2Number = "87654321"
Number2num = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

Team2num = {"White": 1, "Black": -1}
num2Team = [None, "White", "Black"]  # [1]=white, [-1]=black

DEPLACE = "deplace"
EAT = "eat"


# numpy mat, 1er = Ligne


class Position:
    def __init__(self, pos, C=None):
        if C is not None:
            self.L = pos
            self.C = C
        else:
            self.L = pos[0]
            self.C = pos[1]

    def pack(self):
        return self.L, self.C

    def isValid(self):
        return 0 <= self.L <= 7 and 0 <= self.C <= 7

    def __str__(self):
        if self.isValid():
            return num2Letter[self.C] + num2Number[self.L]
        else:
            return "Invalid Position L%d C%d" % (self.C, self.L)


class Move:
    def __init__(self, piece, pos: Position):
        self.piece = piece
        self.team = piece.team
        self.start = piece.p
        self.end = pos
        if isEnemy(piece, self.end):
            self.type = EAT
        else:
            self.type = DEPLACE

    def isValid(self, eatOnly=False):
        one = self.start.isValid() and self.end.isValid()
        # on peut pas bouger sur un allier (pas comestible)
        two = not isAlly(self.piece, self.end)
        if eatOnly:
            two = isEnemy(self.piece, self.end)
        return one and two

    def __str__(self):
        return str(self.piece) + " to " + str(self.end)


class Board:
    def __init__(self):
        self.matrice = np.zeros((8, 8))
        self.InGamePieces = []
        self.AllMoves = []

    def setupStart(self):
        for c in "abcdefgh":
            self.addPieces(Pawn(1, self, c + "2"))
            self.addPieces(Pawn(-1, self, c + "7"))
        for team in range(-1, 2):
            if team == 0:
                continue
            L = "1"
            if team == -1:
                L = "8"
            self.addPieces(Rook(team, self, "a" + L))
            self.addPieces(Rook(team, self, "h" + L))
            self.addPieces(Knight(team, self, "b" + L))
            self.addPieces(Knight(team, self, "g" + L))
            self.addPieces(Bishop(team, self, "c" + L))
            self.addPieces(Bishop(team, self, "f" + L))
        self.addPieces(King(1, self, "e1"))
        self.addPieces(King(-1, self, "e8"))
        self.addPieces(Queen(1, self, "d1"))
        self.addPieces(Queen(-1, self, "d8"))

    def addPieces(self, piece):
        self.InGamePieces.append(piece)

    def getPiecesAtPosition(self, position: Position):
        for Piece in self.InGamePieces:
            # on compare les str car les position ne seront pas le meme objet
            if str(Piece.p) == str(position):
                return Piece
        else:
            return None

    def _loop(self, piece, moves: list, L_opp: int, C_opp: int):
        for i in range(1, 8):
            RelativePos = Position(piece.p.L + i * L_opp, piece.p.C + i * C_opp)
            if self.getPiecesAtPosition(RelativePos):
                # on ne peut pas sauter au dessus d'un pion
                is_enemy = isEnemy(piece, RelativePos)
                m = Move(piece, RelativePos)
                if m.isValid():
                    moves.append(m)
                break
            m = Move(piece, RelativePos)
            if m.isValid():
                moves.append(m)

    def generateLineMoves(self, piece):
        moves = []
        self._loop(piece, moves, 1, 0)
        self._loop(piece, moves, -1, 0)
        self._loop(piece, moves, 0, 1)
        self._loop(piece, moves, 0, -1)
        return moves

    def generateDiagMoves(self, piece):
        moves = []
        self._loop(piece, moves, 1, 1)
        self._loop(piece, moves, 1, -1)
        self._loop(piece, moves, -1, 1)
        self._loop(piece, moves, -1, -1)
        return moves

    def generateAllMoves(self):
        self.AllMoves = []
        for piece in self.InGamePieces:
            self.AllMoves += piece.getValidMoves()

    def updateMatrice(self):
        for piece in self.InGamePieces:
            self.matrice[piece.p.L, piece.p.C] = piece.numID

    def __str__(self):
        self.updateMatrice()
        return str(self.matrice)


class Pawn:
    def __init__(self, team: int, board: Board, position: str):
        self.numID = 1.0 * team
        self.team = team
        self.board = board
        self.board.addPieces(self)
        matricePos = (Number2num[position[1]], Letter2num[position[0]])
        self.p = Position(matricePos)

    def __str__(self):
        return num2Team[self.team] + " Pawn"

    def getValidMoves(self):
        moves = []
        p = self.p
        TeamForward = - 1 * self.team  # On step forward
        m = Move(self, Position(p.L + TeamForward, p.C))
        if m.isValid():
            moves.append(m)
            m2 = Move(self, Position(p.L + 2 * TeamForward, p.C))
            if (p.L == 1 or p.L == 6) and m2.isValid():
                moves.append(m2)

        mEat1 = Move(self, Position(p.L + TeamForward, p.C + 1))
        mEat2 = Move(self, Position(p.L + TeamForward, p.C - 1))
        if mEat1.isValid(eatOnly=True):
            moves.append(mEat1)
        if mEat2.isValid(eatOnly=True):
            moves.append(mEat2)
        return moves


class Knight:
    def __init__(self, team: int, board: Board, position: str):
        self.numID = 3.2 * team
        self.team = team
        self.board = board
        self.board.addPieces(self)
        matricePos = (Number2num[position[1]], Letter2num[position[0]])
        self.p = Position(matricePos)

    def __str__(self):
        return num2Team[self.team] + " knight"

    def _move(self, moves: list, L_rel: int, C_rel: int):
        p = self.p
        RelativePos = Position(p.L + L_rel, p.C + C_rel)
        m = Move(self, RelativePos)
        if m.isValid():
            moves.append(m)

    def getValidMoves(self):
        moves = []
        self._move(moves, 2, 1)
        self._move(moves, 2, -1)
        self._move(moves, 1, 2)
        self._move(moves, -1, 2)
        self._move(moves, -2, 1)
        self._move(moves, -2, -1)
        self._move(moves, 1, -2)
        self._move(moves, -1, -2)
        return moves


class Bishop:
    def __init__(self, team: int, board: Board, position: str):
        self.numID = 3.3 * team
        self.team = team
        self.board = board
        self.board.addPieces(self)
        matricePos = (Number2num[position[1]], Letter2num[position[0]])
        self.p = Position(matricePos)

    def __str__(self):
        return num2Team[self.team] + " rook"

    def getValidMoves(self):
        moves = self.board.generateDiagMoves(self)
        return moves


class Queen:
    def __init__(self, team: int, board: Board, position: str):
        self.numID = 8.8 * team
        self.team = team
        self.board = board
        self.board.addPieces(self)
        matricePos = (Number2num[position[1]], Letter2num[position[0]])
        self.p = Position(matricePos)

    def __str__(self):
        return num2Team[self.team] + " rook"

    def getValidMoves(self):
        moves = self.board.generateLineMoves(self)
        moves += self.board.generateDiagMoves(self)
        return moves


class Rook:
    def __init__(self, team: int, board: Board, position: str):
        self.numID = 5.1 * team
        self.team = team
        self.board = board
        self.board.addPieces(self)
        matricePos = (Number2num[position[1]], Letter2num[position[0]])
        self.p = Position(matricePos)

    def __str__(self):
        return num2Team[self.team] + " rook"

    def getValidMoves(self):
        moves = self.board.generateLineMoves(self)
        return moves


class King:
    def __init__(self, team: int, board: Board, position: str):
        self.numID = 10 * team
        self.team = team
        self.board = board
        self.board.addPieces(self)
        matricePos = (Number2num[position[1]], Letter2num[position[0]])
        self.p = Position(matricePos)

    def __str__(self):
        return num2Team[self.team] + " king"

    def getValidMoves(self):
        moves = []
        p = self.p
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                m = Move(self, Position(p.L + i, p.C + j))
                if m.isValid():
                    moves.append(m)
        return moves


def isEnemy(MApiece, position: Position):
    if not position.isValid():
        return False
    UnknownPiece = MApiece.board.getPiecesAtPosition(position)
    # s'il n'y a aucun piece à cette cordonné
    if UnknownPiece is None:
        return False
    return UnknownPiece.team != MApiece.team


def isAlly(MApiece, position: Position):
    if not position.isValid():
        return False
    UnknownPiece = MApiece.board.getPiecesAtPosition(position)
    # s'il n'y a aucun piece à cette cordonné
    if UnknownPiece is None:
        return False
    return UnknownPiece.team == MApiece.team


str2Piece = {"R": King,
             "D": Queen,
             "F": Bishop,
             "C": Knight,
             "T": Rook}


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.board.setupStart()
        self.board.generateAllMoves()
        self.turn = 1  # turn team

    def read_Move(self, str_move, str_team):
        if len(str_move) == 2:
            lettre = str_move[0]
            chiffre = str_move[1]
            piece_class = Pawn
        elif len(str_move) == 3:
            pion = str_move[0]
            lettre = str_move[1]
            chiffre = str_move[2]
            try:
                piece_class = str2Piece[pion]
            except:
                print("Pion inconnu.")
                return
        else:
            print("connais po.")
            return None
        for move in self.board.AllMoves:
            if str(move.end) == lettre + chiffre:
                if type(move.piece) == piece_class and move.team == Team2num[str_team]:
                    return move
        else:
            print("no valid move find.")
            return None

    def play_next(self):
        self.board.generateAllMoves()
        move = None
        while not move:
            str_team = num2Team[self.turn]
            player_in = input("move for %s: " % str_team)
            move = self.read_Move(player_in, str_team)
        self.turn *= -1  # change team
