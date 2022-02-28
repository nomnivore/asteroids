import math
from pygame.math import Vector2


class Settings:
    def __init__(self):
        self.bg_color = (19, 19, 19)
        self.star_color = (150, 150, 150)
        self.star_size = 2
        self.star_density = 1
        self.screen_size = (1600, 900)
        self.fps = 60

        # self.ship_size = (57, 68)
        self.ship_size = (42, 50)
        self.ship_max_speed = 2.5
        self.ship_acceleration = 5 / 100
        self.ship_turn_speed = 2

        self.STAR_COUNT = math.floor((math.sqrt(
            self.screen_size[0] * self.screen_size[1]) / 10 / 1.5)
                                                      * self.star_density)

        self.VECTOR_UP = Vector2(0, -1)
