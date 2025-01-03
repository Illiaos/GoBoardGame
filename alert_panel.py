from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

#Panel to illustrate an alert made by user, with close option, to quickly recover
class AlertPanel(QDialog):
    def __init__(self, parent, message, title="Alert"):
        super().__init__(parent)
        self.setModal(True)
        self.setParent(parent)
        self.setWindowTitle("")  # No title
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Remove the title bar and close button
        self.setFixedSize(300, 200)  # Set a fixed size for the alert dialog

        #set style for a panel
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
                background-color: #8b4513;
                color: white;
                border: 2px solid #5a3311;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Verdana';
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #a0522d;
            }
        """)

        # Set up the layout and components
        layout = QVBoxLayout()

        # Title at the top, styled as bold, red, and large
        self.title_label = QLabel(title)
        self.title_label.setObjectName("title")
        self.title_label.setStyleSheet("""
        QLabel {
                font-family: 'Verdana';
                font-size: 22px;  /* Larger font size */
                color: red;  /* Red title color */
                font-weight: bold;  /* Bold font */
                background-color: transparent;  /* No background for the title */
                padding: 10px;
                text-align: center;
                margin-bottom: 10px;
        }""")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a label to show the message
        self.message_label = QLabel(message)
        self.message_label.setFont(QFont("Verdana", 12))
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.setFont(QFont("Verdana", 12))
        self.ok_button.clicked.connect(self.hide)  #Connecte a method to close the panel

        layout.addWidget(self.title_label)  # Add title
        layout.addWidget(self.message_label)  # Add message
        layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Add OK button

        self.setLayout(layout)

    def showPanel(self, message):
        self.message_label.setText(message) #Set message text, when window is opened
        self.centerDialog() #Center dialog panel
        super().show()

    def hide(self):
        super().hide()

    def centerDialog(self):
        parent_geometry = self.parent().frameGeometry()
        self_geometry = self.frameGeometry()
        center_point = parent_geometry.center()
        self_geometry.moveCenter(center_point)
        self.move(self_geometry.topLeft())
