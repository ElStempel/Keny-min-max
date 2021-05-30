import pygame
import os

WIDTH,HEIGHT =800,800
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GRAY = (105,105,105)
LIGHT_GRAY=(211,211,211)
CREME = (255, 229, 208)
BROWN =(111,56,26)

CROWN = pygame.transform.scale(pygame.image.load('assets/pepper2.png'), (44, 25))