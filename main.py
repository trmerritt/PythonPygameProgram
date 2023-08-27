# Tuesday 13/06/2023 A Bear's Revenge - a simple game made in Python using pygame
# Used tutorial for help with code structure, but created entirely own design and appearance using my imagination

import pygame
#random module used for randomising respawn of enemy avatar
import random
from pygame import mixer
import math

#need below to initialise pygame module
pygame.init()

#screen creation below - width*height(x,y)
screen = pygame.display.set_mode((1000, 600))


#background sound mixer.music is for longer sounds, mixer.sound is for shorter
mixer.music.load("comic5-25269.wav")
mixer.music.play(-1)

#window icon and title styling
pygame.display.set_caption("A Bear's Revenge")
icon = pygame.image.load("bear.png")
pygame.display.set_icon(icon)

#player avatar
playerImg = pygame.image.load("b.png")
playerX = 500
playerY = 500
playerX_change = 0

#enemy avatar
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("001-man.png"))
    enemyX.append(random.randint(0, 936))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.60)
    enemyY_change.append(40)

#rock projectile sprite - ready means invisible
rockImg = pygame.image.load("001-rock.png")
rockX = 0
rockY = 500
rockX_change = 0
rockY_change = 10
rock_state = "ready"

score_val = 0
font = pygame.font.Font("freesansbold.ttf", 30)

#game over announcement
game_over_font = pygame.font.Font("freesansbold.ttf", 100)
textX = 10
textY = 10

#unlike other instance, this time must render then blit
def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (0, 0, 0))
    screen.blit(score, (x, y))

screen_width = 1000
screen_height = 600

def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (0, 0, 0))
    text_width = game_over.get_width()
    text_height = game_over.get_height()
    x = (screen_width - text_width) // 2
    y = (screen_height - text_height) // 2
    screen.blit(game_over, (x, y))

#blit refers to drawing - drawing player onto surface (screen)
def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))

#The x+16 and y+10 is to make sure the rock is centered on the player avatar
def throw_rock(x,y):
    global rock_state
    rock_state = "fire"
    screen.blit(rockImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, rockX, rockY):
    distance = math.sqrt((math.pow(enemyX-rockX,2)) + (math.pow(enemyY-rockY, 2)))
    if distance < 27:
        return True
    else:
        return False


#anything that happens within the game window is an event - close = a quit event etc
#while loop to allow user to quit game by pressing the close window. This is a game loop
running = True
while running:

    #RGB values in tuple and this is for the screen background
    screen.fill((0, 255, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#keystroke event like all events get logged in pygame.event.get()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.0
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.0
            if event.key == pygame.K_SPACE:
                if rock_state == "ready":
                    rock_sound = mixer.Sound("karate-chop-6357.wav")
                    rock_sound.play()
                    rockX = playerX
                    throw_rock(rockX, rockY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

#The below if/else statements are for ensuring avatars stay within screen boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    for i in range(num_of_enemies):

        #Game over screen
        if enemyY[i] >= 469:
            for x in range(num_of_enemies):
                enemyY[x] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
            enemyX_change[i] = -0.7
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], rockX, rockY)
        if collision:
            rockY = 500
            rock_state = "ready"
            score_val += 1
            #below code allows enemy respawn after hit
            enemyX[i] = random.randint(0, 936)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if rockY <= 0:
        rockY = 500
        rock_state = "ready"


    if rock_state == "fire":
        throw_rock(rockX, rockY)
        rockY -= rockY_change



    player(playerX, playerY)
    show_score(textX, textY)
    # must use update to update the screen continuously for the user
    pygame.display.update()

"""game created by trm, 

attribution for bear avatar back image = <a 
href="https://www.flaticon.com/free-icons/bear" title="bear icons">Bear icons created 
by aslaiart - Flaticon</a>

attribution for hunter avatar icon = <a 
href="https://www.flaticon.com/free-icons/hunter" title="hunter icons">Hunter icons 
created by Skyclick - Flaticon</a>

attribution for rock weapon icon = <a href="https://www.flaticon.com/free-icons/rock" title="rock icons">Rock icons 
created by Freepik - Flaticon</a>

attribution for bear window icon = <a href="https://www.flaticon.com/free-icons/bear" title="bear icons">Bear icons 
created by Freepik - Flaticon</a>

background music = https://pixabay.com/sound-effects/comic5-25269/
sound effect = https://pixabay.com/sound-effects/karate-chop-6357/
"""
