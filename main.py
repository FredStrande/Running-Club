#Add imports
import pygame
from game_state import GameState
from screens.settings_screen import SettingsScreen
import math
from ui.colors import Colors
from ui.button import Button

pygame.init()
pygame.mixer.init()

current_state = GameState.MENU
settings_screen = None

screen = pygame.display.set_mode((1024, 768))

#Load background music
try:
    pygame.mixer.music.load("assets/music/running_club_bg.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-2)
except:
    print("Warning: Could not load background music")

#Load button hover sound
button_hover_sound = pygame.mixer.Sound("assets/sounds/button_hover.wav")
button_hover_sound.set_volume(0.3)

screen_width = screen.get_width()
screen_height = screen.get_height()

#Button properties
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50
BUTTON_SPACING = 25
NUM_BUTTONS = 4

#Calculate position
button_x = (screen_width - BUTTON_WIDTH) // 2
total_height = (NUM_BUTTONS * BUTTON_HEIGHT) + ((NUM_BUTTONS - 1) * BUTTON_SPACING)
start_y = (screen_height - total_height) // 2

#Create buttons with calculated positions
new_game_button = Button(button_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT, "New Game")
load_game_button = Button(button_x, start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "Load Game")
settings_button = Button(button_x, start_y + 2 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Settings")
quit_button = Button(button_x, start_y + 3 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")


#For animated background
clock = pygame.time.Clock()
time_passed = 0 

def draw_background (screen, time):
    # Base dark background
    screen.fill(Colors.BG_DARK)

    #Add sublte animated gradient overlay
    overlay = pygame.Surface((1024,768), pygame.SRCALPHA)
    for y in range (0, 768, 2):
        alpha = int(20 + 10 * math.sin(time + y * 0.01))
        color = (*Colors.BG_MEDIUM, alpha)
        pygame.draw.line(overlay, color, (0, y), (1024, y))

def draw_animated_title(screen, time, screen_width, base_y):
    #Title text
    title_text = "Running Club"
    title_font_size = 85

    #Try to use pixel font, fallback to default
    try:
        title_font = pygame.font.Font("fonts/BoldPixels.ttf", title_font_size)
    except:
        title_font = pygame.font.Font(None, title_font_size)

    #create the title text surface
    title_surface = title_font.render(title_text, True, Colors.TEXT_NEON)
    title_rect = title_surface.get_rect()

    #Calculate bounce offset (Smoothe sine wave)
    bounce_speed = 2.0
    bounce_amplitude = 8
    bounce_offset = math.sin(time * bounce_speed) * bounce_amplitude

    #Calculate position (centered horizontally, above buttons)
    title_x = (screen_width - title_rect.width) // 2
    title_y = base_y - 100 + int(bounce_offset)

        # Shadow offset - downward and to the right for "laying" effect
    shadow_offset_x = 4  # Shadow to the right
    shadow_offset_y = 4  # Shadow downward
    
    # Draw shadow layers for depth (from soft outer to sharp inner)
    shadow_layers = [
        (shadow_offset_x + 3, shadow_offset_y + 3, 40),  # Outer soft shadow
        (shadow_offset_x + 2, shadow_offset_y + 2, 60),  # Middle shadow
        (shadow_offset_x + 1, shadow_offset_y + 1, 100),  # Inner sharp shadow
        (shadow_offset_x, shadow_offset_y, 150),         # Main shadow
    ]
    
    # Draw all shadow layers
    for offset_x, offset_y, alpha in shadow_layers:
        #Render the text in black
        shadow_surface = title_font.render(title_text, True, (0, 0, 0))
        # Set the alpha on the surface directly
        shadow_surface.set_alpha(alpha)
        # Draw the shadow at the offset position
        screen.blit(shadow_surface, (title_x + offset_x, title_y + offset_y))


    #Draw the main title text (on top of shadows)
    screen.blit(title_surface, (title_x, title_y))

    

running = True
while running:
    dt = clock.tick(60)/1000.0 # Delta time in seconds
    time_passed += dt
    mouse_pos = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == GameState.MENU:
                if new_game_button.is_clicked(mouse_pos):
                    print("New Game clicked!")
                elif load_game_button.is_clicked(mouse_pos):
                    print("Load game clicked!")
                elif settings_button.is_clicked(mouse_pos):
                    current_state = GameState.SETTINGS
                    settings_screen = SettingsScreen(screen_width, screen_height, 
                                                    int(pygame.mixer.music.get_volume() * 100))
                elif quit_button.is_clicked(mouse_pos):
                    running = False
            elif current_state == GameState.SETTINGS:
                result = settings_screen.handle_event(event, mouse_pos)
                if result == "BACK":
                    current_state = GameState.MENU
                    pygame.mixer.music.set_volume(settings_screen.get_volume())
        elif current_state == GameState.SETTINGS:
            # Handle other events for settings (mouse motion, mouse up, etc.)
            settings_screen.handle_event(event, mouse_pos)  

        
        # Update based on current state
    if current_state == GameState.MENU:
        # Check for hover transitions and play sound
        if new_game_button.check_hover(mouse_pos) and not new_game_button.was_hovered:
            button_hover_sound.play()
        if load_game_button.check_hover(mouse_pos) and not load_game_button.was_hovered:
            button_hover_sound.play()
        if settings_button.check_hover(mouse_pos) and not settings_button.was_hovered:
            button_hover_sound.play()
        if quit_button.check_hover(mouse_pos) and not quit_button.was_hovered:
            button_hover_sound.play()
        
        # Store previous hover states
        new_game_button.was_hovered = new_game_button.is_hovered
        load_game_button.was_hovered = load_game_button.is_hovered
        settings_button.was_hovered = settings_button.is_hovered
        quit_button.was_hovered = quit_button.is_hovered
    elif current_state == GameState.SETTINGS:
        settings_screen.update(mouse_pos)
        # Update music volume in real-time
        pygame.mixer.music.set_volume(settings_screen.get_volume())


        # Clear screen
    draw_background(screen, time_passed)

    # Draw based on current state
    if current_state == GameState.MENU:
        # Draw animated title (Above buttons)
        draw_animated_title(screen, time_passed, screen_width, start_y)
        
        # Draw buttons
        new_game_button.draw(screen)
        load_game_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)
    elif current_state == GameState.SETTINGS:
        settings_screen.draw(screen)

    pygame.display.flip()

pygame.quit()
