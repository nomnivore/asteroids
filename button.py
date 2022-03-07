from __future__ import annotations
# for ide type hinting
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from asteroids import AsteroidsGame

import pygame as pg
from pygame.font import SysFont


class Button:
    def __init__(self, game: AsteroidsGame, text):
        """Init button attributes"""

        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # dimensions and properties of the button
        self.width = 250
        self.height = 50
        self.button_color = (107, 208, 255)
        self.text_color = (0, 0, 0)
        self.font = SysFont(None, 48)

        # build the rect
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_text(text)

    def _prep_text(self, text):
        self.text_image = self.font.render(
            text, True, self.text_color, self.button_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def draw_button(self):
        """Display the button"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)
