import math

from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush
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
    timerSpeed = 10  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from
    isStarted = False
    squareEdges = [[]]

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

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
        self.boardArray[row][col] = 1
        self.printBoardArray()

    def findClosestPoint(self, rowData, colData):
        min_distance = float('inf')
        nearest_row, nearest_col = -1, -1
        for row_index, row in enumerate(self.squareEdges):
            for col_index, point in enumerate(row):
                if not isinstance(point, (tuple, list)) or len(point) != 2:
                    raise ValueError(f"Invalid point format at row {row_index}, col {col_index}: {point}")
                x, y = point
                # Calculate Euclidean distance
                distance = ((x - rowData) ** 2 + (y - colData) ** 2) ** 0.5
                # Update if this point is closer
                if distance < min_distance:
                    min_distance = distance
                    nearest_row, nearest_col = row_index, col_index

        return nearest_row, nearest_col


    def squareWidth(self):
        #returns the width of one square in the board
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        #returns the height of one square of the board
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if Board.counter == 0:
            print("Game over")
        self.counter -= 1
        print('timerEvent()', self.counter)
        if self.counter < 0:
            self.counter = 10
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.squareEdges = [[0 for _ in range(self.boardWidth + 1)] for _ in range(self.boardHeight + 1)]

        self.squareWidthSize = int(self.squareWidth()) #update width according to size of screen
        self.squareHeightSize = int(self.squareHeight()) #update height according to size of screen
        self.drawBoardSquares(painter) #draw game board

        self.printBoardArray()

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
        for row in range(0, self.boardHeight):
            for col in range(0, self.boardWidth):
                painter.save()
                x = col * self.squareWidthSize
                y = row * self.squareHeightSize
                self.squareEdges[row][col] = (x, y)
                if col == self.boardWidth - 1:
                    self.squareEdges[row][col + 1] = (x + self.squareWidthSize, y)
                painter.translate(x, y)
                painter.setBrush(QBrush(QColor(160, 82, 45)))  # Set brush color
                painter.drawRect(0, 0, self.squareWidthSize, self.squareHeightSize)  # Draw rectangles
                painter.restore()
            if row == self.boardHeight - 1:
                for i in range(0, self.boardWidth):
                    x = i * self.squareWidthSize
                    y = row + 1 * self.squareHeightSize
                    self.squareEdges[row + 1][i] = (x, y)
                    if i == self.boardWidth - 1:
                        self.squareEdges[row + 1][i + 1] = (x + self.squareWidthSize, y)

    def printBoardPointArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardPointArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.squareEdges]))

    def drawPieces(self, painter):
        try :
            for row in range(0, len(self.boardArray)):
                for col in range(0, len(self.boardArray[0])):
                    painter.save()
                    x, y = self.squareEdges[row][col]
                    status = self.boardArray[row][col]
                    if status == 1:
                        painter.setBrush(QBrush(QColor(0, 0, 0)))
                        radius = self.squareWidthSize / 4
                        center = QPoint(int(x), int(y))
                        painter.drawEllipse(center, int(radius), int(radius))
                    painter.restore()
        except Exception as e:
            print(e)