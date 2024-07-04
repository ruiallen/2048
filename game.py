import pygame
import collections

class App:
    def __init__(self):
        self._running = True
        self._gui = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._gui = game_GUI(600,400)
        self._gui.draw_board()
        print('board_drew')
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


class board():
     def __init__(self):
         self.board = (
        [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],    
         ])
    

class block():
    def __init__(self, x,y,val):
        self.x = x
        self.y = y
        self.val = val
    
    def move_up(self):
        pass

    def move_down(self):
        pass
    def move_left(self):
        pass
    def move_right(self):
        pass

class game_GUI():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((30, 222, 236))


    def draw_board(self):
        for x in range(0,self.width,100):
            for y in range(0,self.height,100):
                rect = pygame.Rect(x, y, 100, 100)
                pygame.draw.rect(self.screen, (30, 222, 236), rect, width= 1, border_radius=1)
