import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from alert_panel import AlertDialog
from rules_panel import RulesDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.alertWindow = AlertDialog("")
        self.rulesWindow = RulesDialog()
        self.setWindowTitle("Main Menu")
        self.setFixedSize(800, 800)  # Set screen size to 800x800

        # Set wood-style theme for the main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #deb887; /* Light wood color */
            }
            QLabel, QLineEdit, QPushButton {
                font-family: 'Verdana';
                font-size: 16px;
            }
            QPushButton {
                background-color: #8b4513; /* Dark wood color */
                color: white;
                border: 2px solid #5a3311;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #a0522d;
            }
            QLineEdit {
                background-color: #fff5e1;
                border: 1px solid #8b4513;
                border-radius: 3px;
                padding: 5px;
                color: black;
            }
        """)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        self.layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Game Title
        self.game_title = QLabel("Go Game")
        self.game_title.setFont(QFont("Verdana", 48, QFont.Weight.Bold))
        self.game_title.setStyleSheet("""
            QLabel {
                font-family: 'Verdana';
                font-size: 36px;
            }
        """)
        self.game_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.game_title)

        # Play Button (centered and larger)
        self.play_button = QPushButton("Play")
        self.play_button.setFont(QFont("Verdana", 24, QFont.Weight.Bold))
        self.play_button.setFixedSize(300, 100)
        self.play_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.play_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Rules button
        self.rules_button = QPushButton("Rules")
        self.rules_button.setFont(QFont("Verdana", 24, QFont.Weight.Bold))
        self.rules_button.setFixedSize(200, 50)
        self.rules_button.clicked.connect(self.show_rules_panel)
        self.layout.addWidget(self.rules_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Player 1 Input with Label (centered under Play button)
        self.player1_layout = QHBoxLayout()
        self.player1_input = QLineEdit()
        self.player1_input.setPlaceholderText("Enter player 1 name here...")
        self.player1_input.setFixedWidth(300)
        self.player1_layout.addWidget(self.player1_input)
        self.layout.addLayout(self.player1_layout)
        self.player1_layout.setContentsMargins(10, 10, 10, 10)
        self.player1_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Player 2 Input with Label (centered under Player 1)
        self.player2_layout = QHBoxLayout()
        self.player2_input = QLineEdit()
        self.player2_input.setPlaceholderText("Enter player 2 name here...")
        self.player2_input.setFixedWidth(300)
        self.player2_layout.addWidget(self.player2_input)
        self.layout.addLayout(self.player2_layout)

        # Center-align the Player 2 layout
        self.player2_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Generate Random Names Button (centered below input fields)
        self.generate_button = QPushButton("Generate Random Names")
        self.generate_button.clicked.connect(self.generate_random_names)
        self.layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Spacer to balance the layout
        self.layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.central_widget.setLayout(self.layout)

        #dev info
        self.dev_info = QLabel("Developed by \n Illia Movchan 3098121 \n Olzez")
        self.dev_info.setFont(QFont("Verdana", 14, QFont.Weight.Bold))
        self.dev_info.setStyleSheet("""
            QLabel {
                font-family: 'Verdana';
                font-size: 14px;
                font-style: italic;
                color: black;
            }
        """)
        self.dev_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.dev_info)

    def show_rules_panel(self):
        self.rulesWindow.showPanel()

    def generate_random_names(self):
        """Generate random names for Player 1 and Player 2."""
        random_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Jamie", "Riley", "Drew"]
        self.player1_input.setText(random.choice(random_names))
        self.player2_input.setText(random.choice(random_names))

    def start_game(self):
        if (self.player1_input.text() == "" or len(self.player1_input.text()) == 0) and (self.player2_input.text() == "" or len(self.player2_input.text()) == 0):
            self.alertWindow.showPanel("Enter player names or Select randomly")
        elif self.player1_input.text() == "" or len(self.player1_input.text()) == 0:
            self.alertWindow.showPanel("Enter player 1 name or Select randomly")
        elif self.player2_input.text() == "" or len(self.player2_input.text()) == 0:
            self.alertWindow.showPanel("Enter player 2 name or Select randomly")

        player1 = self.player1_input.text()
        player2 = self.player2_input.text()
        print(f"Starting game with Player 1: {player1}, Player 2: {player2}")
        # Add further logic for starting the game