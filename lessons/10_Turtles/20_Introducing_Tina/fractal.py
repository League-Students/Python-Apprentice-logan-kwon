import pygame
import random
import sys

# 1. INITIALIZE WINDOW FIRST
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

# 2. SAFE FONT LOADING (Uses Pygame's native internal font asset)
font = pygame.font.Font(None, 28)
large_font = pygame.font.Font(None, 74)

# GAME STATE VARIABLES
score = 0
lives = 3
game_over = False

# PLAYER PROPERTIES
player_width = 50
player_height = 40
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - 70
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
enemy_shoot_chance = 0.008  

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
boss_shoot_cooldown = 1200  
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
                p_laser = pygame.Rect(player_x + player_width // 2 - 3, player_y, 6, 15)
                player_lasers.append(p_laser)
            
            if event.key == pygame.K_s and not game_over and not shield_active:
                if current_time - last_shield_time >= shield_cooldown:
                    shield_active = True
                    last_shield_time = current_time
                    shield_end_time = current_time + shield_duration
            
            if event.key == pygame.K_r and game_over:
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
        for laser_data in enemy_lasers[:]:
            laser_rect = laser_data["rect"]
            laser_rect.x += laser_data["vx"]
            laser_rect.y += laser_data["vy"]
            
            if laser_rect.y > SCREEN_HEIGHT or laser_rect.x < 0 or laser_rect.x > SCREEN_WIDTH:
                if laser_data in enemy_lasers: enemy_lasers.remove(laser_data)
                continue

            # Player Hit Detection
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            if laser_rect.colliderect(player_rect):
                if laser_data in enemy_lasers: enemy_lasers.remove(laser_data)
                if not shield_active:
                    lives -= 1
                    if lives <= 0:
                        game_over = True

        # BOSS GAMEPLAY LOGIC
        if boss_active:
            boss_rect.x += boss_speed * boss_direction
            if boss_rect.right >= SCREEN_WIDTH or boss_rect.left <= 0:
                boss_direction *= -1

            if current_time - last_boss_shoot_time >= boss_shoot_cooldown:
                last_boss_shoot_time = current_time
                bx = boss_rect.centerx
                by = boss_rect.centery
                angles = [-3, 0, 3] 
                for vx_val in angles:
                    b_rect = pygame.Rect(bx - 4, by + 40, 8, 18)
                    enemy_lasers.append({"rect": b_rect, "vx": vx_val, "vy": 6, "is_boss": True})

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
                        
            if boss_rect.bottom >= player_y:
                game_over = True

        # NORMAL ENEMY GAMEPLAY LOGIC
        else:
            move_down = False
            for enemy in enemies:
                enemy.x += enemy_speed_x * enemy_direction
                if enemy.right >= SCREEN_WIDTH or enemy.left <= 0:
                    move_down = True
                
                if random.random() < enemy_shoot_chance:
                    el_rect = pygame.Rect(enemy.centerx - 3, enemy.bottom, 6, 14)
                    enemy_lasers.append({"rect": el_rect, "vx": 0, "vy": 5, "is_boss": False})

            if move_down:
                enemy_direction *= -1
                for enemy in enemies:
                    enemy.y += enemy_speed_y
                    if enemy.bottom >= player_y:
                        if shield_active:
                            enemies.remove(enemy)
                        else:
                            game_over = True

            for laser in player_lasers[:]:
                for enemy in enemies[:]:
                    if laser.colliderect(enemy):
                        if laser in player_lasers: player_lasers.remove(laser)
                        if enemy in enemies: enemies.remove(enemy)
                        score += 10
                        break

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
        # Draw Player Ship
        pygame.draw.polygon(screen, GREEN, [
            (player_x + player_width // 2, player_y), 
            (player_x, player_y + player_height), 
            (player_x + player_width, player_y + player_height)
        ])
        pygame.draw.rect(screen, BLUE, (player_x + 12, player_y + 15, 26, 12))  
        
        if shield_active:
            pygame.draw.circle(screen, BLUE, (player_x + player_width // 2, player_y + player_height // 2), 48, 3)

        for laser in player_lasers:
            pygame.draw.rect(screen, GREEN, laser)

        for laser_data in enemy_lasers:
            color = RED if laser_data["is_boss"] else PURPLE
            pygame.draw.rect(screen, color, laser_data["rect"])

        # Draw Aliens
        for enemy in enemies:
            pygame.draw.rect(screen, PURPLE, (enemy.x + 8, enemy.y, 28, enemy.height), border_radius=4)
            pygame.draw.polygon(screen, BLUE, [(enemy.x, enemy.y + 10), (enemy.x + 8, enemy.y), (enemy.x + 8, enemy.y + 25)])
            pygame.draw.polygon(screen, BLUE, [(enemy.right, enemy.y + 10), (enemy.right - 8, enemy.y), (enemy.right - 8, enemy.y + 25)])
            pygame.draw.circle(screen, YELLOW, (enemy.x + 16, enemy.y + 12), 3)
            pygame.draw.circle(screen, YELLOW, (enemy.x + 28, enemy.y + 12), 3)

        # Draw Boss
        if boss_active:
            bx, by = boss_rect.centerx, boss_rect.centery
            pygame.draw.circle(screen, YELLOW, (bx, by), 30)
            pygame.draw.circle(screen, RED, (bx, by), 55, 12)
            pygame.draw.rect(screen, DARK_GRAY, (boss_rect.x, boss_rect.y, 25, 25))
            pygame.draw.rect(screen, DARK_GRAY, (boss_rect.right - 25, boss_rect.y, 25, 25))
            pygame.draw.rect(screen, DARK_GRAY, (boss_rect.x, boss_rect.bottom - 25, 25, 25))
            pygame.draw.rect(screen, DARK_GRAY, (boss_rect.right - 25, boss_rect.bottom - 25, 25, 25))
            
            pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH // 2 - 150, 15, 300, 18))
            hp_width = int(max(0, 300 * (boss_hp / boss_max_hp)))
            pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 150, 15, hp_width, 18))

        # DRAW STATS HUD
        score_txt = font.render(f"SCORE: {score}", True, WHITE)
        lives_txt = font.render(f"LIVES: {lives}", True, RED)
        screen.blit(score_txt, (15, 15))
        screen.blit(lives_txt, (15, 45))

        cooldown = max(0, shield_cooldown - (current_time - last_shield_time))
        if shield_active:
            sh_txt = font.render("SHIELD: UNSTOPPABLE", True, BLUE)
        elif cooldown == 0: