import arcade
import math
from core.player_stats import PlayerStats

class UIManager:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.player_stats = PlayerStats()
        self.animation_time = 0
        
    def update(self, delta_time):
        """Update animations - call this in your game loop"""
        self.animation_time += delta_time
        
    def resize(self, width, height):
        """Call this when window is resized"""
        self.window_width = width
        self.window_height = height
        
    def draw_ornate_frame(self, x, y, width, height, primary_color, secondary_color):
        """Draw an ornate RPG-style frame"""
        for i in range(5):
            alpha = 200 - (i * 30)
            arcade.draw_lrbt_rectangle_filled(
                x - width/2 + i, x + width/2 - i, 
                y - height/2 + i, y + height/2 - i,
                (*primary_color[:3], alpha)
            )
        
        arcade.draw_lrbt_rectangle_outline(
            x - width/2, x + width/2, 
            y - height/2, y + height/2,
            secondary_color, 3
        )
        
        corner_size = 8
        corners = [
            (x - width/2, y - height/2),  # bottom-left
            (x + width/2, y - height/2),  # bottom-right
            (x - width/2, y + height/2),  # top-left
            (x + width/2, y + height/2)   # top-right
        ]
        
        for corner_x, corner_y in corners:
            arcade.draw_circle_filled(corner_x, corner_y, corner_size, secondary_color)
            arcade.draw_circle_filled(corner_x, corner_y, corner_size - 2, primary_color)
    
    def draw_wood_counter(self):
        """Enhanced wood counter with better positioning"""
        padding = 20
        icon_size = 40
        frame_width = 120
        frame_height = 60
        
        x = padding + frame_width/2
        y = self.window_height - padding - frame_height/2
        
        self.draw_ornate_frame(x, y, frame_width, frame_height, 
                             (101, 67, 33), arcade.color.GOLD)
        
        icon_x = x - 30
        icon_y = y
        
        arcade.draw_ellipse_filled(icon_x, icon_y - 5, 25, 15, arcade.color.DARK_BROWN)
        arcade.draw_ellipse_filled(icon_x, icon_y, 22, 12, arcade.color.BROWN)
        
        for i in range(3):
            ring_color = [arcade.color.DARK_BROWN, arcade.color.BROWN, arcade.color.LIGHT_BROWN][i]
            arcade.draw_ellipse_outline(icon_x, icon_y, 18 - i*4, 8 - i*2, ring_color, 2)
        
        glow_alpha = max(50, min(255, int(50 + 30 * math.sin(self.animation_time * 2))))
        arcade.draw_circle_filled(icon_x, icon_y, 20, (*arcade.color.GOLD[:3], glow_alpha))
        
        text_x = x + 25
        text_y = y - 8
        
        arcade.draw_text(f"{self.player_stats.wood_count}", text_x + 2, text_y - 2, 
                        (0, 0, 0, 150), 20, font_name="Arial", bold=True)
        arcade.draw_text(f"{self.player_stats.wood_count}", text_x, text_y, 
                        arcade.color.WHITE, 20, font_name="Arial", bold=True)
        
    def draw_status_bar(self, x, y, width, height, current, maximum, colors, label, show_segments=True):
        """Generic status bar with enhanced visuals"""
        self.draw_ornate_frame(x, y, width + 20, height + 20, 
                             (20, 20, 20), arcade.color.GOLD)
        
        arcade.draw_lrbt_rectangle_filled(
            x - width/2, x + width/2, 
            y - height/2, y + height/2, 
            arcade.color.DARK_GRAY
        )
        
        percentage = current / maximum if maximum > 0 else 0
        fill_width = width * percentage
        
        if percentage > 0.6:
            bar_color = colors[0]
        elif percentage > 0.3:
            bar_color = colors[1]
        else:
            bar_color = colors[2]
        
        if fill_width > 0:
            segments = int(fill_width / 5) + 1
            for i in range(segments):
                segment_x = x - width/2 + i * 5
                segment_width = min(5, fill_width - i * 5)
                if segment_width > 0:
                    alpha = max(128, min(255, int(255 * (0.7 + 0.3 * (i % 2)))))
                    arcade.draw_lrbt_rectangle_filled(
                        segment_x, segment_x + segment_width,
                        y - height/2, y + height/2,
                        (*bar_color[:3], alpha)
                    )
        
        shine_pos = (self.animation_time * 100) % (width + 50) - 25
        if 0 <= shine_pos <= width:
            arcade.draw_line(
                x - width/2 + shine_pos, y - height/2,
                x - width/2 + shine_pos, y + height/2,
                (255, 255, 255, 100), 3
            )
        
        if show_segments:
            segment_count = 5 if label == "HP" else 3
            for i in range(1, segment_count):
                segment_x = x - width/2 + (width / segment_count) * i
                arcade.draw_line(
                    segment_x, y - height/2, 
                    segment_x, y + height/2,
                    (0, 0, 0, 150), 2
                )
        
        label_x = x - width/2 - 40
        label_y = y - 8
        
        arcade.draw_text(label, label_x + 1, label_y - 1, 
                        (0, 0, 0, 200), 16, font_name="Arial", bold=True)
        arcade.draw_text(label, label_x, label_y, 
                        bar_color, 16, font_name="Arial", bold=True)
        
        value_text = f"{int(current)}/{maximum}"
        arcade.draw_text(value_text, x + 1, y - 4, 
                        (0, 0, 0, 200), 12, font_name="Arial", bold=True,
                        anchor_x="center", anchor_y="center")
        arcade.draw_text(value_text, x, y - 3, 
                        arcade.color.WHITE, 12, font_name="Arial", bold=True,
                        anchor_x="center", anchor_y="center")
        
    def draw_health_bar(self):
        """Enhanced health bar with responsive positioning"""
        padding = 20
        bar_width = min(180, self.window_width * 0.15)
        bar_height = 25
        
        x = self.window_width - padding - bar_width/2 - 10
        y = self.window_height - padding - 35
        
        colors = [arcade.color.LIME_GREEN, arcade.color.YELLOW, arcade.color.RED]
        self.draw_status_bar(x, y, bar_width, bar_height, 
                           self.player_stats.health, self.player_stats.max_health, 
                           colors, "HP")
        
    def draw_armor_bar(self):
        """Enhanced armor bar with responsive positioning"""
        padding = 20
        bar_width = min(180, self.window_width * 0.15)
        bar_height = 22
        
        x = self.window_width - padding - bar_width/2 - 10
        y = self.window_height - padding - 80
        
        colors = [arcade.color.STEEL_BLUE, arcade.color.CYAN, arcade.color.LIGHT_BLUE]
        self.draw_status_bar(x, y, bar_width, bar_height, 
                           self.player_stats.armor, self.player_stats.max_armor, 
                           colors, "AR", show_segments=False)
    
    def draw_ui_background(self):
        """Enhanced background with better visual effects"""
        top_panel_height = min(120, self.window_height * 0.15)
        
        gradient_steps = 30
        for i in range(gradient_steps):
            alpha = max(0, int(140 - (i * 4)))
            y_offset = i * (top_panel_height / gradient_steps)
            step_height = top_panel_height / gradient_steps
            
            color_variation = max(0, int(10 + 10 * math.sin(i * 0.3)))
            arcade.draw_lrbt_rectangle_filled(
                0, self.window_width, 
                self.window_height - y_offset - step_height, 
                self.window_height - y_offset, 
                (color_variation, color_variation, color_variation, alpha)
            )
        
        border_y = self.window_height - top_panel_height
        
        arcade.draw_line(0, border_y, self.window_width, border_y, 
                        arcade.color.GOLD, 4)
        
        pattern_spacing = 60
        for i in range(0, self.window_width, pattern_spacing):
            size = 6
            arcade.draw_polygon_filled([
                (i, border_y - size),
                (i + size, border_y),
                (i, border_y + size),
                (i - size, border_y)
            ], arcade.color.GOLD)
            
            glow_alpha = max(50, min(255, int(100 + 50 * math.sin(self.animation_time * 3 + i * 0.1))))
            arcade.draw_circle_filled(i, border_y, size + 2, 
                                    (*arcade.color.GOLD[:3], glow_alpha))
        
        corner_size = 15
        corners = [
            (corner_size, self.window_height - corner_size),
            (self.window_width - corner_size, self.window_height - corner_size)
        ]
        
        for corner_x, corner_y in corners:
            arcade.draw_circle_filled(corner_x, corner_y, corner_size, 
                                    (*arcade.color.GOLD[:3], 150))
            arcade.draw_circle_outline(corner_x, corner_y, corner_size, 
                                     arcade.color.GOLD, 3)
            
            arcade.draw_circle_filled(corner_x, corner_y, corner_size - 5, 
                                    (101, 67, 33, 180))
    
    def draw_minimap_frame(self):
        """Draw a frame for minimap (optional)"""
        if self.window_width > 800: 
            map_size = 120
            padding = 20
            
            x = padding + map_size/2
            y = padding + map_size/2
            
            self.draw_ornate_frame(x, y, map_size + 20, map_size + 20, 
                                 (20, 20, 40), arcade.color.GOLD)
            
            arcade.draw_lrbt_rectangle_filled(
                x - map_size/2, x + map_size/2,
                y - map_size/2, y + map_size/2,
                (40, 40, 60, 180)
            )
            
            arcade.draw_text("MAP", x, y + map_size/2 + 15, 
                           arcade.color.GOLD, 12, font_name="Arial", bold=True,
                           anchor_x="center")
    
    # def add_wood(self, amount):
    #     self.player_stats.add_wood(amount)
        
    # def take_damage(self, damage):
    #     self.player_stats.take_damage(damage)
        
    # def heal(self, amount):
    #     self.player_stats.heal(amount)
        
    # def repair_armor(self, amount):
    #     self.player_stats.repair_armor(amount)
        
    def draw(self):
        """Main draw method with responsive layout"""
        self.draw_ui_background()
        self.draw_wood_counter()
        self.draw_health_bar()
        self.draw_armor_bar()
        
        if self.window_width > 800:
            self.draw_minimap_frame()