import pygame, sys
from pygame.locals import *
import random
import game
 
pygame.init()
 
if __name__ == "__main__":  
    app = game.App()
    app.run_game()