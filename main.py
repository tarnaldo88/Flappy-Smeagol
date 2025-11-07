import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Smeagol")
clock = pygame.time.Clock()

# Load images
try:
    smeagol_img = pygame.image.load('Images/smeagol.png').convert_alpha()
    smeagol_img = pygame.transform.scale(smeagol_img, (40, 30))
    bg_img = pygame.image.load('Images/background.jpg').convert()
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pipe_img = pygame.image.load('Images/sam.png').convert_alpha()
    pipe_img = pygame.transform.scale(pipe_img, (80, 400))
except:
    # Create placeholder images if files not found
    smeagol_img = pygame.Surface((40, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(smeagol_img, (0, 255, 0), (0, 0, 40, 30))
    bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img.fill((135, 206, 235))  # Sky blue
    pipe_img = pygame.Surface((80, 400), pygame.SRCALPHA)
    pygame.draw.rect(pipe_img, (0, 200, 0), (0, 0, 80, 400))

# Game parameters
class Smeagol:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = (40, 30)
        self.image = smeagol_img
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = int(self.y)
        
        # Rotate based on velocity
        self.rotated_image = pygame.transform.rotate(
            self.image, 
            min(max(-30, -self.velocity * 3), 30)  # Limit rotation between -30 and 30 degrees
        )
        self.rect = self.rotated_image.get_rect(center=(self.x + self.size[0]//2, self.y + self.size[1]//2))
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def draw(self, surface):
        surface.blit(self.rotated_image, (self.x, self.y))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 150)
        self.passed = False
        self.size = (80, 400)
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, surface):
        # Draw top pipe (flipped)
        top_pipe = pygame.transform.flip(pipe_img, False, True)
        surface.blit(top_pipe, (self.x, self.gap_y - PIPE_GAP//2 - self.size[1]))
        
        # Draw bottom pipe
        surface.blit(pipe_img, (self.x, self.gap_y + PIPE_GAP//2))
        
    def get_rects(self):
        # Make the hitbox narrower and adjust the height to better match the visible pipe
        hitbox_width = self.size[0] * 0.6  # 60% of the original width
        hitbox_x = self.x + (self.size[0] - hitbox_width) / 2  # Center the hitbox
        
        # Adjust the height of the hitbox to better match the visible part of the pipe
        hitbox_height = self.size[1] * 0.9  # 90% of the original height
        
        # Top pipe hitbox (positioned at the bottom of the top pipe)
        top_rect = pygame.Rect(
            int(hitbox_x), 
            int(self.gap_y - PIPE_GAP//2 - hitbox_height * 0.3),  # Adjust vertical position
            int(hitbox_width), 
            int(hitbox_height * 0.7)  # Only use part of the height
        )
        
        # Bottom pipe hitbox (positioned at the top of the bottom pipe)
        bottom_rect = pygame.Rect(
            int(hitbox_x), 
            int(self.gap_y + PIPE_GAP//2), 
            int(hitbox_width), 
            int(hitbox_height * 0.7)  # Only use part of the height
        )
        return top_rect, bottom_rect

# Game state
game_state = "playing"
score = 0
high_score = 0
pipes = []
last_pipe = pygame.time.get_ticks()
font = pygame.font.SysFont('Arial', 30)

def reset_game():
    global smeagol, pipes, score, last_pipe
    smeagol = Smeagol()
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()

reset_game()

def draw_ui():
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    
    high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 255))
    screen.blit(high_score_text, (20, 50))

def show_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    game_over_text = font.render('Game Over!', True, (255, 255, 255))
    score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
    restart_text = font.render('Press SPACE to Restart', True, (255, 255, 255))
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                SCREEN_HEIGHT//2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 
                            SCREEN_HEIGHT//2))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                              SCREEN_HEIGHT//2 + 50))

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
            elif event.key == pygame.K_SPACE:
                if game_state == "playing":
                    smeagol.flap()
                else:
                    reset_game()
                    game_state = "playing"
    
    # Update game state
    if game_state == "playing":
        # Update Smeagol
        smeagol.update()
        
        # Generate new pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > PIPE_FREQUENCY:
            pipes.append(Pipe(SCREEN_WIDTH))
            last_pipe = current_time
        
        # Update pipes and check for scoring
        for pipe in pipes[:]:
            pipe.update()
            
            # Check if pipe is passed
            if pipe.x + pipe.size[0] < smeagol.x and not pipe.passed:
                score += 1
                pipe.passed = True
                if score > high_score:
                    high_score = score
            
            # Remove off-screen pipes
            if pipe.x < -pipe.size[0]:
                pipes.remove(pipe)
            
            # Check for collisions
            top_rect, bottom_rect = pipe.get_rects()
            if (smeagol.rect.colliderect(top_rect) or 
                smeagol.rect.colliderect(bottom_rect) or
                smeagol.y < 0 or 
                smeagol.y > SCREEN_HEIGHT):
                game_state = "game_over"
    
    # Drawing
    screen.blit(bg_img, (0, 0))
    
    # Draw pipes
    for pipe in pipes:
        pipe.draw(screen)
    
    # Draw Smeagol
    smeagol.draw(screen)
    
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

