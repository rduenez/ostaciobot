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
    WINDOWS_TITLE = 'Ostaciobot v0.0'

    #Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND = WHITE

    COLS = 20;
    ROWS = 20;


    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption(self.WINDOWS_TITLE)
        pygame.init()
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.clock = pygame.time.Clock()
        self.init()

    def init(self):
        self.done = False

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
