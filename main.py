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

# Load Sam image for obstacles
sam_img = pygame.image.load('Images/sam.png').convert_alpha()

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
        screen.fill((135, 206, 235))
        # Render prompt
        prompt = font_input.render('Enter Username:', True, (0,0,0))
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
                bird_velocity = JUMP_STRENGTH
        elif game_state == 'game_over':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                game_state = 'play'

    if game_state == 'play':
        score_saved = False
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

        # Draw pipes as Sam images
        # Top Sam
        top_sam_scaled = pygame.transform.scale(sam_img, (PIPE_WIDTH, max(1, pipe_height)))
        screen.blit(top_sam_scaled, (pipe_x, 0))
        # Bottom Sam
        bottom_pipe_height = SCREEN_HEIGHT - pipe_height - PIPE_GAP
        if bottom_pipe_height > 0:
            bottom_sam_scaled = pygame.transform.scale(sam_img, (PIPE_WIDTH, bottom_pipe_height))
            screen.blit(bottom_sam_scaled, (pipe_x, pipe_height + PIPE_GAP))

        # Draw the bird (Smeagol image)
        screen.blit(smeagol_img, (bird_x, int(bird_y)))

        # Draw the score
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
        # Fill the background
        screen.fill((135, 206, 235))
        screen.blit(score_text, (10, 10)) 
        # Draw pipes as Sam images
        # Top Sam
        top_sam_scaled = pygame.transform.scale(sam_img, (PIPE_WIDTH, max(1, pipe_height)))
        screen.blit(top_sam_scaled, (pipe_x, 0))
        # Bottom Sam
        bottom_pipe_height = SCREEN_HEIGHT - pipe_height - PIPE_GAP
        if bottom_pipe_height > 0:
            bottom_sam_scaled = pygame.transform.scale(sam_img, (PIPE_WIDTH, bottom_pipe_height))
            screen.blit(bottom_sam_scaled, (pipe_x, pipe_height + PIPE_GAP))
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

