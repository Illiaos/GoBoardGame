from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import pyqtSlot, Qt


class ScoreBoard(QDockWidget):
    '''Base the score_board on a QDockWidget'''

    def __init__(self, game_logic, get_player_turn_data):
        """
        :param get_player_turn_data: A function to get the current player's Name
        """
        super().__init__()
        self.game_logic = game_logic
        self.get_player_turn_data = get_player_turn_data
        self.label_turn = QLabel()
        self.label_black_score = QLabel("Black Score: 0")
        self.label_white_score = QLabel("White Score: 0")
        self.initUI()

    def initUI(self):
        '''Initializes ScoreBoard UI'''
        self.resize(200, 200)

        self.setStyleSheet("""
                QWidget {
                    background-color: #f5deb3; /* Wheat color */
                }
                QDialog {
                    background-color: #f5deb3; /* Wheat color for a softer look */
                }
                QLabel {
                    font-family: 'Verdana';
                    font-size: 12px; /* Smaller font for minimalist design */
                    color: black;
                    background-color: #d2b48c; /* Tan color */
                    text-align: center;
                    border: 1px solid #8b4513; /* SaddleBrown border */
                    border-radius: 5px; /* Subtle rounding */
                    padding: 3px; /* Reduced padding for smaller elements */
                }
                QPushButton {
                    background-color: #a0522d; /* Dark wood color */
                    color: white;
                    border: 1px solid #5a3311; /* Subtle border */
                    border-radius: 5px; /* Rounded corners */
                    padding: 5px; /* Reduced padding for buttons */
                    font-size: 12px; /* Smaller font size */
                }
            
                
            """)
        # Create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Determine the current player's turn
        self.label_turn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_turn_label()
        # Create labels for displaying game state
        self.label_timeRemaining = QLabel("Time Remaining: ")



        # Add labels to layout
        self.mainLayout.addWidget(self.label_turn)
        self.mainLayout.addWidget(self.label_black_score)
        self.mainLayout.addWidget(self.label_white_score)
        self.mainLayout.addWidget(self.label_timeRemaining)


        # Add pass button
        self.pass_button = QPushButton("Pass", self)
        self.pass_button.setGeometry(100, 80, 100, 40)  # x, y, width, height
        self.pass_button.clicked.connect(self.pass_call)

        self.mainLayout.addWidget(self.pass_button)
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)

    def update_turn_label(self):
        '''Updates the turn label based on the current player's turn'''
        player_id = self.get_player_turn_data().getPlayerId()
        player_name = self.get_player_turn_data().getPlayerName()
        player_color = "Black" if player_id == 1 else "White"
        self.label_turn.setText(f"{player_name}'s \nTurn: {player_color}")

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

    def pass_call(self):
        self.game_logic.player_pass()

    def update_score(self, black_score, white_score):
        self.label_black_score.setText(f"Black Score: {black_score}")
        self.label_white_score.setText(f"White Score: {white_score}")
