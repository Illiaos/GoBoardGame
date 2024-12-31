from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget
from PyQt6.QtCore import Qt

from board import Board
from score_board import ScoreBoard
from main_menu import MainMenuPanel
from pause_panel import PausePanel


class Go(QMainWindow):
    def __init__(self, game_logic):
        super().__init__()
        self.game_logic = game_logic
        self.mainMenu = MainMenuPanel(self, game_logic)
        self.pausePanel = PausePanel(self)
        self.board = None
        self.scoreBoard = None
        self.setWindowTitle("Go Game")
        self.setFixedSize(800, 800)

    def openMainMenu(self):
        self.setCentralWidget(self.mainMenu)
        self.center()
        self.show()

    def getMainMenu(self):
        return self.mainMenu

    def openGamePlay(self):
        self.board = Board(self, self.game_logic)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.center()
        self.setWindowTitle('Go')
        self.show()


    def center(self):
        '''Centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)





