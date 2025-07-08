import pygame
import sys

# Initialize pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Smeagol')
clock = pygame.time.Clock()

# Bird variables
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_width = 34
bird_height = 24
bird_velocity = 0
GRAVITY = 0.5
JUMP_STRENGTH = -8

# Load Smeagol image
smeagol_img = pygame.image.load('Images/smeagol.png').convert_alpha()
smeagol_img = pygame.transform.scale(smeagol_img, (bird_width, bird_height))

# Load and scale background image
bg_img = pygame.image.load('Images/background.jpg').convert()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Pipe variables
import random
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 150
PIPE_VELOCITY = 3
pipe_x = SCREEN_WIDTH
pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)

def reset_game():
    global bird_x, bird_y, bird_velocity, pipe_x, pipe_height, score, pipe_passed
    bird_x = 50
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipe_x = SCREEN_WIDTH
    pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
    score = 0
    pipe_passed = False

game_state = 'play'  # can be 'play' or 'game_over'
reset_game()

font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == 'play':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = JUMP_STRENGTH
        elif game_state == 'game_over':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                game_state = 'play'

    if game_state == 'play':
        # Bird physics
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Prevent bird from going off-screen
        if bird_y < 0:
            bird_y = 0
            bird_velocity = 0
        if bird_y + bird_height > SCREEN_HEIGHT:
            bird_y = SCREEN_HEIGHT - bird_height
            bird_velocity = 0

        # Move pipes
        pipe_x -= PIPE_VELOCITY
        if pipe_x + PIPE_WIDTH < bird_x and not pipe_passed:
            score += 1
            pipe_passed = True
        if pipe_x < -PIPE_WIDTH:
            pipe_x = SCREEN_WIDTH
            pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            pipe_passed = False

        # Collision detection
        bird_rect = pygame.Rect(bird_x, int(bird_y), bird_width, bird_height)
        top_pipe_rect = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
        bottom_pipe_rect = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP)

        if (bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)):
            game_state = 'game_over'

        # Draw the background image
        screen.blit(bg_img, (0, 0))

        # Draw pipes
        pygame.draw.rect(screen, (34, 139, 34), (pipe_x, 0, PIPE_WIDTH, pipe_height))
        pygame.draw.rect(screen, (34, 139, 34), (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP))

        # Draw the bird (Smeagol image)
        screen.blit(smeagol_img, (bird_x, int(bird_y)))

        # Draw the score
        score_text = score_font.render(f'Score: {score}', True, (0,0,0))
        screen.blit(score_text, (10, 10))

    elif game_state == 'game_over':
        # Fill the background
        screen.fill((135, 206, 235))
        # Draw pipes
        pygame.draw.rect(screen, (34, 139, 34), (pipe_x, 0, PIPE_WIDTH, pipe_height))
        pygame.draw.rect(screen, (34, 139, 34), (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP))
        # Draw the bird
        screen.blit(smeagol_img, (bird_x, int(bird_y)))
        # Draw Game Over text
        text = font.render('Game Over', True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        screen.blit(text, text_rect)
        restart_text = font.render('Press Space to Restart', True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        screen.blit(restart_text, restart_rect)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

