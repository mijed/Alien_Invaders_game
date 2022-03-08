import pygame.font


class Button():
    """Starting game button"""

    def __init__(self, ai_game, msg):

        self.screen = ai_game.screen
        self.rect_screen = self.screen.get_rect()

        # Defining button size
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Creating button and placing it on the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.rect_screen.center

        # Displaying message on a button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # Method for handling button message

        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):

        self.screen.fill(self.button_color, self.rect)

        self.screen.blit(self.msg_image, self.msg_image_rect)
