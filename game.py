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
    #it's easier to move everything on board rather than moving individual squares.
    #once moved, update all blocks accordingly and put them in the right coordinate.
    # basically connect board with blocks 
    def __init__(self):
         self.board = [[0 for _ in range(4)] for _ in range(4) ]
    
    def get_value(self,x,y):
        return self.board[x][y]
    
    def set_value(self,x,y,val):
        self.board[x][y] = val
        return
    
    def get_empty_cell(self):
        empty_list = []
        for x in range(4):
            for y in range(4):
                if self.board[x][y] == 0:
                    empty_list.append((x,y))
        return empty_list
    
    def spawn_new_block(self):
        import random
        empty_list = self.get_empty_cell()
        coord = random.choice(empty_list)
        x,y = coord[0],coord[1]
        self.board[x][y] = 2
    

    #define move operations
    #first move all the blocks to the right place, then merge, then move again because possible empty cell appeasr
    def move_up(self):
        #from top to bottom
        for y in range(4):
            for x in range(1,4):
                if self.get_value(x,y) != 0: #need to move this 
                    val = self.get_value(x,y)
                    dst = x - 1
                    cur = x
                    while dst>=0:
                        if self.get_value(dst,y) == 0: # can move to this place
                            self.set_value(dst,y,val)
                            self.set_value(cur,y,0)
                            dst-=1
                            cur-=1
                        else:
                            break
        return
    
    def move_down(self):
        #from bottom to top
        for y in range(4):
            for x in range(2,-1,-1):
                if self.get_value(x,y) != 0: #need to move this 
                    val = self.get_value(x,y)
                    dst = x + 1
                    cur = x
                    while dst<4:
                        if self.get_value(dst,y) == 0: # can move to this place
                            self.set_value(dst,y,val)
                            self.set_value(cur,y,0)
                            dst+=1
                            cur+=1
                        else:
                            break
        return
    
    def move_left(self):
        #from left to right
        for x in range(4):
            for y in range(1,4):
                if self.get_value(x,y) != 0: #need to move this 
                    val = self.get_value(x,y)
                    dst = y - 1
                    cur = y
                    while dst>=0:
                        if self.get_value(x,dst) == 0: # can move to this place
                            self.set_value(x,dst,val)
                            self.set_value(x,cur,0)
                            dst-=1
                            cur-=1
                        else:
                            break
        return 
    
    def move_right(self):
        #from right to left
        for x in range(4):
            for y in range(2,-1,-1):
                if self.get_value(x,y) != 0: #need to move this 
                    val = self.get_value(x,y)
                    dst = y + 1
                    cur = y
                    while dst<4:
                        if self.get_value(x,dst) == 0: # can move to this place
                            self.set_value(x,dst,val)
                            self.set_value(x,cur,0)
                            dst+=1
                            cur+=1
                        else:
                            break
        return


    #after moving the blocks, now need to merge block together    
    def merge_up(self):
        #from top to bottom
        for y in range(4):
            x = 0
            while x < 3:
                to_merge = x+1
                if self.get_value(x,y) == self.get_value(to_merge,y) and self.get_value(x,y)!=0: # need to merge
                    val = self.get_value(x,y)
                    self.set_value(x,y,val+val)
                    self.set_value(to_merge,y,0)
                    x+=2
                else:
                    x+=1
        return
    
    def merge_down(self):
        #from bottom to top
        for y in range(4):
            x = 3
            while x>0:
                to_merge = x-1
                if self.get_value(x,y) == self.get_value(to_merge,y) and self.get_value(x,y)!=0: # need to merge
                    val = self.get_value(x,y)
                    self.set_value(x,y,val+val)
                    self.set_value(to_merge,y,0)
                    x-=2
                else:
                    x-=1
        return

    def merge_left(self):
        #from left to right
        for x in range(4):
            y = 0
            while y<3:
                to_merge = y + 1
                if self.get_value(x,y) == self.get_value(x,to_merge) and self.get_value(x,y)!=0: # need to merge
                    val = self.get_value(x,y)
                    self.set_value(x,y,val+val)
                    self.set_value(x,to_merge,0)
                    y+=1
                else:
                    y+=1                  
        return 
    
    def merge_right(self):
        #from right to left
        for x in range(4):
            y = 3
            while y>0:
                to_merge = y - 1
                if self.get_value(x,y) == self.get_value(x,to_merge) and self.get_value(x,y)!=0: # need to merge
                    val = self.get_value(x,y)
                    self.set_value(x,y,val+val)
                    self.set_value(x,to_merge,0)
                    y-=2
                else:
                    y-=1                  
        return 



    def action(self,act):
        if act == 'left':
            self.move_left()
            self.merge_left()
            self.move_left()
        elif act == 'right':
            self.move_right()
            self.merge_right()
            self.move_right()
        elif act == 'up':
            self.move_up()
            self.merge_up()
            self.move_up()
        else:
            self.move_down()
            self.merge_down()
            self.move_down()

    

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
        x_skip = self.width//4
        y_skip = self.height//4
        for x in range(0,self.width,x_skip):
            for y in range(0,self.height,y_skip):
                rect = pygame.Rect(x, y, x_skip,  y_skip)
                pygame.draw.rect(self.screen, (30, 222, 236), rect, width= 5, border_radius=1)
