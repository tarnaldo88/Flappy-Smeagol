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

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = JUMP_STRENGTH

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

    # Fill the background
    screen.fill((135, 206, 235))  # Sky blue

    # Draw the bird (rectangle for now)
    pygame.draw.rect(screen, (255, 255, 0), (bird_x, int(bird_y), bird_width, bird_height))

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
