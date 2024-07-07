import random
import pygame
import time
import sys
class App():
    #handles everything related to a game (initialize, exit etc.)
    #main running unit
    def __init__(self):
        self._running = True
        self.board = Board()
        self._gui = game_GUI(800,600)
        self.restart = False

    def press_key(self,event):
        #handle button movements
        try:
            if self._gui.window == 'run':
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.board.action('up')
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.board.action('down')
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.board.action('left')
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.board.action('right')
                elif event.key == pygame.K_r:
                    self.restart = True
                else:
                    raise Exception('not a valid input')
            elif self._gui.window == 'main_menu':
                if event.key == pygame.K_RETURN:
                    self._gui.window = 'set_difficulty' 
                else:
                    raise Exception('not a valid input')
            elif self._gui.window == 'set_difficulty':
                if event.key == pygame.K_1:
                    self.board.set_target(32)
                elif event.key == pygame.K_2:
                    self.board.set_target(512)
                elif event.key == pygame.K_3:
                    self.board.set_target(2048)
                elif event.key == pygame.K_RETURN:
                    self._gui.window = 'run' 
                else:
                    raise Exception('not a valid input')
            elif self._gui.window == 'result':
                if event.key == pygame.K_n:
                    self._running = False
                elif event.key == pygame.K_RETURN:
                    self._gui.window = 'main_menu'
                else:
                    raise Exception('not a valid input')
        except Exception as e:
            self._gui.display_msg(e)
            pygame.display.update()
            time.sleep(0.16)
        finally:
            self.on_render()
        

    def on_render(self):
        if self._gui.window == 'main_menu':
            #when at the main menu, initialize the board
            self.board = Board()
            self._gui.show_main_menu()
        if self._gui.window == 'set_difficulty':
            self._gui.set_difficulty(self.board)
        if self._gui.window == 'run':
            self._gui.draw_board(self.board)
            self._gui.draw_boarder()
            
        if self._gui.window == 'result':
            if self.board.loseFlag:
                self._gui.show_result("Game Over.",self.board)
            elif self.board.winFlag:
                self._gui.show_result("Congratulations!",self.board)
        pygame.display.update()
    
    def on_cleanup(self):
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
        self.target = 2048
        self.moves = 0
        
    def get_value(self,x,y):
        return self.board[x][y]
    
    def set_value(self,x,y,val):
        self.board[x][y] = val
    
    def get_target(self):
        return self.target
    
    def set_target(self,val):
        self.target = val

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
        #check if the game should be eneded at the end of each action
        if self.check_win(): self.winFlag = True
        if not self.check_fail():
            if not self.check_full():
                self.spawn_new_block()
        else:self.loseFlag = True

    def check_win(self):
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
        
    def draw_boarder(self):
        sysFont = pygame.font.SysFont(None, 30)
        x_skip = self.width//4
        y_skip = self.height//4
        for x in range(4):
            for y in range(4):
                #draw boarders
                boarder = pygame.Rect(y*x_skip, x*y_skip, x_skip,  y_skip)
                pygame.draw.rect(self.screen, color=(204,192,179), rect=boarder, width = 10)

    def draw_board(self,board):
        #display the curent board on screen
        colorList = self.blockColor
        self.screen.fill((255, 255, 255))
        sysFont = pygame.font.SysFont(None, 30)
        x_skip = self.width//4
        y_skip = self.height//4
        for x in range(4):
            for y in range(4):
                #left and top, so y and x actually
                block = pygame.Rect(y*x_skip, x*y_skip, x_skip,  y_skip)
                pygame.draw.rect(self.screen,self.blockColor[board.board[x][y]], block, width = 0,border_radius=2 )
                if board.board[x][y] != 0:
                    text = sysFont.render("{}".format(board.board[x][y]),True,(0,0,0))
                    textCoord = text.get_rect(center=(block.centerx, block.centery))
                    self.screen.blit(text,textCoord)
        #update the display flag if ended
        if board.winFlag:
            self.window = 'result'
        if board.loseFlag:
            self.window = 'result'

    
   
    def show_main_menu(self):
        #main menu display
        self.screen.fill((238, 228, 218))
        welcomeText = pygame.font.SysFont('Purisa', 80,bold = True).render("2048 Game", True, (119, 110, 101))
        welcomeCoord = welcomeText.get_rect(center = (0.5*self.width, 0.2*self.height))
        welcomeText2 = pygame.font.SysFont('Purisa', 50).render("by Ruihan Wang", True, (119, 110, 101))
        welcomeCoord2 = welcomeText.get_rect(center = (0.7*self.width, 0.4*self.height))
        self.screen.blit(welcomeText,welcomeCoord)
        self.screen.blit(welcomeText2,welcomeCoord2)
        welcomeText4 = pygame.font.SysFont('Purisa', 50).render("Press Enter to Continue", True, (119, 110, 101))
        welcomeCoord4 = welcomeText.get_rect(center = (0.35*self.width, 0.9*self.height))
        self.screen.blit(welcomeText4,welcomeCoord4)
                
    def set_difficulty(self,board): 
        #difficulty setting display
        self.screen.fill((238, 228, 218))
        welcomeText3 = pygame.font.SysFont('Serif', 30,italic=True).render("Select a difficulty (Current: {})".format(board.get_target()), True, (119, 110, 101))
        welcomeCoord3 = welcomeText3.get_rect(center = (0.5*self.width, 0.3*self.height))
        self.screen.blit(welcomeText3,welcomeCoord3)

        welcomeText3 = pygame.font.SysFont('Serif', 30,italic=True).render("Press 1, 2 or 3 to select".format(board.get_target()), True, (119, 110, 101))
        welcomeCoord3 = welcomeText3.get_rect(center = (0.5*self.width, 0.4*self.height))
        self.screen.blit(welcomeText3,welcomeCoord3)

        difficultyText1 = pygame.font.SysFont('Purisa', 50).render("32", True, (119, 110, 101))
        difficultyCoord1 = difficultyText1.get_rect(center = (0.3*self.width, 0.6*self.height))
        pygame.draw.rect(self.screen,(0, 0, 0),rect = difficultyCoord1, width = 2)
        self.screen.blit(difficultyText1,difficultyCoord1)

        difficultyText2 = pygame.font.SysFont('Purisa', 35).render("512", True, (119, 110, 101))
        difficultyCoord2 = difficultyText1.get_rect(center = (0.5*self.width, 0.6*self.height))
        pygame.draw.rect(self.screen,(0, 0, 0),rect = difficultyCoord2, width = 2)
        self.screen.blit(difficultyText2,difficultyCoord2)

        difficultyText3 = pygame.font.SysFont('Purisa', 25).render("2048", True, (119, 110, 101))
        difficultyCoord3 = difficultyText1.get_rect(center = (0.7*self.width, 0.6*self.height))
        pygame.draw.rect(self.screen,(0, 0, 0),rect = difficultyCoord3, width = 2)
        self.screen.blit(difficultyText3,difficultyCoord3)

        welcomeText4 = pygame.font.SysFont('Purisa', 50).render("Press Enter to start", True, (119, 110, 101))
        welcomeCoord4 = welcomeText4.get_rect(center = (0.5*self.width, 0.9*self.height))
        self.screen.blit(welcomeText4,welcomeCoord4)
        time.sleep(0.2)
            
    def show_result(self,msg,board):
        self.draw_board(board)
        self.draw_boarder()
        loseText = pygame.font.SysFont('Purisa', 90).render("{}".format(msg), True, (119, 110, 101))
        loseCoord = loseText.get_rect(center = (self.width/2, self.height/2))
        againText = pygame.font.SysFont('Purisa', 30).render(
            "Press n to quit or Enter to restart", True, (119, 110, 101))
        againCoord = loseText.get_rect(center = (self.width/2, 2*self.height/3))
        self.screen.blit(loseText,loseCoord)
        self.screen.blit(againText,againCoord)
                

    def display_msg(self,msg):
        #To display an error message
        text = pygame.font.SysFont('Purisa', 70).render("{}".format(msg), True, (119, 110, 101))
        textCoord = text.get_rect(center = (self.width/2, 0.1*self.height))
        self.screen.blit(text,textCoord)


    
