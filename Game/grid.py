import pygame
from .tiles import *
from pygame.math import Vector2
from .utils import *
from .settings import TILE_SIZE


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surf, (10, 10, 30), (0, 0, TILE_SIZE-1, TILE_SIZE-1))

        self.sprites = {
            "move": load_image("move.png"),
            "clone": load_image("clone.png"),
            "tile": surf.convert(),
        }

        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.grid[0][0] = Move(0, 0, TILE_SIZE, TILE_SIZE, self.sprites['move'], self, Vector2(1, 0))
        self.grid[0][5] = Move(5, 0, TILE_SIZE, TILE_SIZE, self.sprites['move'], self, Vector2(0, 0))

    def draw(self, screen):
        z = 0
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col]:
                    if self.grid[row][col].z > z:
                        z = self.grid[row][col].z

        for z in range(z+1):
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.grid[row][col] and z == self.grid[row][col].z:
                        self.grid[row][col].draw(screen)
                    if not self.grid[row][col] and z == 0:
                        pygame.draw.rect(screen, (10, 10, 30), (*grid_to_map(col, row), TILE_SIZE-1, TILE_SIZE-1))
