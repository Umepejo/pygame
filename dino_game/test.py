import pygame as pg
from pygame.constants import K_UP
from settings import Settings
import math
pg.init()

dis = pg.display.set_mode((Settings.dis_width, Settings.dis_height))
dis.fill(Settings.background)

xsize = 40
ysize = 40

run = True

tick = 0

xpos = Settings.dis_width / 2
ypos = Settings.dis_width / 2

ball_rect = pg.Rect(ypos, xpos, xsize, ysize)
pg.draw.rect(dis, (0,0,0), ball_rect)

while run:
    jump_up = -5
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == K_UP:
                while jump_up < 5:
                    if jump_up < 0:
                        ypos += -jump_up**2
                    elif jump_up > 0:
                        ypos += jump_up**2
                    #ypos * -1
                    jump_up += 1
                    ball_rect = pg.Rect(xpos, ypos, xsize, ysize)
                    dis.fill(Settings.background)
                    pg.draw.rect(dis, (0,0,0), ball_rect)
                    pg.time.delay(1000)
                    pg.display.flip()

    pg.display.flip()
pg.quit()