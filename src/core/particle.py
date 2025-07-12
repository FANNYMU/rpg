
import arcade
import random

class WaterParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.change_x = random.uniform(-3, 3)
        self.change_y = random.uniform(1, 5)
        r, g, b = (0, 0, 255)
        self.size = random.randint(2, 6)
        r, g, b = (0, 0, 255)
        r += random.randint(-20, 20)
        g += random.randint(-20, 20)
        b += random.randint(0, 20)

        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        self.color = (r, g, b, 255)
        self.lifetime = 60
        self.alpha = 255

    def update(self):
        self.x += self.change_x
        self.y += self.change_y
        self.change_y -= 0.1
        self.lifetime -= 1
        if self.lifetime < 30:
            self.alpha = int(255 * (self.lifetime / 30))

    def draw(self):
        arcade.draw_circle_filled(
            self.x, 
            self.y, 
            self.size, 
            (self.color[0], self.color[1], self.color[2], self.alpha)
        )

    def is_alive(self):
        return self.lifetime > 0


