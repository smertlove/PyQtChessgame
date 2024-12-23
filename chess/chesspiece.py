from .consts import Color, Piece
from PyQt5.QtWidgets import QLabel


class ChessPiece(QLabel):
    chess_map = {
        Color.WHITE: {
            Piece.PAWN: "♙",
            Piece.ROOK: "♖",
            Piece.KNIGHT: "♘",
            Piece.BISHOP: "♗",
            Piece.QUEEN: "♕",
            Piece.KING: "♔",
        },
        Color.BLACK: {
            Piece.PAWN: "♟",
            Piece.ROOK: "♜",
            Piece.KNIGHT: "♞",
            Piece.BISHOP: "♝",
            Piece.QUEEN: "♛",
            Piece.KING: "♚",
        },
    }

    def __init__(self, color: Color, piece: Piece):
        super().__init__()
        self.text_ = self.chess_map[color][piece]
        self.type = piece
        self.color = color

    def __str__(self):
        return self.text_

    def __repr__(self):
        return self.text_

    def promote(self, to: Piece):
        self.type = to
        self.text_ = self.chess_map[self.color][self.type]
