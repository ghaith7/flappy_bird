import pygame
import neat
import time
import os
import random
from bird import Bird 
from img_getter import *
from pipe import *
pygame.font.init()
WIN_Height = 800
WIN_Width = 500
gen = 0



class Base:
    velocity = 5
    width = BASE_IMG.get_width()
    img = BASE_IMG
    def __init__ (self,y):
        self.y  = y
        self.x1 = 0
        self.x2 = self.width
    def move(self):
        self.x1 = self.x1 - self.velocity
        self.x2 = self.x2 - self.velocity
        if(self.x1+self.width<0):
            self.x1 = self.x2 + self.width
        if(self.x2+self.width<0):
            self.x2 = self.x1 + self.width
    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))
        pygame.display.update()


def draw_window(win, birds,pipes,base,score,gen):
    win.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    text  = pygame.font.SysFont("comicsans",40).render("score : "+ str(score),1,(255,255,255))
    win.blit(text,(WIN_Width-10-text.get_width(),10))
    text  = pygame.font.SysFont("comicsans",40).render("gens : "+ str(gen),1,(255,255,255))
    win.blit(text,(10   ,10))
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()


def main(genomes,config):
    birds = []
    nets = []
    ge = []
    global gen
    gen = gen +1    
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes =[Pipe(700)]

    run =True
    win = pygame.display.set_mode((WIN_Width,WIN_Height))
    clock  = pygame.time.Clock()

    score = 0
    while(run):
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        rem=[]
        add_pipe = False
        pipe_ind = 0
        if( len(birds)>0):
            if len(pipes)>1 and birds[0].x>pipes[0].x+pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run=False
            break
        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness+=0.1
            output = nets[x].activate((bird.y, abs(bird.y-pipes[pipe_ind].height),abs(bird.y-pipes[pipe_ind].bottom)))
            if output[0]>0.5:
                bird.jump()
        for pipe in pipes:
            for x,bird in  enumerate(birds) : 
                if pipe.collide(bird) : 
                    ge[x].fitness-=1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not birds==[]:
                    if not pipe.passed and pipe.x<birds[0].x:
                        pipe.passed = True
                        add_pipe = True
            if pipe.x + pipe.PIPE_BOTTOM.get_width() < 0 : 
                rem.append(pipe)
            pipe.move()
        if add_pipe:
            pipes.append(Pipe(650))
            score +=1
            for g in ge:
                g.fitness += 5
        for r in rem:
            pipes.remove(r)
        for x,bird in enumerate( birds):
            if bird.y +bird.img.get_height()> 730 or bird.y<0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        bird.move()
        base.move()
        draw_window(win,birds,pipes,base,score,gen)

    


def run():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join("config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
                            neat.DefaultSpeciesSet,neat.DefaultStagnation,
                            config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)


if __name__ ==  "__main__":
    run()