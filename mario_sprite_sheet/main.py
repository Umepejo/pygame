import os
import pygame as pg
from pygame import image
from settings import Settings

pg.init()

run = True

d_run_list = []
anim_num = -1

xchange = 0
ychange = 0
xpos = 0
ypos = 0
speed = 10

def image_at(sheet, number, width, height, scale):
    #Make blank and blit image on blank
    image = pg.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((number * width), 0, 24, 24))
    #Modify sprite to "perfection"
    image = pg.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((0, 0, 0))
    return image

def char_define(dir):
    dis.fill(Settings.background)
    
    char = 

#Setting up display
dis = pg.display.set_mode((Settings.dis_width, Settings.dis_height))
dis.fill(Settings.background)

#Load spritesheet
dino_sheet = pg.image.load(os.path.normpath(Settings.cwd+'/pygame/mario_sprite_sheet/assets/DinoSprites.png')).convert_alpha()


#Assign sprites
d_idle = image_at(dino_sheet, 0, 24, 24, 3)
d_run_list.append(image_at(dino_sheet, 5, 24, 24, 3))
d_run_list.append(image_at(dino_sheet, 6, 24, 24, 3))
d_run_list.append(image_at(dino_sheet, 7, 24, 24, 3))
d_run_list.append(image_at(dino_sheet, 8, 24, 24, 3))
d_run_list.append(image_at(dino_sheet, 9, 24, 24, 3))
d_run_list.append(image_at(dino_sheet, 10, 24, 24, 3))

while run:

    #Get keys pressed and movement
    keys = pg.key.get_pressed()

    if keys[pg.K_RIGHT]:
        anim_num += 1
        xchange = speed
        ychange = 0
        if anim_num > 5:
            anim_num = 0
        
        dis.fill(Settings.background)
        dis.blit(d_run_list[anim_num], (xpos, ypos))

    if keys[pg.K_LEFT]:
        anim_num += 1
        xchange = -speed
        ychange = 0
        if anim_num > 5:
            anim_num = 0
        char = pg.transform.flip(d_run_list[anim_num], True, False)
        dis.fill(Settings.background)
        dis.blit(char, (xpos, ypos))
        
    for event in pg.event.get():    
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                run = False

    pg.time.delay(100)
    pg.display.flip()
                

pg.quit()