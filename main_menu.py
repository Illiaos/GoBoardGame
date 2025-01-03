import random
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QSpacerItem,
    QSizePolicy, QFrame, QApplication
)
from PyQt6.QtGui import QFont, QPainter, QPixmap
from PyQt6.QtCore import Qt

from alert_panel import AlertPanel
from rules_panel import RulesPanel

class MainMenuPanel(QFrame):
    def __init__(self, parent: QMainWindow, game_logic):
        super().__init__(parent)
        self.setParent(parent)
        self.game_logic = game_logic
        self.alertWindow = AlertPanel(parent,"")
        self.rulesWindow = RulesPanel(parent)
        parent.setWindowTitle("Main Menu")

        # Create a QLabel for the background
        self.background_label = QLabel(self)
        background_image = QPixmap("./assets/textures/main.png")  # Replace with your image path
        self.background_label.setPixmap(background_image)
        self.background_label.setScaledContents(True)




        # Set the style of the frame
        self.setStyleSheet("""
        
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

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        self.layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))



        # Game Title
        self.game_title = QLabel("Go Game")
        self.game_title.setFont(QFont("Verdana", 48, QFont.Weight.Bold))
        self.game_title.setStyleSheet("""
            QLabel {
                color: #8b4513;
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

        # Add a QLabel for displaying rules (hidden by default)
        self.rules_label = QLabel(
            "Go Board Rules:\n"
        
            "1. Place stones on empty intersections.\n"
            "2. The winning condition = surround more territory than your opponent.\n"
            "3. Stones surrounded by the opponent are captured.\n"
            "4. The game ends when both players pass.\n"
            "5. Scoring is based on territory and captured stones."
        )
        self.rules_label.setFont(QFont("Verdana", 24))
        self.rules_label.setWordWrap(True)
        self.rules_label.setStyleSheet("""
            QLabel {
                font family: 'Verdana';
                font-style: italic;
                text-size: 24px;
                color: white;
                padding: 10px;
                background-color: #8b4513;
                border: 2px solid black;
                border-radius: 5px;
            }
        """)
        self.rules_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.rules_label.hide()  # Initially hidden
        self.layout.addWidget(self.rules_label)

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

        # Dev info
        # Create a container for the background
        self.dev_info_container = QWidget()
        self.dev_info_container.setStyleSheet("""
            QWidget {
                background-color: #8b4513;
                border: 2px solid black;
                border-radius: 10px;
            }
        """)

        # Create the text label
        self.dev_info_text = QLabel("Developed by \n Illia Movchan 3098121 \n Olzhas Samat 3095916")
        self.dev_info_text.setFont(QFont("Verdana", 14, QFont.Weight.Bold))
        self.dev_info_text.setStyleSheet("""
            QLabel {
                font-family: 'Verdana';
                font-size: 14px;
                font-style: italic;
                color: white;
                border: none;
            }
        """)
        self.dev_info_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the text label to the container using a layout
        container_layout = QVBoxLayout(self.dev_info_container)
        container_layout.setContentsMargins(10, 10, 10, 10)  # Padding inside the container
        container_layout.addWidget(self.dev_info_text)

        # Set the container to have a fixed width
        self.dev_info_container.setFixedWidth(300)

        # Create spacers for vertical centering
        self.layout.addWidget(self.dev_info_container,  alignment=Qt.AlignmentFlag.AlignHCenter)  # Center container horizontally

        # Set the layout for this frame
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def show_rules_panel(self):
        """Toggle visibility of the rules label."""
        if self.rules_label.isVisible():
            self.rules_label.hide()
        else:
            self.rules_label.show()

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
        else:
            self.game_logic.start_new_game(self.player1_input.text(), self.player2_input.text())

    def resizeEvent(self, event):
        """Ensure the background image covers the entire widget on resize."""
        self.background_label.setGeometry(self.rect())