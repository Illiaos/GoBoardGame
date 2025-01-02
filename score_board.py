from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSlot


class ScoreBoard(QDockWidget):
    '''Base the score_board on a QDockWidget'''

    def __init__(self, get_player_turn_id):
        """
        :param get_player_turn_id: A function to get the current player's ID
        """
        super().__init__()
        self.get_player_turn_id = get_player_turn_id
        self.initUI()

    def initUI(self):
        '''Initializes ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        # Create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Create labels for displaying game state
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time Remaining: ")

        # Determine the current player's turn
        player_id = self.get_player_turn_id()
        player_color = "Black" if player_id == 1 else "White"
        self.label_turn = QLabel(f"Player {player_id}'s Turn: {player_color}")

        # Add labels to layout
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_turn)

        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)

    def update_turn_label(self):
        '''Updates the turn label based on the current player's turn'''
        player_id = self.get_player_turn_id()
        player_color = "Black" if player_id == 1 else "White"
        self.label_turn.setText(f"Player {player_id}'s Turn: {player_color}")

    def make_connection(self, board):
        '''Handles signals sent from the board class'''
        board.clickLocationSignal.connect(self.setClickLocation)
        board.updateTimerSignal.connect(self.setTimeRemaining)

    @pyqtSlot(str)
    def setClickLocation(self, clickLoc):
        '''Updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: " + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''Updates the time remaining label'''
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
