import pygame
import random
import sys

# 1. INITIALIZE GAME AND WINDOW
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders: Boss & Abilities Edition")
clock = pygame.time.Clock()

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 191, 255)
DARK_GRAY = (50, 50, 50)

# 2. GAME VARIABLES
score = 0
game_over = False
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 72)

# PLAYER PROPERTIES
player_width = 50
player_height = 40
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - 60
player_speed = 6

# SHIELD ABILITY PROPERTIES
shield_active = False
shield_duration = 3000  # 3 seconds active (in milliseconds)
shield_cooldown = 10000  # 10 second cooldown
last_shield_time = -10000  # Allows immediate use at start
shield_end_time = 0

# LASER PROPERTIES
laser_width = 5
laser_height = 15
laser_speed = -10
lasers = []

# NORMAL ENEMY PROPERTIES
enemy_width = 40
enemy_height = 30
enemy_speed_x = 2
enemy_speed_y = 25
enemy_direction = 1
enemies = []

# BOSS PROPERTIES
boss_active = False
boss_width = 120
boss_height = 60
boss_rect = None
boss_hp = 0
boss_max_hp = 50
boss_speed = 4
boss_direction = 1
boss_score_milestone = 500  # Spawns every 500 points

# SPAWN NORMAL ENEMIES
def spawn_enemies():
    for row in range(4):
        for col in range(10):
            x = 80 + col * 60
            y = 60 + row * 45
            enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

# SPAWN BOSS
def spawn_boss():
    global boss_active, boss_rect, boss_hp
    boss_active = True
    boss_hp = boss_max_hp
    boss_rect = pygame.Rect(SCREEN_WIDTH // 2 - boss_width // 2, 50, boss_width, boss_height)
    enemies.clear()  # Clear tiny enemies for the boss duel

spawn_enemies()

# 3. MAIN GAME LOOP
while True:
    current_time = pygame.time.get_ticks()

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            # Fire Laser (SPACEBAR)
            if event.key == pygame.K_SPACE and not game_over:
                laser = pygame.Rect(player_x + player_width // 2 - laser_width // 2, player_y, laser_width, laser_height)
                lasers.append(laser)
            
            # Activate Shield (S KEY)
            if event.key == pygame.K_s and not game_over and not shield_active:
                if current_time - last_shield_time >= shield_cooldown:
                    shield_active = True
                    last_shield_time = current_time
                    shield_end_time = current_time + shield_duration
            
            # Restart Game (R KEY)
            if event.key == pygame.K_r and game_over:
                score = 0
                game_over = False
                boss_active = False
                enemies.clear()
                lasers.clear()
                player_x = SCREEN_WIDTH // 2 - player_width // 2
                spawn_enemies()

    # CHECK SHIELD EXPIRATION
    if shield_active and current_time >= shield_end_time:
        shield_active = False

    if not game_over:
        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # MOVE LASERS
        for laser in lasers[:]:
            laser.y += laser_speed
            if laser.y < 0:
                lasers.remove(laser)

        # BOSS GAMEPLAY LOGIC
        if boss_active:
            boss_rect.x += boss_speed * boss_direction
            if boss_rect.right >= SCREEN_WIDTH or boss_rect.left <= 0:
                boss_direction *= -1
                boss_rect.y += 15  # Slowly creeps downward
            
            # Boss crush condition
            if boss_rect.bottom >= player_y:
                if shield_active:
                    boss_direction *= -1
                    boss_rect.y -= 40  # Push boss back
                else:
                    game_over = True

            # Laser vs Boss Collision
            for laser in lasers[:]:
                if laser.colliderect(boss_rect):
                    lasers.remove(laser)
                    boss_hp -= 1
                    score += 5  # Score per hit
                    
                    if boss_hp <= 0:
                        boss_active = False
                        score += 200  # Bonus for defeating boss
                        boss_max_hp += 15  # Scale difficulty for next boss
                        spawn_enemies()
                        break

        # REGULAR ENEMY GAMEPLAY LOGIC
        else:
            move_down = False
            for enemy in enemies:
                enemy.x += enemy_speed_x * enemy_direction
                if enemy.right >= SCREEN_WIDTH or enemy.left <= 0:
                    move_down = True

            if move_down:
                enemy_direction *= -1
                for enemy in enemies:
                    enemy.y += enemy_speed_y
                    if enemy.bottom >= player_y:
                        if shield_active:
                            enemies.remove(enemy)  # Shield vaporizes normal enemies
                        else:
                            game_over = True

            # Laser vs Regular Enemy Collision
            for laser in lasers[:]:
                for enemy in enemies[:]:
                    if laser.colliderect(enemy):
                        if laser in lasers: lasers.remove(laser)
                        if enemy in enemies: enemies.remove(enemy)
                        score += 10
                        break

            # Win standard wave -> Check if time for Boss, else spawn next wave
            if len(enemies) == 0:
                if score >= boss_score_milestone:
                    spawn_boss()
                    boss_score_milestone += 700  # Setup next milestone
                else:
                    spawn_enemies()
                    enemy_speed_x += 0.5

    # 4. DRAW GRAPHICS
    screen.fill(BLACK)

    if not game_over:
        # Draw Player Ship
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))
        pygame.draw.rect(screen, GREEN, (player_x + 15, player_y - 10, 20, 10))
        
        # Draw Shield Visual Indicator
        if shield_active:
            pygame.draw.circle(screen, BLUE, (player_x + player_width // 2, player_y + player_height // 2), 45, 3)

        # Draw Lasers
        for laser in lasers:
            pygame.draw.rect(screen, YELLOW, laser)

        # Draw Regular Enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Draw Boss and Boss Health Bar
        if boss_active:
            pygame.draw.rect(screen, RED, boss_rect)
            # Health Bar background
            pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH // 2 - 150, 15, 300, 20))
            # Dynamic green health bar matching boss remaining hp ratio
            hp_bar_width = int(300 * (boss_hp / boss_max_hp))
            pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 150, 15, hp_bar_width, 20))
            boss_lbl = font.render("BOSS", True, WHITE)
            screen.blit(boss_lbl, (SCREEN_WIDTH // 2 - 25, 12))

        # DRAW STATS UI
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Shield Status indicator text
        cooldown_remaining = max(0, shield_cooldown - (current_time - last_shield_time))
        if shield_active:
            shield_text = font.render("SHIELD: ACTIVE!", True, BLUE)
        elif cooldown_remaining == 0:
            shield_text = font.render("SHIELD: READY (Press S)", True, GREEN)
        else:
            shield_text = font.render(f"SHIELD COOLDOWN: {cooldown_remaining // 1000 + 1}s", True, RED)
        screen.blit(shield_text, (SCREEN_WIDTH - 280, 10))

    else:
        # Draw Game Over Screen
        go_text = large_font.render("GAME OVER", True, RED)
        restart_text = font.render("Press 'R' to Restart", True, WHITE)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        
        screen.blit(go_text, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 80))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 10))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)