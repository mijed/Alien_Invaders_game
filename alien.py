import pygame
from settings import Settings
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class for handling aliens"""

    def __init__(self, ai_game):

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Loading alien ship image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Placing alien ship on the top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # X coordinate as float number
        self.x = float(self.rect.x)

    def check_edges(self):
        # Return true if alien ship reaches the edge

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):

        # Moving aliens to the right
        self.x += (self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x = self.x
