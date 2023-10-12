import pygame
from settings import *
import random

#show text on surface with parameters given
def draw_text(surface,text,size,color,x,y,orientation):
    font=pygame.font.Font(pygame.font.match_font(FONT_NAME),size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    if orientation=='topleft':
        text_rect.topleft=(x,y)
    elif orientation=='midtop':
        text_rect.midtop=(x,y)
    elif orientation=='center':
        text_rect.center=(x,y)
    elif orientation=='topright':
        text_rect.topright=(x,y)
    surface.blit(text_surface,text_rect)

#classes
class Board(pygame.sprite.Sprite):
    def __init__(self,game,x,y,s):
        self.game=game
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        #create game board
        self.image=pygame.Surface((s,s))
        self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        
        self.BORDER=10
        self.TILE_SIZE=(s-5*self.BORDER)//4
        
        self.moved=True #checks if any tile has actually moved in a turn so a new tile isn't added when none is
        self.moving=False #keep track of move animation time for tiles
        
        #create empty list of tiles
        self.tiles=[]
        for _ in range(4):
            self.tiles.append([None,None,None,None])
            
    #when printed, Board shows matrix of tiles
    def __repr__(self):
        s=''
        for row in self.tiles:
            s=s+str(row)+'\n'
        return s
            
    #refill board based on which tiles are blank
    def update(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                if self.tiles[i][j] is None:
                    pygame.draw.rect(self.image,WHITE,(self.BORDER+j*(self.TILE_SIZE+self.BORDER),self.BORDER+i*(self.TILE_SIZE+self.BORDER),self.TILE_SIZE,self.TILE_SIZE))
                
    #move all tiles based on given direction, then combine tiles if possible
    def move(self,direction):
        self.moved=False
        if direction=='left':
            for i in range(len(self.tiles)):
                for j in range(1,len(self.tiles[i])):
                    if isinstance(self.tiles[i][j],Tile):
                        while j-1>=0 and self.tiles[i][j-1] is None:
                            self.tiles[i][j-1]=self.tiles[i][j]
                            self.tiles[i][j]=None
                            self.tiles[i][j-1].move(i,j-1)
                            j-=1
                            self.moved=True
                        if j-1>=0 and not (self.tiles[i][j-1] is None) and not self.tiles[i][j-1].has_combined and self.tiles[i][j-1].number==self.tiles[i][j].number:
                            self.tiles[i][j-1].number*=2
                            self.tiles[i][j-1].has_combined=True
                            self.tiles[i][j].kill()
                            self.tiles[i][j]=None
                            self.moved=True
                            self.game.score+=self.tiles[i][j-1].number
        elif direction=='right':
            for i in range(len(self.tiles)):
                for j in range(len(self.tiles[i])-2,-1,-1):
                    if isinstance(self.tiles[i][j],Tile):
                        while j+1<len(self.tiles[i]) and self.tiles[i][j+1] is None:
                            self.tiles[i][j+1]=self.tiles[i][j]
                            self.tiles[i][j]=None
                            self.tiles[i][j+1].move(i,j+1)
                            j+=1
                            self.moved=True
                        if j+1<len(self.tiles) and not (self.tiles[i][j+1] is None) and not self.tiles[i][j+1].has_combined and self.tiles[i][j+1].number==self.tiles[i][j].number:
                            self.tiles[i][j+1].number*=2
                            self.tiles[i][j+1].has_combined=True
                            self.tiles[i][j].kill()
                            self.tiles[i][j]=None
                            self.moved=True
                            self.game.score+=self.tiles[i][j+1].number
        elif direction=='up':
            for j in range(len(self.tiles[0])):
                for i in range(1,len(self.tiles)):
                    if isinstance(self.tiles[i][j],Tile):
                        while i-1>=0 and self.tiles[i-1][j] is None:
                            self.tiles[i-1][j]=self.tiles[i][j]
                            self.tiles[i][j]=None
                            self.tiles[i-1][j].move(i-1,j)
                            i-=1
                            self.moved=True
                        if i-1>=0 and not (self.tiles[i-1][j] is None) and not self.tiles[i-1][j].has_combined and self.tiles[i-1][j].number==self.tiles[i][j].number:
                            self.tiles[i-1][j].number*=2
                            self.tiles[i-1][j].has_combined=True
                            self.tiles[i][j].kill()
                            self.tiles[i][j]=None
                            self.moved=True
                            self.game.score+=self.tiles[i-1][j].number
        elif direction=='down':
            for j in range(len(self.tiles[0])):
                for i in range(len(self.tiles)-2,-1,-1):
                    if isinstance(self.tiles[i][j],Tile):
                        while i+1<len(self.tiles) and self.tiles[i+1][j] is None:
                            self.tiles[i+1][j]=self.tiles[i][j]
                            self.tiles[i][j]=None
                            self.tiles[i+1][j].move(i+1,j)
                            i+=1
                            self.moved=True
                        if i+1<len(self.tiles) and not (self.tiles[i+1][j] is None) and not self.tiles[i+1][j].has_combined and self.tiles[i+1][j].number==self.tiles[i][j].number:
                            self.tiles[i+1][j].number*=2
                            self.tiles[i+1][j].has_combined=True
                            self.tiles[i][j].kill()
                            self.tiles[i][j]=None
                            self.moved=True
                            self.game.score+=self.tiles[i+1][j].number
                            
        for row in self.tiles:
            for tile in row:
                if not (tile is None):
                    tile.has_combined=False
        if self.moved:
            self.moving=True
            self.game.add_now=True
            self.game.add_timer=pygame.time.get_ticks()
#         print(self)
        
    def new_tile(self):
        #check if board is full
        full=self.is_full()
        
        #if board is not full, add a new tile and see if it is full with the new tile
        if not full and self.moved:
            done=False
            while not done:
                r=random.randrange(len(self.tiles))
                c=random.randrange(len(self.tiles[r]))
                if self.tiles[r][c] is None:
                    done=True
                    self.tiles[r][c]=Tile(self,r,c,2)
#                     print("New tile at",r,c)
        
            full=self.is_full()
        
        #if board is full, check if there are any possible moves left
        if full:
            for i in range(len(self.tiles)):
                for j in range(len(self.tiles[i])):
                    if i-1>=0 and self.tiles[i][j].number==self.tiles[i-1][j].number:
                        full=False
                        break
                    if i+1<len(self.tiles) and self.tiles[i][j].number==self.tiles[i+1][j].number:
                        full=False
                        break
                    if j-1>=0 and self.tiles[i][j].number==self.tiles[i][j-1].number:
                        full=False
                        break
                    if j+1<len(self.tiles[i]) and self.tiles[i][j].number==self.tiles[i][j+1].number:
                        full=False
                        break
                if not full:
                    break
        
        #if there are no possible moves, end game
        if full:
            self.game.page='end'
        else:
            for row in self.tiles:
                for tile in row:
                    if tile is not None and tile.number==2048:
                        self.game.page='win'
    
    #check if all spaces in board are filled with tiles
    def is_full(self):
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    return False
        return True
    
    def clear(self):
        for row in self.tiles:
            for i in range(len(row)):
                if row[i] is not None:
                    row[i].kill()
                    row[i]=None
    
class Tile(pygame.sprite.Sprite):
    def __init__(self,board,r,c,n):
        self.game=board.game
        self.groups=self.game.all_sprites,self.game.tiles
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        #create tile image
        self.board=board
        self.image=pygame.Surface((self.board.TILE_SIZE,self.board.TILE_SIZE))
        self.image.fill(BLUE)
        self.rect=self.image.get_rect()
        self.rect.topleft=(10+self.board.BORDER+c*(self.board.TILE_SIZE+self.board.BORDER),10+self.board.BORDER+r*(self.board.TILE_SIZE+self.board.BORDER))
        
        self.old_loc=[0,0]
        self.new_loc=[0,0]
        self.set_old_loc(r,c)
        self.set_new_loc(r,c)
        
        self.number=n
        draw_text(self.image,str(self.number),48,BLACK,self.rect.width//2,self.rect.height//2,'center')
        
        self.has_combined=False
        self.is_combined=False
        
    def __repr__(self):
        return 'Tile('+str(self.number)+')'
        
    def update(self):
        self.image.fill(BLUE)
        draw_text(self.image,str(self.number),48,BLACK,self.rect.width//2,self.rect.height//2,'center')
        
    def set_old_loc(self,r,c):
        self.old_loc[0]=10+self.board.BORDER+r*(self.board.TILE_SIZE+self.board.BORDER)
        self.old_loc[1]=10+self.board.BORDER+c*(self.board.TILE_SIZE+self.board.BORDER)
        
    def set_new_loc(self,r,c):
        self.new_loc[0]=10+self.board.BORDER+r*(self.board.TILE_SIZE+self.board.BORDER)
        self.new_loc[1]=10+self.board.BORDER+c*(self.board.TILE_SIZE+self.board.BORDER)
        
    #resets image position to match new position in Board matrix
    def move(self,r,c):
        self.rect.topleft=(10+self.board.BORDER+c*(self.board.TILE_SIZE+self.board.BORDER),10+self.board.BORDER+r*(self.board.TILE_SIZE+self.board.BORDER))

class Button:
    def __init__(self,game,x,y,image):
        self.game=game
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.y=y
        self.clicked=False
    
    def draw(self):
        action=False
        #get mouse pos
        pos=pygame.mouse.get_pos()
        
        #check mouseover and click conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and not self.clicked:
                self.clicked=True
                action=True
            if pygame.mouse.get_pressed()[0]==0 and self.clicked:
                self.clicked=False
        
        self.game.screen.blit(self.image,self.rect)
        return action
