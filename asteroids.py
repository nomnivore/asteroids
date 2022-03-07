import random
import pygame as pg
import sys

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from space_rock import SpaceRock
from button import Button


class AsteroidsGame:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create resources"""

        pg.init()
        self.settings = Settings()
        self.stats = GameStats(self)

        self.screen = pg.display.set_mode(
            self.settings.screen_size)

        self.sb = Scoreboard(self)

        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Asteroids")
        self.clock = pg.time.Clock()

        self.play_button = Button(self, "Play")

        self.star_coords = []
        self._make_stars()

        self.ship = Ship(self)

        self.bullets = pg.sprite.Group()
        self.rocks = pg.sprite.Group()

        # self._prepare_game(reset=True)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.rocks.update()
                self._check_collisions()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start game when player clicks Play"""
        clicked = self.play_button.rect.collidepoint(mouse_pos)
        if clicked and not self.stats.game_active:
            self._prepare_game(reset=True)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pg.K_q:
            pg.quit()
            sys.exit()
        elif event.key == pg.K_SPACE:
            self.ship.fire()

    def _check_collisions(self):
        self._check_bullet_collisions()
        self._check_rock_collisions()

    def _check_bullet_collisions(self):
        # check for bullets that hit the ship
        # bullet = pg.sprite.spritecollideany(self.ship, self.bullets)
        # if bullet:
        #     self._ship_hit()
        # * Actually, the ship's bullets should never be able to hit the ship.
        # * Skipping detection for now.

        rock_hits = pg.sprite.groupcollide(
            self.bullets, self.rocks, True, False)
        if rock_hits:
            for rocks in rock_hits.values():
                for rock in rocks:
                    print(f"Rock hit! (HP: {rock.hp})")
                    rock.hp -= self.settings.bullet_dmg

    def check_rocks_left(self):
        """Check to see if any rocks are left in the current level"""
        if len(self.rocks) == 0:
            self._prepare_game()  # iterates to next level
            pg.time.delay(500)
        print(len(self.rocks))

    def _check_rock_collisions(self):
        # check for rocks that hit the ship
        rock = pg.sprite.spritecollideany(self.ship, self.rocks)
        if rock and not self.ship.invuln:
            self._ship_hit()
            rock.hp -= self.settings.bullet_dmg * 4
            # basically, destroy the rock that hit the ship

        # check for rocks hitting each other
        # rock_hits = pg.sprite.groupcollide(
        #     self.rocks, self.rocks, False, False, self._collide_if_not_self)
        # if rock_hits:
        #     for left_rock, hits in rock_hits.items():
        #         for rock in hits:
        #             if not rock.ignore_collisions:
        #                 rock.direction.reflect_ip(left_rock.pos - rock.pos)
        #                 print("reflected")
        #                 rock.ignore_collide()

    def _collide_if_not_self(self, left, right):
        if left != right:
            return pg.sprite.collide_rect(left, right)
        return False

    def _ship_hit(self):
        """Respond to the ship being hit"""
        self.stats.ships_left -= 1
        self.sb.prep_ships()
        if self.stats.ships_left >= 1:
            # move ship back to center of screen
            self.ship.center_ship()
        else:
            # game over!
            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""

        # background color & pattern
        self.screen.fill(self.settings.bg_color)
        self._draw_stars()

        if self.stats.game_active:
            self.ship.draw()
            self.bullets.draw(self.screen)
            self.rocks.draw(self.screen)
        else:
            self.play_button.draw_button()

        self.sb.show_score()
        # make the most recently drawn screen visible
        pg.display.flip()

    def _make_stars(self):
        print(f"Star count: {self.settings.STAR_COUNT}")
        for _i in range(1, self.settings.STAR_COUNT):
            coord = (random.randint(0, self.settings.screen_size[0]),
                     random.randint(0, self.settings.screen_size[1]))
            self.star_coords.append(coord)

    def _draw_stars(self):
        for coord in self.star_coords:
            pg.draw.circle(self.screen, self.settings.star_color,
                           coord, self.settings.star_size, 0)  # 0 is filled

    def _spawn_rocks_fixed(self):

        rocks_pos = [
            (self.screen_rect.centerx / 2, self.screen_rect.centery / 2),
            (self.screen_rect.centerx * 2, self.screen_rect.centery * 2),
            (self.screen_rect.centerx / 2, self.screen_rect.centery * 2),
            (self.screen_rect.centerx * 2, self.screen_rect.centery / 2)
        ]
        for pos in rocks_pos:
            new_rock = SpaceRock(self, pos)
            self.rocks.add(new_rock)

    def _spawn_rocks_random(self):
        for _ in range(self.settings.rocks_per_level):
            pos = (
                random.randint(0, self.settings.screen_size[0]),
                random.randint(0, self.settings.screen_size[1])
            )
            new_rock = SpaceRock(self, pos)
            self.rocks.add(new_rock)

    def _prepare_game(self, reset=False):
        """Prepare the game"""
        if reset:
            self.stats.game_active = True
            self.stats.reset_stats()
            self.settings.initialize_dynamic_settings()
            self.bullets.empty()
            self.rocks.empty()
            pg.mouse.set_visible(False)
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
        else:
            self.settings.increment_dynamic_settings()
            self.stats.level += 1
            self.sb.prep_level()

        self._spawn_rocks_random()
        self.ship.center_ship()


if __name__ == "__main__":
    ast = AsteroidsGame()
    ast.run_game()
