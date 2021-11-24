import pygame as pg
import os

from pygame.constants import KEYDOWN, QUIT

def _horizontal_collisions(x, y, xStep, yStep, downTime):

    player = pg.Rect(200 + xStep * downTime, y, 24, 24)
    wallsList = open(os.getcwd() + '\\pygame\\game\\walls.txt')
    wallHit = False

    for line in wallsList:
        var = line.split(',')
        walls = pg.Rect(int(var[0]) + x, int(var[1]), int(var[2]), int(var[3]))
        if pg.Rect.colliderect(player, walls):
            if not y < walls[1]:
                xStep = -xStep
                wallHit = True

    x -= xStep * downTime
    if wallHit == True:
        xStep = 0

    return x, xStep

def _vertical_collisions(x, y, yStep, downTime):
    player = pg.Rect(200 - x, y + yStep, 24, 24)
    wallsList = open(os.getcwd() + '\\pygame\\game\\walls.txt')
    grounded = False
    
    for line in wallsList:
        var = line.split(',')
        walls = pg.Rect(int(var[0]) + x, int(var[1]), int(var[2]), int(var[3]))
        if pg.Rect.colliderect(player, walls):
            if y < int(var[1]):
                grounded = True
            yStep = 0

    if grounded == False:
        y += yStep
    
    return y, yStep, grounded
                
#Setup
pg.init()
gameFolder = os.getcwd() + '\\pygame'
running = True

dis = pg.display.set_mode((1200, 240))

#Animation
frame = 0
cur_img = pg.Surface((16, 16))
sc = 0
anim_list = [
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\idle.png'), (24, 24)),
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\run1.png'), (24, 24)),
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\run2.png'), (24, 24)),
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\run3.png'), (24, 24)),
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\jump.png'), (24, 24))
]

bg = pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\levels\\1-1_overworld_clean.png'), (3376, 240))

#Positions
xpos = 0
ypos = 130
xchange = 0
ychange = 0
xaccel = 0.1
yaccel = 1
dir_left = False
m_grounded = False

#Time
clock = pg.time.Clock()
dt = clock.tick(200)

while running:

    #Ressetting variables
    xaccel = 0.1

    #Event handler
    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == pg.K_q:
                running = False

    #Input
    keys = pg.key.get_pressed()

    if keys[pg.K_RIGHT]:
        if frame < 1:
            frame = 1
        elif frame > 2:
            frame = 1   
        frame += 1
        xchange += xaccel
        dir_left = False
    elif keys[pg.K_LEFT]:
        if frame < 1:
            frame = 1
        elif frame > 2:
            frame = 1  
        frame += 1
        xchange -= xaccel
        dir_left = True
    else:
        sc = 0
        if xchange < 0:
            xchange += xaccel
        elif xchange > 0:
            xchange -= xaccel
        if (xchange < 0.1 and xchange > 0) or (xchange > -0.1 and xchange < 0):
            xchange = 0
            frame = 0
    
    if keys[pg.K_SPACE] and m_grounded == True:
        ychange = -14
        m_grounded = False
    else:
        ychange += yaccel

    #Max Speed
    if xchange > 1.4:
        xchange = 1.4
    elif xchange < -1.4:
        xchange = -1.4

    #Collisions
    xpos, xchange = _horizontal_collisions(xpos, ypos, xchange, ychange, dt)
    ypos, ychange, m_grounded = _vertical_collisions(xpos, ypos, ychange, dt)


    #Assigning cur_img
    cur_img = anim_list[frame]
    if dir_left:
        cur_img = pg.transform.flip(cur_img, True, False)
    cur_img.set_colorkey((147, 187, 236))


    #Blitting
    pg.Surface.blit(dis, bg, (xpos, 0))
    pg.Surface.blit(dis, cur_img, (200, ypos))

    #pg.draw.rect(dis, (0,0,0), (200, ypos + ychange, 24, 24))

    #Next frame
    clock.tick(30)
    pg.display.flip()