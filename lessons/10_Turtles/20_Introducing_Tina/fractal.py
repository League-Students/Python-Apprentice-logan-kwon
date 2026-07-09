import pygame
import random
import sys
import math

# 1. HARDWARE-RESILIENT CORE INITIALIZATION
pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass  # Safely bypass systems without active sound cards or audio drivers

# DESIGN RESOLUTION CONFIGURATION
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cosmic Vanguard: Galaxy Under Siege")
clock = pygame.time.Clock()

# ARGB PALETTE SCHEME
BLACK  = (8, 8, 16)
WHITE  = (240, 240, 255)
GREEN  = (40, 240, 120)
RED    = (255, 60, 90)
YELLOW = (255, 220, 0)
BLUE   = (0, 180, 255)
PURPLE = (160, 60, 255)
ORANGE = (255, 130, 40)
DARK_GRAY = (35, 35, 45)

# UNIVERSAL NATIVE ENGINE FONTS
ui_font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 64)

# ==========================================
# 2. GLOBAL SIMULATION STATES
# ==========================================
score = 0
lives = 3
game_stage = 1  # Increments as waves are cleared
game_over = False

# PLAYER PARAMETERS
player_w, player_h = 50, 45
player_x = SCREEN_WIDTH // 2 - player_w // 2
player_y = SCREEN_HEIGHT - 80
player_speed = 6
weapon_type = "SINGLE"  # Changes dynamically via item drops: SINGLE, DOUBLE, TRIPLE

# SHIELD SKILL SPECS
shield_active = False
shield_cooldown = 7000  # Milliseconds
shield_duration = 2500  
last_shield_time = -7000
shield_end_time = 0

# SIMULATION OBJECT LISTS
player_lasers = []
enemy_lasers = []
enemies = []
powerups = []
particles = []

# BACKGROUND AMBIENCE: Parallax Starfield Matrix
stars_layer_1 = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT)} for _ in range(40)]
stars_layer_2 = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT)} for _ in range(25)]

# WAVE MANAGEMENT
enemy_speed_x = 2
enemy_direction = 1
enemy_drop_y = 15

# BOSS MATRIX PARAMETERS
boss_active = False
boss_rect = None
boss_hp = 0
boss_max_hp = 80
boss_speed = 3
boss_dir = 1
boss_last_attack = 0
boss_attack_cooldown = 1100
boss_milestone = 600  # Spawn boss when reaching this score

# ==========================================
# 3. HELPER FUNCTIONS & SPAWNER ENGINES
# ==========================================
def spawn_particles(x, y, color, count=10):
    for _ in range(count):
        particles.append({
            "x": x, "y": y,
            "vx": random.uniform(-4, 4),
            "vy": random.uniform(-4, 4),
            "life": random.randint(15, 30),
            "color": color
        })

def spawn_wave():
    global enemy_speed_x
    enemies.clear()
    enemy_speed_x = 1.8 + (game_stage * 0.3)  # Scale speed slightly per wave level
    rows = 3
    cols = 9
    for row in range(rows):
        for col in range(cols):
            ex = 100 + col * 65
            ey = 80 + row * 52
            # Assign distinctive tactical types based on row numbers
            etype = "SCOUT" if row == 0 else ("FIGHTER" if row == 1 else "BOMBER")
            enemies.append({
                "rect": pygame.Rect(ex, ey, 44, 32),
                "type": etype,
                "hp": 1 if etype == "SCOUT" else (2 if etype == "FIGHTER" else 3)
            })

def spawn_boss_overlord():
    global boss_active, boss_rect, boss_hp, boss_max_hp
    boss_active = True
    boss_max_hp = 70 + (game_stage * 20)
    boss_hp = boss_max_hp
    boss_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, 70, 160, 100)
    enemies.clear()
    enemy_lasers.clear()

spawn_wave()

# ==========================================
# 4. MAIN FLUID ENGINE LOOP
# ==========================================
while True:
    # CRITICAL: Keep memory and cycles uniform with native monitor sync clocks
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    # SYSTEM RECEPTOR INTERACTION
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            # Weapon Trigger Event (SPACE)
            if event.key == pygame.K_SPACE and not game_over:
                mid_x = player_x + player_w // 2
                if weapon_type == "SINGLE":
                    player_lasers.append(pygame.Rect(mid_x - 3, player_y, 6, 16))
                elif weapon_type == "DOUBLE":
                    player_lasers.append(pygame.Rect(player_x + 4, player_y + 10, 6, 16))
                    player_lasers.append(pygame.Rect(player_x + player_w - 10, player_y + 10, 6, 16))
                elif weapon_type == "TRIPLE":
                    player_lasers.append(pygame.Rect(mid_x - 3, player_y, 6, 16))
                    # Storing custom trajectory speeds on specialized side lasers inside raw tuples
                    player_lasers.append({"rect": pygame.Rect(player_x, player_y + 12, 6, 16), "vx": -2})
                    player_lasers.append({"rect": pygame.Rect(player_x + player_w - 6, player_y + 12, 6, 16), "vx": 2})

            # Ability Trigger Event (S)
            if event.key == pygame.K_s and not game_over and not shield_active:
                if current_time - last_shield_time >= shield_cooldown:
                    shield_active = True
                    last_shield_time = current_time
                    shield_end_time = current_time + shield_duration

            # Reset Trigger Event (R)
            if event.key == pygame.K_r and game_over:
                score = 0
                lives = 3
                game_stage = 1
                game_over = False
                boss_active = False
                weapon_type = "SINGLE"
                enemies.clear()
                player_lasers.clear()
                enemy_lasers.clear()
                powerups.clear()
                particles.clear()
                player_x = SCREEN_WIDTH // 2 - player_w // 2
                boss_milestone = 600
                spawn_wave()

    # CORE TIMING CHECKS
    if shield_active and current_time >= shield_end_time:
        shield_active = False

    if not game_over:
        # CONTINUOUS CONTROLLER SAMPLING
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_w:
            player_x += player_speed

        # BACKGROUND SPACE SCROLL
        for star in stars_layer_1:
            star["y"] += 1
            if star["y"] > SCREEN_HEIGHT: star["y"], star["x"] = 0, random.randint(0, SCREEN_WIDTH)
        for star in stars_layer_2:
            star["y"] += 3
            if star["y"] > SCREEN_HEIGHT: star["y"], star["x"] = 0, random.randint(0, SCREEN_WIDTH)

        # UPDATE EXPLOSION PARTICLES
        for p in particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
            if p["life"] <= 0: particles.remove(p)

        # UPDATE DROP SUPPLIES
        for pu in powerups[:]:
            pu["rect"].y += 3
            if pu["rect"].colliderect(pygame.Rect(player_x, player_y, player_w, player_h)):
                weapon_type = pu["type"]
                score += 50
                spawn_particles(pu["rect"].centerx, pu["rect"].centery, GREEN, 15)
                powerups.remove(pu)
            elif pu["rect"].y > SCREEN_HEIGHT:
                powerups.remove(pu)

        # UPDATE FRIENDLY LASERS
        for l in player_lasers[:]:
            if isinstance(l, dict):
                l["rect"].x += l["vx"]
                l["rect"].y -= 8
                r = l["rect"]
                if r.y < 0 or r.x < 0 or r.x > SCREEN_WIDTH: player_lasers.remove(l)
            else:
                l.y -= 9
                if l.y < 0: player_lasers.remove(l)

        # UPDATE HOSTILE BULLETS
        for el in enemy_lasers[:]:
            el["rect"].x += el["vx"]
            el["rect"].y += el["vy"]
            r = el["rect"]
            
            if r.y > SCREEN_HEIGHT or r.x < 0 or r.x > SCREEN_WIDTH:
                enemy_lasers.remove(el)
                continue

            if r.colliderect(pygame.Rect(player_x, player_y, player_w, player_h)):
                enemy_lasers.remove(el)
                if not shield_active:
                    lives -= 1
                    spawn_particles(player_x + player_w//2, player_y + player_h//2, ORANGE, 20)
                    if lives <= 0: game_over = True

        # ==========================================
        # SCENARIO BRANCH A: ACTIVE BOSS FIGHT
        # ==========================================
        if boss_active:
            boss_rect.x += boss_speed * boss_dir
            if boss_rect.right >= SCREEN_WIDTH or boss_rect.left <= 0:
                boss_dir *= -1
                boss_rect.y += 8

            if boss_rect.bottom >= player_y:
                game_over = True

            # Boss Tactical Offense Patterns
            if current_time - boss_last_attack >= boss_attack_cooldown:
                boss_last_attack = current_time
                cx, cy = boss_rect.centerx, boss_rect.bottom
                
                # Dynamic targeted spread spray
                trajectories = [(-3, 5), (0, 6), (3, 5), (-1.5, 5.5), (1.5, 5.5)]
                for vx, vy in trajectories:
                    br = pygame.Rect(cx - 5, cy, 10, 20)
                    enemy_lasers.append({"rect": br, "vx": vx, "vy": vy, "color": RED})

            # Check Player Laser Hits onto Boss Armor
            for l in player_lasers[:]:
                r = l["rect"] if isinstance(l, dict) else l
                if r.colliderect(boss_rect):
                    if l in player_lasers: player_lasers.remove(l)
                    boss_hp -= 1
                    spawn_particles(r.centerx, r.centery, YELLOW, 3)
                    
                    if boss_hp <= 0:
                        spawn_particles(boss_rect.centerx, boss_rect.centery, RED, 50)
                        boss_active = False

