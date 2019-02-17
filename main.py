#!/usr/bin/env python2

import random
import pygame 
import collision

global CHARACTER_HEIGHT
CHARACTER_HEIGHT = 60
global CHARACTER_WIDTH
CHARACTER_WIDTH = 40

global BULLET_WIDTH
BULLET_WIDTH = 4
global BULLET_HEIGHT
BULLET_HEIGHT = 4
global BULLET_VELOCITY
BULLET_VELOCITY = 5

global ENEMY_BULLET_WIDTH
global ENEMY_BULLET_HEIGHT

ENEMY_BULLET_WIDTH = 2
ENEMY_BULLET_HEIGHT = 2

global ENEMY_WIDTH
ENEMY_WIDTH = 15
global ENEMY_HEIGHT
ENEMY_HEIGHT = 15
global ENEMY_VELOCITY
ENEMY_VELOCITY = 2

global SCOREBOARD_CHAR_WIDTH
SCOREBOARD_CHAR_WIDTH = 20
global SCOREBOARD_CHAR_HEIGHT
SCOREBOARD_CHAR_HEIGHT = 26

global counter0
global counter1
global counter2
global counter3
global counter4
global counter5
global counter6
global counter7
global counter8
global counter9

counter0 = pygame.image.load("0.png")
counter1 = pygame.image.load("1.png")
counter2 = pygame.image.load("2.png")
counter3 = pygame.image.load("3.png")
counter4 = pygame.image.load("4.png")
counter5 = pygame.image.load("5.png")
counter6 = pygame.image.load("6.png")
counter7 = pygame.image.load("7.png")
counter8 = pygame.image.load("8.png")
counter9 = pygame.image.load("9.png")
    
global pauseScreen

pauseScreen = pygame.image.load("pause.png")

def generateTriangle(x, y):
    vertex1 = (x, (y + CHARACTER_HEIGHT))
    vertex2 = ((x + (CHARACTER_WIDTH / 2)), y)
    vertex3 = ((x + CHARACTER_WIDTH), (y + CHARACTER_HEIGHT))
    
    return [vertex1, vertex2, vertex3]

def sidesOfEnemy(x, y):
   line1 = ((x), (y)), ((x + ENEMY_WIDTH), (y)) 
   line2 = ((x), (y)), ((x), (y + ENEMY_HEIGHT)) 
   line3 = ((x + ENEMY_WIDTH), (y)), ((x + ENEMY_WIDTH), (y + ENEMY_HEIGHT)) 
   line4 = ((x), (y + ENEMY_HEIGHT)), ((x + ENEMY_WIDTH), (y + ENEMY_HEIGHT)) 
   
   return [line1, line2, line3, line4]

def sidesOfShip(x, y):
    line1 = ((x + (CHARACTER_WIDTH / 2)), (y)), ((x), (y + CHARACTER_HEIGHT))
    line2 = ((x + (CHARACTER_WIDTH / 2)), (y)), ((x + CHARACTER_WIDTH), (y + CHARACTER_HEIGHT))
    line3 = ((x), (y + CHARACTER_HEIGHT)), ((x + CHARACTER_WIDTH), (y + CHARACTER_HEIGHT))
    
    return [line1, line2, line3]

def pickDigit(num):
    if num == 0: return counter0
    if num == 1: return counter1
    if num == 2: return counter2
    if num == 3: return counter3
    if num == 4: return counter4
    if num == 5: return counter5
    if num == 6: return counter6
    if num == 7: return counter7
    if num == 8: return counter8
    if num == 9: return counter9

def scoreboard(score):
    
        scoreboardSurface = pygame.Surface((SCOREBOARD_CHAR_WIDTH * 4, SCOREBOARD_CHAR_HEIGHT))
        
        scoreboardSurface.set_colorkey((0, 0, 0))
        
        scoreboardSurface.blit(pickDigit(score % 10), ((SCOREBOARD_CHAR_WIDTH * 3), 0))
        scoreboardSurface.blit(pickDigit((score / 10) % 10), ((SCOREBOARD_CHAR_WIDTH * 2), 0))
        scoreboardSurface.blit(pickDigit((score / 100) % 10), (SCOREBOARD_CHAR_WIDTH, 0))
        scoreboardSurface.blit(pickDigit((score / 1000) % 10), (0, 0))
        
        return scoreboardSurface
    
def gameLoop(win, WINDOW_MAX_WIDTH, WINDOW_MAX_HEIGHT):
    run = True
    
    score = 0
    
    MOUSE_BUTTON_FIRE = 1

    enemyTimer = 10
    
    bulletList = []
    enemyList = []
    
    while run:
        pygame.time.delay(15)
        
        if enemyTimer > 0:
            enemyTimer -= 1
        else:
            enemyTimer = random.randint(20, 90)
            x = random.randint(CHARACTER_WIDTH, (WINDOW_MAX_WIDTH - CHARACTER_WIDTH))
            y = 0 - ENEMY_HEIGHT
            enemyList.append((x, y))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bulletX, bulletY = event.__dict__['pos']
                bulletPos = ((bulletX + (CHARACTER_WIDTH / 2)), bulletY)
                bulletList.append(bulletPos)
            elif event.type == pygame.KEYDOWN:
                key = event.__dict__['key']
                if key == pygame.K_SPACE:
                    paused = True
                    win.blit(pauseScreen, (0, 0))
                    pygame.display.update()
                    while paused:
                        checkPause = pygame.event.wait()
                        if checkPause.type == pygame.KEYDOWN:
                            key = checkPause.__dict__['key']
                            if key == pygame.K_SPACE:
                                paused = False
                            elif key == pygame.K_q:
                                paused = False
                                run = False
            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        shipX = min(mouse_x, (WINDOW_MAX_WIDTH - CHARACTER_WIDTH))
        shipY = min(mouse_y, (WINDOW_MAX_HEIGHT - CHARACTER_HEIGHT))
                
        win.fill((0, 0, 0))
        
        pygame.draw.polygon(win, (255, 0, 0), generateTriangle(shipX, shipY))
        
        enemyRemoveList = []
        enemyIndex = 0
        for enemyX, enemyY in enemyList:
            enemyY += ENEMY_VELOCITY
            # Determine if a bullet touches this enemy
            for bulletX, bulletY in bulletList:
                if (bulletX > enemyX and
                        bulletX < (enemyX + ENEMY_WIDTH) and
                        bulletY > enemyY and
                        bulletY < (enemyY + ENEMY_HEIGHT)):
                    enemyRemoveList.append(enemyIndex)
                    score += 1
                    break
            # Remove enemy if it reaches bottom of the screen
            if enemyY > WINDOW_MAX_HEIGHT:
                enemyRemoveList.append(enemyIndex)
                run = False
            # Determine if enemy has touched the ship
            for enemyLine in sidesOfEnemy(enemyX, enemyY):
                ePoint1, ePoint2 = enemyLine
                for shipLine in sidesOfShip(shipX, shipY):
                    sPoint1, sPoint2 = shipLine
                    if collision.checkLines(ePoint1, ePoint2, sPoint1, sPoint2):
                        print("COLLISION!!!")
                        run = False
                        break
                if run == False: break
            pygame.draw.rect(win, (0, 255, 0), (enemyX, enemyY, ENEMY_WIDTH, ENEMY_HEIGHT))
            enemyList[enemyIndex] = (enemyX, enemyY)
            enemyIndex += 1
            if run == False: break
        
        bulletRemoveList = []
        bulletIndex = 0
        for bulletX, bulletY in bulletList:
            bulletY -= BULLET_VELOCITY
            if bulletY < 0:
                bulletRemoveList.append(bulletIndex)
            pygame.draw.rect(win, (255, 255, 255), (bulletX, bulletY, BULLET_WIDTH, BULLET_HEIGHT))
            bulletList[bulletIndex] = (bulletX, bulletY)
            bulletIndex += 1
            
        for i in bulletRemoveList:
            bulletList.pop(i)
        
        for i in enemyRemoveList:
            enemyList.pop(i)
            
        #Draw the score
        print((score / 1000) % 10, (score / 100) % 10, (score / 10) % 10, score % 10)
        
        win.blit(scoreboard(score), (WINDOW_MAX_WIDTH - (SCOREBOARD_CHAR_WIDTH * 5), 50))
        
        pygame.display.update()
        
    return score
        
if __name__ == "__main__":
    
    pygame.init()

    WINDOW_MAX_WIDTH = 500
    WINDOW_MAX_HEIGHT = 700
    
    
    newgame = pygame.image.load("main.png")
    yourscore = pygame.image.load("yourscore.png")

    win = pygame.display.set_mode((WINDOW_MAX_WIDTH, WINDOW_MAX_HEIGHT))

    pygame.display.set_caption("BulletPy")
    pygame.mouse.set_visible(False)
    
    score = -1

    while True:
        win.fill((0, 0, 0))
        win.blit(newgame, (0, 0))
        if score >= 0:
            yourscoreX = 125
            yourscoreY = 160
            win.blit(yourscore, (yourscoreX, yourscoreY))
            scoreboardX = (WINDOW_MAX_WIDTH / 2) - (SCOREBOARD_CHAR_WIDTH * 2)
            scoreboardY = (yourscoreY + 50)
            win.blit(scoreboard(score), (scoreboardX, scoreboardY))
        pygame.display.update()
        getSpace = pygame.event.wait()
        if getSpace.type == pygame.KEYDOWN:
            k = getSpace.__dict__['key']
            if k == pygame.K_SPACE:
                print("SPACE!")
                pygame.event.set_grab(True)
                score = gameLoop(win, WINDOW_MAX_WIDTH, WINDOW_MAX_HEIGHT)
            elif k == pygame.K_q:
                break
        elif getSpace.type == pygame.QUIT:
            break
        pygame.event.set_grab(False)
    
pygame.quit()
