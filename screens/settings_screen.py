import pygame
from ui.button import Button
from ui.slider import Slider
from ui.colors import Colors

class SettingsScreen:
    def __init__(self, screen_width, screen_height, current_volume=50):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Back button
        BUTTON_WIDTH = 200
        BUTTON_HEIGHT = 50
        self.back_button = Button(
            (screen_width - BUTTON_WIDTH) // 2,
            screen_height - 100,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "BACK"
        )
        
        # Volume slider
        SLIDER_WIDTH = 400
        SLIDER_HEIGHT = 50
        slider_x = (screen_width - SLIDER_WIDTH) // 2
        slider_y = screen_height // 2
        self.volume_slider = Slider(
            slider_x, slider_y, SLIDER_WIDTH, SLIDER_HEIGHT,
            current_volume, min_value=0, max_value=100
        )
        
        # Font for labels
        try:
            self.font = pygame.font.Font("fonts/BoldPixels.ttf", 36)
        except:
            self.font = pygame.font.Font(None, 36)
    
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(mouse_pos):
                return "BACK"
            elif self.volume_slider.check_click(mouse_pos):
                pass  # Slider handles its own click
        elif event.type == pygame.MOUSEBUTTONUP:
            self.volume_slider.stop_drag()
        elif event.type == pygame.MOUSEMOTION:
            self.volume_slider.update_drag(mouse_pos)
        
        return None
    
    def update(self, mouse_pos):
        self.back_button.check_hover(mouse_pos)
    
    def draw(self, screen):
        # Draw title
        title_text = "SETTINGS"
        title_surface = self.font.render(title_text, True, Colors.TEXT_NEON)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_surface, title_rect)
        
        # Draw volume label
        volume_text = f"VOLUME: {self.volume_slider.value}%"
        volume_surface = self.font.render(volume_text, True, Colors.TEXT_NEON)
        volume_rect = volume_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
        screen.blit(volume_surface, volume_rect)
        
        # Draw slider
        self.volume_slider.draw(screen)
        
        # Draw back button
        self.back_button.draw(screen)
    
    def get_volume(self):
        """Get current volume as 0.0-1.0"""
        return self.volume_slider.value / 100.0