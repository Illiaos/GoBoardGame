import math

from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QRadialGradient
from exceptiongroup import catch

import piece


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7 #
    squareWidthSize = 90
    squareHeightSize = 90
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from
    isStarted = False
    squareEdges = [[]]

    def __init__(self, parent, game_logic):
        super().__init__(parent)
        self.initBoard()
        self.game_logic = game_logic
        parent.setWindowTitle("GamePlay")
        # Set the style of the frame
        self.setStyleSheet("""
            QFrame {
                background-color: #deb887;
            }
            """)

    def initBoard(self):
        '''initiates board'''
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.boardArray = [[0 for _ in range(self.boardWidth + 1)] for _ in range(self.boardHeight + 1)]  # TODO - create a 2d int/Piece array to store the state of the game
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        self.findClosestPoint(event.position().x(), event.position().y())
        (row, col) = self.findClosestPoint(event.position().x(), event.position().y())
        print('(row, col):', row, col)
        if row != -1 and col != -1 or self.boardArray[row][col] == 0:
            self.boardArray[row][col] = self.game_logic.get_player_turn_id()
            self.resetTimer()
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
        self.updateTimerSignal.emit(self.counter)

    def resetTimer(self):
        self.counter = 10
        self.game_logic.change_turn()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.squareEdges = [[0.0 for _ in range(self.boardWidth + 1)] for _ in range(self.boardHeight + 1)]
        self.squareWidthSize = int(self.squareWidth()) #update width according to size of screen
        self.squareHeightSize = int(self.squareHeight()) #update height according to size of screen
        self.drawBoardSquares(painter) #draw game board
        self.drawPieces(painter) #draw game parts

    def mousePressEvent(self, event):
        try:
            self.mousePosToColRow(event)
        except Exception as e:
            print(f"Error occurred: {e}")


    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        pass  # Implement this method according to your logic

    def drawBoardSquares(self, painter):
        for row in range(0, int(self.boardHeight)):
            for col in range(0, int(self.boardWidth)):
                painter.save()
                x = col * self.squareWidthSize + 10
                y = row * self.squareHeightSize + 10
                self.squareEdges[row][col] = (x, y)
                if col == self.boardWidth - 1:
                    self.squareEdges[row][col + 1] = (x + self.squareWidthSize, y)
                painter.translate(x, y)
                painter.setBrush(QBrush(QColor(160, 82, 45)))  # Set brush color
                painter.drawRect(0, 0, self.squareWidthSize, self.squareHeightSize)  # Draw rectangles
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