import pygame
import random
import math
from pygame import mixer

pygame.init()

# set the screen
screen = pygame.display.set_mode((800, 600))

# add a background
background = pygame.image.load('backgroundforgame.png')

# add background sound (-1 to loop)
mixer.music.load('background.wav')
mixer.music.play(-1)

# caption and icon
pygame.display.set_caption("Space Invaders")

# player and x y position
PlayerImg = pygame.image.load("spaceship.png")
PlayerX = 370
PlayerY = 480
PlayerX_change = 0
PlayerY_change = 0

# enemy and x y position
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load("enemy.png"))
    EnemyX.append(random.randint(0, 800))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(4)
    EnemyY_change.append(40)

# bullet
# ready state - cant see bullet
# other state - bullet in motion
BulletImg = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 480
BulletY_change = 10
bullet_state = 'ready'
score_value = 0
testX = 10
testY = 10

# Score
font = pygame.font.Font('freesansbold.ttf', 32)

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render(f"Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render(f"GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB for background
    screen.fill((120, 32, 43))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # up down left right main character and bullet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -5
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0

    # stops player from reaching the edge
    PlayerX += PlayerX_change
    if PlayerX <= 5:
        PlayerX = 5
    elif PlayerX > 736:
        PlayerX = 730

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if EnemyY[i] > 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break


        # enemy movement
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 5:
            EnemyX_change[i] = 4
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] > 736:
            EnemyY[i] += EnemyY_change[i]
            EnemyX_change[i] = -4



        # collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            BulletY = 480
            bullet_state = 'ready'
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)

            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()


        enemy(EnemyX[i], EnemyY[i], i)

    # bullet movement

    if BulletY <= 0:
        BulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    show_score(testX,testY)
    pygame.display.update()
