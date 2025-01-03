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
        self.setWindowIcon(QIcon("assets/icons/game_icon.png")) #Set Icon for a game
        self.setFixedSize(800, 800)

    #Method to open and display the main menu panel
    def openMainMenu(self):
        self.mainMenu = MainMenuPanel(self, self.game_logic)
        self.setCentralWidget(self.mainMenu)
        #If a score board exists, remove it from the window
        if self.scoreBoard is not None:
            self.removeDockWidget(self.scoreBoard)
        self.center()
        self.show()

    def getMainMenu(self):
        return self.mainMenu

    #Method to initialize and open the game board and related UI components
    def openGamePlay(self):
        self.board = Board(self, self.game_logic)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard(self.game_logic, self.game_logic.get_player_turn_data)
        #Add the ScoreBoard widget as a dockable widget on the right side of the main window
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        #Establish connections between the ScoreBoard and the Board, such as updating the score
        self.scoreBoard.make_connection(self.board)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    #Centers the window on the screen
    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    #Method to open win screen
    def open_win_screen(self, player_1_name, player_2_name, player_1_score, player_2_score, restart_game_event, main_menu_event):
        win_screen = WinPanel(self, player_1_name, player_2_name, player_1_score, player_2_score, restart_game_event, main_menu_event)
        win_screen.show()

    #Method to update players score
    def update_scoreboard(self, black_score, white_score):
        self.scoreBoard.update_score(black_score, white_score)

    #Method to return board class
    def get_board(self):
        return self.board
