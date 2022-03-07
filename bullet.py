from __future__ import annotations
# for ide type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from asteroids import AsteroidsGame

from ast_object import AstObject
import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
from pygame.transform import rotozoom


class Bullet(Sprite, AstObject):
    """A class to manage bullets fired by the ship"""

    def __init__(self, game: AsteroidsGame):
        """Create a bullet at the ship's current position"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # rotate the bullet to the same angle as the ship
        self.original_image = pg.Surface(
            (self.settings.bullet_width, self.settings.bullet_height))
        self.original_image.fill(self.color)

        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = game.ship.pos
        self.pos = vec(self.rect.center)
        self.direction = game.ship.direction
        self.vel = self.direction * self.settings.bullet_speed
        self.angle = game.ship.angle

        self.image = pg.transform.rotate(self.original_image, self.angle)

        self.distance_travelled = 0.0

    def update(self):
        self.wrap_around_screen()

        # self._move()

        self.pos += self.vel
        self.rect.center = self.pos

        # add to ship's total distance travelled
        self.distance_travelled += self.vel.length()
        self._check_expiration()

    def _check_expiration(self):
        if (self.distance_travelled >=
                self.settings.bullet_speed * self.settings.bullet_lifetime):
            self.kill()

    def draw(self):
        angle = self.direction.angle_to(self.settings.VECTOR_UP)
        self.image = rotozoom(self.original_image, angle, 1)
        blit_pos = self.pos - vec(self.image.get_size()) * 0.5
        self.screen.blit(self.image, blit_pos)
