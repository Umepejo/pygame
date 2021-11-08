import os
import pygame as pg
from pygame import image
from pygame.constants import K_LSHIFT, K_SPACE
from settings import Settings as S
 
pg.init()
cwd = os.getcwd()


#Constants
run = True

#Dino posistions and actions
d_width = 20
d_height = 20
direction = ""
jump = False
last_dir = "right"
m_grounded = True
m_run = False
xpos = 50
ypos = S.dis_height / 2
dinoRect = pg.Rect(ypos + 10, xpos + 10, d_width, d_height)

#Lists
all_animation_lists = []
d_idle = []
d_walk = []
d_jump = []
d_run = []
char = []
jump_return = []

#Counters and checks
a_num = -1
tick = 0
leftOrRight = False
delay = False
falling_modifier = 1

bg_img = pg.image.load(cwd+'/pygame/dino_game/assets/1-1.png')

#Setting up display
dis = pg.display.set_mode((S.dis_width, S.dis_height))
dis.blit(bg_img, (0, 0))

def _collisions_setup():
    
    groundRect = 0
    setup_list = []
    rectList = [(0,208,1103,208),(1136,208,239,208),(1424,208,1023,208),(2480,208,895,208)]

    for x in rectList:
        groundRect = pg.Rect(x)
        setup_list.append(groundRect)
    
    return setup_list

m_ground = _collisions_setup()

def _check_collisions(char_rect):
    ground = m_ground
    temp = False
    for x in ground:
        if pg.Rect.colliderect(x, char_rect):
            temp = True

    return temp
            

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

    dino_sheet = pg.image.load(os.path.normpath(cwd+'/pygame/dino_game/assets/DinoSprites.png')).convert_alpha()
    
    d_idle_list = []
    d_walk_list = []
    d_jump_list = []
    d_run_list = []
    d_size_modif = 1.5

    #Assign sprites
    d_idle_list.append(_image_at(dino_sheet, 0, 24, 24, d_size_modif, False))
    d_idle_list.append(_image_at(dino_sheet, 0, 24, 24, d_size_modif, True))
    d_walk_list.append(_image_at(dino_sheet, 5, 24, 24, d_size_modif, False))
    d_walk_list.append(_image_at(dino_sheet, 6, 24, 24, d_size_modif, False))
    d_walk_list.append(_image_at(dino_sheet, 7, 24, 24, d_size_modif, False))
    d_walk_list.append(_image_at(dino_sheet, 8, 24, 24, d_size_modif, False))
    d_walk_list.append(_image_at(dino_sheet, 9, 24, 24, d_size_modif, False))
    d_jump_list.append(_image_at(dino_sheet, 11, 24, 24, d_size_modif, False))
    d_jump_list.append(_image_at(dino_sheet, 12, 24, 24, d_size_modif, False))
    d_jump_list.append(_image_at(dino_sheet, 11, 24, 24, d_size_modif, True))
    d_jump_list.append(_image_at(dino_sheet, 12, 24, 24, d_size_modif, True))
    d_run_list.append(_image_at(dino_sheet, 17, 24, 24, d_size_modif, False))
    d_run_list.append(_image_at(dino_sheet, 18, 24, 24, d_size_modif, False))
    d_run_list.append(_image_at(dino_sheet, 19, 24, 24, d_size_modif, False))
    d_run_list.append(_image_at(dino_sheet, 20, 24, 24, d_size_modif, False))
    d_run_list.append(_image_at(dino_sheet, 21, 24, 24, d_size_modif, False))
    d_run_list.append(_image_at(dino_sheet, 22, 24, 24, d_size_modif, False))
    d_run_list.append(_image_at(dino_sheet, 23, 24, 24, d_size_modif, False))
    d_run_list.append(_image_at(dino_sheet, 17, 24, 24, d_size_modif, True))
    d_run_list.append(_image_at(dino_sheet, 18, 24, 24, d_size_modif, True))
    d_run_list.append(_image_at(dino_sheet, 19, 24, 24, d_size_modif, True))
    d_run_list.append(_image_at(dino_sheet, 20, 24, 24, d_size_modif, True))
    d_run_list.append(_image_at(dino_sheet, 21, 24, 24, d_size_modif, True))
    d_run_list.append(_image_at(dino_sheet, 22, 24, 24, d_size_modif, True))
    d_run_list.append(_image_at(dino_sheet, 23, 24, 24, d_size_modif, True))

    return d_idle_list, d_walk_list, d_jump_list, d_run_list
    
all_animation_lists = _animation_setup()
d_idle = all_animation_lists[0]
d_walk = all_animation_lists[1]
d_jump = all_animation_lists[2]
d_run = all_animation_lists[3]

def _move_char(flip, x, y, anim_num, dino_run):
    #Define
    change = 0
    speed = 8
    char_img = ""

    if dino_run:
        speed = 12

    #Moving left or right based on input + cycling animation
    anim_num += 1
    if anim_num > 4:
        anim_num = 0
    if flip:
        speed = -speed
    change = speed
    x += change

    if not dino_run:
        char_img = pg.transform.flip(d_walk[anim_num], flip, False)
    else:
        char_img = pg.transform.flip(d_run[anim_num], flip, False)
    char_img.set_colorkey((0, 0, 0))
    char_temp = [char_img, x, y, anim_num]

    return char_temp

def _jump(dire, grounded, x, y, anim_list, dino_run, dino_rect):
    #Define
    speed = 8
    change = 0
    jump_up = -15
    anim_num_j = -1
    anim_change = 0

    if dino_run:
        speed = 12

    if dire == "left":
        speed = -speed
        anim_change = 2
        cur_dir = "left"
    else:
        cur_dir = "right"
    change = speed
    
    grounded = False
    while not grounded:
        if jump_up > 0:
            y += 0.1 * (jump_up**2)
            anim_num_j = 0 + anim_change
        elif jump_up < 0:
            y -= 0.1 * (jump_up**2)
            anim_num_j = 1 + anim_change
        jump_up += 1
        x += change
        dis.blit(bg_img, (0, 0))
        dis.blit(anim_list[anim_num_j], (x, y))
        dinoRect = (x + 10, y + 10, d_width, d_height)
        grounded = _check_collisions(dino_rect)
        pg.draw.rect(dis, (0,0,255), (0,208,1103,208))
        pg.draw.rect(dis, (255,0,0), dinoRect)
        pg.display.flip()    
        pg.time.delay(50)
        dino_rect = (x, y, d_width, d_height)
        grounded = _check_collisions(dino_rect)
        #if y >= S.dis_height / 2:
            #y = S.dis_height / 2
            #grounded = True
        keys = pg.key.get_pressed()
    pg.time.delay(10)
    if keys[pg.K_RIGHT]:
        cur_dir = "right"
    elif keys[pg.K_LEFT]:
        cur_dir = "left"
    return x, y, cur_dir
        


while run:

    keys = pg.key.get_pressed()
    
    if keys[pg.K_RIGHT]:
        direction = "right"    
    elif keys[pg.K_LEFT]:
        direction = "left"

    for event in pg.event.get():    
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                run = False
            elif event.key == pg.K_UP:
                jump = True
                delay = True

    if direction == "right":
        if jump:
            if keys[K_LSHIFT]:
                m_run = True
            jump_return = _jump(last_dir, m_grounded, xpos, ypos, d_jump, m_run, dinoRect)
            action = ""
            xpos = jump_return[0]
            ypos = jump_return[1]
            last_dir = jump_return[2]
            jump = False
            m_run = False
        else:
            if keys[K_LSHIFT]:
                m_run = True
            char = _move_char(False, xpos, ypos, a_num, m_run)
            last_dir = "right"
            a_num = -1
            leftOrRight = True
            xpos = char[1]
            ypos = char [2]
            a_num = char[3]
            dis.blit(bg_img, (0, 0))
            dis.blit(char[0], (xpos, ypos))
            m_run = False
    elif direction == "left":
        if jump:
            if keys[K_LSHIFT]:
                m_run = True
            jump_return = _jump(last_dir, m_grounded, xpos, ypos, d_jump, m_run, dinoRect)
            action = ""
            xpos = jump_return[0]
            ypos = jump_return[1]
            last_dir = jump_return[2]
            jump = False
            m_run = False
        else:
            if keys[K_LSHIFT]:
                m_run = True
            char = _move_char(True, xpos, ypos, a_num, m_run)
            last_dir = "left"
            a_num = -1
            leftOrRight = True
            xpos = char[1]
            ypos = char [2]
            a_num = char[3]
            dis.blit(bg_img, (0, 0))
            dis.blit(char[0], (xpos, ypos))
            m_run = False
    
    if not leftOrRight and jump:
        for x in range(-15, 0, 1):
            ypos -= 0.1 * (x**2)
            if last_dir == "left":
                a_num = 2
            else:
                a_num = 0
            dis.blit(bg_img, (0, 0))
            dis.blit(d_jump[a_num], (xpos, ypos))
            pg.display.flip()
            pg.time.delay(50)
        m_grounded = False
        while m_grounded == False:
            ypos += 0.1 * (falling_modifier**2)
            if last_dir == "left":
                a_num = 3
            else:
                a_num = 1
            falling_modifier += 1
            dis.blit(bg_img, (0, 0))
            dis.blit(d_jump[a_num], (xpos, ypos))
            pg.draw.rect(dis, (0,0,255), (0,208,1103,208))
            pg.draw.rect(dis, (255,0,0), dinoRect)
            pg.display.flip()
            pg.time.delay(50)
            m_grounded = _check_collisions((dinoRect))
        falling_modifier = 1
        jump = False


    if not leftOrRight:
        dis.blit(bg_img, (0, 0))
        if last_dir == "right":
            dis.blit(d_idle[0], (xpos, ypos))
        elif last_dir == "left":
            dis.blit(d_idle[1], (xpos, ypos))

    direction = ""            
    leftOrRight = False

    if delay == True:
        pg.event.clear()
        delay = False

    dinoRect = pg.Rect(xpos + 10, ypos + 10, d_width, d_height)

    m_grounded = _check_collisions(dinoRect)

    while m_grounded == False:
        ypos += 0.1 * (falling_modifier**2)
        if last_dir == "left":
            a_num = 3
        else:
            a_num = 1
        falling_modifier += 1
        dis.blit(bg_img, (0, 0))
        dis.blit(d_jump[a_num], (xpos, ypos))
        dinoRect = pg.Rect(xpos + 10, ypos + 10, d_width, d_height)
        pg.draw.rect(dis, (0,0,255), (0,208,1103,208))
        pg.draw.rect(dis, (255,0,0), dinoRect)
        pg.display.flip()
        pg.time.delay(50)
        m_grounded = _check_collisions((dinoRect))
    falling_modifier = 1

    #TESTING
    pg.draw.rect(dis, (0,0,255), (0,208,1103,208))
    pg.draw.rect(dis, (255,0,0), dinoRect)

    pg.display.flip()                   

pg.quit()