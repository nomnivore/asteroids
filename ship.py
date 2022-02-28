from __future__ import annotations
# for ide type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from asteroids import AsteroidsGame
import pygame as pg
from pygame.math import Vector2 as vec
from pygame.transform import rotozoom


class Ship(pg.sprite.Sprite):
    """A class to manage the ship."""

    def __init__(self, game: AsteroidsGame):
        """Initialize the ship and set its starting position."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        image = pg.image.load("media/ast-ship.png")
        self.image = pg.transform.scale(image, self.settings.ship_size)
        image_move = pg.image.load("media/ast-ship-moving.png")
        self.image_move = pg.transform.scale(
            image_move, self.settings.ship_size)
        self.original_image = self.image.copy()
        self.original_image_move = self.image_move.copy()

        self.rect = self.image.get_rect()

        self.rect.center = self.screen_rect.center
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.direction = vec(0, -1)
        self.angle = 0
        self.turn_speed = 0

        self.accelerating = False

    def update(self):
        """Move according to the ship's velocity, angle, and turn speed"""
        self.wrap_around_screen()
        keys = pg.key.get_pressed()
        # doing it this way lets acceleration build up while the key is held
        if keys[pg.K_LEFT]:
            self.turn_speed = -self.settings.ship_turn_speed
            self._rotate()
        if keys[pg.K_RIGHT]:
            self.turn_speed = self.settings.ship_turn_speed
            self._rotate()

        # accelerate if up is pressed, decelerate otherwise
        if keys[pg.K_UP]:
            self._move()
            self.accelerating = True
        else:
            # self.vel += self.accel.copy().reflect()
            self.accelerating = False

        # max speed
        if self.vel.length() > self.settings.ship_max_speed:
            self.vel.scale_to_length(self.settings.ship_max_speed)

        # friction
        # self.vel *= 0.999

        # update the ship's position vector and rect
        self.pos += self.vel
        self.rect.center = self.pos

    def _move(self):
        self.vel += self.direction * self.settings.ship_acceleration

    def _rotate(self):
        self.direction.rotate_ip(self.turn_speed)
        self.angle += self.turn_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    # refactor to new reusable method
    def wrap_around_screen(self):
        """Wrap around screen."""
        if self.pos.x > self.settings.screen_size[0]:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.settings.screen_size[0]
        if self.pos.y <= 0:
            self.pos.y = self.settings.screen_size[1]
        if self.pos.y > self.settings.screen_size[1]:
            self.pos.y = 0

    # is this the best way?
    def draw(self):
        """Draw the ship at its current location"""
        angle = self.direction.angle_to(self.settings.VECTOR_UP)
        self.image = rotozoom(self.original_image, angle, 1)
        self.image_move = rotozoom(self.original_image_move, angle, 1)
        blit_pos = self.pos - vec(self.image.get_size()) * 0.5
        if self.accelerating:
            self.screen.blit(self.image_move, blit_pos)
        else:
            self.screen.blit(self.image, blit_pos)
