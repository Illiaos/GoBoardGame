from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class PausePanel(QDialog):
    def __init__(self, parent, title="Pause Menu"):
        super().__init__(parent)
        self.setModal(True)
        self.setParent(parent)
        self.setWindowTitle("")  # No title
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Remove the title bar and close button
        self.setFixedSize(200, 300)  # Set a fixed size for the alert dialog

        self.setStyleSheet("""
            QDialog {
                background-color: #deb887;
                border: 5px solid black;
                border-radius: 10px;
            }
            QLabel {
                font-family: 'Verdana';
                font-size: 12px;
                color: black;
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

        layout = QVBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
        QLabel {
                font-family: 'Verdana';
                font-size: 22px;  /* Larger font size */
                color: black;  /* Red title color */
                font-weight: bold;  /* Bold font */
                background-color: transparent;  /* No background for the title */
                padding: 10px;
                text-align: center;
                margin-bottom: 10px;
        }""")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create resume button
        self.resume_button = QPushButton("Resume")
        self.resume_button.setFont(QFont("Verdana", 12))
        self.resume_button.setFixedSize(100, 50)
        self.resume_button.clicked.connect(self.resume_game)

        # Create restart button
        self.restart_button = QPushButton("Restart")
        self.restart_button.setFont(QFont("Verdana", 12))
        self.restart_button.setFixedSize(100, 50)
        self.restart_button.clicked.connect(self.restart_game)

        # Create main menu button
        self.menu_button = QPushButton("Main Menu")
        self.menu_button.setFont(QFont("Verdana", 12))
        self.menu_button.setFixedSize(100, 50)
        self.menu_button.clicked.connect(self.open_main_menu)

        layout.addWidget(self.title_label)  # Add title
        layout.addWidget(self.resume_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.restart_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.menu_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def resume_game(self):
        self.hide()

    def restart_game(self):
        self.hide()

    def open_main_menu(self):
        self.hide()

    def hide(self):
        super().hide()

    def centerDialog(self):
        parent_geometry = self.parent().frameGeometry()
        self_geometry = self.frameGeometry()
        center_point = parent_geometry.center()
        self_geometry.moveCenter(center_point)
        self.move(self_geometry.topLeft())
