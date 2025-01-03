from numpy.ma.extras import row_stack

import board
from player_data import Player_Info
from go import Go

class GameLogic:
    def __init__(self):
        super().__init__()
        self.go = Go(self)
        self.player_1 = Player_Info(1, "", False)
        self.player_2 = Player_Info(2,"", False)
        self.captured_stones = {1: 0, 2: 0}
        self.pass_count = 0
        self.prev_board = None
        self.komi_score = 6.5
        self.go.openMainMenu()

    #Method to initialize players for a new game
    def start_new_game(self, player_name_1, player_name_2):
        self.player_1 = Player_Info(1, player_name_1, True)
        self.player_2 = Player_Info(2, player_name_2, False)
        self.go.openGamePlay() #open game play

    #Get ID of active player
    def get_player_turn_id(self):
        if self.player_1.player_turn:
            return 1
        elif self.player_2.player_turn:
            return  2

    #Get active player
    def get_player_turn_data(self):
        if self.player_1.player_turn:
            return  self.player_1
        else:
            return self.player_2

    #Method to change player turns
    def change_turn(self):
        if self.player_1.player_turn:
            self.player_1.player_turn = False
            self.player_2.player_turn = True
        else:
            self.player_1.player_turn = True
            self.player_2.player_turn = False
        self.go.scoreBoard.update_turn_label() #call update of a scoreboard

    #Reset to default player turn and reset to default values
    def set_default_player_turn(self):
        # Set the initial turn to Player 1
        self.player_1.player_turn = True
        self.player_2.player_turn = False
        # Initialize the previous board state to None
        self.prev_board = None
        # Initialize captured stones count for both players
        self.captured_stones = {1: 0, 2: 0}
        self.pass_count = 0

        # Check if the scoreboard exists and update its labels and scores
        if self.go.scoreBoard is not None:
            self.go.scoreBoard.update_turn_label()  # Update the UI to show the current player's turn
            self.go.scoreBoard.update_score(0, 0) # Reset and display the scores as 0 for both players

    #Method to check if the game is over
    def check_game_over(self, board, restart_game_event, main_menu_event):
        #Check if number of pass are >= 2 in a row
        if self.pass_count >= 2:
            # Calculate scores for black and white players
            black_score, white_score = self.calculate_nuber_of_stones(board)

            # Add komi (handicap score) to white's score
            white_score += self.komi_score
            self.go.get_board().timer.stop()
            # Open the win screen with player names, scores, and event callbacks
            self.go.open_win_screen(self.player_1.getPlayerName(), self.player_2.getPlayerName(), black_score, white_score, restart_game_event, main_menu_event)
            return True # Game is over

        # Iterate through the board to check if there are valid moves remaining
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == 0:
                    # Simulate moves for both black and white players to check if a move is valid
                    if self.check_move_simulation(board, x, y, 1) or self.check_move_simulation(board, x, y, 2):
                        return  False #Can make move

        # If no valid moves are found, calculate final scores
        black_score, white_score = self.calculate_nuber_of_stones(board)
        white_score += self.komi_score
        # Open the win screen with player names, scores, and event callbacks
        self.go.open_win_screen(self.player_1.getPlayerName(), self.player_2.getPlayerName(), black_score, white_score, restart_game_event, main_menu_event)
        return True # Game is over

    #Method to simulate a move and check if it's valid
    def check_move_simulation(self, board, x, y, id):
        # Duplicate board, make vision of move
        temp_board = [row[:] for row in board]
        if temp_board[x][y] != 0:
            return False  # Move not possible

        temp_board[x][y] = id

        #Check can move or capture opponent
        return any(0 <= nx < len(board) and 0 <= ny < len(board[0]) and temp_board[nx][ny] == 0
            for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        )

    #Method to check if player can move
    def can_make_move(self, board, x, y):
        #If already occupied
        if board[x][y] != 0:
            return False
        if self.check_ko(board, x, y):
            return  False

        #Cache board for KO rules
        self.prev_board = [row[:] for row in board]

        #Mark board
        board[x][y] = self.get_player_turn_id()

        #Check if player collect opponents stones
        self.check_if_capture_opponent(board, x, y)

        #Reset pass counter
        self.pass_count = 0

        #Upade score
        black_score, white_score = self.calculate_nuber_of_stones(board)
        self.go.update_scoreboard(black_score, white_score)
        return True

    #Method to check for a Ko rule violation
    def check_ko(self, board, x, y):
        # Check if a previous board state exists for comparison
        if self.prev_board:
            temp = [row[:] for row in board]
            temp[x][y] = self.get_player_turn_id()

            if temp == self.prev_board:
                return True
        # If no Ko violation is detected or there is no previous board state
        return False

    #Method to check if placing a stone captures an opponent's group
    def check_if_capture_opponent(self, board, x, y):
        height = len(board) - 1
        width = len(board[0]) - 1

        #Define opponent id
        opponent_id = 1
        if self.get_player_turn_id() == 1:
            opponent_id = 2

        #Define the possible directions to check for adjacent stones
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width:
                if board[nx][ny] == opponent_id:
                    # If the opponent's stone is found, check if it's captured
                    self.capture_group(board, nx, ny, opponent_id)

    #Method to check if catch opponents stone
    def capture_group(self, board, x, y, opponent_id):
        # Get the dimensions of the board (height and width)
        height = len(board) - 1
        width = len(board[0]) - 1
        captured = set()
        stack = [(x, y)]
        #Perform DFS to find all stones of the opponent's group
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) not in captured:
                captured.add((cx, cy))
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                # Explore all 4 neighboring cells
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < height and 0 <= ny < width:
                        if board[nx][ny] == opponent_id and (nx, ny) not in captured:
                            stack.append((nx, ny))

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
                break # If one of the captured stones has liberties, we can stop checking

        # If no liberties, capture the group
        if not has_liberties:
            for cx, cy in captured:
                board[cx][cy] = 0  # Remove the captured stone
            self.captured_stones[self.get_player_turn_id()] += len(captured) #Increase score of catch stones

    #Method to Count the number of black and white stones on the board
    def calculate_nuber_of_stones(self, board):
        black_score = sum(row.count(1) for row in board) + self.captured_stones[1]
        white_score = sum(row.count(2) for row in board) + self.captured_stones[2]
        return black_score, white_score

    #Method to handle a player's pass turn
    def player_pass(self):
        self.pass_count += 1
        self.change_turn()
        self.check_game_over(self.go.get_board().boardArray, self.go.get_board().resetGame, self.go.get_board().pausePanelMainMenuEvent)