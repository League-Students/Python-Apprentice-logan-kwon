import pygame
import random
import sys
import math

# 1. INITIALIZE GAME AND WINDOW
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders: Elite Edition")
clock = pygame.time.Clock()

# COLORS
BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 191, 255)
PURPLE = (180, 50, 255)
DARK_GRAY = (40, 40, 40)

# 2. GAME VARIABLES
score = 0
lives = 3
game_over = False
font = pygame.font.SysFont("Arial", 22, bold=True)
large_font = pygame.font.SysFont("Arial", 72, bold=True)

# PLAYER PROPERTIES
player_width = 50
player_height = 40
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - 60
player_speed = 6

# SHIELD ABILITY PROPERTIES
shield_active = False
shield_duration = 3000  
shield_cooldown = 8000  
last_shield_time = -8000  
shield_end_time = 0

# LASER CONTAINERS
player_lasers = []
enemy_lasers = []

# NORMAL ENEMY PROPERTIES
enemy_width = 44
enemy_height = 32
enemy_speed_x = 2
enemy_speed_y = 20
enemy_direction = 1
enemies = []
enemy_shoot_chance = 0.005  # Chance per frame for EACH alien to shoot

# BOSS PROPERTIES
boss_active = False
boss_width = 140
boss_height = 140
boss_rect = None
boss_hp = 0
boss_max_hp = 60
boss_speed = 3
boss_direction = 1
boss_score_milestone = 400
boss_shoot_cooldown = 1200  # Shoots every 1.2 seconds
last_boss_shoot_time = 0

# SPAWN NORMAL ENEMIES
def spawn_enemies():
    enemies.clear()
    for row in range(3):
        for col in range(9):
            x = 100 + col * 65
            y = 70 + row * 50
            enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

# SPAWN BOSS
def spawn_boss():
    global boss_active, boss_rect, boss_hp
    boss_active = True
    boss_hp = boss_max_hp
    boss_rect = pygame.Rect(SCREEN_WIDTH // 2 - boss_width // 2, 60, boss_width, boss_height)
    enemies.clear()
    enemy_lasers.clear()

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
            if event.key == pygame.K_SPACE and not game_over:
                # Fire Player Laser
                p_laser = pygame.Rect(player_x + player_width // 2 - 3, player_y, 6, 15)
                player_lasers.append(p_laser)
            
            if event.key == pygame.K_s and not game_over and not shield_active:
                if current_time - last_shield_time >= shield_cooldown:
                    shield_active = True
                    last_shield_time = current_time
                    shield_end_time = current_time + shield_duration
            
            if event.key == pygame.K_r and game_over:
                # Reset Everything
                score = 0
                lives = 3
                game_over = False
                boss_active = False
                enemies.clear()
                player_lasers.clear()
                enemy_lasers.clear()
                player_x = SCREEN_WIDTH // 2 - player_width // 2
                boss_score_milestone = 400
                spawn_enemies()

    # SHIELD TIMER CHECK
    if shield_active and current_time >= shield_end_time:
        shield_active = False

    if not game_over:
        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # MOVE PLAYER LASERS
        for laser in player_lasers[:]:
            laser.y -= 9
            if laser.y < 0:
                player_lasers.remove(laser)

        # MOVE ENEMY LASERS
        for laser in enemy_lasers[:]:
            if hasattr(laser, 'vx'):
                laser.x += laser.vx
            laser.y += laser.vy if hasattr(laser, 'vy') else 5
            
            if laser.y > SCREEN_HEIGHT or laser.x < 0 or laser.x > SCREEN_WIDTH:
                if laser in enemy_lasers: enemy_lasers.remove(laser)
                continue

            # Player Hit Check
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            if laser.colliderect(player_rect):
                if laser in enemy_lasers: enemy_lasers.remove(laser)
                if not shield_active:
                    lives -= 1
                    if lives <= 0:
                        game_over = True

        # BOSS GAMEPLAY LOGIC
        if boss_active:
            boss_rect.x += boss_speed * boss_direction
            if boss_rect.right >= SCREEN_WIDTH or boss_rect.left <= 0:
                boss_direction *= -1

            # Boss Attacks
            if current_time - last_boss_shoot_time >= boss_shoot_cooldown:
                last_boss_shoot_time = current_time
                bx = boss_rect.centerx
                by = boss_rect.centery
                angles = [-1.5, 0, 1.5]
                for angle in angles:
                    b_laser = pygame.Rect(bx - 4, by + 40, 8, 18)
                    b_laser.vx = angle * 2
                    b_laser.vy = 6
                    enemy_lasers.append(b_laser)

            # Player Laser vs Boss HP
            for laser in player_lasers[:]:
                if laser.colliderect(boss_rect):
                    player_lasers.remove(laser)
                    boss_hp -= 1
                    score += 5
                    if boss_hp <= 0:
                        boss_active = False
                        score += 300
                        boss_max_hp += 20
                        spawn_enemies()
                        break

        # NORMAL ENEMY GAMEPLAY LOGIC
        else:
            move_down = False
            for enemy in enemies:
                enemy.x += enemy_speed_x * enemy_direction
                if enemy.right >= SCREEN_WIDTH or enemy.left <= 0:
                    move_down = True
                
                # Random shooting
                if random.random() < enemy_shoot_chance:
                    el = pygame.Rect(enemy.centerx - 3, enemy.bottom, 6, 14)
                    el.vy = 5
                    enemy_lasers.append(el)

            if move_down:
                enemy_direction *= -1
                for enemy in enemies:
                    enemy.y += enemy_speed_y
                    if enemy.bottom >= player_y:
                        if shield_active:
                            enemies.remove(enemy)
                        else:
                            game_over = True

            # Player Laser vs Regular Enemy
            for laser in player_lasers[:]:
                for enemy in enemies[:]:
                    if laser.colliderect(enemy):
                        if laser in player_lasers: player_lasers.remove(laser)
                        if enemy in enemies: enemies.remove(enemy)
                        score += 10
                        break

            # Win Wave Logic
            if len(enemies) == 0:
                if score >= boss_score_milestone:
                    spawn_boss()
                    boss_score_milestone += 600
                else:
                    spawn_enemies()
                    enemy_speed_x += 0.4

    # 4. DRAW GRAPHICS
    screen.fill(BLACK)

    if not game_over:
        # Draw Upgraded Player Ship
        pygame.draw.polygon(screen, GREEN, [
            (player_x + player_width // 2, player_y), 
            (player_x, player_y + player_height), 
            (player_x + player_width, player_y + player_height)
        ])
        pygame.draw.rect(screen, BLUE, (player_x + 12, player_y + 15, 26, 12))  # Cockpit Window
        
        # Shield Bubble Visual
        if shield_active:
            pygame.draw.circle(screen, BLUE, (player_x + player_width // 2, player_y + player_height // 2), 48, 3)

        # Draw Player Lasers
        for laser in player_lasers:
            pygame.draw.rect(screen, GREEN, laser)

        # Draw Enemy Lasers
        for laser in enemy_lasers:
            color = RED if hasattr(laser, 'vx') else PURPLE
            pygame.draw.rect(screen, color, laser)

        # Draw Detailed Regular Alien Ships
        for enemy in enemies:
            pygame.draw.rect(screen, PURPLE, (enemy.x + 8, enemy.y, 28, enemy.height), border_radius=4)
            pygame.draw.polygon(screen, BLUE, [(enemy.x, enemy.y + 10), (enemy.x + 8, enemy.y), (enemy.x + 8, enemy.y + 25)])
            pygame.draw.polygon(screen, BLUE, [(enemy.right, enemy.y + 10), (enemy.right - 8, enemy.y), (enemy.right - 8, enemy.y + 25)])
            pygame.draw.circle(screen, YELLOW, (enemy.x + 16, enemy.y + 12), 3)
            pygame.draw.circle(screen, YELLOW, (enemy.x + 28, enemy.y + 12), 3)

        # Draw Unique Boss Shape: Mechanical Multi-Armed Ring
        if boss_active:
            bx, by = boss_rect.centerx, boss_rect.centery
            pygame.draw.circle(screen, YELLOW, (bx, by), 30)
            pygame.draw.circle(screen, RED, (bx, by), 55, 12)
            pygame.draw.rect(screen, DARK_GRAY, (boss_rect.x, boss_rect.y, 25, 25))
            pygame.draw.rect(screen, DARK_GRAY, (boss_rect.right - 25, boss_rect.y, 25, 25))
            pygame.draw.rect(screen, DARK_GRAY, (boss_rect.x, boss_rect.bottom - 25, 25, 25))
            pygame.draw.rect(screen, DARK_GRAY, (boss_rect.right - 25, boss_rect.bottom - 25, 25, 25))
            
            # Boss Health UI Bar
            pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH // 2 - 150, 15, 300, 18))
            hp_width = int(300 * (boss_hp / boss_max_hp))
            pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 150, 15, hp_width, 18))

        # DRAW STATS HUD
        score_txt = font.render(f"SCORE: {score}", True, WHITE)