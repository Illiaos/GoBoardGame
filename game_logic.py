from player_data import Player_Info
from go import Go

class GameLogic:
    def __init__(self):
        super().__init__()
        self.go = Go(self)
        self.player_1 = Player_Info()
        self.player_2 = Player_Info()
        self.go.openMainMenu()

        #self.go.openMainMenu()
    def start_new_game(self, player_name_1, player_name_2):
        self.player_1 = Player_Info(player_name_1)
        self.player_2 = Player_Info(player_name_2)
        self.go.openGamePlay()
