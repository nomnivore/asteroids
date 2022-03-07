from __future__ import annotations
# for ide type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from asteroids import AsteroidsGame

import pygame as pg
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, game: AsteroidsGame):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # font settings
        self.text_color = (107, 208, 255)
        self.font = pg.font.SysFont(None, 48)

        # prepare the initial score images
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = int(round(self.stats.score, -1))

        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # display at top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = f"Level {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color)

        # position the level at the top center of the screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.screen_rect.centerx
        self.level_rect.top = self.score_rect.top

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for num in range(self.stats.ships_left):
            ship = Ship(self.game, False)
            ship.rect.x = 10 + num * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw info to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
