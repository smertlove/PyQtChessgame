from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QLabel,
)

from PyQt5.QtGui import QFont

from .consts import Piece, Color, LIGHT_SQUARE_BG, DARK_SQUARE_BG
from .chesspiece import ChessPiece
from .tools import set_obj_color


class BoardSquare(QLabel):

    color_palette = {
        Color.WHITE: {"bg": LIGHT_SQUARE_BG, "text": DARK_SQUARE_BG},
        Color.BLACK: {"bg": DARK_SQUARE_BG, "text": LIGHT_SQUARE_BG},
    }

    def __init__(
        self,
        text: str | None,
        type_: Color,
        transparent=False,
        text_alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,
    ):
        super().__init__()
        if text is not None:
            self.setText(text)
            self.setFont(QFont("Arial", 16))

        palette = self.color_palette[type_]
        bg_color = "rgba(0, 0, 0, 0)" if transparent else palette["bg"]
        set_obj_color(
            self,
            palette["text"],
            bg_color,
        )

        self.setAlignment(text_alignment)


class PlayingSquare(QLabel):

    letters = "abcdefgh"

    def __init__(
        self,
        master: "PlayingChessBoard",
        i,
        j,
    ):
        super().__init__()
        self.coords = (i, j)
        self.get_transparent()
        self.setFont(QFont("Arial", 48))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.piece: ChessPiece | None = None
        self.master = master

    def get_darker(self):
        set_obj_color(
            self,
            "rgba(0, 0, 0, 255)",
            "rgba(0, 0, 0, 150)",
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.piece} {self.coords})"

    def get_transparent(self):
        set_obj_color(
            self,
            "rgba(0, 0, 0, 255)",
            "rgba(0, 0, 0, 0)",
        )

    def get_name(self) -> str:
        return f"{self.letters[self.coords[1]]}{8 - self.coords[0]}"

    def place_piece(self, piece: ChessPiece):
        if (
            self.coords[0] == 0
            and piece.type == Piece.PAWN
            and piece.color == Color.WHITE
        ):
            piece.promote(Piece.QUEEN)
        elif (
            self.coords[0] == 7
            and piece.type == Piece.PAWN
            and piece.color == Color.BLACK
        ):
            piece.promote(Piece.QUEEN)

        self.setText(str(piece))
        self.piece = piece

    def rm_piece(self):
        self.setText("")
        self.piece = None

    def has_piece(self):
        return self.piece is not None

    def __gt__(self, other):
        other.place_piece(self.piece)
        self.rm_piece()

    def mousePressEvent(self, event):
        self.master.selected = self


class ChessBoardGrid(QWidget):

    n = 8
    m = 8

    square_types = (Color.WHITE, Color.BLACK,)

    letters = "abcdefgh"
    numbers = "87654321"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QGridLayout()

        for i in range(self.n):
            for j in range(self.m):
                squares = self.make_squares(i, j)
                for square in squares:
                    layout.addWidget(square, i, j)

        layout.setSpacing(0)
        self.setLayout(layout)

    def make_squares(self, i, j) -> list[BoardSquare | PlayingSquare]:
        raise NotImplementedError


class ChessBoardMarkup(ChessBoardGrid):

    def make_squares(self, i, j) -> list[BoardSquare | PlayingSquare]:
        squares = [BoardSquare(None, self.square_types[(i + j) % 2])]

        if j == 0:
            digit_square = BoardSquare(
                self.numbers[i],
                self.square_types[(i + j) % 2],
                transparent=True,
                text_alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
            )
            squares.append(digit_square)

        if i == self.n - 1:
            letter_square = BoardSquare(
                self.letters[j],
                self.square_types[(i + j) % 2],
                transparent=True,
                text_alignment=Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignBottom,
            )
            squares.append(letter_square)

        return squares


class PlayingChessBoard(ChessBoardGrid):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._selected: None | PlayingSquare = None
        self.to_move = Color.WHITE
        print("White to move...")

    @property
    def selected(self) -> None | PlayingSquare:
        return self._selected

    @selected.setter
    def selected(self, target: PlayingSquare) -> None:

        if self.selected is not None:
            self._selected.get_transparent()  # type: ignore

        if (
            self._selected is None
            or not self._selected.has_piece()
            or self.selected.piece.color != self.to_move  # type: ignore
            or (
                self.selected is not None
                and
                target.piece is not None
                and
                self.selected.piece.color == target.piece.color
            )
        ):
            self._selected = target
            self._selected.get_darker()

        else:
            print(f"MOVE {self._selected} > {target}")
            self._selected > target
            self._selected = None

            if self.to_move == Color.WHITE:
                self.to_move = Color.BLACK
                print("Black to move...")
            else:
                self.to_move = Color.WHITE
                print("White to move...")

    def __repr__(self):
        return f"{self.__class__.__name__}({self._selected})"

    def make_squares(self, i, j):
        playing_square = PlayingSquare(self, i, j)

        piece_needed = self.piece_needed(i, j)
        if piece_needed:
            playing_square.place_piece(ChessPiece(*piece_needed))
        return [playing_square]

    @classmethod
    def piece_needed(cls, i, j) -> tuple[Color, Piece] | bool:
        if i == 1:
            return Color.BLACK, Piece.PAWN

        elif i == 0:
            if j in (0, 7):
                return Color.BLACK, Piece.ROOK

            elif j in (1, 6):
                return Color.BLACK, Piece.KNIGHT

            elif j in (2, 5):
                return Color.BLACK, Piece.BISHOP

            elif j == 3:
                return Color.BLACK, Piece.QUEEN

            elif j == 4:
                return Color.BLACK, Piece.KING

        elif i == 6:
            return Color.WHITE, Piece.PAWN

        elif i == 7:
            if j in (0, 7):
                return Color.WHITE, Piece.ROOK

            elif j in (1, 6):
                return Color.WHITE, Piece.KNIGHT

            elif j in (2, 5):
                return Color.WHITE, Piece.BISHOP

            elif j == 3:
                return Color.WHITE, Piece.QUEEN

            elif j == 4:
                return Color.WHITE, Piece.KING

        return False


class ChessBoard(QWidget):
    def __init__(self, h: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(h)
        self.setFixedHeight(h)
        layout = QGridLayout()
        layout.addWidget(ChessBoardMarkup(), 0, 0)
        layout.addWidget(PlayingChessBoard(), 0, 0)
        self.setLayout(layout)
