import pygame as pg
import os

from pygame.constants import KEYDOWN
from pygame.surface import Surface
from settings import Settings as S

def _collisions(player_x, player_y, ychange, ground, jc):
    
    counter = 0
    player = pg.Rect(player_x, player_y, 32, 32)
    g_rect = ""
    grounded = False
    
    for line in ground:
        x = line.split(',')
        g_rect = pg.Rect(int(x[0]), int(x[1]), int(x[2]), int(x[3]))
        print("not that")
        if pg.Rect.colliderect(player, g_rect): 
            player_y = int(x[1]) - 31
            ychange = 0
            jc = 0
            grounded = True
            print("collision")
        counter += 4
    counter = 0

    player = pg.Rect(player_x, player_y, 32, 32)
    return player, ychange, jc, grounded

pg.init()
dis = pg.display.set_mode((S.dis_width, S.dis_height))

m_bg = (147, 187, 236)

running = True

#Defining Sprites
gameFolder = os.getcwd()
m_anim_list = [
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\idle.png'), (32, 32)),
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\run1.png'), (32, 32)),
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\run2.png'), (32, 32)),
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\run3.png'), (32, 32)),
    pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\mariosprites\\jump.png'), (32, 32))
]
level01 = pg.transform.scale(pg.image.load(gameFolder+'\\game\\assets\\levels\\1-1_overworld_clean.png'), (6752, 480))

#Time
clock = pg.time.Clock()
dt = clock.tick(200)

#Position
xpos = 50
ypos = 300
xchange = 0
speed = 0.8
dir_left = False
player_rect = (xpos, ypos, 32, 32)

#Vertical movement
m_ychange = 0
jump_count = 0
yaccel = 0.8
jump = False
m_grounded = False

#Animation
anim_num = 0
cur_img = Surface((36, 36))
cur_img.set_colorkey((0,0,0))

#Ground
groundList = open(gameFolder+'\\game\\ground.txt', 'r')
ground_rect = (0, 0, 0, 0)

for x in m_anim_list:
    x.set_colorkey(m_bg)

while running:

    dis.blit(level01, (0,0))
    cur_img.fill((0,0,0))

    keys = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == pg.K_q:
                running = False

    if keys[pg.K_SPACE]:
        jump = True

    if keys[pg.K_RIGHT]:
        xchange = speed
        anim_num += 1
        if anim_num == 4:
            anim_num = 1
        
        pg.Surface.blit(cur_img, m_anim_list[anim_num], (0,0))
        cur_img.set_colorkey((0,0,0))

        dir_left = False
    elif keys[pg.K_LEFT]:
        xchange = -speed
        anim_num += 1
        if anim_num == 4:
            anim_num = 1
        
        pg.Surface.blit(cur_img, m_anim_list[anim_num], (0,0))
        cur_img = pg.transform.flip(cur_img, True, False)
        cur_img.set_colorkey((0,0,0))

        dir_left = True
    else:
        xchange = 0
        anim_num = 0
        pg.Surface.blit(cur_img, m_anim_list[anim_num], (0,0))
        if dir_left == True:
            cur_img = pg.transform.flip(cur_img, True, False)
        cur_img.set_colorkey((0,0,0))
    
    if jump == True and jump_count != 1:
        jump_count += 1
        m_ychange = -14
    else:
        m_ychange += yaccel
        jump = False
    
    ypos += m_ychange
    xpos += xchange * dt

    player_rect = pg.Rect(xpos, ypos, 32, 32)

    groundList = open(gameFolder+'\\game\\ground.txt', 'r')
    player_rect, m_ychange, jump_count, m_grounded = _collisions(xpos, ypos, m_ychange, groundList, jump_count)

    if m_grounded == False:
        cur_img.fill((0,0,0))
        pg.Surface.blit(cur_img, m_anim_list[4], (0,0))
        if dir_left == True:
            cur_img = pg.transform.flip(cur_img, True, False)
        cur_img.set_colorkey((0,0,0))

    ypos = player_rect[1]
    pg.Surface.blit(dis, cur_img, (xpos, ypos))

    groundList = open(gameFolder+'\\game\\ground.txt', 'r')
    for line in groundList:
        number_list = line.split(",")
        ground_rect = pg.Rect(int(number_list[0]), int(number_list[1]), int(number_list[2]), int(number_list[3]))
        pg.draw.rect(dis, (255, 0, 255), ground_rect)
    
    clock.tick(30)
    pg.display.flip()