import os
import pygame
from pygame.locals import *
from random import randint


class Game(object):

    #Animation properties
    FRAMES_PER_SECOND = 30

    #Canvas/Map Properties
    WIDTH, HEIGHT = 700, 700

    #Window Properties
    RESOLUTION = WIDTH + 100,HEIGHT
    WINDOWS_TITLE = 'Ostaciobot v0.1'

    #Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FIREBRICK = (170, 13, 3)
    STEELBLUE = (70,130,180)
    FORESTGREEN = (34, 139, 34)
    GOLD = (255, 215, 0)
    BACKGROUND = WHITE

    #Map dimentions
    COLS = 20;
    ROWS = 20;

    #Slot values
    CLEAR = 0;


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
        slot_width = (self.WIDTH//self.COLS)
        slot_height = (self.HEIGHT//self.ROWS)

        #Paint the map

        for i in range(0, self.ROWS):
            for j in range (0,self.COLS):
                position_x = j*slot_width
                position_y = i*slot_height
                rect = pygame.Rect((position_x,position_y), (slot_width,slot_height))

                if (self.map[i][j]==self.CLEAR):
                    pygame.draw.rect(self.screen, self.WHITE, rect)

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
