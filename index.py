import pygame as pg
import random
from pygame import mixer
#initialize pygame
pg.init()

#set screen width and height
screen = pg.display.set_mode(( 800,600) )

#Title and Icon
pg.display.set_caption("Space Invaders")

#load image
icon = pg.image.load('ufo.png')
pg.display.set_icon( icon )

background = pg.image.load('space_background.png')

#play music continuosly a loop
mixer.music.load("background_music.wav")
mixer.music.play(-1)
#player
playerImg  = pg.image.load('player.png')
#player X,Y positions
playerX = 370
playerY = 480

#enemy
enemyImg  = []
#enemy X,Y positions
enemyX = []
enemyY = []

enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range( num_of_enemies ):
    enemyImg.append( pg.image.load('enemy.png') )
    #enemy X,Y positions
    enemyX.append(random.randint(5,734))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet
BulletImg  = pg.image.load('bullet.png')
#bullet X,Y positions
bulletX = 0
bulletY = 480
bulletY_change = 50
#bullet state ready means you can't see bullet on screen
#bullet state fire means it's moving on screen
bullet_state = "ready"
score = 0
font = pg.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#gameover text

game_over_font = pg.font.Font('freesansbold.ttf',64)

def show_score( x, y ):
    score_value = font.render("Score: {}".format(score),True,(255,0,255) )
    screen.blit( score_value,(x,y))
def game_over_text():
    game_over = game_over_font.render("GAME OVER",True,(255,255,255) )
    screen.blit( game_over,(200,250))
def player( x, y ):
    #draw the player cordinates on screen
    screen.blit( playerImg,(x,y))
def enemy( x, y,index ):
    #draw the enemy cordinates on screen
    screen.blit( enemyImg[index],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BulletImg, (x + 16 , y + 10 ))
def is_collison(x1,y1,x2,y2):
    distance = ( ((x2-x1)**2) + ( (y2-y1)**2) ) ** 0.5
    if ( distance < 27 ):
        return True
    return False
running = True

#display screen untill exit button is clicked
while running:
    #change backgrounnd color  (colors in rgb ) ( 255,0,0) is red
    screen.fill((255, 255, 0))
    screen.blit(background, (0,0))
    for event in pg.event.get():
        #make running to false if exit button is clicked on screen window
        if event.type == pg.QUIT:
            running = False
        #press arrow keys
        if event.type == pg.KEYDOWN:
            #if event.key == pg.K_UP:
            #   playerY -= 1
            if event.key == pg.K_LEFT:
                playerX -= 5
            if event.key == pg.K_RIGHT:
                playerX += 5
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    #buller_sound = mixer.Sound("laser.wav")
                    #buller_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT or event.key == pg.K_LEFT :
                pass

    #preventing spaceship to move out of boundaries
    if playerX <=0:
        playerX = 0
    if playerX >= 748:
        playerX = 748
    for i in range( num_of_enemies ):
        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text( )
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >=700:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collison
        collison = is_collison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            #crash_sound = pg.mixer.Sound("explosion.wav")
            #pg.mixer.Sound.play(crash_sound)
            #pg.mixer.music.stop()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        # position the enemy
        enemy(enemyX[i], enemyY[i],i)
    #position the player
    player( playerX,playerY )
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    show_score(textX,textY)
    #update the display
    pg.display.update()
