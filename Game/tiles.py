import pygame
from pygame.math import Vector2
from .utils import *


class Tile:
    def __init__(self, x, y, width, height, image, grid):
        self.x = x
        self.y = y
        self.z = 0

        self.width = width
        self.height = height

        self.grid = grid

        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.grid_loc = Vector2(x, y)
        self.loc = Vector2(*grid_to_map(x, y))

        self.direction = Vector2(0, 0)
        self.cii = self.grid.grid[int(self.grid_loc.x + self.direction.x)][int(self.grid_loc.y + self.direction.y)]

    def update(self, *args):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Move(Tile):
    def __init__(self, x, y, width, height, image, grid, direction=Vector2(0, 0)):
        super().__init__(x, y, width, height, image, grid)
        self.image = image

        self.selected = False
        self.direction = direction

        self.z = 1

    def move(self, gridx, gridy):
        self.x, self.y = (self.loc.x, self.loc.y)

    def draw(self, screen):
        pygame.draw.rect(screen,
                         (10, 10, 30),
                         (*grid_to_map(self.grid_loc.x, self.grid_loc.y), TILE_SIZE-1, TILE_SIZE-1))
        screen.blit(self.image, (self.loc.x, self.loc.y))

    def update(self, play=False):
        if play:
            next_x = int(self.grid_loc.x + self.direction.x)
            next_y = int(self.grid_loc.y + self.direction.y)
            if 0 <= next_x < self.grid.cols and 0 <= next_y < self.grid.rows:
                if not self.grid.grid[next_y][next_x]:
                    self.grid.grid[int(self.grid_loc.y)][int(self.grid_loc.x)] = None
                    self.loc += self.direction
                    self.grid_loc = Vector2(*map_to_grid(self.loc.x, self.loc.y))
                    self.grid.grid[int(self.grid_loc.y)][int(self.grid_loc.x)] = self
                else:
                    (self.grid.grid[int(self.grid_loc.y) + int(self.direction.y)][int(self.grid_loc.x) + int(self.direction.x)]
                     .direction) = self.direction
                    self.direction = Vector2(0, 0)
        else:
            self.loc = Vector2(*grid_to_map(self.grid_loc.x, self.grid_loc.y))
