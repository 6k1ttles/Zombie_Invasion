import pygame as pg
from config import *


class Level:
    def __init__(self, sc, textures):
        self.level = []
        with open('etc/level.txt', 'r') as file:
            for line in file.readlines():
                line = line.replace('\n', '')
                self.level.append(line)

            self.screen = sc
            self.textures = {".": textures['ground_bottom'],
                             # "=": textures['ground_top'],
                             "#": textures['stone']}

    # создание коллизий и прорисовка объектов в соответствии с картой
    def update(self, scroll):
        colliders = []
        for i, line in enumerate(self.level):
            for j, symb in enumerate(line):
                if symb != '.':
                    colliders.append(pg.Rect((j * BLOCK_SIZE, i * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE)))
                self.screen.blit(self.textures[symb], (j * BLOCK_SIZE - scroll[0], i * BLOCK_SIZE - scroll[1]))
        return colliders
