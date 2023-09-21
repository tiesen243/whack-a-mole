# Importing modules
import pygame
import random

from pygame import display, event, sprite
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, USEREVENT

from enermy import Enermy
from attacker import Attacker
from utils import drawMatrix, mode, draw_text


# Initialize pygame
pygame.init()
screen = display.set_mode((1000, 1000))
display.set_caption("Whack-a-mole")
display.set_icon(pygame.image.load("../assets/imgs/logo.png"))

# Set up background
BG = pygame.transform.scale(
    pygame.image.load("../assets/imgs/bg.png").convert_alpha(), (1000, 1000)
)

# Set up background music
bgm = pygame.mixer.Sound("../assets/sounds/UsagiFlap.mp3")
bgm.set_volume(0.1)
bgm.play()
hitSfx = pygame.mixer.Sound("../assets/sounds/bonk.mp3")
missSfx = pygame.mixer.Sound("../assets/sounds/miss.mp3")


# Create a matrix of enermy position (3x3 for normal mode, 6x6 for hard mode)
robo_list_rect = []

# Attacker group
attacker = Attacker()
atk_group = sprite.Group()
atk_group.add(attacker)

# Enermy Group
enermy_group = sprite.Group()


# Set up game variables
score = 0
heart = 4
bomb = 4
hitung = 5
isBomb = False
lastUpdate = pygame.time.get_ticks()
current_mode = mode["NORMAL"]
clock = pygame.time.Clock()

# Generate enermy
delay = 4000
rand = 4
time = -500
pygame.time.set_timer(USEREVENT + 1, delay)


def Generate_Enermy():
    amount = 1 if current_mode == mode["NORMAL"] else random.randint(2, rand)
    enermy_group.empty()
    for _ in range(amount):
        enermy = Enermy()
        enermy_group.add(enermy)
        enermy_group.update(robo_list_rect)


# Main loop
isRunning = True
while isRunning:
    e = event.poll()
    isGameOver = True if heart == 0 else False

    # Foreach 10s, decrease delay by 0.5s (hard) or 0.1s (normal) and increase rand by 1 (hard only)
    time += 1
    if time % 1000 == 0 and time != 0 and delay >= 500:
        delay -= 100 if current_mode == mode["NORMAL"] else 500
        rand += 1 if current_mode == mode["HARD"] else 0

    if e.type == QUIT:
        isRunning = False

    if not isGameOver and hitung == 0:
        if e.type == MOUSEBUTTONDOWN and not isBomb:
            if attacker.hit(enermy_group):
                for enermy in enermy_group:
                    if enermy.rect.collidepoint(e.pos):
                        enermy.die()
                score += 1
                hitSfx.play()
            else:
                missSfx.play()
                heart -= 1

        elif e.type == MOUSEBUTTONUP and not isBomb:
            attacker.unhit()

        elif (
            e.type == pygame.KEYDOWN
            and e.key == pygame.K_SPACE
            and bomb > 0
            and current_mode == mode["HARD"]
        ):
            isBomb = not isBomb
            attacker.bomb() if isBomb else attacker.unhit()

        elif e.type == pygame.MOUSEBUTTONDOWN and isBomb:
            score += attacker.boom(enermy_group)
            for enermy in enermy_group:
                enermy.die()
            attacker.unhit()
            Generate_Enermy()
            isBomb = False
            bomb -= 1

            pygame.time.set_timer(USEREVENT + 1, delay)

        elif e.type == USEREVENT + 1:
            Generate_Enermy()

    elif e.type == pygame.KEYDOWN and e.key == pygame.K_r and isGameOver:
        score = 0
        heart = 4
        hitung = 5
        bomb = 4
        lastUpdate = pygame.time.get_ticks()
        delay = 4000
        time = -500
        current_mode = mode["NORMAL"]
        attacker.unhit()
        robo_list_rect.clear()

    now = pygame.time.get_ticks()
    if now - lastUpdate > 1000 and hitung > 0:
        hitung -= 1
        lastUpdate = now
        Generate_Enermy()

    screen.blit(BG, (0, 0))
    drawMatrix(current_mode, screen, robo_list_rect)
    draw_text(f"Score: {score}", 50, 10, 10, screen)
    draw_text(f"Bomb: {bomb}", 50, 430, 10, screen) if current_mode == mode[
        "HARD"
    ] else None
    draw_text(f"Heart: {heart}", 50, 810, 10, screen)

    if hitung > 0:
        screen.blit(BG, (0, 0))
        draw_text(f"Ready in {hitung}", 100, 250, 350, screen)
        draw_text("Press N for Normal Mode", 50, 200, 500, screen)
        draw_text("Press H for Hard Mode", 50, 200, 600, screen)
        m = "NORMAL" if current_mode == mode["NORMAL"] else "HARD"
        draw_text(f"Your current mode is {m}", 50, 200, 700, screen)
        draw_text("Press Q to quit", 50, 200, 800, screen)

        if e.type == pygame.KEYDOWN and e.key == pygame.K_n:
            current_mode = mode["NORMAL"]
            robo_list_rect.clear()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_h:
            current_mode = mode["HARD"]
            robo_list_rect.clear()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_q:
            isRunning = False

    elif isGameOver:
        screen.blit(BG, (0, 0))
        pygame.mouse.set_visible(True)
        draw_text("Game Over", 100, 300, 400, screen)
        draw_text(f"Score: {score}", 69, 400, 500, screen)
        draw_text('Press "R" to restart', 50, 350, 600, screen)

    else:
        pygame.mouse.set_visible(False)

        enermy_group.draw(screen)
        atk_group.draw(screen)

        atk_group.update()

        clock.tick(60)

    display.flip()

pygame.quit()
