from PyQt6.QtWidgets import QApplication
from main_menu import MainWindow

from go import Go
import sys

app = QApplication([])
#myGo = Go()
mainMenu = MainWindow()
mainMenu.show()
sys.exit(app.exec())
