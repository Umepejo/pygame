import pygame as pg
import os

from pygame.constants import KEYDOWN
from pygame.surface import Surface
from settings import Settings as S

def _collisions(player, ychange):
    ground = []
    for x in ground:
        if pg.Rect.colliderect(player, x):


pg.init()
dis = pg.display.set_mode((S.dis_width, S.dis_height))

m_bg = (147, 187, 236)

running = True

#Defining Sprites
cwd = os.getcwd()

m_anim_list = [
    pg.transform.scale(pg.image.load(cwd+'/pygame/game/assets/mariosprites/idle.png'), (32, 32)),
    pg.transform.scale(pg.image.load(cwd+'/pygame/game/assets/mariosprites/run1.png'), (32, 32)),
    pg.transform.scale(pg.image.load(cwd+'/pygame/game/assets/mariosprites/run2.png'), (32, 32)),
    pg.transform.scale(pg.image.load(cwd+'/pygame/game/assets/mariosprites/run3.png'), (32, 32))
]

#Time
clock = pg.time.Clock()
dt = clock.tick(200)

#Position
xpos = 50
ypos = 300
xchange = 0
speed = 2
dir_left = False
player_rect = (xpos, ypos, 32, 32)

#Vertical movement
m_ychange = 0
yaccel = 0.1

#Animation
anim_num = 0
cur_img = Surface((36, 36))
cur_img.set_colorkey((0,0,0))

for x in m_anim_list:
    x.set_colorkey(m_bg)

while running:

    dis.fill(S.background)
    cur_img.fill((0,0,0))

    keys = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == pg.K_q:
                running = False

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

    ychange += yaccel
    ypos += ychange
    xpos += xchange * dt

    player_rect = (xpos, ypos, 32, 32)

    pg.Surface.blit(dis, cur_img, (xpos, ypos))

    clock.tick(60)
    pg.display.flip()