class GameStats:
    def __init__(self,ai_game):
        self.setting = ai_game.setting
        self.reset_stats()
        self.game_active = False
        self.score = 0
        self.high_score = 0
    def reset_stats(self):
        self.score = 0
        self.ships = self.setting.ship_limit
