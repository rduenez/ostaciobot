import os
import pygame
from pygame.locals import *
from random import randint
import sys

#get linear position from a node over the map
def get_line_position(r, c):
    return (Game.COLS*r)+c

#get row and column from a linear node
def get_row(lp):
    return lp // Game.COLS

def get_column(lp):
    return lp % Game.COLS

class Game(object):

    #Animation properties
    FRAMES_PER_SECOND = 60

    #Canvas/Map Properties
    WIDTH, HEIGHT = 1000, 750
    MAP_BORDER = 10

    #Window Properties
    RESOLUTION = WIDTH + 100,HEIGHT
    WINDOWS_TITLE = 'Ostaciobot v1.0'

    #Colors
    WHITE = (255, 255, 255)
    #Color before black after purple
    BLACK = (128, 0, 128)
    FIREBRICK = (170, 13, 3)
    STEELBLUE = (70,130,180)
    FORESTGREEN = (34, 139, 34)
    GOLD = (255, 215, 0)
    DARKSLATEBLUE = (72, 61, 139)
    PALEGOLDENROAD = (238, 232, 170)
    DARKBLUE = (0, 0, 139)
    LIGHTSLATEGRAY = (119, 136, 153)
    LIGHTYELLOW = (255,255,116)
    TOMATO = (255, 99, 71)
    ORANGE = (255, 165, 0)
    LIME = (50, 205, 50)

    BACKGROUND = WHITE
    TRACE_MARK	= 6;

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
    BATTERY_STEPS = 100;
    #movements
    MOVES = 4;
    UP = 0;
    LEFT = 1;
    DOWN = 2;
    RIGHT = 3;

    #Path in graph values
    NOT_INIT = -1
    SHORTPATH = sys.maxsize-1

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption(self.WINDOWS_TITLE)
        pygame.init()
        script_path = os.path.dirname(os.path.realpath(__file__))
        font_path = os.path.join(script_path, "digital-7.ttf")
        font_size = 36
        self.font = pygame.font.Font(font_path, font_size)
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.clock = pygame.time.Clock()
        self.map = [[0 for x in range(self.COLS)] for y in range(self.ROWS)]
        #Dijkstra lists
        self.adjacency_matrix = [[0 for x in range(self.MOVES)] for y in range(self.ROWS*self.COLS)]
        self.distance = [None]*(self.ROWS*self.COLS)
        self.visited = [None]*(self.ROWS*self.COLS)
        self.node_sequence = [None]*(self.ROWS*self.COLS);
        self.init()

    def init(self):
        self.done = False
        self.found = False
        self.win = False

        #Dijkstra lists
        for i in range (0,(self.ROWS*self.COLS)):
            self.distance[i]=sys.maxsize;
            self.node_sequence[i]=self.NOT_INIT;
            self.visited[i]=False;

        for i in range (0,(self.ROWS*self.COLS)):
            for j in range (0,self.MOVES):
                self.adjacency_matrix[i][j]=sys.maxsize;

        for i in range(0,self.ROWS):
            for j in range(0,self.COLS):
                self.map[i][j] = self.CLEAR

        self.initial_i = randint(0,self.ROWS-1);
        self.initial_j = randint(0,self.COLS-1);

        self.battery = self.BATTERY_STEPS;

        self.current_i = self.initial_i;
        self.current_j = self.initial_j;

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

        if keys[K_SPACE] or keys[K_b]:
             self.battery = self.BATTERY_STEPS
        if keys[K_BACKSPACE] or keys[K_r]:
            self.init()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return
        # TODO: Handle players events here

        if (self.battery <= 0):
            return

        #check if target was found
        if(not self.found):
            #search for the target or increase visit count
            if(self.map[self.current_i][self.current_j]!=self.TARGET):
                self.map[self.current_i][self.current_j]+=1;
            else:
                self.found=True
                #calculate shortest route from current to landing spot
                self.clear_adjacency()
                self.dijkstra(get_line_position(self.initial_i,self.initial_j),get_line_position(self.current_i,self.current_j))
                return

            #locate slot with the lower visit count
            lower_visited = sys.maxsize

            for movs in range (0,self.MOVES):
                if (movs==self.UP):
                    if(self.current_i > 0):
                        if(self.map[self.current_i-1][self.current_j]<lower_visited):
                            lower_visited=self.map[self.current_i-1][self.current_j];
                if (movs==self.LEFT):
                    if(self.current_j > 0):
                        if(self.map[self.current_i][self.current_j-1]<lower_visited):
                            lower_visited=self.map[self.current_i][self.current_j-1];
                if (movs==self.DOWN):
                    if(self.current_i < self.ROWS - 1):
                        if(self.map[self.current_i+1][self.current_j]<lower_visited):
                            lower_visited=self.map[self.current_i+1][self.current_j];
                if (movs==self.RIGHT):
                    if(self.current_j < self.COLS - 1):
                        if(self.map[self.current_i][self.current_j+1]<lower_visited):
                            lower_visited=self.map[self.current_i][self.current_j+1];

            #append to a list the movement on slots with same visit count (lowest)
            directions = [];

            for movs in range (0,self.MOVES):
                if (movs==self.UP):
                    if(self.current_i > 0):
                        if(self.map[self.current_i-1][self.current_j]==lower_visited):
                            directions.append(movs);
                if (movs==self.LEFT):
                    if(self.current_j > 0):
                        if(self.map[self.current_i][self.current_j-1]==lower_visited):
                            directions.append(movs);
                if (movs==self.DOWN):
                    if(self.current_i < self.ROWS - 1):
                        if(self.map[self.current_i+1][self.current_j]==lower_visited):
                            directions.append(movs);
                if (movs==self.RIGHT):
                    if(self.current_j < self.COLS - 1):
                        if(self.map[self.current_i][self.current_j+1]==lower_visited):
                            directions.append(movs);

            #generate the direction to be taken based on random suggested move
            movement = directions[randint (0,len(directions)-1)]

            #bot moves marking the new slot and considering constraints
            if (movement==self.UP):
                if(self.current_i > 0):
                    self.adjacency_matrix[get_line_position(self.current_i,self.current_j)][self.UP]=1;
                    self.adjacency_matrix[get_line_position(self.current_i-1,self.current_j)][self.DOWN]=1;
                    self.current_i-=1;
            if (movement==self.LEFT):
                if(self.current_j > 0):
                    self.adjacency_matrix[get_line_position(self.current_i,self.current_j)][self.LEFT]=1;
                    self.adjacency_matrix[get_line_position(self.current_i,self.current_j-1)][self.RIGHT]=1;
                    self.current_j-=1;
            if (movement==self.DOWN):
                if(self.current_i < self.ROWS - 1):
                    self.adjacency_matrix[get_line_position(self.current_i,self.current_j)][self.DOWN]=1;
                    self.adjacency_matrix[get_line_position(self.current_i+1,self.current_j)][self.UP]=1;
                    self.current_i+=1;
            if (movement==self.RIGHT):
                if(self.current_j < self.COLS - 1):
                    self.adjacency_matrix[get_line_position(self.current_i,self.current_j)][self.RIGHT]=1;
                    self.adjacency_matrix[get_line_position(self.current_i,self.current_j+1)][self.LEFT]=1;
                    self.current_j+=1;

            self.battery -= 1;

        else:
            if(self.current_i == self.initial_i and self.current_j == self.initial_j):
                self.win=True;
                return;
            else:
                #Mark as visited while moving back
                if (self.map[self.current_i][self.current_j]!=self.TARGET):
                    self.map[self.current_i][self.current_j]=self.SHORTPATH;

                #get the next node to be marked
                val=get_line_position(self.current_i,self.current_j);
                prev=self.node_sequence[val];

                #get column and row
                self.current_i=get_row(prev);
                self.current_j=get_column(prev);

                self.battery -= 1;

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

                if(self.map[i][j]==self.SHORTPATH):
                    pygame.draw.rect(self.screen, self.FIREBRICK, rect)

                if (self.map[i][j]<(self.WALL-1) and self.map[i][j]>self.TARGET):
                    if (self.map[i][j]>=self.TRACE_MARK):
                        val = self.TRACE_MARK-1;
                    else:
                        val = self.map[i][j];
                    c = 255 - (val * 256//self.TRACE_MARK);
                    color = (c,c,c)
                    pygame.draw.rect(self.screen, color, rect)

                if (self.map[i][j]==self.TARGET):
                    pygame.draw.rect(self.screen, self.STEELBLUE, rect)

                if (i==self.initial_i and j==self.initial_j):
                    pygame.draw.rect(self.screen, self.FORESTGREEN, rect)

                if (i==self.current_i and j==self.current_j):
                    pygame.draw.rect(self.screen, self.GOLD, rect)

                #pygame.draw.rect(self.screen, self.BLACK, rect, 1)

        #Draw displays
        display_found = pygame.Rect((self.WIDTH+5,self.HEIGHT-40), (90,35))
        pygame.draw.rect(self.screen, self.PALEGOLDENROAD, display_found)
        pygame.draw.rect(self.screen, self.BLACK, display_found, 1)

        display_battery = pygame.Rect((self.WIDTH+5,self.HEIGHT-80), (90,35))
        pygame.draw.rect(self.screen, self.PALEGOLDENROAD, display_battery)
        pygame.draw.rect(self.screen, self.BLACK, display_battery, 1)

        display_done = pygame.Rect((self.WIDTH+5,self.HEIGHT-120), (90,35))
        pygame.draw.rect(self.screen, self.PALEGOLDENROAD, display_done)
        pygame.draw.rect(self.screen, self.BLACK, display_done, 1)


        if(self.found):
            surface_found = self.font.render('FOUND', False, self.DARKSLATEBLUE)
            rect = surface_found.get_rect( center = (self.WIDTH+50 , self.HEIGHT-25 ))
            self.screen.blit(surface_found, rect)

        if(self.battery <= 0):
            surface_battery = self.font.render('P OFF', False, self.DARKSLATEBLUE)
        elif (self.battery <= self.BATTERY_STEPS//5):
            surface_battery = self.font.render('P LOW', False, self.DARKSLATEBLUE)
        else:
            surface_battery = self.font.render('PW ON', False, self.DARKSLATEBLUE)
        rect = surface_battery.get_rect( center = (self.WIDTH+50 , self.HEIGHT-65 ))
        self.screen.blit(surface_battery, rect)

        if(self.win):
            surface_done = self.font.render('WIN', False, self.DARKSLATEBLUE)
            rect = surface_done.get_rect( center = (self.WIDTH+50 , self.HEIGHT-105 ))
            self.screen.blit(surface_done, rect)

        #Draw battery icon
        terminal = pygame.Rect((self.WIDTH+48,4),(12,6))
        jacket = pygame.Rect((self.WIDTH+44,10),(20,40))
        pygame.draw.rect(self.screen, self.LIGHTSLATEGRAY, terminal)
        pygame.draw.rect(self.screen, self.DARKBLUE, jacket)
        pygame.draw.line(self.screen, self.LIGHTYELLOW,(self.WIDTH+50,19),(self.WIDTH+57,19),2)
        pygame.draw.line(self.screen, self.LIGHTYELLOW,(self.WIDTH+53,16),(self.WIDTH+53,23),2)
        pygame.draw.line(self.screen, self.LIGHTYELLOW,(self.WIDTH+50,39),(self.WIDTH+57,39),2)

        #Draw battery indicator
        delta_bat = (self.HEIGHT-185) / self.BATTERY_STEPS

        if(self.battery > 0):
            indicator = pygame.Rect((self.WIDTH+40,((self.BATTERY_STEPS-self.battery)*delta_bat)+55),(30,self.battery*delta_bat))
            if(self.battery <= self.BATTERY_STEPS//5):
                pygame.draw.rect(self.screen, self.TOMATO, indicator)
            elif (self.battery <= self.BATTERY_STEPS//2):
                pygame.draw.rect(self.screen, self.ORANGE, indicator)
            else:
                pygame.draw.rect(self.screen, self.LIME, indicator)

        bar = pygame.Rect((self.WIDTH+40,55),(30,self.BATTERY_STEPS*delta_bat))
        pygame.draw.rect(self.screen, self.BLACK, bar, 1)

        pygame.display.flip()

    def wait(self):
        self.clock.tick(self.FRAMES_PER_SECOND)

    def clear_adjacency(self):
        for i in range(0,self.ROWS):
            for j in range (0,self.COLS):
                for movs in range (0,self.MOVES):
                    if (movs==self.UP):
                        if(i > 0):
                            if(self.map[i-1][j]>0 and self.map[i-1][j] != self.WALL):
                                self.adjacency_matrix[get_line_position(i,j)][self.UP]=1;
                    if (movs==self.LEFT):
                        if(j > 0):
                            if(self.map[i][j-1]>0 and self.map[i][j-1] != self.WALL):
                                self.adjacency_matrix[get_line_position(i,j)][self.LEFT]=1;
                    if (movs==self.DOWN):
                        if(i < self.ROWS - 1):
                            if(self.map[i+1][j]>0 and self.map[i+1][j] != self.WALL):
                                self.adjacency_matrix[get_line_position(i,j)][self.DOWN]=1;
                    if (movs==self.RIGHT):
                        if(j < self.COLS - 1):
                            if(self.map[i][j+1]>0 and self.map[i][j+1] != self.WALL):
                                self.adjacency_matrix[get_line_position(i,j)][self.RIGHT]=1;

    def dijkstra(self,origin,destination):
        current = origin
        shortest = sys.maxsize
        current_distance = self.distance[current]
        k = self.NOT_INIT
        new_distance = sys.maxsize

        self.distance[origin]=0
        self.node_sequence[origin]=origin
        self.visited[origin]=True

        while(current!=destination):
            shortest = sys.maxsize
            current_distance = self.distance[current]
            new_distance = sys.maxsize

            for i in range (0,(self.COLS*self.ROWS)):
                if(self.visited[i]==False):
                    if(i==current-self.COLS):
                        if(self.adjacency_matrix[current][self.UP]==sys.maxsize):
                            new_distance = sys.maxsize
                        else:
                            new_distance = current_distance+self.adjacency_matrix[current][self.UP]
                    elif(i==current-1):
                        if(self.adjacency_matrix[current][self.LEFT]==sys.maxsize):
                            new_distance = sys.maxsize
                        else:
                            new_distance = current_distance+self.adjacency_matrix[current][self.LEFT]
                    elif(i==current+self.COLS):
                        if(self.adjacency_matrix[current][self.DOWN]==sys.maxsize):
                            new_distance = sys.maxsize
                        else:
                            new_distance = current_distance+self.adjacency_matrix[current][self.DOWN]
                    elif (i==current+1):
                        if(self.adjacency_matrix[current][self.RIGHT]==sys.maxsize):
                            new_distance = sys.maxsize
                        else:
                            new_distance = current_distance+self.adjacency_matrix[current][self.RIGHT]
                    else:
                        new_distance=sys.maxsize

                    if(new_distance<self.distance[i]):
                        self.distance[i]=new_distance
                        self.node_sequence[i]=current

                    if(self.distance[i]<shortest):
                        shortest=self.distance[i]
                        k=i

            current=k;
            self.visited[current]=True;

def main():
    game = Game()
    while not game.done:
        game.update()
        game.draw()
        game.wait()

main()
