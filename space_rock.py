from __future__ import annotations
# for ide type hinting
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from asteroids import AsteroidsGame

from ast_object import AstObject
import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
import random


class SpaceRock(Sprite, AstObject):
    """A class to manage the space rocks."""

    def __init__(self, game: AsteroidsGame, rock_pos: Tuple[int, int] = None,
                 rock_size=1, parent: SpaceRock = None, rotate=0):
        """Create a new space rock with a given size

        Parameters
        ----------
        game : AsteroidsGame
            The game instance
        rock_size : int
            1 = largest, 3 = smallest
        """
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.size = rock_size

        image = pg.image.load(f"media/ast-rock-{self.size}.png")
        self.image = pg.transform.scale(image,
                                        self.settings.rocks_size[self.size-1])

        self.rect = self.image.get_rect()

        # # fixed position (for testing)
        # self.rect.centerx = self.screen_rect.centerx / 2
        # self.rect.centery = self.screen_rect.centery / 2

        if rock_pos:
            self.rect.centerx = rock_pos[0]
            self.rect.centery = rock_pos[1]
        self.pos = vec(self.rect.center)

        # set random direction
        self.direction = vec(0, 0)
        self.direction.x = random.random()
        self.direction.y = random.random()
        # self.direction.normalize()

        # inherit certain values from the parent (if applicable)
        if parent:
            self.pos = parent.pos.copy()
            self.direction = parent.direction.copy()
            self.direction.rotate_ip(rotate)

        # set speed
        self.vel = (self.settings.rock_base_speed +
                    (random.uniform(0, self.settings.rock_speed_mult) *
                     self.size))

        # set hp
        self.hp = self.settings.rock_base_hp + (
            (4 - self.size) * self.settings.rock_base_hp)

        # make rock ignore collisions with itself for a few ticks
        self.ignore_collide()

    def update(self):
        self.wrap_around_screen()

        self.pos += (self.direction * self.vel)
        self.rect.center = self.pos

        if self.hp <= 0:
            # split rock into multiple smaller rocks
            self.game.stats.score += self.settings.rock_points / self.size
            self.game.sb.prep_score()
            self._split()
            self.kill()
            self.game.check_rocks_left()

        if self.ignore_collisions:
            if pg.time.get_ticks() - self.ignore_start_time > 5:
                self.ignore_collisions = False
                print("reflection allowed")

    def ignore_collide(self):
        self.ignore_collisions = True
        self.ignore_start_time = pg.time.get_ticks()

    def _split(self):
        # ! STUB !
        if self.size < 3:
            rock1 = SpaceRock(self.game, None, self.size+1,
                              self, random.randint(15, 90))
            rock2 = SpaceRock(self.game, None, self.size+1,
                              self, -random.randint(15, 90))

            # position rocks based on direction of self
            rock1.pos += (rock1.direction *
                          (self.settings.rocks_size[self.size-1][0] / 2.5))
            rock2.pos -= (rock1.direction *
                          (self.settings.rocks_size[self.size-1][0] / 2.5))

            rock1.rect.center = rock1.pos
            rock2.rect.center = rock2.pos

            self.game.rocks.add(rock1)
            self.game.rocks.add(rock2)

    def draw(self):
        self.screen.blit(self.image, self.rect)
