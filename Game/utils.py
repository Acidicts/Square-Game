import pygame
import os
from .settings import TILE_SIZE

BASE_IMG_PATH = "Game/Assets/images/"


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    if "icon_" in path:
        img = pygame.transform.scale(img, (16, 16))
    return img


def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + str(img_name)))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images))
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]


def map_to_grid(x, y):
    x = x // TILE_SIZE
    y = y // TILE_SIZE

    return x, y


def grid_to_map(gridx, gridy):
    x = gridx * TILE_SIZE
    y = gridy * TILE_SIZE

    return x, y
