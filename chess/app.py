from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)

from screeninfo import get_monitors
import sys

from .tools import set_obj_color
from .consts import BG_COLOR
from .chessboard import ChessBoard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("chess.ru")

        h = int(get_monitors()[0].height / 1.5)

        set_obj_color(self, "white", BG_COLOR)

        chessboard = ChessBoard(h)
        self.setCentralWidget(chessboard)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
