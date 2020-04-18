import pygame as pg
import os
import random
import time
import math

pg.init()
### --- Window definitions --- ###
width = 600
height = 600
screen = pg.display.set_mode((width, height))

def write(text, x, y, size):
    """This functions writes a text message in a specified location"""
    cz = pg.font.SysFont("Arial", size)
    rend = cz.render(text, 1, (255, 0, 0))
    screen.blit(rend, (x, y))

class obstacle():
    """This class represents a pair of obstacles faced by the players. The y dimensions are randomly generated"""
    def __init__(self, x, width):
        self.x = x
        self.width = width
        self.y_up = 0
        self.h_up = random.randint(150, 250)
        self.space = 300 # This parameter determines the space between upper and lower obstacles
        self.y_down = self.h_up + self.space
        self.h_down = height - self.y_down
        self.color = (160, 140, 190)
        self.shape_up = pg.Rect(self.x, self.y_up, self.width, self.h_up)
        self.shape_down = pg.Rect(self.x, self.y_down, self.width, self.h_down)
    def draw(self):
        pg.draw.rect(screen, self.color, self.shape_up, 0)
        pg.draw.rect(screen, self.color, self.shape_down, 0)
    def movement(self, v):
        self.x = self.x - v
        ### --- Shapes need to be updated as they are used for drawing and collision detection --- ###
        self.shape_up = pg.Rect(self.x, self.y_up, self.width, self.h_up)
        self.shape_down = pg.Rect(self.x, self.y_down, self.width, self.h_down)
    def collision(self, player):
        if self.shape_up.colliderect(player.shape) or self.shape_down.colliderect(player.shape):
            return True
        else:
            return False

class bird():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 30
        self.width = 30
        self.shape = pg.Rect(self.x, self.y, self.width, self.height)
        self.sprite = pg.image.load(os.path.join('heli_sprite.png'))
        self.v = 0
        self.v_max = 1
    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
    def physics(self):
        self.v = self.v - g
        #if tempo
    def impulse(self, imp):
        self.v = self.v + imp
    def move(self):
        self.x = self.x # For the player there is no horizontal movement of helicopter as only the obstacles move in that direction
        self.y = self.y - self.v
        self.shape = pg.Rect(self.x, self.y, self.width, self.height)


### --- Initial game setup --- ###
whatShows = 'menu'
obstacles = []
for i in range(21):
    obstacles.append(obstacle(int(i * width/20), int(width/20))) # Generation of initial obstacles
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if whatShows != 'gameplay':
                    whatShows = 'gameplay'
                    v_screen = 1
                    dy = 0
                    points = 0
                    imp_value = 0.1
                    g = 0.01
                    player = bird(300, 300)
                    clicked = 0
                elif whatShows == 'gameplay' and clicked == 0:
                    imp_value = 2
                    clicked = 1
        if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            clicked = 0
            imp_value = 0

    screen.fill((0,0,0))

    if whatShows == 'menu':
        graphic = pg.image.load(os.path.join('logo.png'))
        screen.blit(graphic, (0, 0))
        write('Press space to start', 200, 450, 20)
    elif whatShows == 'gameover':
        write('Game over!, please press space to try again!', width/8, height/2, 20)
        write('Your score is ' + str(points), width / 8, 3 * height / 4, 20)
    elif whatShows == 'gameplay':
        for o in obstacles:
            o.movement(v_screen)
            o.draw()
            #if o.collision(player):
            #    whatShows = 'gameover'
        for o in obstacles:
            if o.x <= -o.width: # This clause detects if the obstacle has left the screen
                obstacles.remove(o)
                obstacles.append(obstacle(width, int(width/20)))
                points = points + math.fabs(dy)
        player.draw()
        player.physics()
        player.impulse(imp_value)
        imp_value = 0
        player.move()
        write('score : ' + str(points), 50, 20, 20)
        write('v = ' + str(player.v), 50, 50, 20)
        write('clicked = ' + str(clicked), 50, 70, 20)
        write('clicked = ' + str(imp_value), 50, 90, 20)
   # time.sleep(0.001) # This wait time is calibrated to provide the best experience
    pg.display.update()
