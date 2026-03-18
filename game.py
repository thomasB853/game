import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Web-friendly settings (Pygbag)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Web Shooter Game")

# Clock for frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5
player_health = 3

# Bullet settings
bullet_size = (10, 5)
bullet_speed = 8
bullets = []

# Enemy settings
enemy_size = 40
enemy_speed = 2
enemies = []
enemy_spawn_rate = 60  # Spawn 1 enemy every 60 frames

# Score
score = 0
font = pygame.font.Font(None, 40)

# Game states
game_over = False
game_running = True

# Player movement function
def move_player(keys):
    global player_x, player_y
    if keys[K_a] or keys[K_LEFT]:
        player_x -= player_speed
    if keys[K_d] or keys[K_RIGHT]:
        player_x += player_speed
    if keys[K_w] or keys[K_UP]:
        player_y -= player_speed
    if keys[K_s] or keys[K_DOWN]:
        player_y += player_speed

    # Keep player on screen
    player_x = max(0, min(player_x, WIDTH - player_size))
    player_y = max(0, min(player_y, HEIGHT - player_size))

# Spawn enemy function
def spawn_enemy():
    # Spawn from top/bottom/left/right
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WIDTH - enemy_size)
        y = -enemy_size
    elif side == "bottom":
        x = random.randint(0, WIDTH - enemy_size)
        y = HEIGHT
    elif side == "left":
        x = -enemy_size
        y = random.randint(0, HEIGHT - enemy_size)
    else:  # right
        x = WIDTH
        y = random.randint(0, HEIGHT - enemy_size)
    enemies.append([x, y])

# Shoot bullet function
def shoot_bullet(mouse_pos):
    # Calculate bullet direction (from player to mouse)
    player_center_x = player_x + player_size // 2
    player_center_y = player_y + player_size // 2
    
    dx = mouse_pos[0] - player_center_x
    dy = mouse_pos[1] - player_center_y
    distance = (dx**2 + dy**2)**0.5
    
    if distance > 0:
        dx /= distance
        dy /= distance
        bullets.append([
            player_center_x - bullet_size[0]//2,
            player_center_y - bullet_size[1]//2,
            dx * bullet_speed,
            dy * bullet_speed
        ])

# Collision detection
def check_collision(rect1, rect2):
    return (
        rect1[0] < rect2[0] + rect2[2] and
        rect1[0] + rect1[2] > rect2[0] and
        rect1[1] < rect2[1] + rect2[3] and
        rect1[1] + rect1[3] > rect2[1]
    )

# Main game loop
def main_game_loop():
    global player_x, player_y, bullets, enemies, score, game_over, game_running
    frame_count = 0

    while game_running and not game_over:
        screen.fill(BLACK)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE):
                if not game_over:
                    shoot_bullet(pygame.mouse.get_pos())
            if event.type == KEYDOWN and event.key == K_r and game_over:
                # Reset game
                player_x = WIDTH // 2 - player_size // 2
                player_y = HEIGHT // 2 - player_size // 2
                bullets = []
                enemies = []
                score = 0
                player_health = 3
                game_over = False

        # Spawn enemies
        frame_count += 1
        if frame_count % enemy_spawn_rate == 0 and not game_over:
            spawn_enemy()
            # Make game harder over time (reduce spawn rate)
            if enemy_spawn_rate > 20:
                enemy_spawn_rate -= 1

        # Player movement
        keys = pygame.key.get_pressed()
        if not game_over:
            move_player(keys)

        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

        # Update and draw bullets
        new_bullets = []
        for bullet in bullets:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            # Keep bullet if it's on screen
            if 0 < bullet[0] < WIDTH and 0 < bullet[1] < HEIGHT:
                pygame.draw.rect(screen, GREEN, (bullet[0], bullet[1], bullet_size[0], bullet_size[1]))
                new_bullets.append(bullet)
        bullets = new_bullets

        # Update and draw enemies
        new_enemies = []
        player_rect = (player_x, player_y, player_size, player_size)
        
        for enemy in enemies:
            # Move enemy toward player
            dx = player_x + player_size//2 - (enemy[0] + enemy_size//2)
            dy = player_y + player_size//2 - (enemy[1] + enemy_size//2)
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 0:
                dx /= distance
                dy /= distance
                enemy[0] += dx * enemy_speed
                enemy[1] += dy * enemy_speed

            # Check enemy-player collision
            enemy_rect = (enemy[0], enemy[1], enemy_size, enemy_size)
            if check_collision(player_rect, enemy_rect) and not game_over:
                player_health -= 1
                if player_health <= 0:
                    game_over = True
            else:
                # Check bullet-enemy collision
                hit = False
                for bullet in bullets[:]:
                    bullet_rect = (bullet[0], bullet[1], bullet_size[0], bullet_size[1])
                    if check_collision(bullet_rect, enemy_rect):
                        bullets.remove(bullet)
                        score += 10
                        hit = True
                        break
                if not hit:
                    pygame.draw.rect(screen, RED, enemy_rect)
                    new_enemies.append(enemy)
        
        enemies = new_enemies

        # Draw UI
        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Health
        health_text = font.render(f"Health: {player_health}", True, WHITE)
        screen.blit(health_text, (WIDTH - 150, 10))

        # Game over screen
        if game_over:
            game_over_text = font.render("GAME OVER!", True, RED)
            restart_text = font.render("Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
            screen.blit(restart_text, (WIDTH//2 - 120, HEIGHT//2 + 10))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main_game_loop()