from math import dist, sqrt
from re import A
import pygame
from classes import minesweeper, system, bfs
from random import randrange
from geneticAlgorythm import geneticAligouwu

class AI:
    window:system.Window
    current_map:minesweeper.Map
    saper:minesweeper.Minesweeper

    the_way:list
    
    #jak True to można się poruszać strzałkami, jak False sam się porusza
    user_controlled=False
    
    def __init__(self, window, current_map, saper):
        self.window = window
        self.current_map = current_map
        self.saper = saper
        whereMines = []
        for encounter in current_map.encounters:
            whereMines.append((encounter.position_x, encounter.position_y))
        self.route = geneticAligouwu(whereMines)

    def giveNextDestination(self):
        x = self.route.pop(0)
        return x

    
    
    #co ma zrobić tylko na początku
    def ready(self):
        self.saper.set_map(self.current_map)
        self.bfs()
    
    #co ma robić przy każdym FPS'ie
    def updateFPS(self):
        pass

    #co ma zrobić przy każdym ruchu <------------------------- najważniejsze
    def updateTile(self, model):
        #aktualne pola (do debugu)
        sensor = self.saper.sensor()

        #print(sensor[0])
        #print(sensor[1])
        #print(sensor[2])
        #print("-------")


        #podniesienie bomby jeśli jest jakaś na tym polu
        self.saper.pick_up(model)

        #poruszenie się
        if self.user_controlled:
            self.minesweeper_controls()
            return
        self.way_controls()
        
            
    def minesweeper_controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.saper.move(0)
        elif keys[pygame.K_UP]:
            self.saper.move(180)
        elif keys[pygame.K_LEFT]:
            self.saper.move(270)
        elif keys[pygame.K_RIGHT]:
            self.saper.move(90)
    
    def chaos_controls(self):
        dir = randrange(4)
        if dir==0:
            self.saper.rotate("N")
        elif dir==1:
            self.saper.rotate("S")
        elif dir==2:
            self.saper.rotate("W")
        elif dir==3:
            self.saper.rotate("E")
        self.saper.move()

    def way_controls(self):
        if type(self.the_way) is list and len(self.the_way)>0:
            way = self.the_way.pop(0)
            if way=="move":
                self.saper.move()
            elif way=="left" or way=="right":
                self.saper.rotate(way)
            else:
                self.saper.rotate(way)
                self.saper.move()
        elif len(self.current_map.encounters)!=0:
            self.bfs()

            
    
    def bfs(self):
        goal_state = [0,0]
        goal_stateTemp = self.giveNextDestination()
        goal_state[0] = goal_stateTemp[0]
        goal_state[1] = goal_stateTemp[1]
        print(f'We go to {goal_state}')

        find_path = bfs.BFS(self.saper, self.window)
        tmp = find_path.graphsearch([], [], bfs.BFS.successor, goal_state)
        #print(f'tmp = {tmp}')
        if tmp is None:
            raise Exception("Error, path does not exist")
        else:
            self.the_way = tmp