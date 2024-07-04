import pygame, sys
from pygame.locals import *
import random
from game import *
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
gui = game_GUI(400,600)
screen = gui.screen
#DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

 
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
     
    screen.fill(WHITE)
    gui.draw_board()
    pygame.display.update()
    FramePerSec.tick(FPS)