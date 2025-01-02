from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class WinPanel(QDialog):
    def __init__(self, parent, player_1_name, player_2_name, black_score, white_score, restart_callback, main_menu_callback):
        super().__init__(parent)
        self.setModal(True)
        self.setParent(parent)
        self.setWindowTitle("")  # No title
        self.centerDialog()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Remove the title bar and close button
        self.setFixedSize(300, 200)  # Set a fixed size for the alert dialog
        self.restart_callback = restart_callback
        self.main_menu_callback = main_menu_callback
        self.setStyleSheet("""
            QDialog {
                background-color: #deb887; /* Light wood color */
                border: 5px solid black;  /* Black border around the window */
                border-radius: 10px;  /* Rounded corners */
            }
            QLabel {
                font-family: 'Verdana';
                font-size: 12px;  /* Larger font size */
                color: black;  /* Red title color */
                font-weight: bold;  /* Bold font */
                background-color: transparent;  /* No background for the title */
                padding: 10px;
                text-align: center;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #8b4513; /* Dark wood color */
                color: white;
                border: 2px solid #5a3311;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Verdana';
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #a0522d;  /* Lighter wood color on hover */
            }
        """)

        # Set up the layout and components
        layout = QVBoxLayout()

        # Title at the top, styled as bold, red, and large
        layout.addStretch()
        self.win_label = QLabel(self)
        if black_score > white_score:
            self.win_label.setText(f"🎉 {player_1_name} Win! 🎉")
        else:
            self.win_label.setText(f"🎉 {player_2_name} Win! 🎉")
        self.win_label.setStyleSheet("font-size: 24px;")
        self.win_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.win_label.setWordWrap(True)  # Enable word wrapping
        self.win_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        #set black score
        self.black_score_label = QLabel(self)
        self.black_score_label.setText(f"Black score: {black_score}")
        self.black_score_label.setStyleSheet("font-size: 20px; color: black;")
        self.black_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #set white score
        self.white_score_label = QLabel(self)
        self.white_score_label.setText(f"White score: {white_score}")
        self.white_score_label.setStyleSheet("font-size: 20px; color: black;")
        self.white_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create Restart Button button
        self.restart_button = QPushButton("Restart Game")
        self.restart_button.setFont(QFont("Verdana", 12))
        self.restart_button.clicked.connect(self.restart_game)

        # Create Main Menu Button button
        self.menu_button = QPushButton("Main Menu")
        self.menu_button.setFont(QFont("Verdana", 12))
        self.menu_button.clicked.connect(self.main_menu)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.restart_button)
        button_layout.addWidget(self.menu_button)

        layout.addWidget(self.win_label)  # Add title
        layout.addWidget(self.black_score_label) #Add black score
        layout.addWidget(self.white_score_label) #Add white score
        #layout.addWidget(self.restart_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Add Restart button
        #layout.addWidget(self.menu_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Add Main Menu button
        layout.addLayout(button_layout)

        self.setLayout(layout)
    def restart_game(self):
        self.restart_callback()
        self.hide()

    def main_menu(self):
        self.main_menu_callback()
        self.hide()

    def centerDialog(self):
        parent_geometry = self.parent().frameGeometry()
        self_geometry = self.frameGeometry()
        center_point = parent_geometry.center()
        self_geometry.moveCenter(center_point)
        self.move(self_geometry.topLeft())
