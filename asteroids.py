import random
import pygame as pg
import sys

from settings import Settings
from ship import Ship


class AsteroidsGame:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create resources"""

        pg.init()
        self.settings = Settings()

        self.screen = pg.display.set_mode(
            self.settings.screen_size)

        pg.display.set_caption("Asteroids")
        self.clock = pg.time.Clock()

        self.star_coords = []
        self._make_stars()

        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Respond to kwypresses and mouse events"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        self.ship.update()

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""

        # background color & pattern
        self.screen.fill(self.settings.bg_color)
        self._draw_stars()

        self.ship.draw()
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


if __name__ == "__main__":
    ast = AsteroidsGame()
    ast.run_game()
