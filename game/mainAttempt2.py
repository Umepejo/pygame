import os
import pygame as pg
from pygame import image
from settings import Settings as S  

pg.init()
cwd = os.getcwd()

def _move_char(flip, x, y, anim_num, m_display, bg, idle, jmp, jump_counter, d_grounded):
    def _image_at(sheet, number, width, height, scale, flip):
            image = pg.Surface((width, height))
            image.blit(sheet, (0, 0), ((number * width), 0, width, height))

            if flip == True:
                image = pg.transform.flip(image, True, False)
            image = pg.transform.scale(image, (width * scale, height * scale))
            image.set_colorkey((0, 0, 0))
            return image

    def _animation_setup(size_modif):
        cwd = os.getcwd()
        dino_sheet = pg.image.load((cwd+'/pygame/dino_game/assets/smolmariov3.png')).convert_alpha()
        pg.Surface.set_colorkey(dino_sheet, (147, 187, 236))

        d_idle_list = []
        d_walk_list = []
        d_jump_list = []

        d_idle_list.append(_image_at(dino_sheet, 0, 16, 16, size_modif, False))
        d_idle_list.append(_image_at(dino_sheet, 0, 16, 16, size_modif, True))
        d_walk_list.append(_image_at(dino_sheet, 2, 16, 16, size_modif, False))
        d_walk_list.append(_image_at(dino_sheet, 3, 16, 16, size_modif, False))
        d_walk_list.append(_image_at(dino_sheet, 4, 16, 16, size_modif, False))
        d_jump_list = _image_at(dino_sheet, 6, 16, 16, size_modif, False)

        return d_idle_list, d_walk_list, d_jump_list
    #GOAL: Make ALL movements go through _move_char() (maybe have jumps go though seperate func)

    #Define
    change = 0
    speed = 4
    char_img = ""
    s_modif = 1.2

    #Animation Lists
    all_animation_lists = []
    d_idle = []
    d_walk = []
    d_jump = ""

    #Grab lists from earlier setup
    all_animation_lists = _animation_setup(s_modif)
    d_idle = all_animation_lists[0]
    d_walk = all_animation_lists[1]
    d_jump = all_animation_lists[2]

    #Background
    m_display.blit(bg, (0,0))

    #Flipping and displaying
    char_img = pg.transform.flip(d_walk[anim_num], flip, False)
    char_img.set_colorkey((0,0,0))

    #Idle
    if idle:
        if flip == False:
            char_img = d_idle[0]
        elif flip == True:
            char_img = d_idle[1]

    else:
        #Cycling sprites
        if flip == True:
            speed = -speed
        change = speed
        x += change

    if jmp:
        if jump_counter > 0:
            y -= 1
            jump_counter -= 1

    m_display.blit(char_img, (x, y))

    pg.display.flip()
    pg.time.delay(20)

    return x, y

def _check_collisions(d_rect):

    ground = pg.Rect(0, 208, 1200, 32)

    if pg.Rect.colliderect(d_rect, ground):
        return True
    else:
        return False

#Constants
run = True

#Dino positions
xpos = 50
ypos = S.dis_height / 2 #Should be changed
#Dino Size
d_width = 20
d_height = 20
#Dino Actions
cur_dir = ""
last_dir = ""
jump = False
#Checks
m_grounded = False
m_jump = False
m_run = False
leftOrRight = False
#Rects
dinoRect = pg.Rect(ypos + 10, xpos + 10, d_width, d_height)
#Counters
jmp_counter = 5
a_num = 0
#Lists from functions
char = []
jump_return = []
collisions = []

#Display and background setup
bg_img = pg.image.load(cwd+'/pygame/dino_game/assets/1-1.png')
dis = pg.display.set_mode((S.dis_width, S.dis_height))
dis.blit(bg_img, (0, 0))

if run == True:
    
    leftOrRight = False
    cur_dir = ""

    #Get input
    keys = pg.key.get_pressed()

    if keys[pg.K_RIGHT]:
        cur_dir = "right"
        leftOrRight = True
    elif keys[pg.K_LEFT]:
        cur_dir = "left"
        leftOrRight = True

    if keys[pg.K_UP]:
        jump = True

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                run = False
    
    if cur_dir == "right":
        char = _move_char(False, xpos, ypos, a_num, dis, bg_img, False, jump, jmp_counter, m_grounded)
        last_dir = "right"
        a_num += 1
    elif cur_dir == "left":
        char = _move_char(True, xpos, ypos, a_num, dis, bg_img, False, jump, jmp_counter, m_grounded)
        last_dir = "left"
        a_num += 1
    else:
        a_num = 0
        if last_dir == "right":
            char = _move_char(False, xpos, ypos, a_num, dis, bg_img, True, jump, jmp_counter, m_grounded)
        elif last_dir == "left":
            char = _move_char(True, xpos, ypos, a_num, dis, bg_img, True, jump, jmp_counter, m_grounded)
   
    if a_num == 3:
        a_num = 0
    
    #Redefining dino-hitbox
    if leftOrRight == True:
        xpos = char[0]
        ypos = char[1]
        dinoRect = pg.Rect(xpos, ypos, d_width, d_height)

    

    #Resetting checks
    leftOrRight = False

    jump = False

    m_grounded = _check_collisions(dinoRect)

    if m_grounded == False:
        ypos += 1

    pg.display.flip()