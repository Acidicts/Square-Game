import pygame

from .settings import TILE_SIZE
from .tiles import *
from .grid import Grid
from .rainbow import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cubed")

        self.WIDTH = 1280
        self.HEIGHT = 640

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Game/Assets/images/Oxanium-Bold.ttf", 32)
        self.mixer = pygame.mixer

        self.grid_size = (self.WIDTH // TILE_SIZE, self.HEIGHT // TILE_SIZE)

        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surf, (10, 10, 30), (0, 0, TILE_SIZE - 1, TILE_SIZE - 1))

        self.grid = Grid(self.grid_size[1], self.grid_size[0])

        self.selected_tile = None
        self.current_tile = None

        self.blink = None
        self.show_playing_text = True
        self.letters = []

        self.classes = [Move, Clone, Destroy, Rotate]
        self.choice = 0

    def run(self):
        running = True
        playing = False

        surf = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        playing = not playing

                    if event.key == pygame.K_ESCAPE:
                        self.__init__()

                    if event.key == pygame.K_RETURN:
                        self.grid.save("Game/Assets/images/save.txt")

                    if event.key == pygame.K_HASH:
                        self.grid.load("Game/Assets/images/save.txt")

                    if self.current_tile:
                        if event.key == pygame.K_RIGHT:
                            self.current_tile.direction = Vector2(1, 0)
                            self.current_tile = None

                        if event.key == pygame.K_LEFT:
                            self.current_tile.direction = Vector2(-1, 0)
                            self.current_tile = None

                        if event.key == pygame.K_UP:
                            self.current_tile.direction = Vector2(0, -1)
                            self.current_tile = None

                        if event.key == pygame.K_DOWN:
                            self.current_tile.direction = Vector2(0, 1)
                            self.current_tile = None

                    if event.key == pygame.K_r:
                        if "r" not in self.letters:
                            self.letters.append("r")
                        else:
                            self.letters = []

                    if event.key == pygame.K_a:
                        if "a" not in self.letters:
                            self.letters.append("a")
                        else:
                            self.letters = []

                    if event.key == pygame.K_i:
                        if "i" not in self.letters:
                            self.letters.append("i")
                        else:
                            self.letters = []

                    if event.key == pygame.K_n:
                        if "n" not in self.letters:
                            self.letters.append("n")
                        else:
                            self.letters = []

                    if event.key == pygame.K_b:
                        if "b" not in self.letters:
                            self.letters.append("b")
                        else:
                            self.letters = []

                    if event.key == pygame.K_o:
                        if "o" not in self.letters:
                            self.letters.append("o")
                        else:
                            self.letters = []

                    if event.key == pygame.K_w:
                        if "w" not in self.letters:
                            self.letters.append("w")
                        else:
                            self.letters = []

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.current_tile:
                            x, y = map_to_grid(*pygame.mouse.get_pos())
                            if not playing:
                                if not self.grid.grid[y][x] and self.selected_tile:
                                    new_cell = self.selected_tile(x, y, TILE_SIZE, TILE_SIZE,
                                                                  self.grid.sprites[self.selected_tile.__name__.lower()],
                                                                  self.grid)
                                    self.grid.grid[y][x] = new_cell
                                    self.current_tile = self.grid.grid[y][x]
                        if not self.selected_tile:
                            x, y = map_to_grid(*pygame.mouse.get_pos())
                            self.current_tile = self.grid.grid[y][x]

                    elif event.button == 3:
                        if self.selected_tile:
                            self.selected_tile = None
                        else:
                            x, y = map_to_grid(*pygame.mouse.get_pos())
                            tile = self.grid.grid[y][x]
                            if tile:
                                self.grid.grid[y][x] = None

                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.choice = (self.choice - 1) % len(self.classes)
                    elif event.y < 0:
                        self.choice = (self.choice + 1) % len(self.classes)
                    self.selected_tile = self.classes[self.choice]

            if self.current_tile and self.current_tile.cat == "destroy":
                self.current_tile = None

            for row in self.grid.grid:
                for cell in row:
                    if cell:
                        cell.update(playing)

            cells = 0
            for row in self.grid.grid:
                for cell in row:
                    if cell:
                        cells += 1

            if len(self.letters) == 7:
                surf = pygame.surface.Surface((self.WIDTH, self.HEIGHT))
                surf.fill((0, 0, 0))
                surf.set_colorkey((0, 0, 0))
                surf.blit(create_rainbow_gradient(self.WIDTH, self.HEIGHT), (0, 0))
                print("RAINBOW")
                self.letters = []

            self.screen.fill((0, 0, 0))

            if surf:
                self.screen.blit(surf, (0, 0))

            self.grid.draw(self.screen)

            if self.selected_tile:
                x, y = map_to_grid(*pygame.mouse.get_pos())
                cell = self.grid.sprites[self.selected_tile.__name__.lower()].copy()
                cell.set_alpha(120)
                self.screen.blit(cell, grid_to_map(x, y))

            text = self.font.render(f"Cells: {cells}", True, (255, 255, 255))
            self.screen.blit(text, (2, 2))

            if playing:
                if self.blink is None or pygame.time.get_ticks() - self.blink > 500:
                    self.show_playing_text = not self.show_playing_text
                    self.blink = pygame.time.get_ticks()

                if self.show_playing_text:
                    text = self.font.render("Playing", True, (255, 255, 255))
                    self.screen.blit(text, (self.WIDTH - text.get_width() - 2, 2))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
