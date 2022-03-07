class GameStats:
    """Track statistics for Asteroids."""

    def __init__(self, game):
        self.game = game
        self.reset_stats()

        # start in an inactive state
        self.game_active = False

    def reset_stats(self):
        self.score = 0
        self.level = 1
        self.ships_left = self.game.settings.max_ships
