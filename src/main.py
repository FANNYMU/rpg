import arcade
import math
from core.particle_manager import ParticleManager
from core.tree import Tree

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"
PLAYER_SPEED = 300 
PARTICLE_COUNT = 30 


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.AMAZON
        self.mouse_sprite_list = arcade.SpriteList()

        # Inisialisasi particle manager
        self.particle_manager = ParticleManager()

        self.mouse_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            scale=0.5,
        )
        self.mouse_sprite.center_x = WINDOW_WIDTH / 2
        self.mouse_sprite.center_y = WINDOW_HEIGHT / 2
        self.target_position = None
        self.mouse_sprite_list.append(self.mouse_sprite)

        self.tree = Tree(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        self.is_chopping = False
        self.chop_target_position = None

    def reset(self):
        """Reset the game to the initial state."""
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        self.clear()

        self.tree.draw()

        self.mouse_sprite_list.draw()

        self.particle_manager.draw()

    def on_update(self, delta_time):
        self.particle_manager.update()

        self.tree.update(delta_time)

        if self.is_chopping and self.chop_target_position is not None:
            start_x = self.mouse_sprite.center_x
            start_y = self.mouse_sprite.center_y
            dest_x, dest_y = self.chop_target_position

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            distance = math.sqrt(x_diff**2 + y_diff**2)

            max_move_dist = PLAYER_SPEED * delta_time

            if distance <= max_move_dist:
                self.mouse_sprite.center_x = self.chop_target_position[0]
                self.mouse_sprite.center_y = self.chop_target_position[1]
                self.tree.start_chopping()
            else:
                self.mouse_sprite.center_x += math.cos(angle) * PLAYER_SPEED * delta_time
                self.mouse_sprite.center_y += math.sin(angle) * PLAYER_SPEED * delta_time
        else:
            if self.target_position:
                start_x = self.mouse_sprite.center_x
                start_y = self.mouse_sprite.center_y

                dest_x, dest_y = self.target_position

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                distance = math.sqrt(x_diff**2 + y_diff**2)

                max_move_dist = PLAYER_SPEED * delta_time

                if distance <= max_move_dist:
                    self.mouse_sprite.center_x = self.target_position[0]
                    self.mouse_sprite.center_y = self.target_position[1]
                    self.target_position = None
                else:
                    self.mouse_sprite.center_x += math.cos(angle) * PLAYER_SPEED * delta_time
                    self.mouse_sprite.center_y += math.sin(angle) * PLAYER_SPEED * delta_time

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.tree.check_hover(x, y):
            if not self.is_chopping:
                self.is_chopping = True
                self.chop_target_position = (self.tree.x, self.tree.y)
                self.target_position = None
            else:
                self.is_chopping = False
                self.chop_target_position = None
                self.tree.stop_chopping()
        else:
            if self.is_chopping:
                self.is_chopping = False
                self.chop_target_position = None
                self.tree.stop_chopping()
            self.target_position = (x, y)
            self.particle_manager.create_splash(x, y, PARTICLE_COUNT)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    game = GameView()

    window.show_view(game)

    arcade.run()


if __name__ == "__main__":
    main()
