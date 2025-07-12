import arcade
import time

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 80
        self.chopping = False
        self.chop_progress = 0.0
        self.chop_duration = 3.0
        self.last_update_time = None
        self.regrow_time = 5.0
        self.chopped = False
        self.regrow_start_time = None

        self.default_cursor = None
        self.axe_cursor = None

    def draw(self):
        if self.chopped:
            left = self.x - self.width / 2
            right = self.x + self.width / 2
            bottom = self.y - self.height / 4 - self.height / 4
            top = self.y - self.height / 4 + self.height / 4
            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_BROWN)
        else:
            left = self.x - (self.width / 3) / 2
            right = self.x + (self.width / 3) / 2
            bottom = self.y - self.height / 2
            top = self.y + self.height / 2
            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_BROWN)
            arcade.draw_circle_filled(self.x, self.y + self.height / 2, self.width, arcade.color.DARK_GREEN)
            arcade.draw_circle_filled(self.x - self.width / 2, self.y + self.height / 3, self.width / 2, arcade.color.DARK_GREEN)
            arcade.draw_circle_filled(self.x + self.width / 2, self.y + self.height / 3, self.width / 2, arcade.color.DARK_GREEN)

        if self.chopping:
            bar_width = self.width
            bar_height = 10
            bar_x = self.x
            bar_y = self.y + self.height / 2 + 20

            left = bar_x - bar_width / 2
            right = bar_x + bar_width / 2
            bottom = bar_y - bar_height / 2
            top = bar_y + bar_height / 2
            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.GRAY)
            progress_width = bar_width * (self.chop_progress / self.chop_duration)
            left = bar_x - bar_width / 2
            right = left + progress_width
            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.GREEN)

    def update(self, delta_time):
        if self.chopping:
            if self.last_update_time is None:
                self.last_update_time = time.time()
            else:
                now = time.time()
                elapsed = now - self.last_update_time
                self.last_update_time = now
                self.chop_progress += elapsed
                if self.chop_progress >= self.chop_duration:
                    self.chopping = False
                    self.chopped = True
                    self.chop_progress = 0.0
                    self.regrow_start_time = time.time()

        if self.chopped and self.regrow_start_time is not None:
            if time.time() - self.regrow_start_time >= self.regrow_time:
                self.chopped = False
                self.regrow_start_time = None

    def check_hover(self, x, y):
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        bottom = self.y - self.height / 2
        top = self.y + self.height / 2
        return left <= x <= right and bottom <= y <= top

    def start_chopping(self):
        if not self.chopped and not self.chopping:
            self.chopping = True
            self.chop_progress = 0.0
            self.last_update_time = time.time()

    def stop_chopping(self):
        self.chopping = False
        self.chop_progress = 0.0
        self.last_update_time = None

