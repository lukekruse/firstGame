
# The base for this code is from the following source.
#
#   KidsCanCode - Game Development with Pygame video series
#   Tile-based game - Part 2
#   Collisions and Tilemaps
#   Video link: https://youtu.be/ajR4BZBKTr4
#
# It was modified to include a random dungeon generator that was taken from yet
# another source,
#   
#   Author: James Spencer
#   Site Link: http://www.roguebasin.com/index.php?title=
#       A_Simple_Dungeon_Generator_for_Python_2_or_3
#
#

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from scripts.dungeonGenerator import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
 
        self.map_data = []
        gen = mapGenerator(width = GRIDWIDTH, height = GRIDHEIGHT)
        # gen = mapGenerator(width = GRIDHEIGHT, height = GRIDWIDTH)
        gen.gen_level()
        gen.gen_tiles_level()

        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.floors = pg.sprite.Group()

        MAP = {}
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles.strip()):
                MAP[(col, row)] = int(tile)
                print((col, row), tile) 
        playerexists = False
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles.strip()):
                if MAP[(col, row)] == 1:
                    if DEVLOG: print(col, row)
                    Wall(self, col, row,  MAP)
                else:
                    Floor(self, col, row)
                    if not playerexists:
                        self.player = Player(self, col, row)
                        playerexists = True


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
