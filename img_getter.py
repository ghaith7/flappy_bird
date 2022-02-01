import os
import pygame


file_List=os.listdir("imgs")

all_imgs = []
for f in file_List:
    img = pygame.image.load(os.path.join("imgs",f))
    all_imgs.append(pygame.transform.scale2x(img))

BIRD_IMGs = [all_imgs[2],all_imgs[3],all_imgs[4]]
PIPE_IMG = all_imgs[5]
BASE_IMG = all_imgs[0]
BG_IMG = all_imgs[1]