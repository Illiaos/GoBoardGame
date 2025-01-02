from player_data import Player_Info
from go import Go

class GameLogic:
    def __init__(self):
        super().__init__()
        self.go = Go(self)
        self.player_1 = Player_Info("", False)
        self.player_2 = Player_Info("", False)
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

        # Update the scoreboard
        self.go.scoreBoard.update_turn_label()

    def set_default_player_turn(self):
        self.player_1.player_turn = True
        self.player_2.player_turn = False
    def start_new_game(self, player_name_1, player_name_2):
        self.player_1 = Player_Info(player_name_1, True)
        self.player_2 = Player_Info(player_name_2, False)
        self.set_default_player_turn()
        self.go.openGamePlay()
