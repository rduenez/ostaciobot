import os
import pygame
from pygame.locals import *
from random import randint
import sys


class Game(object):

    #Animation properties
    FRAMES_PER_SECOND = 30

    #Canvas/Map Properties
    WIDTH, HEIGHT = 700, 700
    MAP_BORDER = 10

    #Window Properties
    RESOLUTION = WIDTH + 100,HEIGHT
    WINDOWS_TITLE = 'Ostaciobot v0.2'

    #Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FIREBRICK = (170, 13, 3)
    STEELBLUE = (70,130,180)
    FORESTGREEN = (34, 139, 34)
    GOLD = (255, 215, 0)
    BACKGROUND = WHITE

    #Map dimentions and values
    COLS = 20;
    ROWS = 20;
    WALLS = 100;

    #Slot values
    CLEAR = 0;
    TARGET = -sys.maxsize
    WALL = sys.maxsize

    #Bot internal values
    initial_i = 0;
    initial_j = 0;

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption(self.WINDOWS_TITLE)
        pygame.init()
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.clock = pygame.time.Clock()
        self.map = [[0 for x in range(self.COLS)] for y in range(self.ROWS)]
        self.init()

    def init(self):
        self.done = False
        for i in range(0,self.ROWS):
            for j in range(0,self.COLS):
                self.map[i][j] = self.CLEAR

        self.initial_i = randint(0,self.ROWS-1);
        self.initial_j = randint(0,self.COLS-1);

        for i in range (0,self.WALLS):
            barrier_i = randint(0,self.ROWS-1)
            barrier_j = randint(0,self.COLS-1)

            if(barrier_i!=self.initial_i and barrier_j!=self.initial_j):
                self.map[barrier_i][barrier_j]=self.WALL;

        destination_i = randint(0,self.ROWS-1);
        destination_j = randint(0,self.COLS-1);

        self.map[destination_i][destination_j]=self.TARGET;

    def update(self):
        # Handle exit events
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE] or keys[K_q]:
            self.done = True
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return
        # TODO: Handle players events here

    def draw(self):
        self.screen.fill(self.BACKGROUND)
        slot_width = ((self.WIDTH-self.MAP_BORDER)//self.COLS)
        slot_height = ((self.HEIGHT-self.MAP_BORDER)//self.ROWS)

        #Paint the map

        for i in range(0, self.ROWS):
            for j in range (0,self.COLS):
                position_x = j*slot_width
                position_y = i*slot_height
                rect = pygame.Rect((position_x+self.MAP_BORDER,position_y+self.MAP_BORDER), (slot_width,slot_height))

                if (self.map[i][j]==self.CLEAR):
                    pygame.draw.rect(self.screen, self.WHITE, rect)

                if (self.map[i][j]==self.WALL):
                    pygame.draw.rect(self.screen, self.BLACK, rect)

                if (self.map[i][j]==self.TARGET):
                    pygame.draw.rect(self.screen, self.STEELBLUE, rect)

                if (i==self.initial_i and j==self.initial_j):
                    pygame.draw.rect(self.screen, self.FORESTGREEN, rect)

                pygame.draw.rect(self.screen, self.BLACK, rect, 1)

        pygame.display.flip()

    def wait(self):
        self.clock.tick(self.FRAMES_PER_SECOND)

def main():
    game = Game()
    while not game.done:
        game.update()
        game.draw()
        game.wait()

main()
