import pygame
from pygame.math import Vector2
from .utils import *


class Tile:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.z = 0

        self.width = width
        self.height = height

        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.grid_loc = Vector2(x, y)
        self.loc = Vector2(*grid_to_map(x, y))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Move(Tile):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        surf = pygame.Surface((self.width, self.height))
        pygame.draw.rect(surf, (10, 10, 150), (0, 0, self.width-1, self.height-1))
        self.image = surf.convert()

        self.selected = False
        self.direction = Vector2(1, 1)

        self.z = 1

    def move(self, gridx, gridy):
        self.x, self.y = (self.loc.x, self.loc.y)

    def draw(self, screen):
        screen.blit(self.image, (self.loc.x, self.loc.y))

    def update(self, play):
        if play:
            self.loc += self.direction
            self.grid_loc = Vector2(*map_to_grid(self.loc.x, self.loc.y))
        else:
            self.loc = Vector2(*grid_to_map(self.grid_loc.x, self.grid_loc.y))
