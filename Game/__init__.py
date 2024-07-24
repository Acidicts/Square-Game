import pygame

from .settings import TILE_SIZE
from .tiles import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cubed")

        self.WIDTH = 1280
        self.HEIGHT = 640

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.grid_size = (self.WIDTH//TILE_SIZE, self.HEIGHT//TILE_SIZE)

        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surf, (10, 10, 30), (0, 0, TILE_SIZE-1, TILE_SIZE-1))

        self.grid = [[Move(x, y, TILE_SIZE, TILE_SIZE, surf.convert_alpha())
                      for x in range(self.grid_size[0])] for y in range(self.grid_size[1])]

    def draw_grid(self):
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                cell = self.grid[y][x]
                self.screen.blit(cell.image, (cell.x * TILE_SIZE, cell.y * TILE_SIZE))

    def run(self):
        running = True
        playing = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        playing = not playing

            for row in self.grid:
                for cell in row:
                    cell.update()

            self.screen.fill((0, 0, 0))

            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
