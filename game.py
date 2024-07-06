import random
import pygame
import collections

class App():
    #handles everything related to a game (initialize, exit etc.)
    def __init__(self):
        self._running = True
        self._gui = game_GUI(600,400)
        self.board = Board()

    def on_init(self):
        pygame.init()
        #print('board_drew')
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            self.press_key(event)


    def press_key(self,event):
        if event.key == pygame.K_UP:
            self.board.action('up')
        elif event.key == pygame.K_DOWN:
            self.board.action('down')
        elif event.key == pygame.K_LEFT:
            self.board.action('left')
        elif event.key == pygame.K_RIGHT:
            self.board.action('right')

    def on_loop(self):
        pass
    def on_render(self):
        self._gui.draw_board(self.board)
        pygame.display.update()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            #self.on_loop()
            self.on_render()
        self.on_cleanup()


class Board():
    import random
    #it's easier to move everything on board rather than moving individual squares.
    #once moved, update all blocks accordingly and put them in the right coordinate.
    # basically connect board with blocks 
    def __init__(self):
        self.board = [[0 for _ in range(4)] for _ in range(4) ]
        cnt = 0
        while cnt<2:
            x1,y1 = random.randint(0,3),random.randint(0,3)
            if self.board[x1][y1] == 0:
                self.board[x1][y1] = 2
                cnt+=1
            else:continue
    def get_value(self,x,y):
        return self.board[x][y]
    
    def set_value(self,x,y,val):
        self.board[x][y] = val
    
    def get_empty_cell(self):
        empty_list = []
        for x in range(4):
            for y in range(4):
                if self.board[x][y] == 0:
                    empty_list.append((x,y))
        return empty_list
    
    def spawn_new_block(self):
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
         
    def check_full(self):
        for x in range(4):
            for y in range(4):
                if self.board[x][y] == 0:
                    return False
        return True

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
        self.spawn_new_block()


class game_GUI():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))

    
    def draw_board(self,board):
        #cannot find a elegant way to update the whole screen
        self.screen.fill((255, 255, 255))
        print(board.board)
        sysfont = pygame.font.SysFont(None, 30)
        x_skip = self.width//4
        y_skip = self.height//4
        for x in range(4):
            for y in range(4):
                #left and top, so y and x actually
                block = pygame.Rect(y*x_skip, x*y_skip, x_skip,  y_skip)
                pygame.draw.rect(self.screen, (30, 222, 236), block, width = 5 )
                if board.board[x][y] != 0:
                    text = sysfont.render("{}".format(board.board[x][y]),True,(0,0,0))
                    text_coord = text.get_rect(center=(block.centerx, block.centery))
                    self.screen.blit(text,text_coord)
        #pygame.display.update()