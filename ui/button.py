import pygame
import math
from ui.colors import Colors

class Button: 
    def __init__(self, x, y, width, height, text, font_size = 32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        try:
            self.font = pygame.font.Font("fonts/BoldPixels.ttf", font_size)
        except:
            self.font = pygame.font.Font(None, font_size)

        self.base_color = Colors.BUTTON_DARK
        self.hover_color = Colors.BUTTON_HOVER
        self.glow_color = Colors.BUTTON_GLOW
        self.text_color = Colors.TEXT_NEON
        self.is_hovered = False
        self.glow_intensity = 0
        self.was_hovered = False  # Track previous hover state


    def draw(self, screen):

        button_surface = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)

        if self.is_hovered:
            self.glow_intensity = min(255, self.glow_intensity + 15)
        else:
            self.glow_intensity = max(0, self.glow_intensity - 10)


        if self.glow_intensity > 0:
            glow_alpha = int(self.glow_intensity * 0.3)
            glow_color = (*self.glow_color, glow_alpha)
            pygame.draw.rect(button_surface, glow_color, (0, 0, self.rect.width + 20, self.rect.height + 20), border_radius=8)


        # Draw button background with rounded corners (simulated with multiple rectangles)
        color = self.hover_color if self.is_hovered else self.base_color
        pygame.draw.rect(button_surface, color, (10, 10, self.rect.width, self.rect.height), border_radius=6)


        #Draw inner border
        border_color = Colors.NEON_CYAN if self.is_hovered else Colors.BUTTON_DARK
        pygame.draw.rect(button_surface, border_color, (10, 10, self.rect.width, self.rect.height), width = 2, border_radius = 6)

        #Blit button surface to screen
        screen.blit(button_surface, (self.rect.x - 10, self.rect.y - 10))

        # Draw text with shadow for depth
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Text shadow
        shadow_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(shadow_surface, (text_rect.x + 2, text_rect.y + 2))
        
        # Main text
        screen.blit(text_surface, text_rect)
    

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

