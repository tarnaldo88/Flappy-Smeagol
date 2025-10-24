import pygame
import sys

# Initialize pygame
pygame.init()

import math

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800  # Make it square for better spiral movement
FPS = 60
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

# Camera settings
ZOOM_FACTOR = 1.0
MIN_ZOOM = 0.5
MAX_ZOOM = 2.0
TARGET_ZOOM = 1.0
CAMERA_SMOOTHING = 0.05
camera_x, camera_y = 0, 0

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spiral Smeagol')
clock = pygame.time.Clock()

# Bird variables in polar coordinates (r, theta)
bird_radius = 100  # Initial distance from center
bird_angle = 0      # Initial angle in radians
bird_width = 34
bird_height = 24
bird_angular_velocity = 0
ANGULAR_ACCELERATION = 0.001
ANGULAR_JUMP_STRENGTH = -0.1

# Load Smeagol image
smeagol_img = pygame.image.load('Images/smeagol.png').convert_alpha()
smeagol_img = pygame.transform.scale(smeagol_img, (bird_width, bird_height))

# Load and scale background image
bg_img = pygame.image.load('Images/background.jpg').convert()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Sam image for obstacles
sam_img = pygame.image.load('Images/sam.png').convert_alpha()

# Spiral parameters
SPIRAL_TIGHTNESS = 0.02  # How quickly the spiral tightens (smaller = more gradual)
SPIRAL_LENGTH = 2000  # How long the spiral path is in pixels (smaller = tighter)
SPIRAL_START_RADIUS = 100  # Starting radius of the spiral
SPIRAL_WALL_THICKNESS = 80  # Thickness of the spiral wall
ANGULAR_ACCELERATION = 0.0003  # Reduced for better control
ANGULAR_JUMP_STRENGTH = -0.1  # Slightly stronger for better control
BIRD_SPEED_MULTIPLIER = 2.0  # How fast the bird moves along the spiral

# Pipe variables
import random
PIPE_WIDTH = 52
PIPE_GAP = 150
PIPE_ANGULAR_VELOCITY = 0.03  # How fast pipes move in the spiral
PIPE_ANGULAR_SPACING = 0.5    # Angular distance between pipes

class Pipe:
    def __init__(self, angle, gap_angle):
        self.angle = angle
        self.gap_angle = gap_angle  # Angle where the gap is
        self.passed = False

def reset_game():
    global bird_radius, bird_angle, bird_angular_velocity, pipes, last_pipe_angle, score
    bird_radius = 50  # Start closer to center
    bird_angle = 0
    bird_angular_velocity = 0.02  # Constant forward motion
    pipes = []
    last_pipe_angle = 0
    score = 0

game_state = 'play'  # can be 'play' or 'game_over'
reset_game()

font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 36)

# --- Username Input Screen ---
def get_username():
    input_box = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 32, 200, 48)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    username = ''
    done = False
    font_input = pygame.font.SysFont(None, 48)
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if username.strip():
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 16 and event.unicode.isprintable():
                            username += event.unicode
        screen.fill((0, 0, 0))
        # Render prompt
        prompt = font_input.render('Enter Username:', True, (255,255,255))
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(prompt, prompt_rect)
        # Render input
        txt_surface = font_input.render(username, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)
    return username

def show_lobby():
    screen.fill((135, 206, 235))
    title_font = pygame.font.SysFont(None, 64)
    title = title_font.render('Flappy Smeagol', True, (0, 0, 0))
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
    screen.blit(title, title_rect)
    prompt_font = pygame.font.SysFont(None, 36)
    prompt = prompt_font.render('Press Space to Start', True, (0, 0, 0))
    prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
    screen.blit(prompt, prompt_rect)
    pygame.display.flip()

# Get username before starting the game
username = get_username()

# To prevent saving multiple times per game over event
score_saved = False

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == 'lobby':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = 'username'
        elif game_state == 'username':
            # Username input handled below
            pass      
    if game_state == 'lobby':
        show_lobby()
        clock.tick(30)
        continue
    if game_state == 'username':
        username = get_username()
        game_state = 'play'
        pygame.event.clear()  # Clear event queue so spacebar isn't "held over"
        continue
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == 'play':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_angular_velocity = ANGULAR_JUMP_STRENGTH
        elif game_state == 'game_over':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                game_state = 'play'
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Main Menu button is clicked
                menu_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 80, 160, 50)
                if menu_button_rect.collidepoint(event.pos):
                    reset_game()
                    game_state = 'lobby'

    if game_state == 'play':
        score_saved = False
        
        # Bird physics - move forward along spiral
        bird_angle += bird_angular_velocity
        
        # Calculate target radius based on angle (r = theta)
        target_radius = bird_angle * SPIRAL_TIGHTNESS * 1000
        
        # Adjust bird's radius based on input (steering within the tunnel)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Move outward in the tunnel
            bird_radius = min(bird_radius + 2.0, target_radius + SPIRAL_WALL_THICKNESS/2 - 20)
        else:
            # Gently move inward in the tunnel
            bird_radius = max(bird_radius - 1.5, target_radius - SPIRAL_WALL_THICKNESS/2 + 20)
        
        # Game over if bird hits the tunnel walls
        if (bird_radius > target_radius + SPIRAL_WALL_THICKNESS/2 - 10 or 
            bird_radius < target_radius - SPIRAL_WALL_THICKNESS/2 + 10):
            game_state = 'game_over'
        
        # Convert polar to cartesian for drawing
        bird_x = CENTER_X + (bird_radius * math.cos(bird_angle))
        bird_y = CENTER_Y + (bird_radius * math.sin(bird_angle))
        
        # Generate new pipes
        if not pipes or (bird_angle - last_pipe_angle) > PIPE_ANGULAR_SPACING:
            gap_angle = random.uniform(0, 2 * math.pi)
            pipes.append(Pipe(bird_angle + 2 * math.pi, gap_angle))
            last_pipe_angle = bird_angle
        
        # Update pipes and check for scoring
        for pipe in pipes[:]:
            pipe.angle -= PIPE_ANGULAR_VELOCITY
            
            # Check if pipe is behind the bird and not yet passed
            if pipe.angle < bird_angle and not pipe.passed:
                score += 1
                pipe.passed = True
            
            # Remove pipes that are too far behind
            if pipe.angle < bird_angle - math.pi * 2:
                pipes.remove(pipe)
        
        # Collision detection with spiral walls
        current_angle = bird_angle % (2 * math.pi)
        wall_radius = SPIRAL_START_RADIUS + (current_angle * SPIRAL_TIGHTNESS * 500)
        
        # Calculate distance from center of wall
        distance_from_wall_center = abs(bird_radius - wall_radius)
        
        # Calculate the safe zone (where the bird can fly)
        inner_wall = wall_radius - SPIRAL_WALL_THICKNESS/2
        outer_wall = wall_radius + SPIRAL_WALL_THICKNESS/2
        
        # Check if bird is outside the safe zone
        if (bird_radius < inner_wall - bird_width/2 or 
            bird_radius > outer_wall + bird_width/2):
            game_state = 'game_over'
            
        # Collision detection with pipes
        for pipe in pipes:
            # Calculate angle difference between pipe gap and bird
            angle_diff = abs((bird_angle - pipe.gap_angle + math.pi) % (2 * math.pi) - math.pi)
            
            # If bird is in the pipe's angle range and not in the gap
            if (abs(pipe.angle - bird_angle) < 0.2 and 
                (angle_diff > math.radians(30) or bird_radius < 50)):
                game_state = 'game_over'

        # Camera follows bird with smooth movement
        target_zoom = 1.0  # Keep zoom constant for now
        ZOOM_FACTOR += (target_zoom - ZOOM_FACTOR) * CAMERA_SMOOTHING
        
        # Calculate camera position to keep bird centered
        camera_x = SCREEN_WIDTH//2 - bird_x
        camera_y = SCREEN_HEIGHT//2 - bird_y
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw the background image (scaled and positioned)
        bg_scaled = pygame.transform.scale(bg_img, 
                                         (int(SCREEN_WIDTH * ZOOM_FACTOR), 
                                          int(SCREEN_HEIGHT * ZOOM_FACTOR)))
        screen.blit(bg_scaled, (camera_x, camera_y))
        
        # Draw the spiral tunnel
        wall_angle = 0
        wall_radius = 0
        segments = int(SPIRAL_LENGTH / 10)  # Number of segments to draw
        
        # Draw the spiral path
        for i in range(segments):
            # Calculate radius at this angle (r = a*theta)
            wall_radius = wall_angle * SPIRAL_TIGHTNESS * 1000
            
            # Calculate inner and outer edges of the tunnel
            outer_radius = wall_radius + SPIRAL_WALL_THICKNESS/2
            inner_radius = max(10, wall_radius - SPIRAL_WALL_THICKNESS/2)
            
            # Calculate points for the outer and inner walls
            x_outer = CENTER_X + outer_radius * math.cos(wall_angle)
            y_outer = CENTER_Y + outer_radius * math.sin(wall_angle)
            x_inner = CENTER_X + inner_radius * math.cos(wall_angle)
            y_inner = CENTER_Y + inner_radius * math.sin(wall_angle)
            
            # Draw the tunnel walls
            if i > 0:  # Skip first segment
                # Draw outer wall (blue)
                pygame.draw.line(screen, (0, 100, 255), 
                               (prev_x_outer + camera_x, prev_y_outer + camera_y),
                               (x_outer + camera_x, y_outer + camera_y), 3)
                
                # Draw inner wall (darker blue)
                pygame.draw.line(screen, (0, 50, 150),
                               (prev_x_inner + camera_x, prev_y_inner + camera_y),
                               (x_inner + camera_x, y_inner + camera_y), 3)
                
                # Draw connecting lines to create tunnel effect
                if i % 5 == 0:  # Draw connecting lines less frequently for better performance
                    pygame.draw.line(screen, (0, 150, 200),
                                   (x_outer + camera_x, y_outer + camera_y),
                                   (x_inner + camera_x, y_inner + camera_y), 1)
            
            # Save points for next segment
            prev_x_outer, prev_y_outer = x_outer, y_outer
            prev_x_inner, prev_y_inner = x_inner, y_inner
            
            # Increment angle for next segment
            wall_angle += 0.1
            
            # Stop drawing if we've gone far enough ahead of the bird
            if wall_angle > bird_angle + math.pi * 2:  # One full rotation ahead
                break
        
        # Draw the bird (Smeagol image)
        bird_rotated = pygame.transform.rotate(
            pygame.transform.scale(smeagol_img, 
                                 (int(bird_width * ZOOM_FACTOR), 
                                  int(bird_height * ZOOM_FACTOR))),
            math.degrees(bird_angle) + 90
        )
        bird_screen_x = (bird_x - camera_x) * ZOOM_FACTOR - bird_rotated.get_width() // 2
        bird_screen_y = (bird_y - camera_y) * ZOOM_FACTOR - bird_rotated.get_height() // 2
        screen.blit(bird_rotated, (bird_screen_x, bird_screen_y))

        # Draw the score (always at fixed screen position)
        score_text = score_font.render(f'Score: {score}', True, (255,0,0))
        screen.blit(score_text, (10, 10))

    elif game_state == 'game_over':
        if not score_saved:
            try:
                with open('scores.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{username}: {score}\n')
            except Exception as e:
                print(f'Error saving score: {e}')
            score_saved = True
        # Fill the background with dark red
        screen.fill((139, 0, 0))  # Dark red color
        screen.blit(score_text, (10, 10)) 
        
        # Draw the bird in its final position
        screen.blit(smeagol_img, (bird_x, int(bird_y)))
        
        # Game over text with semi-transparent background
        text = font.render('Game Over', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        
        # Restart instructions
        restart_text = font.render('Press Space to Restart', True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        
        # Draw Main Menu button with more space
        menu_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 70, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), menu_button_rect, border_radius=8)
        
        # Use a smaller font for the menu button text
        menu_font = pygame.font.SysFont(None, 36)
        menu_text = menu_font.render('Main Menu', True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        
        # Draw all elements
        screen.blit(text, text_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(menu_text, menu_text_rect)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

