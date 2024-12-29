from PyQt6.QtWidgets import QApplication
from game_logic import GameLogic
import sys

app = QApplication([])
game_logic = GameLogic()
sys.exit(app.exec())
