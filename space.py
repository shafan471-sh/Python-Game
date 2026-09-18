import pygame
import random

# ==========================================
# INITIALIZATION
# ==========================================

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
FPS = 60

# ==========================================
# COLORS
# ==========================================

BLACK = (5, 5, 20)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
PURPLE = (150, 50, 255)
YELLOW = (255, 230, 0)
BLUE = (50, 150, 255)

# ==========================================
# FONTS
# ==========================================

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 70)

# ==========================================
# PLAYER
# ==========================================

player_width = 50
player_height = 50

player_x = WIDTH // 2
player_y = HEIGHT - 80

player_speed = 6

# ==========================================
# BULLETS
# ==========================================

bullets = []

bullet_width = 6
bullet_height = 18
bullet_speed = 9

# ==========================================
# ENEMIES
# ==========================================

enemies = []

enemy_width = 45
enemy_height = 45
enemy_speed = 3

enemy_timer = 0

# ==========================================
# GAME VARIABLES
# ==========================================

score = 0
lives = 3
game_over = False

# ==========================================
# STARS
# ==========================================

stars = []

for i in range(100):

    star = {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed": random.randint(1, 4)
    }

    stars.append(star)


# ==========================================
# DRAW STARS
# ==========================================

def draw_stars():

    for star in stars:

        pygame.draw.circle(
            screen,
            WHITE,
            (star["x"], star["y"]),
            2
        )

        star["y"] += star["speed"]

        if star["y"] > HEIGHT:

            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)


# ==========================================
# DRAW PLAYER
# ==========================================

def draw_player():

    # Main spaceship

    pygame.draw.polygon(
        screen,
        PURPLE,
        [
            (player_x, player_y - 25),
            (player_x - 25, player_y + 25),
            (player_x, player_y + 10),
            (player_x + 25, player_y + 25)
        ]
    )

    # Cockpit

    pygame.draw.circle(
        screen,
        BLUE,
        (player_x, player_y),
        8
    )

    # Engine flame

    pygame.draw.polygon(
        screen,
        YELLOW,
        [
            (player_x - 8, player_y + 20),
            (player_x, player_y + 40),
            (player_x + 8, player_y + 20)
        ]
    )


# ==========================================
# CREATE ENEMY
# ==========================================

def create_enemy():

    enemy = pygame.Rect(
        random.randint(20, WIDTH - 65),
        -50,
        enemy_width,
        enemy_height
    )

    enemies.append(enemy)


# ==========================================
# DRAW ENEMY
# ==========================================

def draw_enemy(enemy):

    # Enemy body

    pygame.draw.polygon(
        screen,
        RED,
        [
            (enemy.centerx, enemy.bottom),
            (enemy.left, enemy.top),
            (enemy.right, enemy.top)
        ]
    )

    # Enemy eyes

    pygame.draw.circle(
        screen,
        WHITE,
        (enemy.centerx - 10, enemy.top + 15),
        4
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (enemy.centerx + 10, enemy.top + 15),
        4
    )


# ==========================================
# SHOOT BULLET
# ==========================================

def shoot():

    bullet = pygame.Rect(
        player_x - bullet_width // 2,
        player_y - 35,
        bullet_width,
        bullet_height
    )

    bullets.append(bullet)


# ==========================================
# RESET GAME
# ==========================================

def reset_game():

    global score
    global lives
    global game_over
    global player_x

    score = 0
    lives = 3
    game_over = False

    player_x = WIDTH // 2

    bullets.clear()
    enemies.clear()


# ==========================================
# MAIN GAME LOOP
# ==========================================

running = True

while running:

    clock.tick(FPS)

    # ======================================
    # EVENTS
    # ======================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # Shoot

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if not game_over:

                    shoot()

            # Restart

            if event.key == pygame.K_r:

                if game_over:

                    reset_game()

    # ======================================
    # GAME LOGIC
    # ======================================

    if not game_over:

        # ----------------------------------
        # PLAYER MOVEMENT
        # ----------------------------------

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:

            player_x -= player_speed

        if keys[pygame.K_RIGHT]:

            player_x += player_speed

        # Keep player inside screen

        if player_x < 30:

            player_x = 30

        if player_x > WIDTH - 30:

            player_x = WIDTH - 30

        # ----------------------------------
        # BULLET MOVEMENT
        # ----------------------------------

        for bullet in bullets[:]:

            bullet.y -= bullet_speed

            if bullet.bottom < 0:

                bullets.remove(bullet)

        # ----------------------------------
        # CREATE ENEMIES
        # ----------------------------------

        enemy_timer += 1

        if enemy_timer >= 35:

            create_enemy()

            enemy_timer = 0

        # ----------------------------------
        # ENEMY MOVEMENT
        # ----------------------------------

        for enemy in enemies[:]:

            enemy.y += enemy_speed

            # Enemy reaches bottom

            if enemy.top > HEIGHT:

                enemies.remove(enemy)

                lives -= 1

                if lives <= 0:

                    game_over = True

        # ----------------------------------
        # BULLET COLLISION
        # ----------------------------------

        for bullet in bullets[:]:

            for enemy in enemies[:]:

                if bullet.colliderect(enemy):

                    if bullet in bullets:

                        bullets.remove(bullet)

                    if enemy in enemies:

                        enemies.remove(enemy)

                    score += 10

                    break

    # ======================================
    # DRAW BACKGROUND
    # ======================================

    screen.fill(BLACK)

    draw_stars()

    # ======================================
    # DRAW BULLETS
    # ======================================

    for bullet in bullets:

        pygame.draw.rect(
            screen,
            YELLOW,
            bullet
        )

    # ======================================
    # DRAW ENEMIES
    # ======================================

    for enemy in enemies:

        draw_enemy(enemy)

    # ======================================
    # DRAW PLAYER
    # ======================================

    if not game_over:

        draw_player()

    # ======================================
    # SCORE
    # ======================================

    score_text = font.render(
        "Score: " + str(score),
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    # ======================================
    # LIVES
    # ======================================

    lives_text = font.render(
        "Lives: " + str(lives),
        True,
        WHITE
    )

    screen.blit(
        lives_text,
        (680, 20)
    )

    # ======================================
    # GAME OVER SCREEN
    # ======================================

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(180)
        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 -
                game_over_text.get_width() // 2,
                220
            )
        )

        final_score = font.render(
            "Final Score: " + str(score),
            True,
            WHITE
        )

        screen.blit(
            final_score,
            (
                WIDTH // 2 -
                final_score.get_width() // 2,
                310
            )
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            YELLOW
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 -
                restart_text.get_width() // 2,
                360
            )
        )

    # ======================================
    # UPDATE SCREEN
    # ======================================

    pygame.display.flip()


# ==========================================
# QUIT
# ==========================================

pygame.quit()