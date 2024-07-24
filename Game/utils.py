from .settings import TILE_SIZE

def map_to_grid(x, y):
    x = x // TILE_SIZE
    y = y // TILE_SIZE

    return x, y

def grid_to_map(gridx, gridy):
    x = gridx * TILE_SIZE
    y = gridy * TILE_SIZE

    return x, y
