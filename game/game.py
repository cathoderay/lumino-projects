import random
import time
import pygame
from lumino import Lumino

width = 1024
height = 768
resolution = (width, height)
pygame.init()
screen = pygame.display.set_mode(resolution)
pygame.display.toggle_fullscreen()

background = pygame.Surface(screen.get_size())
background = background.convert()

running = True
scorea = 0
scoreb = 0
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
task = 0
tasks = {0: "small", 1: "half", 2: "big"}
last_ts = 0
speed = 3
TOLERANCE = 20
BIG = 160
HALF = 100
SMALL = 40
level = 1
in_level = False
to_pass = 500
wina = 0
winb = 0


def draw_text(text, target, position, size, color=GRAY):
    font = pygame.font.SysFont(None, size)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=position[0], centery=position[1])
    target.blit(text, textpos)


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and \
           event.key == pygame.K_ESCAPE:
           running = False
           pygame.quit()


def show_level(n, target):
    draw_text("Level %s" % n, target, (width/2, height/2), 50)


pygame.mixer.init()
pygame.mixer.music.load('./song.mp3')
tone = pygame.mixer.Sound('./tone.wav')


lumino = Lumino('/dev/ttyUSB0')
while running:
    if not in_level:
        background.fill(BLACK)
        pygame.mixer.music.stop()
        tone.play()
        show_level(level, background)
        draw_text(str(wina), background, (width/4, height/2), 200, color=RED)
        draw_text(str(winb), background, (3*width/4, height/2), 200, color=BLUE)

        screen.blit(background, (0, 0))
        pygame.display.update()
        time.sleep(3)
        in_level = True
        pygame.mixer.music.play(-1)
        continue

    if scorea > 0 and scoreb > 0 and (scorea % to_pass == 0 or scoreb % to_pass == 0):
        if scorea % to_pass == 0:
            wina += 1
        if scoreb % to_pass == 0:
            winb += 1

        level += 1
        to_pass += 100
        speed -= 0.1
        in_level = False
        scorea = 0
        scoreb = 0
        continue

    ts = time.time()
    pointsa = 0
    pointsb = 0
    ra, rb = lumino.get()
    rad, rbd = ra/4, rb/4

    if rad <= SMALL + (HALF - SMALL)/2:
        rad = SMALL
    elif rad > SMALL + (HALF - SMALL)/2 and rad <= HALF + (BIG - HALF)/2:
        rad = HALF
    else:
        rad = BIG

    if rbd <= SMALL + (HALF - SMALL)/2:
        rbd = SMALL
    elif rbd > SMALL + (HALF - SMALL)/2 and rbd <= HALF + (BIG - HALF)/2:
        rbd = HALF
    else:
        rbd = BIG

    background.fill(BLACK)

    if task == 0:
        if rad <= SMALL + TOLERANCE and rad >= SMALL - TOLERANCE:
            pointsa += 1
        if rbd <= SMALL + TOLERANCE and rbd >= SMALL - TOLERANCE:
            pointsb += 1
    elif task == 1:
        if rad <= HALF + TOLERANCE and rad >= HALF - TOLERANCE:
            pointsa += 1
        if rbd <= HALF + TOLERANCE and rbd >= HALF - TOLERANCE:
            pointsb += 1
    else:
        if rad <= BIG + TOLERANCE and rad >= BIG - TOLERANCE:
            pointsa += 1
        if rbd <= BIG + TOLERANCE and rbd >= BIG - TOLERANCE:
            pointsb += 1

    scorea += pointsa
    scoreb += pointsb

    if ts - last_ts > speed:
        task = random.choice(tasks.keys())
        last_ts = ts

    # center line
    pygame.draw.line(background, GRAY, (width/2, 0), (width/2, height), 3)

    # baselines
    pygame.draw.circle(background, GRAY, (3*width/4, height/2), SMALL, 3)
    pygame.draw.circle(background, GRAY, (3*width/4, height/2), HALF, 3)
    pygame.draw.circle(background, GRAY, (3*width/4, height/2), BIG, 3)

    pygame.draw.circle(background, GRAY, (width/4, height/2), SMALL, 3)
    pygame.draw.circle(background, GRAY, (width/4, height/2), HALF, 3)
    pygame.draw.circle(background, GRAY, (width/4, height/2), BIG, 3)

    # balls
    pygame.draw.circle(background, RED, (width/4, height/2), rad, 10)
    pygame.draw.circle(background, BLUE, (3*width/4, height/2), rbd, 10)

    # score
    if pointsa > 0:
        color = GREEN
        size = 150
    else:
        color = GRAY
        size = 70
    draw_text(str(scorea), background, (width/4, 100), size, color=color)

    if pointsb > 0:
        size = 150
        color = GREEN
    else:
        size = 70
        color = GRAY
    draw_text(str(scoreb), background, (3*width/4, 100), size, color=color)


    if scorea > scoreb:
        draw_text("the best", background, (width/4, height - 50), 200, color=RED)
    elif scoreb > scorea:
        draw_text("the best", background, (3*width/4, height - 50), 200, color=BLUE)


    # task
    draw_text(str(tasks[task]), background, (width/2, height/2), 200, color=WHITE)

    screen.blit(background, (0, 0))
    pygame.display.update()

    handle_events()
