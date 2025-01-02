import board
from player_data import Player_Info
from go import Go

class GameLogic:
    def __init__(self):
        super().__init__()
        self.go = Go(self)
        self.player_1 = Player_Info("", False)
        self.player_2 = Player_Info("", False)
        self.captured_stones = {1: 0, 2: 0}
        self.go.openMainMenu()

        #self.go.openMainMenu()
    def start_new_game(self, player_name_1, player_name_2):
        self.player_1 = Player_Info(player_name_1, True)
        self.player_2 = Player_Info(player_name_2, False)
        self.go.openGamePlay()

    def get_player_turn_id(self):
        if self.player_1.player_turn:
            return 1
        elif self.player_2.player_turn:
            return  2

    def change_turn(self):
        if self.player_1.player_turn:
            self.player_1.player_turn = False
            self.player_2.player_turn = True
        else:
            self.player_1.player_turn = True
            self.player_2.player_turn = False

    def set_default_player_turn(self):
        self.player_1.player_turn = True
        self.player_2.player_turn = False

    def can_make_move(self, board, x, y):
        #if already occupied
        if board[x][y] != 0:
            return False

        board[x][y] = self.get_player_turn_id()
        self.check_if_capture_opponent(board, x, y)
        #if self.ko_check(board, x, y):
            #board[x][y] = 0
            #return False

        return True

    def check_if_capture_opponent(self, board, x, y):
        height = len(board) - 1
        width = len(board[0]) - 1

        #define opponent id
        opponent_id = 1
        if self.get_player_turn_id() == 1:
            opponent_id = 2

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width:
                if board[nx][ny] == opponent_id:
                    # If the opponent's stone is found, check if it's captured
                    self.capture_group(board, nx, ny, opponent_id)

    def capture_group(self, board, x, y, opponent_id):
        height = len(board) - 1
        width = len(board[0]) - 1
        captured = set()
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) not in captured:
                captured.add((cx, cy))
                # Directions to check: up, down, left, right
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < height and 0 <= ny < width:
                        if board[nx][ny] == opponent_id and (nx, ny) not in captured:
                            stack.append((nx, ny))

        # Now we have a complete group of captured stones
        # Check if the group has liberties (empty spots adjacent to the group)
        has_liberties = False
        for cx, cy in captured:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < height and 0 <= ny < width:
                    if board[nx][ny] == 0:
                        has_liberties = True
                        break
            if has_liberties:
                break

        # If no liberties, capture the group
        if not has_liberties:
            for cx, cy in captured:
                board[cx][cy] = 0  # Remove the captured stone
            self.captured_stones[self.get_player_turn_id()] += len(captured)
            black, white = self.calculate_nuber_of_stones(board)
            print("Black:", black)
            print("White:", white)

    def calculate_nuber_of_stones(self, board):
        # Count the number of black and white stones on the board
        black_score = sum(row.count(1) for row in board) + self.captured_stones[1]
        white_score = sum(row.count(2) for row in board) + self.captured_stones[2]
        return black_score, white_score

