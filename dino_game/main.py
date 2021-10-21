import os
import pygame as pg
from pygame import image
from settings import Settings

pg.init()

run = True

xpos = 0
ypos = 0

char = []

a_num = -1

cwd = os.getcwd()

def _image_at(sheet, number, width, height, scale):
    #Make blank and blit image on blank
    image = pg.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((number * width), 0, 24, 24))
    #Modify sprite to "perfection"
    image = pg.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((0, 0, 0))
    return image

def _move_char(flip, x, y, a_num):
    #Define
    d_run_list = []
    change = 0
    speed = 10
    anim_num = a_num
    char_img = ""
    char = ""

    #Load spritesheet
    dino_sheet = pg.image.load(os.path.normpath(cwd+'/dino_game/assets/DinoSprites.png')).convert_alpha()

    #Assign sprites
    d_idle = _image_at(dino_sheet, 0, 24, 24, 3)
    d_run_list.append(_image_at(dino_sheet, 5, 24, 24, 3))
    d_run_list.append(_image_at(dino_sheet, 6, 24, 24, 3))
    d_run_list.append(_image_at(dino_sheet, 7, 24, 24, 3))
    d_run_list.append(_image_at(dino_sheet, 8, 24, 24, 3))
    d_run_list.append(_image_at(dino_sheet, 9, 24, 24, 3))
    d_run_list.append(_image_at(dino_sheet, 10, 24, 24, 3))

    #Moving left or right based on input + cycling animation
    anim_num += 1
    if anim_num < 5:
        anim_num = 0
    if flip:
        speed = -speed
    change = speed
    x += change

    char_img = pg.transform.flip(d_run_list[anim_num], flip, False)
    char_img.set_colorkey((0, 0, 0))
    char_temp = [char_img, x, y, anim_num]

    return char_temp

#Setting up display
dis = pg.display.set_mode((Settings.dis_width, Settings.dis_height))
dis.fill(Settings.background)

while run:

    #Get keys pressed and movement
    keys = pg.key.get_pressed()

    if keys[pg.K_RIGHT]:
        char = _move_char(False, xpos, ypos, a_num)
        xpos = char[1]
        ypos = char[2]
        a_num = char[3]
        print(char[0])
        print(type(char[0]))
        dis.fill(Settings.background)
        dis.blit(char[0], (xpos, ypos))
        

    if keys[pg.K_LEFT]:
        pass
    for event in pg.event.get():    
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                run = False

    pg.time.delay(100)
    pg.display.flip()
                

pg.quit()