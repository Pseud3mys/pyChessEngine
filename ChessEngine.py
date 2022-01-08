import numpy as np

# position = (Ligne, Colonne)
num2Letter = "ABCDEFGH"
Letter2num = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
num2Number = "87654321"
Number2num = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

Team2num = {"White": 1, "Black": -1}
num2Team = [None, "White", "Black"]  # [1]=white, [-1]=black

DEPLACE = "deplace"
EAT = "eat"


# numpy mat, 1er = Ligne


def isEnemy(MApiece, position):
    if not position.isValid():
        return False
    UnknownPiece = MApiece.board.getPiecesAtPosition(position)
    # s'il n'y a aucun piece à cette cordonné
    if UnknownPiece is None:
        return False
    return UnknownPiece.team != MApiece.team


def isAlly(MApiece, position):
    if not position.isValid():
        return False
    UnknownPiece = MApiece.board.getPiecesAtPosition(position)
    # s'il n'y a aucun piece à cette cordonné
    if UnknownPiece is None:
        return False
    return UnknownPiece.team == MApiece.team


def append_ifPossible(array, move):
    if move.start.isValid() and move.end.isValid():
        array.append(move)


class Board:
    def __init__(self):
        self.matrice = np.zeros((8, 8))
        self.InGamePieces = []

    def setupStart(self):
        for c in "ABCDEFGH":
            self.addPieces(Pion(1, self, c+"2"))
            self.addPieces(Pion(-1, self, c+"7"))
        for team in range(-1, 2):
            if team == 0:
                continue
            L = "1"
            if team == -1:
                L = "8"
            self.addPieces(Rook(team, self, "A"+L))
            self.addPieces(Rook(team, self, "H"+L))
            self.addPieces(Knight(team, self, "B"+L))
            self.addPieces(Knight(team, self, "G"+L))
            self.addPieces(Bishop(team, self, "C"+L))
            self.addPieces(Bishop(team, self, "F"+L))
        self.addPieces(King(1, self, "E1"))
        self.addPieces(King(-1, self, "E8"))
        self.addPieces(Queen(1, self, "D1"))
        self.addPieces(Queen(-1, self, "D8"))

    def addPieces(self, piece):
        self.InGamePieces.append(piece)

    def getPiecesAtPosition(self, position):
        for Piece in self.InGamePieces:
            # on compare les str car les position ne seront pas le meme objet
            if str(Piece.p) == str(position):
                return Piece
        else:
            return None

    def _loop(self, piece, moves, L_opp, C_opp):
        for i in range(1, 8):
            RelativePos = Position(piece.p.L+i*L_opp, piece.p.C+i*C_opp)
            if self.getPiecesAtPosition(RelativePos):
                # on ne peut pas sauter au dessus d'un pion
                is_enemy = isEnemy(piece, RelativePos)
                if not is_enemy:
                    break
                if is_enemy:
                    append_ifPossible(moves, Move(piece, RelativePos))
                    break
            append_ifPossible(moves, Move(piece, RelativePos))

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

    def updateMatrice(self):
        for piece in self.InGamePieces:
            self.matrice[piece.p.L, piece.p.C] = piece.numID

    def __str__(self):
        self.updateMatrice()
        return str(self.matrice)


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
            return "No Valid Position L%d C%d"%(self.C, self.L)


class Move:
    def __init__(self, piece, pos):
        self.piece = piece
        self.start = piece.p
        self.end = pos
        if isEnemy(piece, self.end):
            self.type = EAT
        else:
            self.type = DEPLACE

    def __str__(self):
        return str(self.piece) + " to " + str(self.end)


class Pion:
    def __init__(self, team: int, board, position: str):
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
        devant_team = - 1 * self.team
        # peut avancer que s'il n'y a pas de piece devant
        if self.board.getPiecesAtPosition(Position((p.L + 1 * devant_team, p.C))) is None:
            append_ifPossible(moves, Move(self, (p.L + 1 * devant_team, p.C)))
            if (p.L == 1 or p.L == 6) and self.board.getPiecesAtPosition(
                    Position((p.L + 2 * devant_team, p.C))) is None:
                append_ifPossible(moves, Move(self, (p.L + 2 * devant_team, p.C)))

        if isEnemy(self, Position((p.L + 1 * devant_team, p.C + 1))):
            append_ifPossible(moves, Move(self, (p.L + 1 * devant_team, p.C + 1)))
        if isEnemy(self, Position((p.L + 1 * devant_team, p.C - 1))):
            append_ifPossible(moves, Move(self, (p.L + 1 * devant_team, p.C - 1)))
        return moves


class Knight:
    def __init__(self, team: int, board, position: str):
        self.numID = 3.2 * team
        self.team = team
        self.board = board
        self.board.addPieces(self)
        matricePos = (Number2num[position[1]], Letter2num[position[0]])
        self.p = Position(matricePos)

    def __str__(self):
        return num2Team[self.team] + " knight"

    def _move(self, moves, L_rel, C_rel):
        p = self.p
        RelativePos = Position(p.L + L_rel, p.C + C_rel)
        is_ally = isAlly(self, RelativePos)
        if not is_ally:
            append_ifPossible(moves, Move(self, RelativePos))

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
    def __init__(self, team: int, board, position: str):
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
    def __init__(self, team: int, board, position: str):
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
    def __init__(self, team: int, board, position: str):
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
    def __init__(self, team: int, board, position: str):
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
                append_ifPossible(moves, Move(self, Position(p.L + i, p.C + j)))
        return moves
