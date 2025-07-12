import arcade
import math
from core.particle_manager import ParticleManager
from core.tree import Tree
from core.ui_manager import UIManager
from core.player_stats import PlayerStats

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"
PLAYER_SPEED = 300 
PARTICLE_COUNT = 30 

# Camera settings
CAMERA_SPEED = 0.1 
CAMERA_DEADZONE = 50


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.AMAZON
        self.mouse_sprite_list = arcade.SpriteList()

        self.particle_manager = ParticleManager()
        self.ui_manager = UIManager(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.player_stats = PlayerStats()

        # Create camera
        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()
        
        self.camera_target_x = WINDOW_WIDTH / 2
        self.camera_target_y = WINDOW_HEIGHT / 2

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

    def center_camera_on_player(self):
        """Center the camera on the player with smooth movement"""
        viewport_width = self.window.width
        viewport_height = self.window.height

        target_x = self.mouse_sprite.center_x - viewport_width / 2
        target_y = self.mouse_sprite.center_y - viewport_height / 2

        current_x, current_y = self.camera.position

        new_x = current_x + (target_x - current_x) * CAMERA_SPEED
        new_y = current_y + (target_y - current_y) * CAMERA_SPEED

        self.camera.position = (new_x, new_y)

    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        camera_x, camera_y = self.camera.position
        screen_x = world_x - camera_x
        screen_y = world_y - camera_y
        return screen_x, screen_y

    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        camera_x, camera_y = self.camera.position
        world_x = screen_x + camera_x
        world_y = screen_y + camera_y
        return world_x, world_y

    def reset(self):
        """Reset game state"""
        self.mouse_sprite.center_x = WINDOW_WIDTH / 2
        self.mouse_sprite.center_y = WINDOW_HEIGHT / 2
        self.target_position = None
        self.is_chopping = False
        self.chop_target_position = None
        self.camera.position = (0, 0)

    def on_draw(self):
        self.clear()

        self.camera.use()
        
        self.tree.draw()
        self.mouse_sprite_list.draw()
        self.particle_manager.draw()
        
        self.ui_camera.use()
        
        self.ui_manager.draw()

    def on_update(self, delta_time):
        self.ui_manager.update(delta_time)
        
        self.particle_manager.update()

        tree_chopped = self.tree.update(delta_time)
        if tree_chopped:
            self.player_stats.add_wood(3)

        self._handle_player_movement(delta_time)

        self.center_camera_on_player()

    def _handle_player_movement(self, delta_time):
        """Handle player movement logic"""
        if self.is_chopping and self.chop_target_position is not None:
            if self._move_to_target(self.chop_target_position, delta_time):
                self.tree.start_chopping()
        elif self.target_position:
            if self._move_to_target(self.target_position, delta_time):
                self.target_position = None

    def _move_to_target(self, target_position, delta_time):
        """Move player towards target position. Returns True if reached."""
        start_x = self.mouse_sprite.center_x
        start_y = self.mouse_sprite.center_y
        dest_x, dest_y = target_position

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        distance = math.sqrt(x_diff**2 + y_diff**2)

        max_move_dist = PLAYER_SPEED * delta_time
        if distance <= max_move_dist:
            self.mouse_sprite.center_x = dest_x
            self.mouse_sprite.center_y = dest_y
            return True
        else:
            angle = math.atan2(y_diff, x_diff)
            self.mouse_sprite.center_x += math.cos(angle) * PLAYER_SPEED * delta_time
            self.mouse_sprite.center_y += math.sin(angle) * PLAYER_SPEED * delta_time
            return False

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.H:
            self.player_stats.heal(10)
        elif key == arcade.key.D:
            self.player_stats.take_damage(15)
        elif key == arcade.key.R:
            self.player_stats.repair_armor(5)
        elif key == arcade.key.C:
            self.camera.position = (
                self.mouse_sprite.center_x - self.window.width / 2,
                self.mouse_sprite.center_y - self.window.height / 2
            )
        elif key == arcade.key.ESCAPE:
            self.is_chopping = False
            self.chop_target_position = None
            self.target_position = None
            self.tree.stop_chopping()

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Only handle left mouse button
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        world_x, world_y = self.screen_to_world(x, y)
        
        if self.tree.check_hover(world_x, world_y):
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
            
            self.target_position = (world_x, world_y)
            self.particle_manager.create_splash(world_x, world_y, PARTICLE_COUNT)

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass

    def on_resize(self, width, height):
        """Handle window resize"""
        self.ui_manager.resize(width, height)


def main():
    # FIXME: Camera Position not centering correctly on player sprite
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

    game = GameView()
    window.show_view(game)

    arcade.run()


if __name__ == "__main__":
    main()