import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooter Game")

#sound
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")
lose_point_sound = pygame.mixer.Sound("sounds/lose_point.wav")

#images
player_img = pygame.image.load("images/player.png").convert_alpha()
enemy_img = pygame.image.load("images/enemy.png").convert_alpha()

# Set the frame rate
clock = pygame.time.Clock()
clock_value = 60

# Fonts
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Player settings
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5
player_health = 3

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemies = []
enemy_timer = 0
enemy_spawn_time = 2000

# Game state
score = 0
game_over = False

# Collision detection function
def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                shoot_sound.play()
                bullets.append([bullet_x, bullet_y])

    if not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Update bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed
        bullets = [bullet for bullet in bullets if bullet[1] > 0]

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - enemy_timer > enemy_spawn_time:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = -enemy_height
            enemies.append([enemy_x, enemy_y])
            enemy_timer = current_time

        # Move enemies
        for enemy in enemies:
            enemy[1] += enemy_speed

        # Collision detection
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if check_collision((bullet[0], bullet[1], bullet_width, bullet_height),
                                   (enemy[0], enemy[1], enemy_width, enemy_height)):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    if score % 5 == 0:
                        enemy_speed += 1
                        player_speed += 1
                    explosion_sound.play()

                    break

        # Check if any enemies reached bottom
        for enemy in enemies[:]:
            if enemy[1] > screen_height:
                enemies.remove(enemy)
                player_health -= 1
                lose_point_sound.play()
                if player_health <= 0:
                    game_over_sound.play()
                    game_over = True

    # Drawing
    screen.fill((0, 0, 0))

    if game_over:
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2,
                                     screen_height // 2 - game_over_text.get_height() // 2))
    else:
        # pygame.draw.rect(screen, (0, 128, 255), (player_x, player_y, player_width, player_height))
        
        # Draw player
        screen.blit(player_img, (player_x, player_y))

        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], bullet_width, bullet_height))

        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))

            # pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], enemy_width, enemy_height))

        # Draw score and health
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        health_text = font.render(f"Health: {player_health}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))

    pygame.display.flip()
    clock.tick(clock_value)
