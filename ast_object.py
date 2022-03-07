class AstObject:
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
