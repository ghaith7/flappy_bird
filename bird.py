from img_getter import *
import pygame


class Bird():
    imgs=BIRD_IMGs
    max_rot = 25
    rot_velocity = 20
    animation_time = 5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt = 0
        self.tick_count = 0
        self.vel  = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.imgs[0]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        dist  = self.vel * self.tick_count + 1.5*self.tick_count**2
        if(dist>16):
            dist = 16
        if(dist<0):
            dist =dist - 2
        self.y=self.y+dist
        if dist <0 or self.y<self.height+50:
            if self.tilt < self.max_rot:
                self.tilt = self.max_rot
        else : 
            if self.tilt>-90 :
                self.tilt = self.tilt - self.rot_velocity
    def draw(self,win):
        self.img_count = self.img_count+1
        if( self.img_count<self.animation_time):
            self.img = self.imgs[0]
        elif self.img_count<self.animation_time*2:
            self.img = self.imgs[1]
        elif self.img_count<self.animation_time*3:
            self.img = self.imgs[2]
        elif self.img_count<self.animation_time*4:
            self.img = self.imgs[1]
        elif self.img_count==self.animation_time* 4 +1:
            self.img = self.imgs[0]
            self.img_count=0
        
        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
