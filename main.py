# pygame - biblioteka do symulacji graficznych
from multiprocessing import freeze_support
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from chefboost import Chefboost as chef
import pandas as pd
# system - klasy związane z pygame
# minesweeper - klasy związane z samym saperem
# ai - klasa wykonująca ruchy sapera
from classes import system, minesweeper, ai, decisionTrees

# ustalenie wielkości pojedyńczych kawałków mapy, oraz wielkości mapy
TILE_SIZE = 72
TILES_X = int(12)
TILES_Y = int(10)

# wł/wył muzyki
MUSIC = False

# ustalenie FPS
FPS = 60

# włączenie tekstu
pygame.font.init()


def main():


    if MUSIC:
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("assets/music.ogg"), -1)

    # utworzenie okna do gry
    window = system.Window(TILE_SIZE * TILES_X, TILE_SIZE * TILES_Y, "Intelligent Minesweeper", "icon.png")

    # utworzenie objektu mapy, wygenerowanie jej i narysowanie na ekranie
    map = minesweeper.Map(window, TILE_SIZE, TILES_X, TILES_Y)
    map.generate()
    map.draw_tiles()

    # utworzenie sapera
    saper = minesweeper.Minesweeper(0, 0, TILE_SIZE)

    # pierwszy render
    map.draw_tiles()
    map.draw_objects()
    saper.draw(window.window, 0.1)
    pygame.display.update()

    # utworzenie objektu klasy AI
    AI = ai.AI(window, map, saper)
    # wykonanie funkcji ready() AI
    AI.ready()

    # główna pętla
    game_loop = True
    clock = pygame.time.Clock()

    # create decision tree
    tree = decisionTrees.DecisionTrees()
    model = tree.create_model()

    while game_loop:
        # wdrożenie FPS, delta - czas od ostatniej klatki
        delta = clock.tick(FPS)

        # wykonanie funkcji update() AI
        AI.updateFPS()

        if saper.offset_x == 0 and saper.offset_y == 0:
            AI.updateTile(model)

        # narysowanie terenu i obiektów
        map.draw_tiles()
        map.draw_objects()
        saper.draw(window.window, delta)

        # odświeżenie ekranu
        pygame.display.update()

        # sprawdzanie różnych interakcji użytkownika
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
                pygame.quit()
            elif event.type in [i.timer_event for i in map.mines]:
                for i in map.mines:
                    i.explosion_timer -= 1


if __name__ == "__main__":
    freeze_support()
    main()
