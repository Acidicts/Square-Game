import pygame
from .tiles import *
from pygame.math import Vector2
from .utils import *
from .settings import TILE_SIZE
import os


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
            "destroy": load_image("destroy.png"),
            "rotate": load_image("rotate.png"),
        }

        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col]:
                    self.grid[row][col].draw(screen)
                else:
                    pygame.draw.rect(screen, (10, 10, 30),
                                     (*grid_to_map(col, row),
                                      TILE_SIZE - 1, TILE_SIZE - 1))

    def save(self, path):
        with open(path, "w") as f:
            for row in self.grid:
                for cell in row:
                    if cell:
                        f.write(f"{cell.cat}({int(cell.direction.x)},{int(cell.direction.y)}) ")
                    else:
                        f.write("none ")
                f.write("\n")

    def load(self, path):
        with open(path, "r") as f:
            lines = f.readlines()
            for y, line in enumerate(lines):
                for x, cell in enumerate(line.split()):
                    if cell != "none":
                        class_name = cell.split('(')[0].capitalize()
                        direction_str = cell[
                                        cell.find("(") + 1:cell.find(")")].strip()
                        try:
                            direction = Vector2(*map(int, direction_str.split(",")))
                        except ValueError:
                            direction = Vector2(0, 0)
                        self.grid[y][x] = eval(class_name)(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE,
                                                           self.sprites[cell.split('(')[0].lower()], self, direction)
