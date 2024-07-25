import pygame
import colorsys

def create_rainbow_gradient(width, height):
    surface = pygame.Surface((width, height))
    for x in range(width):
        hue = x / width
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))
        pygame.draw.line(surface, color, (x, 0), (x, height))
    return surface
