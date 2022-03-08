class Settings:
    """Class of game settings"""

    def __init__(self):
        # Init of the settings

        self.screen_width = 1200
        self.screen_height = 800
        self.FPS = 60

        # Number of ships available for player
        self.ships_limit = 3

        # Score scaling
        self.score_scale = 1.5

        # Background color
        self.bg_color = (230, 230, 230)

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 5

        # Movement of alien fleet in y direction
        self.fleet_drop_speed = 10

        # Changing difficulty of the game
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Method for dynamic settings"""

        # Alien movement settings
        self.alien_speed = 1

        # Points for shooting alien
        self.alien_points = 50

        # Ship settings
        self.ship_velocity = 5

        self.bullet_speed = 5

        self.fleet_direction = 1

    def increase_speed(self):
        """Increasing difficulty"""

        self.ship_velocity *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
