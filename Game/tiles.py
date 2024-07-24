import pygame
from pygame.math import Vector2
from .utils import *


class Tile:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        pass


class Move(Tile):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        surf = pygame.Surface((self.width, self.height))
        pygame.draw.rect(surf, (10, 10, 150), (0, 0, self.width-1, self.height-1))
        self.image = surf.convert()

        self.selected = False
        self.direction = Vector2(0, 1)

    def move(self, x, y):
        self.x, self.y = grid_to_map(x, y)

    def update(self):
        self.x, self.y = (Vector2.x * 32, Vector2.y * 32)
        mouse = pygame.mouse.get_pressed()

        if mouse[0] and not self.selected:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True

        elif mouse[0] and self.selected:
            self.selected = False
            self.move(*map_to_grid(*pygame.mouse.get_pos()))

        elif mouse[1] and self.selected:
            self.selected = False
