import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Module for handling players ship settings and funcionalities"""

    def __init__(self, ai_game):

        super().__init__()

        # Initialization of ship starting position

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Loading ship's image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Position of each new ship - Position in pygame is a tuple (X,Y), (0,0) point is located on the top left corner of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    # Method that displays ship image on the screen

    def blitme(self):
        self.screen.blit(self.image, self.rect)
