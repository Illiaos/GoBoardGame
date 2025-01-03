import math

from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QRadialGradient, QPixmap, QFont
from PyQt6.uic.Compiler.qtproxies import QtCore
from exceptiongroup import catch

import piece
from pause_panel import PausePanel


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 9  # board is 0 squares wide # TODO this needs updating
    boardHeight = 9 #
    squareWidthSize = 90
    squareHeightSize = 90
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from
    isStarted = False
    squareEdges = [[]]

    def __init__(self, parent, game_logic):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.game_logic = game_logic
        self.ui_logic = parent
        self.pause_panel = PausePanel(self, self.pausePanelCloseEvent, self.pausePanelResetGameEvent, self.pausePanelMainMenuEvent)
        parent.setWindowTitle("GamePlay")
        # Set the style of the frame
        self.setStyleSheet("""
            QFrame {
                background-color: #deb887;
            }
            """)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        self.findClosestPoint(event.position().x(), event.position().y())
        (row, col) = self.findClosestPoint(event.position().x(), event.position().y())
        print('(row, col):', row, col)
        if self.game_logic.can_make_move(self.boardArray, row, col):
            self.resetTimer()
            if self.game_logic.check_game_over(self.boardArray, self.resetGame, self.pausePanelMainMenuEvent):
                self.timer.stop()
            self.game_logic.change_turn()
        self.printBoardArray()
        self.update()

    def findClosestPoint(self, row_data, col_data):
        min_distance = float('inf')
        nearest_row, nearest_col = -1, -1
        for row_index, row in enumerate(self.squareEdges):
            for col_index, point in enumerate(row):
                if not isinstance(point, (tuple, list)) or len(point) != 2:
                    raise ValueError(f"Invalid point format at row {row_index}, col {col_index}: {point}")
                x, y = point
                # Calculate Euclidean distance
                distance = ((x - row_data) ** 2 + (y - col_data) ** 2) ** 0.5
                # Update if this point is closer
                if distance < min_distance:
                    min_distance = distance
                    nearest_row, nearest_col = row_index, col_index

        return nearest_row, nearest_col

    def squareWidth(self):
        #returns the width of one square in the board
        return (self.contentsRect().width() / self.boardWidth) - 20

    def squareHeight(self):
        #returns the height of one square of the board
        return (self.contentsRect().height() / self.boardHeight) - 20

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        self.counter -= 1
        if self.counter < 0:
            self.resetTimer()
            self.game_logic.change_turn()
        self.updateTimerSignal.emit(self.counter)

    def resetTimer(self):
        self.counter = 10

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the background image
        background_image = QPixmap("./assets/textures/qwe.png")  # Replace with the actual image path
        painter.drawPixmap(self.rect(), background_image)
        self.squareEdges = [[0.0 for _ in range(self.boardWidth + 1)] for _ in range(self.boardHeight + 1)]
        self.squareWidthSize = int(self.squareWidth())  # Update width according to size of screen
        self.squareHeightSize = int(self.squareHeight())  # Update height according to size of screen

        self.drawBoardSquares(painter)  # Draw game board
        self.drawPieces(painter)  # Draw game pieces
        self.drawLabels(painter)  # Draw labels for rows and columns

    def drawLabels(self, painter):
        """
        Draws letters for vertical rows and numbers for horizontal columns.
        """
        painter.setPen(QColor(200, 200, 200))

        # Set a custom font for the labels
        font = QFont("Verdana", 18, QFont.Weight.Bold)  # Font family, size, weight
        painter.setFont(font)

        # Draw column labels (letters)
        letters = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'[:self.boardWidth]  # Adjust for board size
        for col in range(self.boardWidth):
            x = col * self.squareWidthSize + 80
            y = 50  # Padding from the top
            painter.drawText(x, y, self.squareWidthSize, 20, Qt.AlignmentFlag.AlignCenter, letters[col])

        # Draw row labels (numbers)
        for row in range(self.boardHeight):
            x = 50  # Padding from the left
            y = row * self.squareHeightSize + 80
            painter.drawText(x, y, 20, self.squareHeightSize, Qt.AlignmentFlag.AlignCenter, str(row + 1))

    def mousePressEvent(self, event):
        try:
            self.mousePosToColRow(event)
        except Exception as e:
            print(f"Error occurred: {e}")

    def resetGame(self):
        self.boardArray = [[0 for _ in range(self.boardWidth + 1)] for _ in range(self.boardHeight + 1)]
        self.game_logic.set_default_player_turn()
        self.resetTimer()
        self.timer.start(self.timerSpeed)
        self.update()

    def drawBoardSquares(self, painter):
        background_image = QPixmap("./assets/textures/dsa.png")  # Replace with the actual image path
        for row in range(0, int(self.boardHeight)):
            for col in range(0, int(self.boardWidth)):
                painter.save()
                x = col * self.squareWidthSize + 80
                y = row * self.squareHeightSize + 80
                self.squareEdges[row][col] = (x, y)
                if col == self.boardWidth - 1:
                    self.squareEdges[row][col + 1] = (x + self.squareWidthSize, y)
                painter.translate(x, y)

                painter.drawPixmap(0, 0, self.squareWidthSize, self.squareHeightSize, background_image)  # Draw rectangles
                painter.restore()
        last_row = self.squareEdges[-2]
        modified_row = [(x, y + self.squareHeightSize) for x, y in last_row]
        self.squareEdges[-1] = modified_row

    def drawPieces(self, painter):
        try :
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            for row in range(0, len(self.boardArray)):
                for col in range(0, len(self.boardArray[0])):
                    painter.save()
                    x, y = self.squareEdges[row][col]
                    status = self.boardArray[row][col]
                    if status == 0:
                        continue
                    if status == 1:
                        painter.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle.SolidPattern))
                    elif status == 2:
                        painter.setBrush(QBrush(QColor(255, 255, 255), Qt.BrushStyle.SolidPattern))
                    radius = self.squareWidthSize / 4
                    center = QPoint(int(x), int(y))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(center, int(radius), int(radius))
                    painter.restore()
        except Exception as e:
            print(e)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape.value:
            if self.pause_panel.isHidden():
                self.pause_panel.show()
                self.timer.stop()
                print("CALL")
        super().keyPressEvent(event)

    def pausePanelCloseEvent(self):
        self.timer.start(self.timerSpeed)
        self.updateTimerSignal.emit(self.counter)

    def pausePanelResetGameEvent(self):
        self.resetGame()

    def pausePanelMainMenuEvent(self):
        self.timer.stop()
        self.ui_logic.openMainMenu()