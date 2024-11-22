import numpy as np
import pygame as pg

class Bird:
    def __init__(self, pos, vel = [0,0], acc = [0,0], auth = 0.5, color = [255,255,255]):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.auth = auth
        self.color = color
        return
    
    def update(self,dt):
        self.pos += self.vel*dt
        self.vel += self.acc*dt
        self.acc = np.array([0.0,0.0])

        return
    
    def fix_out_of_bounds(self,width, height):
        self.pos = np.remainder(self.pos,[width,height])
        return