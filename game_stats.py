# Module for game statistics


class GameStats:
    """Class for game statistics"""

    def __init__(self, ai_game):

        self.settings = ai_game.settings
        self.reset_stats()

        # If True run the game in active mode
        self.game_active = False

        # Saving highest score
        self.highest_score = 0

    # Reset the game

    def reset_stats(self):

        self.ships_left = self.settings.ships_limit

        # Starting score
        self.score = 0
        # Difficulty level of the game
        self.level = 1
