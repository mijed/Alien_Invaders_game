from hashlib import new
import sys
from matplotlib.style import available
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Main class of the game
                             """

    def __init__(self):
        # initialization of the game

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invaders")

        self.stats = GameStats(self)
        # Scoreboard instance
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play!")

    # underscore before function or method points that this is auxiliary method
    def _check_events(self):
        # Method for event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

        # Checking all of the pressed keys
        keys_pressed = pygame.key.get_pressed()

        # Moving the ship (left and right), ad keys and arrows
        if keys_pressed[pygame.K_d]:
            if self.ship.rect.right < self.settings.screen_width:
                self.ship.rect.x += self.settings.ship_velocity
        if keys_pressed[pygame.K_a]:
            if self.ship.rect.left > 0:
                self.ship.rect.x -= self.settings.ship_velocity

        if keys_pressed[pygame.K_RIGHT]:
            if self.ship.rect.right < self.settings.screen_width:
                self.ship.rect.x += self.settings.ship_velocity
        if keys_pressed[pygame.K_LEFT]:
            if self.ship.rect.left > 0:
                self.ship.rect.x -= self.settings.ship_velocity

        # Pressing Q button exits the game
        if keys_pressed[pygame.K_q]:
            sys.exit()

    def _check_play_button(self, mouse_pos):

        # Collidepoint check if mouseclick point is inside button rectangle
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # If the button is pressed reset the game and set the game to active mode
            self.stats.reset_stats()
            self.stats.game_active = True
            # Proper display of score and level after reseting the game
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse cursor in active mode
            pygame.mouse.set_visible(False)

    def _create_fleet(self):
        # Creating alien fleet

        alien = Alien(self)
        # rect.size returns a tuple (width,height)
        alien_width, alien_height = alien.rect.size

        # Available space on x axis for alien ships
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # Number of aliens ships that fit on the screen
        number_aliens_x = available_space_x // (2*alien_width)

        # Avaiable space on y axis
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - \
            (3*alien_height) - ship_height

        number_rows = available_space_y // (2*alien_height)

        # Creating rows of alien ships
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Method for creating aliens
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 2*alien.rect.height + 2*alien_height*row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        # First check if alien ship is near the edge then update ships position
        self._check_fleet_edges()
        self.aliens.update()

        # Detect collisions between alien and ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        # Method for applying movement of the ships if they reach edge of the screen
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        # Reaction on collision between ship and alien

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Remove all the bullets and aliens
            self.aliens.empty()
            self.bullets.empty()

            # (Reset the game) create new fleet and place ship in the center of the screen
            self._create_fleet()
            self.ship.center_ship()

            # Short pause
            sleep(0.5)
        else:
            # If there's no ship left set game_active as False
            self.stats.game_active = False

            # Show mouse cursor in active mode
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        # If alien ship reaches bottom of the screen apply _ship_hit() method
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        # Moving every alien ship down by fleet_drop_speed parameter
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        # Changing direction of ships movement
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Setting background color
        self.screen.fill(self.settings.bg_color)

        # Drawing ship, aliens and bullets
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Displaying scoreboard
        self.sb.show_score()

        # If game is passive state draw button
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Displaying the latest modification of the screen
        pygame.display.update()

    # Method handling firing bullets

    def _fire_bullet(self):
        # Creating new bullet and adding them to group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):

        # Refreshing position of bullets
        self.bullets.update()

        # Removing bullets outside the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # Checking for collisions with alien ships
        # sprite.groupcollide method returns a dict with a key - bullets and values - alien ships that were hit by a bullet)
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_highest_score()

        # If there is no aliens on the screen, remove all bullets and create new fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

            # Increase difficulty after clearing aliens
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def run_game(self):
        """Main loop of the game"""
        clock = pygame.time.Clock()
        while True:
            # This control the speed of while loop, this makes sure that while loop runs 60 times per second
            clock.tick(self.settings.FPS)
            self._check_events()

            # If game is active
            if self.stats.game_active:
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
