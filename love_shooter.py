import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star-Heart Shooter 💘")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("Consolas", 16, bold=True)  # monospace for star hearts
big_font = pygame.font.SysFont("Arial", 60, bold=True)
score_font = pygame.font.SysFont("Arial", 30)

# Clock
clock = pygame.time.Clock()

# ASCII Heart made with stars (*)
HEART_PATTERN = [
    " **   ** ",
    "**** ****",
    "*********",
    " ******* ",
    "  *****  ",
    "   ***   ",
    "    *    "
]

def draw_star_heart(x, y):
    """Draws a star-heart at (x, y) using text lines"""
    for i, line in enumerate(HEART_PATTERN):
        text = font.render(line, True, RED)
        screen.blit(text, (x, y + i * 12))  # 12px line spacing


def game_loop():
    global screen
    # Player setup
    player_width, player_height = 40, 20
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 50
    player_speed = 7

    # Bullets
    bullets = []
    bullet_speed = 8

    # Hearts
    hearts = []
    for _ in range(5):
        x = random.randint(50, WIDTH - 100)
        y = random.randint(-200, -40)
        hearts.append(pygame.Rect(x, y, 80, 80))  # bigger area for ASCII heart

    # Score
    score = 0
    running = True

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:  # limit bullets
                bullets.append(pygame.Rect(player_x + player_width // 2 - 2, player_y, 4, 10))

        # Difficulty: hearts get faster as score increases
        heart_speed = 3 + (score // 5)

        # Update bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Update hearts
        for heart in hearts[:]:
            heart.y += heart_speed
            if heart.y > HEIGHT:  # Game Over condition
                return score  # exit loop, return final score

        # Collision detection
        for bullet in bullets[:]:
            for heart in hearts[:]:
                if bullet.colliderect(heart):
                    bullets.remove(bullet)
                    hearts.remove(heart)
                    score += 1
                    x = random.randint(50, WIDTH - 100)
                    y = random.randint(-200, -40)
                    hearts.append(pygame.Rect(x, y, 80, 80))
                    break

        # Draw player (triangle shooter)
        pygame.draw.polygon(screen, YELLOW, [(player_x, player_y + player_height),
                                             (player_x + player_width, player_y + player_height),
                                             (player_x + player_width // 2, player_y)])

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Draw hearts (ASCII star hearts)
        for heart in hearts:
            draw_star_heart(heart.x, heart.y)

        # Draw score
        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(final_score):
    global screen
    screen.fill(BLACK)

    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = score_font.render(f"Final Score: {final_score}", True, WHITE)
    restart_text = score_font.render("Press ENTER to Restart or ESC to Quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # restart
                    waiting = False
                if event.key == pygame.K_ESCAPE:  # quit
                    pygame.quit()
                    sys.exit()


# Main loop
while True:
    final_score = game_loop()
    game_over_screen(final_score)
