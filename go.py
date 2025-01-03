from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget
from PyQt6.QtCore import Qt

from board import Board
from score_board import ScoreBoard
from main_menu import MainMenuPanel
from win_panel import WinPanel

class Go(QMainWindow):
    def __init__(self, game_logic):
        super().__init__()
        self.game_logic = game_logic
        self.mainMenu = MainMenuPanel(self, game_logic)
        self.board = None
        self.scoreBoard = None
        self.setWindowTitle("Go Game")
        self.setWindowIcon(QIcon("assets/icons/game_icon.png"))
        self.setFixedSize(800, 800)

    def openMainMenu(self):
        self.mainMenu = MainMenuPanel(self, self.game_logic)
        self.setCentralWidget(self.mainMenu)
        if self.scoreBoard is not None:
            self.removeDockWidget(self.scoreBoard)
        self.center()
        self.show()

    def getMainMenu(self):
        return self.mainMenu

    def openGamePlay(self):
        self.board = Board(self, self.game_logic)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard(self.game_logic, self.game_logic.get_player_turn_data)
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

    def open_win_screen(self, player_1_name, player_2_name, player_1_score, player_2_score, restart_game_event, main_menu_event):
        win_screen = WinPanel(self, player_1_name, player_2_name, player_1_score, player_2_score, restart_game_event, main_menu_event)
        win_screen.show()

    def update_scoreboard(self, black_score, white_score):
        self.scoreBoard.update_score(black_score, white_score)

    def get_board(self):
        return self.board
