import pygame as pg
import os
import random
import math
import numpy as np
import pandas as pd

pg.init()
### --- Window definitions --- ###
width = 600
height = 600
screen = pg.display.set_mode((width, height))

def write(text, x, y, size):
    """This function writes a text message in a specified location"""
    cz = pg.font.SysFont("Arial", size)
    rend = cz.render(text, 1, (255, 0, 0))
    screen.blit(rend, (x, y))

class obstacle():
    """This class represents a pair of obstacles faced by the players. The y dimensions are randomly generated"""
    def __init__(self, x):
        self.x = x
        self.width = 50
        self.y_up = 0
        self.h_up = random.randint(50, 350)
        self.space = 150 # This parameter determines the space between upper and lower obstacles
        self.y_down = self.h_up + self.space
        self.h_down = height - self.y_down
        self.color = (160, 140, 190)
        self.shape_up = pg.Rect(self.x, self.y_up, self.width, self.h_up)
        self.shape_down = pg.Rect(self.x, self.y_down, self.width, self.h_down)
        self.shape_score = pg.Rect(self.x, self.y_up, self.width, 600)
        self.scored = 0
    def draw(self):
        pg.draw.rect(screen, self.color, self.shape_up, 0)
        pg.draw.rect(screen, self.color, self.shape_down, 0)
        pg.draw.rect(screen, (0, 0, 200), self.shape_score, 1)
    def movement(self, v):
        self.x = self.x - v
        ### --- Shapes need to be updated as they are used for drawing and collision detection --- ###
        self.shape_up = pg.Rect(self.x, self.y_up, self.width, self.h_up)
        self.shape_down = pg.Rect(self.x, self.y_down, self.width, self.h_down)
        self.shape_score = pg.Rect(self.x, self.y_up, self.width, 600)
    def collision(self, player):
        if self.shape_up.colliderect(player.shape) or self.shape_down.colliderect(player.shape):
            return True
        else:
            return False
    def is_scored(self, player):
        """This method makes the player score if they go through the gap between obstacles. .scored attribute makes sure that each ostacle is counted only once"""
        if self.shape_score.colliderect(player.shape) and self.scored == 0:
            self.scored = 1
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
        """This method calculates the velocity of the player, taking into account the maximal velocity"""
        tempor = self.v - g
        if math.fabs(tempor) > math.fabs(self.v_max) and tempor < 0:
            self.v = -self.v_max
        elif math.fabs(tempor) > math.fabs(self.v_max) and tempor > 0:
            self.v = self.v_max
        else:
            self.v = tempor
    def impulse(self, imp):
        """This method implements the vertical velocity input that the player provides"""
        self.v = self.v + imp
    def move(self):
        self.x = self.x # For the player there is no horizontal movement of helicopter as only the obstacles move in that direction
        self.y = self.y - self.v
        self.shape = pg.Rect(self.x, self.y, self.width, self.height)

class environment():
    """This class holds the parameters describing the environment. It is used for learning"""
    def __init__(self, player, next_obstacle, width, height):
        self.dx_norm = (next_obstacle.x - player.x)#/width
        self.dy_norm = (next_obstacle.y_down - player.y)#/height
        self.v_norm = player.v#/1
    def give_env(self):
        tempor = [self.dx_norm, self.dy_norm, self.v_norm]
        return tempor
    def get_discrete(self, discrete_os_win_size, min_values):
        state = [self.dx_norm, self.dy_norm, self.v_norm]
        discrete_state = (np.array(state) - np.array(min_values))/np.array(discrete_os_win_size)
        #discrete_state = discrete_state - 1 # This is to ensure proper indexing
        return tuple(discrete_state.astype(np.int))


### --- Initial game setup --- ###

whatShows = 'menu'
mod = 11 # This variable controls how spaced the obstacles are

### --- Q learning setup --- ###
### --- 3 environment parameters implies 3 dimensional matrix. For each set of int there are 2 actions - jump or not jump --- ###
LEARNING_RATE = 0.5
reward = 0
DISCOUNT = 0.95
EPISODES = 50000
dim_env = [100] * 3
dim_act = 2
max_x = (mod-1) * width/20
max_y = height
v_max = 1 # This is determined by the bird class
min_x = -30 # This is determined by the bird class
min_y = -height
v_min = -1 # This is determined by the bird class
discrete_os_win_size = np.array([max_x - min_x, max_y - min_y, v_max - v_min]) / np.array(dim_env) # This discretises the environment variables
min_values = [min_x, min_y, v_min]
Q = np.random.uniform(low = -2, high = 0, size = list(np.array(dim_env) + 1) + [dim_act]) #As the reward is -1000 when the agent loses and 0 otherwise, those values do not matter much as long as they are inbetween -1000 and 0



render_modulo = 500
EPISODES = 10000
episode = 0
moving_avg_range = 100
results = {'Episode': [], 'Score': [], 'MAVG': []}
while episode < EPISODES:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if whatShows == 'menu':
                    whatShows = 'gameplay'
                    v_screen = 1
                    score = 0
                    imp_value = 0.1
                    g = 1
                    player = bird(300, 300)
                    clicked = 0
                    obstacles = []
                    for i in range(0, 21):
                        if i % mod == 0:
                            obstacles.append(obstacle(int(i * width / 20)))  # Generation of initial obstacles

    screen.fill((0,0,0))

    if whatShows == 'menu':
        graphic = pg.image.load(os.path.join('logo.png'))
        screen.blit(graphic, (0, 0))
        write('Press space to start', 200, 450, 20)
        pg.display.update()
    elif whatShows == 'gameplay':
        next_obstacle_x = -1000
        for o in obstacles:
            if o.x > player.x and next_obstacle_x < o.x:  # This clause spots the next obstacle on the way of the player - neccessary for the environment variable
                next_obstacle = o
                next_obstacle_x = o.x
        environ = environment(player, next_obstacle, width, height)
        state = environ.get_discrete(discrete_os_win_size, min_values)
        action = np.argmax(Q[state])

        ### --- The value of impulse needs to be comparable to value of g. If g is far smaller then in initiate random state the agent will go up in most of cases --- ###
        ### --- It will hence take far longer for the agent to notice the states in the lower part of the game space. If g is far larger than impulse the reverse will happen --- ###
        if action == 0:
            imp_value = 0
        else:
            imp_value = 2

        ### --- Updating the game --- ###
        for o in obstacles:
            o.movement(v_screen)
            o.draw()
            if o.collision(player):
                whatShows = 'gameover'
                episode = episode + 1
            if o.is_scored(player):
                score = score + 1
        if player.y > height or player.y < 0:  # If player gets out of bonds
            whatShows = 'gameover'
            episode = episode + 1
        next_obstacle_x = -10000
        for o in obstacles:
            if o.x > player.x and next_obstacle_x < o.x:  # This clause spots the next obstacle on the way of the player - neccessary for the environment variable
                next_obstacle = o
                next_obstacle_x = o.x
            elif o.x <= -o.width:  # This clause detects if the obstacle has left the screen and then spawns the next obstacle
                obstacles.remove(o)
                obstacles.append(obstacle(width))
        player.impulse(imp_value)
        player.physics()
        player.move()

        ### --- Getting new state --- ###
        environ_new = environment(player, next_obstacle, width, height)
        new_state = environ_new.get_discrete(discrete_os_win_size, min_values)

        if not whatShows == 'gameover':
            ### --- This clause applies the Q - learning formula --- ###
            max_future_q = np.max(Q[new_state])
            current_q = Q[state + (action,)]
            new_q = (1-LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            Q[state + (action,)] = new_q
        if whatShows == 'gameover':
            Q[state + (action,)] = -1000 # If the agent loses it is penalised. If the reward is not a positive number this value is not crucial as long as it is < 0

        ### --- This sets up a new game if the agent has lost and collects episode data --- ###
        if whatShows != 'gameplay':
            results['Episode'].append(episode)
            results['Score'].append(score)
            tempor = sum(results['Score'][-moving_avg_range:])/len(results['Score'][-moving_avg_range:])
            results['MAVG'].append(tempor)
            whatShows = 'gameplay'
            score = 0
            player = bird(300, 300)
            clicked = 0
            obstacles = []
            for i in range(0, 21):
                if i % mod == 0:
                    obstacles.append(obstacle(int(i * width / 20)))  # Generation of initial obstacles

        ### --- This clause contains all the graphic representation of the game and renders only in certain conditions to minimise computing time --- ###
        if True:#episode % render_modulo == 0:
            write('score : ' + str(score), 50, 20, 20)
            write('episode = ' + str(episode), 50, 50, 20)
            write('state = ' + str(environ.give_env()), 50, 70, 20)
            if len(results['MAVG']) > 0:
                write('mavg = ' + str(results['MAVG'][-1]), 50, 90, 20)
            player.draw()
            pg.display.update()
output = pd.DataFrame(results)
output.to_csv(os.path.join('./iteration_score.csv'))