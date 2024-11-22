import numpy as np
import pygame as pg
import time
import bird as bd
from arrow import draw_arrow

def ToroidalDistance (x1 : float, y1 : float, x2 : float, y2 : float):

    dx : float = (x2 - x1)
    dy : float = (y2 - y1)
 
    if (abs(dx) > 0.5 * SCREEN_WIDTH):
        dx = dx-SCREEN_WIDTH*np.sign(dx)
 
    if (abs(dy) > 0.5 * SCREEN_HEIGHT):
        dy = dy-SCREEN_HEIGHT*np.sign(dx)
 
    return dx, dy, np.sqrt(dx*dx + dy*dy)

def bird_intimidation(bird_1 : bd.Bird, bird_2 : bd.Bird):
    *distance, length   = ToroidalDistance(*bird_1.pos, *bird_2.pos)
    direction           = distance/np.linalg.norm(distance)
    auth_prop           = bird_2.auth/bird_1.auth
    within_distance     = (0.5+0.5*np.sign(100-length))
    if within_distance:
        desired_distance    = 50
        separation          = -50*np.exp(-length/desired_distance) * direction
        alignment           = 0.05*(bird_2.vel*auth_prop**2 - bird_1.vel)
        cohesion            = 50*np.exp((length-100)/desired_distance)* direction

        a = separation+alignment+cohesion
    else:
        a = 0
    acc_1 = a
    acc_2 = -a / auth_prop
    # print(a,acc_1,acc_2,auth_prop)

    return acc_1, acc_2

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH/2

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
surface = pg.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pg.SRCALPHA)

NUMBER_OF_BIRDS = 10
birdbox = np.zeros(NUMBER_OF_BIRDS, dtype = bd.Bird)
for i in range(NUMBER_OF_BIRDS):
    pos = np.random.uniform(size = 2) * np.array([SCREEN_WIDTH,SCREEN_HEIGHT])
    vel = np.random.uniform(-100,100,size = 2)
    acc = [0.0,0.0]
    auth = np.random.uniform(0.5,1)
    color = *np.random.uniform(0,255,3), 50+auth*50
    birdbox[i] = bd.Bird(pos, vel, acc, auth, color)

t = time.time()
run = True
while run:
    screen.fill((0,0,0))
    surface.fill((0,0,0))
    dt = time.time() - t
    t = time.time()

    for i, bird_1 in enumerate(birdbox):
        for bird_2 in birdbox[i+1:]:
            acc_1, acc_2 = bird_intimidation(bird_1, bird_2)
            bird_1.acc += acc_1
            bird_2.acc += acc_2

    for bird in birdbox:
        pg.draw.line(screen,bird.color,bird.pos,bird.pos+bird.acc)
        bird.update(dt)
        bird.fix_out_of_bounds(SCREEN_WIDTH,SCREEN_HEIGHT)
        pg.draw.circle(screen, bird.color,bird.pos,10)
        pg.draw.circle(screen, bird.color,bird.pos,50,1)



    print(f"Total momentum: {sum([bird.vel*bird.auth for bird in birdbox])}")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            exit()
    pg.display.update()





