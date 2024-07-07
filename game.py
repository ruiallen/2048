import random
import pygame
import collections
import time
import sys
class App():
    #handles everything related to a game (initialize, exit etc.)
    #main running unit
    def __init__(self):
        pygame.init()
        self._running = True
        self._gui = game_GUI(600,400)
        self.board = Board()
        self.restart = False

    def press_key(self,event):
        #key events during the game run
        try:
            if event.key == pygame.K_UP:
                self.board.action('up')
            elif event.key == pygame.K_DOWN:
                self.board.action('down')
            elif event.key == pygame.K_LEFT:
                self.board.action('left')
            elif event.key == pygame.K_RIGHT:
                self.board.action('right')
            elif event.key == pygame.K_r:
                self.restart = True
            else:
                raise Exception('not a valid input')
        except Exception as e:
            self._gui.display_msg(e)
            pygame.display.update()
            time.sleep(0.3)
            #go back to the previous display
            self.on_render()
        

    def on_render(self):
        if self._gui.window == 'main_menu':
            self._gui.show_main_menu()
            #when at the main menu, initialize the board
            self.board = Board()
        if self._gui.window == 'run':
            self._gui.draw_board(self.board)
            if self.board.winFlag:
                self._gui.show_result("Congratulations!")
            if self.board.loseFlag:
                self._gui.show_result("Game Over.")
        pygame.display.update()
    
    def on_cleanup():
        pygame.quit()
        sys.exit()

    def run_game(self):
        while( self._running ):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.KEYDOWN:
                    self.press_key(event)
                    if self.restart:
                        self._gui.window = 'main_menu'
                        self.restart = False
            self.on_render()
        self.on_cleanup()

class Board():
    import random
    #fundamental logic object of the game
    #it's easier to move everything on board rather than moving individual squares.
    def __init__(self):
        self.board = [[0 for _ in range(4)] for _ in range(4) ]
        cnt = 0
        while cnt<2:
            x1,y1 = random.randint(0,3),random.randint(0,3)
            if self.board[x1][y1] == 0:
                self.board[x1][y1] = 2
                cnt+=1
            else:continue
        self.score = 0
        self.loseFlag = False
        self.winFlag = False
        self.target = 32
        self.moves = 0
        
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
                    self.score = max(self.score,val+val)
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
                    self.score = max(self.score,val+val)
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
                    self.score = max(self.score,val+val)
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
                    self.score = max(self.score,val+val)
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
        #after a full cycle of actions (move, merge and move), check if win or lose
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
        win = self.check_win(64)
        if win: self.winFlag = True
        fail = self.check_fail()
        if not fail:
            if not self.check_full():
                self.spawn_new_block()
        else:self.loseFlag = True

    def check_win(self,target):
        return self.score >= self.target

    def check_fail(self):
        #if not full, not fail yet
        if not self.check_full():
            return False
        #if full but can still make a move, not fail yet
        else:
            for row in range(4):
                for col in range(3):
                    if self.board[row][col+1] == self.board[row][col]:
                        return False
            for col in range(4):
                for row in range(3):
                    if self.board[row+1][col] == self.board[row][col]:
                        return False
        return True

class game_GUI():
    #a class that is responsible for displaying everything
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))
        self.window = 'main_menu'
        self.blockColor = {
        0:(204,192,179),
        2:(238,228,218),
        4:(237,224,200),
        8:(242,177,121),
        16:(245,149,99),
        32: (246,124,95),
        64: (246,94,59),
        128: (237,204,114),
        256: (237,204,97),
        512: (237,200,80),
        1024: (237,197,63),
        2048: (237,194,46)
    }
        
    def draw_board(self,board):
        #cannot find a elegant way to update the whole screen
        colorList = self.blockColor
        self.screen.fill((255, 255, 255))
        sysFont = pygame.font.SysFont(None, 30)
        x_skip = self.width//4
        y_skip = self.height//4
        for x in range(4):
            for y in range(4):
                #draw boardes
                boarder = pygame.Rect(x*x_skip, y*y_skip, x_skip,  y_skip)
                pygame.draw.rect(self.screen, color=colorList[0], rect=boarder, width = 10)
        for x in range(4):
            for y in range(4):
                #left and top, so y and x actually
                block = pygame.Rect(y*x_skip, x*y_skip, x_skip,  y_skip)
                pygame.draw.rect(self.screen,self.blockColor[board.board[x][y]], block, width = 0,border_radius=2 )
                if board.board[x][y] != 0:
                    text = sysFont.render("{}".format(board.board[x][y]),True,(0,0,0))
                    textCoord = text.get_rect(center=(block.centerx, block.centery))
                    self.screen.blit(text,textCoord)
    
    def show_main_menu(self):
        self.screen.fill((238, 228, 218))
        loseText = pygame.font.SysFont('Purisa', 90).render(
            "2048 Game", True, (119, 110, 101))
        loseCoord = loseText.get_rect(center = (self.width/2, self.height/2))
        self.screen.blit(loseText,loseCoord)
        time.sleep(0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.window = 'run'


    def show_result(self,msg):
        time.sleep(0.5)
        #self.screen.fill((238, 228, 218))
        loseText = pygame.font.SysFont('Purisa', 90).render("{}".format(msg), True, (119, 110, 101))
        loseCoord = loseText.get_rect(center = (self.width/2, self.height/2))
        againText = pygame.font.SysFont('Purisa', 30).render(
            "Press y or Enter to try again, or n to quit", True, (119, 110, 101))
        againCoord = loseText.get_rect(center = (self.width/2, 2*self.height/3))

        self.screen.blit(loseText,loseCoord)
        self.screen.blit(againText,againCoord)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_y:
                    self.window = 'main_menu'
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()
                
    
    def display_msg(self,msg):
        #To display a message on screen for a short time
        text = pygame.font.SysFont('Purisa', 90).render("{}".format(msg), True, (119, 110, 101))
        textCoord = text.get_rect(center = (self.width/2, self.height/2))
        self.screen.blit(text,textCoord)


    
