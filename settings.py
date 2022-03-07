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
        self.max_ships = 3
        self.ship_size = (42, 50)
        self.ship_max_speed = 4
        self.ship_acceleration = 8.5 / 100
        self.ship_turn_speed = 3.5
        self.ship_fire_rate = 0.25  # in seconds
        self.ship_invuln_time = 5  # in seconds

        self.STAR_COUNT = math.floor((math.sqrt(
            self.screen_size[0] * self.screen_size[1]) / 10 / 1.5)
            * self.star_density)

        self.VECTOR_UP = Vector2(0, -1)

        self.bullet_color = (255, 255, 255)
        self.bullet_width = 4
        self.bullet_height = 4
        self.bullet_speed = 10
        self.bullet_lifetime = 60
        self.bullet_dmg = 20

        self.rock_speed_mult = 0.25
        self.rocks_per_level = 4
        self.rocks_size = [
            (150, 150),
            (100, 100),
            (50, 50)
        ]

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.rock_base_speed = 1.5
        self.rock_base_hp = 10
        self.rock_points = 100  # points / rock_size

    def increment_dynamic_settings(self):
        self.rock_base_speed += 0.25
        self.rock_base_hp += 3
        self.rock_points *= 1.1
