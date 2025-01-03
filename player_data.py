class Player_Info:
    #Class to represent player data
    def __init__(self, id, player_name, turn_state):
        self.player_id = id
        self.player_name = player_name
        self.player_turn = turn_state

    def getPlayerId(self):
        return self.player_id

    def getPlayerName(self):
        return self.player_name

    def getPlayerTurn(self):
        return self.player_turn

    def setPlayerTurn(self, state):
        self.player_turn = state