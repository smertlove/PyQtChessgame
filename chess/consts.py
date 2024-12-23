from enum import Enum


SQUARE_SIZE = 20

BG_COLOR = "#302c2b"

LIGHT_SQUARE_BG = "#eeeed2"
DARK_SQUARE_BG = "#769656"


class Color(Enum):
    BLACK = 1
    WHITE = 2


class Piece(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
