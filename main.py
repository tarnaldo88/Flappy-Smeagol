import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smeagol's Spiral Journey")
clock = pygame.time.Clock()

# Load images
try:
    smeagol_img = pygame.image.load('Images/smeagol.png').convert_alpha()
    bg_img = pygame.image.load('Images/background.jpg').convert()
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ring_img = pygame.image.load('Images/sam.png').convert_alpha()
    ring_img = pygame.transform.scale(ring_img, (40, 40))
except:
    # Create placeholder images if files not found
    smeagol_img = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(smeagol_img, (0, 255, 0), (20, 20), 20)
    bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img.fill((50, 50, 100))
    ring_img = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(ring_img, (255, 200, 0), (20, 20), 20, 3)

# Game parameters
class Smeagol:
    def __init__(self):
        self.angle = 0  # Current angle in radians
        self.radius = 100  # Distance from center
        self.target_radius = 100  # Target radius for smooth movement
        self.speed = 0.03  # Base angular speed
        self.radius_speed = 2.0  # Radius change speed
        self.size = 25  # Size of Smeagol
        self.image = pygame.transform.scale(smeagol_img, (self.size, self.size))
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        
    def update(self, keys):
        # Move forward/backward with left/right arrow keys or A/D
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.speed * 1.5  # Move forward (clockwise)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.speed * 1.5  # Move backward (counter-clockwise)
        
        # Control radius with up/down or W/S
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.target_radius = max(50, self.target_radius - self.radius_speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.target_radius = min(350, self.target_radius + self.radius_speed)
            
        # Smooth radius transition
        self.radius += (self.target_radius - self.radius) * 0.1
        
        # Calculate position (fixed center)
        self.x = CENTER_X + math.cos(self.angle) * self.radius
        self.y = CENTER_Y + math.sin(self.angle) * self.radius
        self.rect.center = (int(self.x), int(self.y))

class Ring:
    def __init__(self, angle, radius):
        self.angle = angle
        self.radius = radius
        self.size = 30  # Size of rings
        self.collected = False
        self.image = pygame.transform.scale(ring_img, (self.size, self.size))
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        # Initialize position
        self.update_position()
        
    def update_position(self):
        # Calculate fixed position based on angle and radius
        self.x = CENTER_X + math.cos(self.angle) * self.radius
        self.y = CENTER_Y + math.sin(self.angle) * self.radius
        self.rect.center = (int(self.x), int(self.y))

# Game state
game_state = "playing"
score = 0
font = pygame.font.SysFont(None, 48)

def reset_game():
    global smeagol, rings, score, game_state
    smeagol = Smeagol()
    rings = []
    score = 0
    game_state = "playing"
    
    # Create initial rings
    for i in range(5):
        angle = smeagol.angle + (i + 1) * 1.5
        radius = random.randint(100, 300)
        rings.append(Ring(angle, radius))

# Initialize game
reset_game()

def draw_spiral(surface, num_loops=5, line_width=2):
    """Draw a fixed spiral path"""
    points = []
    for i in range(360 * num_loops):
        angle = math.radians(i)
        # Make the spiral expand more gradually
        radius = 50 + i * 0.3
        x = CENTER_X + math.cos(angle) * radius
        y = CENTER_Y + math.sin(angle) * radius
        points.append((x, y))
    
    if len(points) > 1:
        pygame.draw.lines(surface, (100, 100, 200, 100), False, points, line_width)
        
        # Draw radial lines for better depth perception
        for i in range(0, len(points), 30):
            if i < len(points):
                pygame.draw.line(surface, (80, 80, 180, 80), 
                               (CENTER_X, CENTER_Y), points[i], 1)

def draw_ui():
    """Draw score and other UI elements"""
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

def show_game_over():
    """Show game over screen"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    game_over_text = font.render('Game Over!', True, (255, 255, 255))
    score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
    restart_text = font.render('Press R to Restart', True, (255, 255, 255))
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                SCREEN_HEIGHT//2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 
                            SCREEN_HEIGHT//2 + 10))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                              SCREEN_HEIGHT//2 + 70))

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and game_state == "game_over":
                reset_game()
    
    # Get keyboard state
    keys = pygame.key.get_pressed()
    
    # Update game state
    if game_state == "playing":
        # Update Smeagol
        smeagol.update(keys)
        
        # Update rings
        for ring in rings[:]:
            if not ring.collected:
                ring.update()
                # Check for collection
                if smeagol.rect.colliderect(ring.rect):
                    ring.collected = True
                    score += 10
                    
                    # Add new ring ahead on the spiral
                    new_angle = smeagol.angle + random.uniform(1.5, 3.0)
                    # Keep rings at a reasonable distance from the center
                    new_radius = random.randint(100, 300)
                    rings.append(Ring(new_angle, new_radius))
        
        # Remove collected rings
        rings = [ring for ring in rings if not ring.collected]
        
        # Game over if too far from center or too close
        if smeagol.radius > 350 or smeagol.radius < 50:
            game_state = "game_over"
    
    # Drawing
    screen.blit(bg_img, (0, 0))
    
    # Draw fixed spiral path
    draw_spiral(screen, num_loops=5)
    
    # Draw rings
    for ring in rings:
        if not ring.collected:
            screen.blit(ring.image, ring.rect)
    
    # Draw Smeagol with rotation based on movement direction
    # Calculate movement direction for proper rotation
    movement_angle = math.atan2(smeagol.y - CENTER_Y, smeagol.x - CENTER_X)
    angle_degrees = math.degrees(movement_angle) - 90  # -90 to point along the spiral
    rotated_smeagol = pygame.transform.rotate(smeagol.image, -angle_degrees)
    rect = rotated_smeagol.get_rect(center=(smeagol.x, smeagol.y))
    screen.blit(rotated_smeagol, rect.topleft)
    
    # Draw UI
    draw_ui()
    
    # Show game over screen if needed
    if game_state == "game_over":
        show_game_over()
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Clean up
pygame.quit()
sys.exit()
    #             game_state = 'play'
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             # Check if Main Menu button is clicked
    #             menu_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 80, 160, 50)
    #             if menu_button_rect.collidepoint(event.pos):
    #                 reset_game()
    #                 game_state = 'lobby'

    # if game_state == 'play':
    #     score_saved = False
        
    #     # Add a small delay before starting to prevent immediate game over
    #     if bird_angle < 0.1:  # First few frames
    #         bird_angular_velocity = 0.01  # Start slow
        
    #     # Bird physics - move forward along spiral
    #     bird_angular_velocity = 0.02  # Reset to base speed each frame
    #     bird_angle += bird_angular_velocity
        
    #     # Calculate target radius based on angle (r = a*theta)
    #     target_radius = SPIRAL_START_RADIUS + (bird_angle * SPIRAL_TIGHTNESS * 10000)
        
    #     # Adjust bird's radius based on input (steering within the tunnel)
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_SPACE]:
    #         # Move outward in the tunnel
    #         bird_radius = min(bird_radius + 4.0, target_radius + SPIRAL_WALL_THICKNESS/2 - 20)
    #     else:
    #         # Gently move inward in the tunnel
    #         bird_radius = max(bird_radius - 3.0, target_radius - SPIRAL_WALL_THICKNESS/2 + 20)
        
    #     # Game over if bird hits the tunnel walls (with more lenient collision)
    #     # Only check for collisions after the bird has moved a bit from the center
    #     if bird_radius > 10:  # Allow the bird to start from the center
    #         wall_margin = 20  # Extra margin before game over
    #         if (bird_radius > target_radius + SPIRAL_WALL_THICKNESS/2 + wall_margin or 
    #             bird_radius < max(10, target_radius - SPIRAL_WALL_THICKNESS/2 - wall_margin)):
    #             game_state = 'game_over'
        
    #     # Convert polar to cartesian for drawing
    #     bird_x = (bird_radius * math.cos(bird_angle))
    #     bird_y = (bird_radius * math.sin(bird_angle))
        
    #     # Generate new pipes
    #     if not pipes or (bird_angle - last_pipe_angle) > PIPE_ANGULAR_SPACING:
    #         gap_angle = random.uniform(0, 2 * math.pi)
    #         pipes.append(Pipe(bird_angle + 2 * math.pi, gap_angle))
    #         last_pipe_angle = bird_angle
        
    #     # Update pipes and check for scoring
    #     for pipe in pipes[:]:
    #         pipe.angle -= PIPE_ANGULAR_VELOCITY
            
    #         # Check if pipe is behind the bird and not yet passed
    #         if pipe.angle < bird_angle and not pipe.passed:
    #             score += 1
    #             pipe.passed = True
            
    #         # Remove pipes that are too far behind
    #         if pipe.angle < bird_angle - math.pi * 2:
    #             pipes.remove(pipe)
        
    #     # Collision detection with spiral walls
    #     current_angle = bird_angle % (2 * math.pi)
    #     wall_radius = SPIRAL_START_RADIUS + (current_angle * SPIRAL_TIGHTNESS * 10000)
        
    #     # Calculate the safe zone (where the bird can fly)
    #     inner_wall = wall_radius - SPIRAL_WALL_THICKNESS/2
    #     outer_wall = wall_radius + SPIRAL_WALL_THICKNESS/2
        
    #     # Check if bird is outside the safe zone (with more lenient collision)
    #     safe_margin = 15  # Extra margin before game over
        
    #     # Only check for collisions after the bird has moved a bit from the center
    #     if bird_radius > 10:  # Allow the bird to start from the center
    #         if (bird_radius < max(0, inner_wall - bird_width/2 - safe_margin) or 
    #             bird_radius > outer_wall + bird_width/2 + safe_margin):
    #             game_state = 'game_over'
            
    #     # Collision detection with pipes
    #     for pipe in pipes:
    #         # Calculate angle difference between pipe gap and bird
    #         angle_diff = abs((bird_angle - pipe.gap_angle + math.pi) % (2 * math.pi) - math.pi)
            
    #         # If bird is in the pipe's angle range and not in the gap
    #         if (abs(pipe.angle - bird_angle) < 0.2 and 
    #             (angle_diff > math.radians(30) or bird_radius < 50)):
    #             game_state = 'game_over'

    #     # Calculate target camera position to keep bird centered
    #     target_camera_x = CENTER_X - bird_x
    #     target_camera_y = CENTER_Y - bird_y
        
    #     # Smooth camera follow with easing
    #     camera_x += (target_camera_x - camera_x) * CAMERA_SMOOTHING * 3
    #     camera_y += (target_camera_y - camera_y) * CAMERA_SMOOTHING * 3
        
    #     # Dynamic zoom based on bird's position in the spiral
    #     # As bird moves outward, gradually zoom out to keep more of the spiral in view
    #     distance_from_center = math.sqrt(bird_x**2 + bird_y**2)
    #     zoom_factor = 1.0 + (distance_from_center / 1000)  # Adjust divisor for zoom sensitivity
    #     target_zoom = min(MAX_ZOOM, max(MIN_ZOOM, TARGET_ZOOM / zoom_factor))
        
    #     # Smooth zoom transition
    #     ZOOM_FACTOR += (target_zoom - ZOOM_FACTOR) * CAMERA_SMOOTHING
        
    #     # Clear screen
    #     screen.fill((0, 0, 0))
        
    #     # Draw the background image (scaled and positioned with zoom)
    #     bg_scaled = pygame.transform.scale(bg_img, 
    #                                      (int(SCREEN_WIDTH * ZOOM_FACTOR), 
    #                                       int(SCREEN_HEIGHT * ZOOM_FACTOR)))
    #     # Center the background on the bird
    #     bg_x = (SCREEN_WIDTH - bg_scaled.get_width()) // 2 + (camera_x * ZOOM_FACTOR)
    #     bg_y = (SCREEN_HEIGHT - bg_scaled.get_height()) // 2 + (camera_y * ZOOM_FACTOR)
    #     screen.blit(bg_scaled, (bg_x, bg_y))
        
    #     # Draw the spiral tunnel
    #     wall_angle = max(0, bird_angle - math.pi * 0.3)  # Start drawing slightly behind the bird
    #     wall_radius = 0
    #     segments = int(SPIRAL_LENGTH / 4)  # Draw more segments for smoother spiral
        
    #     # Draw the spiral path
    #     for i in range(segments):
    #         # Calculate radius at this angle (r = a*theta)
    #         wall_radius = SPIRAL_START_RADIUS + (wall_angle * SPIRAL_TIGHTNESS * 10000)
            
    #         # Calculate inner and outer edges of the tunnel
    #         outer_radius = wall_radius + SPIRAL_WALL_THICKNESS/2
    #         inner_radius = max(10, wall_radius - SPIRAL_WALL_THICKNESS/2)
            
    #         # Calculate points for the outer and inner walls
    #         x_outer = CENTER_X + outer_radius * math.cos(wall_angle)
    #         y_outer = CENTER_Y + outer_radius * math.sin(wall_angle)
    #         x_inner = CENTER_X + inner_radius * math.cos(wall_angle)
    #         y_inner = CENTER_Y + inner_radius * math.sin(wall_angle)
            
    #         # Draw the tunnel walls
    #         if i > 0:  # Skip first segment
    #             # Draw outer wall (blue)
    #             pygame.draw.line(screen, (0, 100, 255), 
    #                            (prev_x_outer + camera_x, prev_y_outer + camera_y),
    #                            (x_outer + camera_x, y_outer + camera_y), 3)
                
    #             # Draw inner wall (darker blue)
    #             pygame.draw.line(screen, (0, 50, 150),
    #                            (prev_x_inner + camera_x, prev_y_inner + camera_y),
    #                            (x_inner + camera_x, y_inner + camera_y), 3)
                
    #             # Draw connecting lines to create tunnel effect
    #             if i % 5 == 0:  # Draw connecting lines less frequently for better performance
    #                 pygame.draw.line(screen, (0, 150, 200),
    #                                (x_outer + camera_x, y_outer + camera_y),
    #                                (x_inner + camera_x, y_inner + camera_y), 1)
            
    #         # Save points for next segment
    #         prev_x_outer, prev_y_outer = x_outer, y_outer
    #         prev_x_inner, prev_y_inner = x_inner, y_inner
            
    #         # Increment angle for next segment
    #         wall_angle += 0.1
            
    #         # Stop drawing if we've gone far enough ahead of the bird
    #         if wall_angle > bird_angle + math.pi * 2:  # One full rotation ahead
    #             break
        
    #     # Draw the bird (Smeagol image)
    #     bird_rotated = pygame.transform.rotate(
    #         pygame.transform.scale(smeagol_img, 
    #                              (int(bird_width * ZOOM_FACTOR), 
    #                               int(bird_height * ZOOM_FACTOR))),
    #         math.degrees(bird_angle) + 90
    #     )
    #     # Draw bird at screen center (since camera follows it)
    #     bird_screen_x = (SCREEN_WIDTH - bird_rotated.get_width()) // 2
    #     bird_screen_y = (SCREEN_HEIGHT - bird_rotated.get_height()) // 2
    #     screen.blit(bird_rotated, (bird_screen_x, bird_screen_y))

    #     # Draw the score (always at fixed screen position)
    #     score_text = score_font.render(f'Score: {score}', True, (255,0,0))
    #     screen.blit(score_text, (10, 10))

    # elif game_state == 'game_over':
    #     if not score_saved:
    #         try:
    #             with open('scores.txt', 'a', encoding='utf-8') as f:
    #                 f.write(f'{username}: {score}\n')
    #         except Exception as e:
    #             print(f'Error saving score: {e}')
    #         score_saved = True
    #     # Fill the background with dark red
    #     screen.fill((139, 0, 0))  # Dark red color
    #     screen.blit(score_text, (10, 10)) 
        
    #     # Draw the bird in its final position
    #     screen.blit(smeagol_img, (bird_x, int(bird_y)))
        
    #     # Game over text with semi-transparent background
    #     text = font.render('Game Over', True, (255, 255, 255))
    #     text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        
    #     # Restart instructions
    #     restart_text = font.render('Press Space to Restart', True, (255, 255, 255))
    #     restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        
    #     # Draw Main Menu button with more space
    #     menu_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 70, 200, 50)
    #     pygame.draw.rect(screen, (0, 0, 0), menu_button_rect, border_radius=8)
        
    #     # Use a smaller font for the menu button text
    #     menu_font = pygame.font.SysFont(None, 36)
    #     menu_text = menu_font.render('Main Menu', True, (255, 255, 255))
    #     menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        
    #     # Draw all elements
    #     screen.blit(text, text_rect)
    #     screen.blit(restart_text, restart_rect)
    #     screen.blit(menu_text, menu_text_rect)

    # # Update the display
    # pygame.display.flip()
    # clock.tick(FPS)

