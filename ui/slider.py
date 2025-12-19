import pygame
from ui.colors import Colors

class Slider:
    def __init__(self, x, y, width, height, value, min_value = 0, max_value = 100):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.is_dragging = False

        # Slider track properties
        self.track_height = 8
        self.handle_radius = 12


    def get_handle_x(self):
        """calculate handle position based on current value"""
        percentage = (self.value - self.min_value) / (self.max_value - self.min_value)
        return self.rect.x + int(percentage * self.rect.width)

    def set_value_from_x(self, x):
        """Calculate handle position from mouse x position"""
        relative_x = max(0, min(self.rect.width, x - self.rect.x))
        percentage = relative_x / self.rect.width
        self.value = int(self.min_value + percentage * (self.max_value - self.min_value))
        return self.value

    def check_click(self, mouse_pos):
        """Check if the slider handle is clicked and start dragging"""
        handle_x = self.get_handle_x()
        handle_rect = pygame.Rect(handle_x - self.handle_radius, self.rect.centery - self.handle_radius, self.handle_radius * 2, self.handle_radius * 2)

        if handle_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos):
            self.is_dragging = True
            self.set_value_from_x(mouse_pos[0])
            return True
        return False

    def update_drag(self, mouse_pos):
        """Update the slider value while dragging"""
        if self.is_dragging:
            self.set_value_from_x(mouse_pos[0])

    def stop_drag(self):
        """Stop dragging and clamp the value to the valid range"""
        self.is_dragging = False

    def draw(self, screen):
        #Draw track background
        track_rect = pygame.Rect(self.rect.x, self.rect.centery - self.track_height // 2, self.rect.width, self.track_height)
        pygame.draw.rect(screen, Colors.BUTTON_DARK, track_rect, border_radius=4)

        #Draw filled portion (left side of handle)
        handle_x = self.get_handle_x()
        filled_width = handle_x - self.rect.x
        if filled_width > 0:
            filled_rect = pygame.Rect(self.rect.x, self.rect.centery - self.track_height // 2, filled_width, self.track_height)
            pygame.draw.rect(screen, Colors.NEON_CYAN, filled_rect, border_radius=4)

        #Draw handle
        handle_center = (handle_x, self.rect.centery)
        pygame.draw.circle(screen, Colors.NEON_CYAN, handle_center, self.handle_radius)
        pygame.draw.circle(screen, Colors.TEXT_WHITE, handle_center, self.handle_radius -2 )

        #Draw borders around handle when dragging
        if self.is_dragging:
            pygame.draw.circle(screen, Colors.NEON_YELLOW, handle_center, self.handle_radius + 2, 2)
