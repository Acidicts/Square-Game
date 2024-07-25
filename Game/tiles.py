import pygame
from pygame.math import Vector2
from .utils import *


class Tile:
    def __init__(self, x, y, width, height, image, grid):
        self.x = x
        self.y = y
        self.z = 0

        self.cat = "tile"

        self.width = width
        self.height = height

        self.grid = grid

        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.grid_loc = Vector2(x, y)
        self.loc = Vector2(*grid_to_map(x, y))

        self.direction = Vector2(0, 0)
        next_x = int(self.grid_loc.x + self.direction.x)
        next_y = int(self.grid_loc.y + self.direction.y)
        if 0 <= next_x < self.grid.cols and 0 <= next_y < self.grid.rows:
            self.cii = self.grid.grid[next_y][next_x]
        else:
            self.cii = None

    def update(self, *args):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.loc.x, self.loc.y))


class Move(Tile):
    def __init__(self, x, y, width, height, image, grid, direction=Vector2(0, 0)):
        super().__init__(x, y, width, height, image, grid)
        self.image = image

        self.cat = "move"

        self.selected = False
        self.direction = direction

        self.z = 1

    def draw(self, screen):
        pygame.draw.rect(screen,
                         (10, 10, 30),
                         (*grid_to_map(self.grid_loc.x, self.grid_loc.y), TILE_SIZE - 1, TILE_SIZE - 1))
        if self.direction.x == 1:
            screen.blit(self.image, (self.loc.x, self.loc.y))
        elif self.direction.x == -1:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.loc.x, self.loc.y))
        elif self.direction.y == -1:
            screen.blit(pygame.transform.rotate(self.image, 90), (self.loc.x, self.loc.y))
        elif self.direction.y == 1:
            screen.blit(pygame.transform.rotate(self.image, -90), (self.loc.x, self.loc.y))
        else:
            pygame.draw.rect(screen, (0, 0, 70),
                             (*grid_to_map(self.grid_loc.x, self.grid_loc.y), TILE_SIZE - 1, TILE_SIZE - 1))

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
                    cell = (self.grid.grid[int(self.grid_loc.y) + int(self.direction.y)][
                        int(self.grid_loc.x) + int(self.direction.x)])
                    if cell.cat == "move":
                        buffer = cell.direction
                        cell.direction = self.direction
                        self.direction = buffer
            else:
                self.direction = Vector2(0, 0)

        else:
            self.loc = Vector2(*grid_to_map(self.grid_loc.x, self.grid_loc.y))


class Clone(Tile):
    def __init__(self, x, y, width, height, image, grid, direction=Vector2(0, 0)):
        super().__init__(x, y, width, height, image, grid)
        self.wait = pygame.time.get_ticks()
        self.direction = direction
        self.z = 2

        self.cat = "clone"

    def update(self, play=False):
        if play and pygame.time.get_ticks() - self.wait > 500:
            source_x = int(self.grid_loc.x - self.direction.x)
            source_y = int(self.grid_loc.y - self.direction.y)
            target_x = int(self.grid_loc.x + self.direction.x)
            target_y = int(self.grid_loc.y + self.direction.y)

            if 0 <= target_x < self.grid.cols and 0 <= target_y < self.grid.rows:
                if not self.grid.grid[target_y][target_x]:
                    cell = self.grid.grid[source_y][source_x]
                    if cell:
                        # Create a new cell of the same class at the target location
                        new_cell = type(cell)(target_x, target_y, cell.width, cell.height, cell.image, self.grid,
                                              cell.direction)
                        self.grid.grid[target_y][target_x] = new_cell

                        # Update the new cell's position
                        new_cell.grid_loc = Vector2(target_x, target_y)
                        new_cell.loc = Vector2(*grid_to_map(target_x, target_y))
        else:
            self.loc = Vector2(*grid_to_map(self.grid_loc.x, self.grid_loc.y))

    def draw(self, screen):
        pygame.draw.rect(screen,
                         (10, 10, 30),
                         (*grid_to_map(self.grid_loc.x, self.grid_loc.y), TILE_SIZE - 1, TILE_SIZE - 1))
        if self.direction.x == 1:
            screen.blit(self.image, (self.loc.x, self.loc.y))
        elif self.direction.x == -1:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.loc.x, self.loc.y))
        elif self.direction.y == -1:
            screen.blit(pygame.transform.rotate(self.image, 90), (self.loc.x, self.loc.y))
        elif self.direction.y == 1:
            screen.blit(pygame.transform.rotate(self.image, -90), (self.loc.x, self.loc.y))
        else:
            pygame.draw.rect(screen, (0, 70, 0),
                             (*grid_to_map(self.grid_loc.x, self.grid_loc.y), TILE_SIZE - 1, TILE_SIZE - 1))


class Destroy(Tile):
    def __init__(self, x, y, width, height, image, grid, direction=Vector2(0, 0)):
        super().__init__(x, y, width, height, image, grid)
        self.z = 3
        self.cat = "destroy"

    def update(self, *args):
        cells_around = {
            "up": self.grid_loc + Vector2(0, -1),
            "down": self.grid_loc + Vector2(0, 1),
            "left": self.grid_loc + Vector2(-1, 0),
            "right": self.grid_loc + Vector2(1, 0)
        }

        for direction, loc in cells_around.items():
            if 0 <= loc.x < self.grid.cols and 0 <= loc.y < self.grid.rows:
                cell = self.grid.grid[int(loc.y)][int(loc.x)]
                if cell:
                    if direction == "up" and cell.direction == Vector2(0, 1):
                        self.grid.grid[int(loc.y)][int(loc.x)] = None
                    elif direction == "down" and cell.direction == Vector2(0, -1):
                        self.grid.grid[int(loc.y)][int(loc.x)] = None
                    elif direction == "left" and cell.direction == Vector2(1, 0):
                        self.grid.grid[int(loc.y)][int(loc.x)] = None
                    elif direction == "right" and cell.direction == Vector2(-1, 0):
                        self.grid.grid[int(loc.y)][int(loc.x)] = None

    def draw(self, screen):
        pygame.draw.rect(screen,
                         (10, 10, 30),
                         (*grid_to_map(self.grid_loc.x, self.grid_loc.y), TILE_SIZE - 1, TILE_SIZE - 1))
        screen.blit(self.image, (self.loc.x, self.loc.y))


class Rotate(Tile):
    def __init__(self, x, y, width, height, image, grid):
        super().__init__(x, y, width, height, image, grid)
        self.z = 2
        self.wait = pygame.time.get_ticks()
        self.images = [self.image, pygame.transform.rotate(self.image, 90)]
        self.img = 0

    def update(self, play=False):
        cells_around = {
            "up": self.grid_loc + Vector2(1, -1),
            "down": self.grid_loc + Vector2(-1, 1),
            "left": self.grid_loc + Vector2(-1, -1),
            "right": self.grid_loc + Vector2(1, 1)
        }

        for direction, loc in cells_around.items():
            if 0 <= loc.x < self.grid.cols and 0 <= loc.y < self.grid.rows:
                cell = self.grid.grid[int(loc.y)][int(loc.x)]
                if cell and play:
                    if direction == "up" and cell.direction == Vector2(0, 1):
                        cell.direction = Vector2(1, 0)
                    elif direction == "down" and cell.direction == Vector2(0, -1):
                        cell.direction = Vector2(-1, 0)
                    elif direction == "left" and cell.direction == Vector2(1, 0):
                        cell.direction = Vector2(0, -1)
                    elif direction == "right" and cell.direction == Vector2(-1, 0):
                        cell.direction = Vector2(0, 1)

    def draw(self, screen):
        if self.wait:
            if pygame.time.get_ticks() - self.wait > 1000:
                self.img += 1
                if self.img == 2:
                    self.img = 0
        elif not self.wait:
            self.wait = pygame.time.get_ticks()
        screen.blit(self.images[self.img], (self.loc.x, self.loc.y))
