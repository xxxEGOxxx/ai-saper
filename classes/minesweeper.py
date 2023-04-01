from tkinter import EventType
import pygame
from classes import system
from random import randrange
from classes import decisionTrees
from classes.neuralNetwork import NeuralNetwork

pygame.mixer.init()

class NotMine():

    position_x: int
    position_y: int
    size: int
    ismine: bool
    image_path: str
    image: pygame.surface.Surface
    font: pygame.font.Font
    done_text: pygame.surface.Surface

    def __init__(self, position_x, position_y, size):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.ismine = False
        self.image_path = "assets/sprites/notmines/" + str(randrange(1, 15)) + ".jpg"
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.font = pygame.font.SysFont('Comic Sans MS', int(self.size * 0.25))
        self.done_text = self.font.render("", False, (255,0,0))

    def draw(self, window):
        position_on_screen = (self.size * self.position_x, self.size * self.position_y)
        window.blit(self.image, position_on_screen)
        window.blit(self.done_text, (position_on_screen[0] + self.size / 4, position_on_screen[1] - self.size / 8))

class Mine():

    position_x: int
    position_y: int
    size: int
    ismine: bool
    image_path: str
    image: pygame.surface.Surface
    font: pygame.font.Font
    image_text: pygame.surface.Surface
    timer_text: pygame.surface.Surface
    diff_text: pygame.surface.Surface
    timer_event: pygame.USEREVENT
    difficulty: int = 1
    weight: float = 1.0
    explosion_timer: int = 100

    def __init__(self, position_x, position_y, size, difficulty=1, weight=1.0, timer=100):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.ismine = True
        self.weight = weight
        self.explosion_timer = timer
        self.difficulty = difficulty
        self.image_path = "assets/sprites/mines/" + str(randrange(1, 8)) + ".jpg"
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.font = pygame.font.SysFont('Comic Sans MS', int(self.size * 0.25))
        self.image_text = self.font.render(str(self.weight), False, (255, 0, 0))
        self.timer_text = self.font.render(str(self.explosion_timer), False, (255, 0, 0))
        self.difficulty_text = self.font.render(str(self.difficulty), False, (255, 0, 0))
        timer_interval = 1000
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, timer_interval)

    def draw(self, window):
        self.timer_text = self.font.render(str(self.explosion_timer), False, (255, 0, 0))
        position_on_screen = (self.size * self.position_x, self.size * self.position_y)
        window.blit(self.image, position_on_screen)
        window.blit(self.image_text, (position_on_screen[0] + self.size / 4, position_on_screen[1] + self.size / 2))
        window.blit(self.timer_text, (position_on_screen[0] + self.size / 4, position_on_screen[1] - self.size / 8))
        window.blit(self.difficulty_text, (position_on_screen[0] + self.size / 1.5, position_on_screen[1] + self.size / 6 ))
        



class Cliff:
    position_x: int
    position_y: int
    size: int
    image: pygame.surface.Surface

    type: int
    rotation: int

    def __init__(self, position_x, position_y, size, rotation, type=0):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.rotation = rotation
        self.type = type
        if self.type == 0:
            self.image = pygame.image.load("assets/sprites/cliff.png")
        elif self.type == 1:
            self.image = pygame.image.load("assets/sprites/cliff_corner.png")
        elif self.type == 2:
            self.image = pygame.image.load("assets/sprites/cliff_end1.png")
        elif self.type == 3:
            self.image = pygame.image.load("assets/sprites/cliff_end2.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.rotate(self.image, self.rotation)

    def draw(self, window):
        position_on_screen = (self.size * self.position_x, self.size * self.position_y)
        window.blit(self.image, position_on_screen)


# mapa
class Map:
    window: system.Window
    tile_size: int
    tiles_x: int
    tiles_y: int

    tile_palette: list
    terrain_matrix: list

    cliffs = []
    encounters = []
    mines = []
    notmines = []

    def __init__(self, window: system.Window, tile_size: int = 64, tiles_x: int = 8, tiles_y: int = 8):
        self.window = window
        self.tile_size = tile_size
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y

        # dodanie grafik wszystkich typów terenu do jednej listy
        self.tile_palette = [None] * 20
        image = pygame.image.load("assets/sprites/grass.png")
        image = pygame.transform.scale(image, (tile_size, tile_size))
        self.tile_palette[0] = image

        image = pygame.image.load("assets/sprites/stone.png")
        image = pygame.transform.scale(image, (tile_size, tile_size))
        self.tile_palette[10] = image

        image = pygame.image.load("assets/sprites/slowgrass.png")
        image = pygame.transform.scale(image, (tile_size, tile_size))
        self.tile_palette[5] = image

    def generate(self):
        # generowanie terenu
        matrix = []
        for i in range(self.tiles_y):
            matrix.append([])
            for j in range(self.tiles_x):
                # sprawdza czy są tu jakieś klify
                ok = True
                for cliff in self.cliffs:
                    for i2 in range(i - 1, i + 2):
                        if (j, i2) == (cliff.position_x, cliff.position_y):
                            ok = False
                            break
                        elif (j - 1, i2) == (cliff.position_x, cliff.position_y):
                            ok = False
                            break
                        elif (j + 1, i2) == (cliff.position_x, cliff.position_y):
                            ok = False
                            break
                # od liczby zależy jaki teren, np. 0 - piasek
                rng = randrange(10)
                if ok and rng == 0 and not (i < 2 and j < 3):
                    matrix[i].append(10)  # kamień
                elif ok and rng > 6 and not (i < 2 and j < 3):
                    matrix[i].append(5)  # trawa
                elif ok and rng < 2 and not (i < 2 and j < 3):
                    matrix[i].append(0)  # piasek
                    rand_rotate = 0  # randrange(4)*90
                    if rand_rotate == 0 and j + 3 < self.tiles_x and not (
                            i == 0 or i == self.tiles_y - 1 or j == 0 or j == self.tiles_x - 1):
                        cliff = Cliff(j, i, self.tile_size, rand_rotate, type=2)
                        # self.cliffs.append(cliff)
                        cliff = Cliff(j + 1, i, self.tile_size, rand_rotate, type=0)
                        # self.cliffs.append(cliff)
                        cliff = Cliff(j + 2, i, self.tile_size, rand_rotate, type=3)
                        # self.cliffs.append(cliff)
                else:
                    matrix[i].append(0)
        self.terrain_matrix = matrix

        for i in range(self.tiles_y):
            for j in range(self.tiles_x):
                if matrix[i][j] < 10:
                    ok = True
                    for cliff in self.cliffs:
                        if (j, i) == (cliff.position_x, cliff.position_y):
                            ok = False
                            break
                    if ok and randrange(10) == 0 and not (i < 2 and j < 3):
                        #zależnie od wylosowanej liczby mina lub niemina
                        if randrange(0, 10) > 3: #odpowiednia wartość to > 3
                            difficulty = randrange(0, 4) + 1
                            weight = randrange(10, 31) / 10
                            timer = randrange(100, 200)
                            mine = Mine(j, i, self.tile_size, difficulty, weight, timer)
                            self.mines.append(mine)
                            self.encounters.append(mine)
                        else:
                            notmine = NotMine(j, i, self.tile_size)
                            self.notmines.append(notmine)
                            self.encounters.append(notmine)

    def draw_tiles(self):
        # narysowanie na ekranie terenu
        for i in range(len(self.terrain_matrix)):
            for j in range(len(self.terrain_matrix[i])):
                self.window.window.blit(self.tile_palette[self.terrain_matrix[i][j]],
                                        (self.tile_size * j, self.tile_size * i))

    def draw_objects(self):
        for mine in self.mines:
            mine.draw(self.window.window)
        for notmine in self.notmines:
            notmine.draw(self.window.window)
        for cliff in self.cliffs:
            cliff.draw(self.window.window)




# broń
class Weapon:
    size: int
    image: pygame.surface.Surface
    rotated_image: pygame.surface.Surface

    owner: str
    weight: float
    weapon_type: int


# baza operacji
class Base:
    position_x: int
    position_y: int
    size: int
    image: pygame.surface.Surface

    weapon_level: int
    weapons = []


# schron
class Shelter:
    position_x: int
    position_y: int
    size: int
    image: pygame.surface.Surface


# składowisko
class Dumpster:
    position_x: int
    position_y: int
    size: int
    image: pygame.surface.Surface


# cywile
class NPC:
    position_x: int
    position_y: int
    size: int
    image: pygame.surface.Surface
    rotated_image: pygame.surface.Surface
    offset_x: int = 0
    offset_y: int = 0
    current_map: Map

    type: str
    value: int
    weight: float


# saper
class Minesweeper:
    size: int
    rotation_degrees: int
    position_x: int
    position_y: int
    image: pygame.surface.Surface
    rotated_image: pygame.surface.Surface
    offset_x: int = 0
    offset_y: int = 0
    current_map: Map

    carried_objects = []

    speed = 1
    ability = 1
    max_carried_weight = 5.0

    def __init__(self, position_x=0, position_y=0, size=64):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.image = pygame.image.load("assets/sprites/saper_fun_sized.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rotated_image = self.image
        self.rotation_degrees = 0
        self.neural_network = NeuralNetwork()

    def set_map(self, map: Map):
        self.current_map = map

    def update_offset(self, delta: float):
        dist = round(self.speed * delta / 8)
        finished = False
        if self.offset_x > 0:
            self.offset_x -= dist
            if self.offset_x <= 0:
                finished = True
        elif self.offset_x < 0:
            self.offset_x += dist
            if self.offset_x >= 0:
                finished = True
        if self.offset_y > 0:
            self.offset_y -= dist
            if self.offset_y <= 0:
                finished = True
        elif self.offset_y < 0:
            self.offset_y += dist
            if self.offset_y < -self.size and self.offset_y > -1.2 * self.size:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/ledge.wav"))
            if self.offset_y >= 0:
                finished = True

        if finished:
            pygame.mixer.Channel(1).stop()
            self.offset_y = 0
            self.offset_x = 0
            if self.current_map.terrain_matrix[self.position_y][self.position_x] < 5:
                self.speed = 1

    def draw(self, window, delta: float):
        position_on_screen = (self.size * self.position_x + self.offset_x, self.size * self.position_y + self.offset_y)
        window.blit(self.rotated_image, position_on_screen)
        self.update_offset(delta)

    def rotate(self, dir: str):
        dirr = 0
        if dir == "N":
            dirr = 180
        elif dir == "S":
            dirr = 0
        elif dir == "W":
            dirr = 270
        elif dir == "E":
            dirr = 90

        elif dir == "left":
            dirr = (self.rotation_degrees + 90) % 360
        elif dir == "right":
            dirr = (self.rotation_degrees - 90) % 360
        else:
            return

        self.rotation_degrees = dirr
        self.rotated_image = pygame.transform.rotate(self.image, dirr)

    def move(self, dir: int = -1):
        # południe - 0
        # wschód - 90
        # północ - 180
        # zachód - 270
        if self.offset_x != 0 or self.offset_y != 0:
            return

        if dir == -1:
            dir = self.rotation_degrees
        else:
            self.rotation_degrees = dir
            self.rotated_image = pygame.transform.rotate(self.image, dir)

        move_legal = True
        cliff_jump = False
        next_x = self.position_x
        next_y = self.position_y
        if dir == 0:
            next_y = self.position_y + 1
        elif dir == 180:
            next_y = self.position_y - 1
        elif dir == 270:
            next_x = self.position_x - 1
        elif dir == 90:
            next_x = self.position_x + 1

        if next_x == self.current_map.tiles_x or next_x == -1:
            move_legal = False
        elif next_y == self.current_map.tiles_y or next_y == -1:
            move_legal = False
        elif self.current_map.terrain_matrix[next_y][next_x] > 9:
            move_legal = False

        for cliff in self.current_map.cliffs:
            if (next_x, next_y) == (cliff.position_x, cliff.position_y):
                if dir == 0 and cliff.rotation == 0:
                    cliff_jump = True
                else:
                    move_legal = False

        if move_legal:
            if self.current_map.terrain_matrix[next_y][next_x] > 4:
                self.speed = 0.5
            pygame.mixer.Channel(1).set_volume(0.01) #from 0.3
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/moving.wav"))
            if dir == 0:
                self.position_y += 1
                self.offset_y = -self.size
                if cliff_jump:
                    self.position_y += 1
                    self.offset_y = -2 * self.size
            elif dir == 180:
                self.position_y -= 1
                self.offset_y = self.size
            elif dir == 270:
                self.position_x -= 1
                self.offset_x = self.size
            elif dir == 90:
                self.position_x += 1
                self.offset_x = -self.size
        else:
            pygame.mixer.Channel(2).set_volume(0.01) #from 0.5
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("assets/sounds/collision.wav"))

    def pick_up(self, model):
        if self.offset_x != 0 or self.offset_y != 0:
            return
        for encounter in self.current_map.encounters:
            if (self.position_x, self.position_y) == (encounter.position_x, encounter.position_y):
                
                #wykrywanie po zadjęciu czy mina czy nie
                decisionismine = self.neural_network.recognize(encounter.image_path)
                
                #wykryto błędnie
                if decisionismine != encounter.ismine:
                    print("ERROR: Decision was not correct")
                    #self.current_map.encounters.clear()
                    if encounter.ismine:
                            encounter.image_text = encounter.font.render("MISS", False, (255, 0, 0))
                            encounter.difficulty_text = encounter.font.render("", False, (255, 0, 0))
                    else: 
                            encounter.done_text = encounter.font.render("MISS", False, (255,0,0))
                    self.current_map.encounters.remove(encounter)
                    print("")
                    break
                #wykryto poprawnie, że mina
                elif decisionismine:
                    print("Decision was correct")
                    print("Mine? - Yes")
                    print("")
                    tree = decisionTrees.DecisionTrees()
                    decision = tree.return_predict(model)
                    print("Decision : ", decision, "\n")

                    self.current_map.mines.remove(encounter)
                    self.current_map.encounters.remove(encounter)
                    pygame.mixer.Channel(3).set_volume(0.01) #from 0.7
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound("assets/sounds/pickup.wav"))
                    break
                #wykryto poprawnie, że niemina
                else:
                    print("Decision was correct")
                    print("Mine? - No")
                    print("")
                    encounter.done_text = encounter.font.render("X", False, (255,0,0))
                    self.current_map.encounters.remove(encounter)
                    pygame.mixer.Channel(3).set_volume(0.01)
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound("assets/sounds/notmine.wav"))
                    break


    def drop_bombs(self):
        pass

    def drop_civilians(self):
        pass

    def sensor(self, x: int = -1, y: int = -1):
        if x == -1:
            x = self.position_x
        if y == -1:
            y = self.position_y
        sensor_list = [["", "", ""], ["", "", ""], ["", "", ""]]
        for i in range(3):
            for j in range(3):
                posx = x - 1 + j
                posy = y - 1 + i
                if posx >= self.current_map.tiles_x or posx <= -1:
                    sensor_list[i][j] = "wall"
                elif posy >= self.current_map.tiles_y or posy <= -1:
                    sensor_list[i][j] = "wall"
                elif self.current_map.terrain_matrix[posy][posx] > 9:
                    sensor_list[i][j] = "wall"
                elif self.current_map.terrain_matrix[posy][posx] > 4:
                    sensor_list[i][j] = "slowfloor"
                else:
                    sensor_list[i][j] = "floor"
                for cliff in self.current_map.cliffs:
                    if (posx, posy) == (cliff.position_x, cliff.position_y):
                        if cliff.rotation == 0:
                            sensor_list[i][j] = "cliff_south"
                        elif cliff.rotation == 90:
                            sensor_list[i][j] = "cliff_east"
                        elif cliff.rotation == 180:
                            sensor_list[i][j] = "cliff_north"
                        elif cliff.rotation == 270:
                            sensor_list[i][j] = "cliff_west"
                        break
                for encounter in self.current_map.encounters:
                    if (posx, posy) == (encounter.position_x, encounter.position_y):
                        sensor_list[i][j] = "encounter"
                        break

        return sensor_list
