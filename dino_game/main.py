import os
import pygame as pg
from pygame import image
from settings import Settings
 
pg.init()

#Globals
global d_walk_list

#Constants
run = True

#Dino posistions
direction = ""
last_dir = "right"
xpos = 0
ypos = 0

#Lists
all_animation_lists = []
d_walk_list = []
char = []

#Counters
a_num = 0
tick = 0

#Setting up display
dis = pg.display.set_mode((Settings.dis_width, Settings.dis_height))
dis.fill(Settings.background)

def _animation_setup(): #Stuff that should be ran once but looks better separated from main body of code (maybe diffrent file?)
    def _image_at(sheet, number, width, height, scale, flip): #Ran multiple times but all times at the same time
        #Make blank and blit image on blank
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((number * width), 0, 24, 24))
        #Flips image horizontally if nessesary
        if flip:
            image = pg.transform.flip(image, True, False)
        #Modify sprite to "perfection"
        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0, 0, 0))
        return image
    
    cwd = os.getcwd()

    dino_sheet = pg.image.load(os.path.normpath(cwd+'/dino_game/assets/DinoSprites.png')).convert_alpha()
    
    d_idle_list = []
    d_walk_list = []

    #Assign sprites
    d_idle_list.append(_image_at(dino_sheet, 0, 24, 24, 3, False))
    d_idle_list.append(_image_at(dino_sheet, 0, 24, 24, 3, True))
    d_walk_list.append(_image_at(dino_sheet, 5, 24, 24, 3, False))
    d_walk_list.append(_image_at(dino_sheet, 6, 24, 24, 3, False))
    d_walk_list.append(_image_at(dino_sheet, 7, 24, 24, 3, False))
    d_walk_list.append(_image_at(dino_sheet, 8, 24, 24, 3, False))
    d_walk_list.append(_image_at(dino_sheet, 9, 24, 24, 3, False))
    d_walk_list.append(_image_at(dino_sheet, 10, 24, 24, 3, False))

    return d_idle_list, d_walk_list
    
all_animation_lists = _animation_setup()
d_idle = all_animation_lists[0]
d_walk_list = all_animation_lists[1]

def _move_char(flip, x, y, anim_num): #Simple move script
    #Define
    change = 0
    speed = 10
    char_img = ""

    #Moving left or right based on input + cycling animation
    anim_num += 1
    if anim_num > 5:
        anim_num = 0
    if flip:
        speed = -speed
    change = speed
    x += change

    char_img = pg.transform.flip(d_walk_list[anim_num], flip, False)
    char_img.set_colorkey((0, 0, 0))
    char_temp = [char_img, x, y, anim_num]

    return char_temp

while run:
    #Get keys pressed and movement
    keys = pg.key.get_pressed()
    #Delay to take input every millisecond but not update screen as often
    if tick <= 100:
        if keys[pg.K_RIGHT]:
            direction = "right"    
        elif keys[pg.K_LEFT]:
            direction = "left"
        tick += 1
        pg.time.delay(1)
    else:

        tick = 0

        if direction == "right":
            char = _move_char(False, xpos, ypos, a_num)
            last_dir = "right"
        elif direction == "left":
            char = _move_char(True, xpos, ypos, a_num)
            last_dir = "left"
        
        if direction == "right" or direction == "left":
            xpos = char[1]
            ypos = char [2]
            a_num = char[3]
            dis.fill(Settings.background)
            dis.blit(char[0], (xpos, ypos))

        else:
            dis.fill(Settings.background)
            if last_dir == "right":
                dis.blit(d_idle[0], (xpos, ypos))
            elif last_dir == "left":
                dis.blit(d_idle[1], (xpos, ypos))
        
        
        for event in pg.event.get():    
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    run = False



        direction = ""            

        pg.display.flip()                   

pg.quit()