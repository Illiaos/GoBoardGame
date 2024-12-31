class Player_Info:

    def __init__(self, player_name, turn_state):
        self.player_name = player_name
        self.player_score = 0
        self.player_turn = turn_state

    def getPlayerName(self):
        return self.player_name

    def getPlayerScore(self):
        return self.player_score

    def getPlayerTurn(self):
        return self.player_turn

    def setPlayerTurn(self, state):
        self.player_turn = state