import pygame
import random
import math
from pygame import mixer

pygame.init()

score = 0
font=pygame.font.Font('freesansbold.ttf',32)

over=pygame.font.Font('freesansbold.ttf',64)

screen = pygame.display.set_mode((800, 600))

def dis_score():
    show=font.render("Score: "+str(score),True,(255,255,255))
    screen.blit(show,(10,10))

background = pygame.image.load('background(2).jpg')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

pimg = pygame.image.load('spaceship (1).png')
pimgx = 370
pimgy = 480
xchange = 0.0
ychange = 0.0

enemyimg = []
enemyx = []
enemyy = []
enemyxchange = []
enemyychange = []
numenemies = 10

for i in range(numenemies):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyxchange.append(3)
    enemyychange.append(0.0)

bullet = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletxchange = 0.0
bulletychange = 1
bullet_state = "ready"


def player(x, y):
    screen.blit(pimg, (x, y))

def enemy(x, y,i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))

def gameover():
    overscore=over.render("GAME OVER",True,(255,255,255))
    screen.blit(overscore,(200,250))
    show = over.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(show, (250,350))


def iscollision(enemyx, enemyy, bulletx, bullety):
    dist = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
    if dist < 27:
        return True
    else:
        return False


check = True
while check:
    screen.fill((120, 150, 75))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xchange = -2
            if event.key == pygame.K_RIGHT:
                xchange = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    collision_sound=mixer.Sound('laser.wav')
                    collision_sound.play()
                    fire_bullet(pimgx, bullety)
                    bulletx = pimgx

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                xchange = 0

    pimgx = (pimgx + xchange)
    if pimgx <= 0:
        pimgx = 0
    elif pimgx >= 736:
        pimgx = 736

    for i in range(numenemies):
        enemy(enemyx[i], enemyy[i], i)

        if(enemyy[i]>=440):
            for j in range(numenemies):
                enemyy[j]=1500 #All the enemies go out of screen when Game Over
            gameover()
        if enemyx[i] <= 0:
            enemyxchange[i] = 3
            enemyy[i] += 40
        if enemyx[i] >= 736:
            enemyxchange[i] = -3
            enemyy[i] += 40

        if bullety <= 0:
            bullety = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletx, bullety)
            bullety -= bulletychange


        enemyx[i] += enemyxchange[i]

        player(pimgx, pimgy)

        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullet_state = "ready"
            bullety = 480
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            score += 1
            print(score)
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)
        dis_score()
        pygame.display.update()
