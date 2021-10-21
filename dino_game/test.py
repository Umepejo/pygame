import os
import pygame as pg

pg.init()

d_run_list = []

dis = pg.display.set_mode((600,600))

cwd = os.getcwd()

print(cwd)

def image_at(sheet, number, width, height, scale):
    #Make blank and blit image on blank
    image = pg.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((number * width), 0, 24, 24))
    #Modify sprite to "perfection"
    image = pg.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((0, 0, 0))
    return image


dino_sheet = pg.image.load(cwd+'/dino_game/assets/DinoSprites.png').convert_alpha()

while True:
    d_run_list.append(image_at(dino_sheet, 5, 24, 24, 3))
    d_run_list.append(image_at(dino_sheet, 6, 24, 24, 3))
    d_run_list.append(image_at(dino_sheet, 7, 24, 24, 3))
    d_run_list.append(image_at(dino_sheet, 8, 24, 24, 3))
    d_run_list.append(image_at(dino_sheet, 9, 24, 24, 3))
    d_run_list.append(image_at(dino_sheet, 10, 24, 24, 3))
    cd = pg.time.Clock().tick()
    print(cd)