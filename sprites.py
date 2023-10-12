import pygame
from settings import *
import random
from os import path
from math import log2

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
        self.image.fill(BG_COLOR_1)
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        
        #tile dimensions set
        self.BORDER=10
        self.TILE_SIZE=(s-5*self.BORDER)//4
        
        #tile images loaded
        self.tile_img_dir=path.join(self.game.img_dir,TILE_SET)
        self.tile_imgs=[None]
        for i in range(1,14): #goes up to 8192, or 2^13
            number=2**i
            try: #try png first, and if not that then jpg. otherwise, image DNE and use number instead
                img=pygame.image.load(path.join(self.tile_img_dir,str(number)+".png")).convert()
                img=pygame.transform.scale(img,(self.TILE_SIZE,self.TILE_SIZE))
            except:
                try:
                    img=pygame.image.load(path.join(self.tile_img_dir,str(number)+".jpg")).convert()
                    img=pygame.transform.scale(img,(self.TILE_SIZE,self.TILE_SIZE))
                except:
                    img=pygame.Surface((self.TILE_SIZE,self.TILE_SIZE))
                    img.fill(TILE_COLORS[min(int(log2(number)),12)]) #gives color corresponding to numbers 2-2048, or RED for higher
                    draw_text(img,str(number),48,BLACK,img.get_rect().width//2,img.get_rect().height//2,'center')
            self.tile_imgs.append(img)
        
        self.moved=True #checks if any tile has actually moved in a turn so a new tile isn't added when none is
        self.moving=False #keep track of move animation time for tiles
        self.has_won=False #keep track of if 2048 has been reached yet
        self.combined_tiles=[]
        
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
                    pygame.draw.rect(self.image,BG_COLOR_2,(self.BORDER+j*(self.TILE_SIZE+self.BORDER),self.BORDER+i*(self.TILE_SIZE+self.BORDER),self.TILE_SIZE,self.TILE_SIZE))
                
    #move all tiles based on given direction, then combine tiles if possible
    def move(self,direction):
        self.moved=False
        self.combined_tiles.clear()
        
        if direction=='left':
            for i in range(len(self.tiles)):
                for j in range(1,len(self.tiles[i])):
                    if isinstance(self.tiles[i][j],Tile):
                        if j-1>=0 and self.tiles[i][j-1] is None:
                            self.tiles[i][j].set_old_loc(i,j)
                            
                            while j-1>=0 and self.tiles[i][j-1] is None:
                                self.tiles[i][j-1]=self.tiles[i][j]
                                self.tiles[i][j]=None
                                self.tiles[i][j-1].set_new_loc(i,j-1)
                                j-=1
                                self.moved=True
                        if j-1>=0 and not (self.tiles[i][j-1] is None) and not self.tiles[i][j-1].has_combined and self.tiles[i][j-1].number==self.tiles[i][j].number:
#                             self.tiles[i][j-1].number*=2
                            self.tiles[i][j-1].has_combined=True
                            
                            self.tiles[i][j].set_new_loc(i,j-1)
                            self.combined_tiles.append(self.tiles[i][j])
                            
#                             self.tiles[i][j].kill()
                            self.tiles[i][j]=None
                            self.moved=True
#                             self.game.score+=self.tiles[i][j-1].number
        elif direction=='right':
            for i in range(len(self.tiles)):
                for j in range(len(self.tiles[i])-2,-1,-1):
                    if isinstance(self.tiles[i][j],Tile):
                        if j+1<len(self.tiles[i]) and self.tiles[i][j+1] is None:
                            self.tiles[i][j].set_old_loc(i,j)
                            
                            while j+1<len(self.tiles[i]) and self.tiles[i][j+1] is None:
                                self.tiles[i][j+1]=self.tiles[i][j]
                                self.tiles[i][j]=None
                                self.tiles[i][j+1].set_new_loc(i,j+1)
                                j+=1
                                self.moved=True
                        if j+1<len(self.tiles) and not (self.tiles[i][j+1] is None) and not self.tiles[i][j+1].has_combined and self.tiles[i][j+1].number==self.tiles[i][j].number:
#                             self.tiles[i][j+1].number*=2
                            self.tiles[i][j+1].has_combined=True
                            
                            self.tiles[i][j].set_new_loc(i,j+1)
                            self.combined_tiles.append(self.tiles[i][j])
                            
#                             self.tiles[i][j].kill()
                            self.tiles[i][j]=None
                            self.moved=True
#                             self.game.score+=self.tiles[i][j+1].number
        elif direction=='up':
            for j in range(len(self.tiles[0])):
                for i in range(1,len(self.tiles)):
                    if isinstance(self.tiles[i][j],Tile):
                        if i-1>=0 and self.tiles[i-1][j] is None:
                            self.tiles[i][j].set_old_loc(i,j)
                            
                            while i-1>=0 and self.tiles[i-1][j] is None:
                                self.tiles[i-1][j]=self.tiles[i][j]
                                self.tiles[i][j]=None
                                self.tiles[i-1][j].set_new_loc(i-1,j)
                                i-=1
                                self.moved=True
                        if i-1>=0 and not (self.tiles[i-1][j] is None) and not self.tiles[i-1][j].has_combined and self.tiles[i-1][j].number==self.tiles[i][j].number:
#                             self.tiles[i-1][j].number*=2
                            self.tiles[i-1][j].has_combined=True
                            
                            self.tiles[i][j].set_new_loc(i-1,j)
                            self.combined_tiles.append(self.tiles[i][j])
                            
#                             self.tiles[i][j].kill()
                            self.tiles[i][j]=None
                            self.moved=True
#                             self.game.score+=self.tiles[i-1][j].number
        elif direction=='down':
            for j in range(len(self.tiles[0])):
                for i in range(len(self.tiles)-2,-1,-1):
                    if isinstance(self.tiles[i][j],Tile):
                        if i+1<len(self.tiles) and self.tiles[i+1][j] is None:
                            self.tiles[i][j].set_old_loc(i,j)
                            
                            while i+1<len(self.tiles) and self.tiles[i+1][j] is None:
                                self.tiles[i+1][j]=self.tiles[i][j]
                                self.tiles[i][j]=None
                                self.tiles[i+1][j].set_new_loc(i+1,j)
                                i+=1
                                self.moved=True
                        if i+1<len(self.tiles) and not (self.tiles[i+1][j] is None) and not self.tiles[i+1][j].has_combined and self.tiles[i+1][j].number==self.tiles[i][j].number:
#                             self.tiles[i+1][j].number*=2
                            self.tiles[i+1][j].has_combined=True
                            
                            self.tiles[i][j].set_new_loc(i+1,j)
                            self.combined_tiles.append(self.tiles[i][j])
                            
#                             self.tiles[i][j].kill()
                            self.tiles[i][j]=None
                            self.moved=True
#                             self.game.score+=self.tiles[i+1][j].number
                            
#         for row in self.tiles:
#             for tile in row:
#                 if not (tile is None):
#                     tile.has_combined=False
        if self.moved:
            self.moving=True
            self.game.add_now=True
            self.game.add_timer=pygame.time.get_ticks()
#         print(self)
        
    def new_tile(self,four_able): #four able if tile can be 4 (ie not the first two tiles)
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
                    n=2
                    if four_able and random.random()<1/10:
                        n=4
                    self.tiles[r][c]=Tile(self,r,c,n)
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
        
        #check if game is won, if so don't do anything
        if self.check_win(True):
            return
        #if there are no possible moves, end game
        if full:
            self.game.page='end'
         
    #check for 2048 tile on board and if there is one, end game
    def check_win(self,play_sound):
        if not self.has_won:
            for row in self.tiles:
                for tile in row:
                    if tile is not None and tile.number>=2048:
                        self.has_won=True
                        self.game.page='win'
                        if play_sound:
                            pygame.mixer.Sound(path.join(self.game.snd_dir,'victory.ogg')).play()
                        return True
    
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
        self.has_won=False
                    
    #save current arrangement of tiles on board and current score
    def save(self):
        o_f = open('board.txt', 'w')
        o_f.write(str(self.game.score)+'\n')
        for row in self.tiles:
            for tile in row:
                if tile:
                    o_f.write(str(tile.number)+' ')
                else:
                    o_f.write('X ')
            o_f.write('\n')
        o_f.close()
        
    #load data from board.txt into board in program
    def load(self):
        self.clear()
        try:
            i_f=open('board.txt','r')
            lines=i_f.readlines()
            self.game.score=int(lines[0])
            for i in range(1,len(lines)):
                line=lines[i].split()
                for j in range(len(line)):
                        try:
                            self.tiles[i-1][j]=Tile(self,i-1,j,int(line[j]))
                        except:
                            pass
            i_f.close()
            
            self.has_won=self.check_win(False)
            
        except:
            self.game.score=0
            for _ in range(2):
                self.new_tile(False)
    
class Tile(pygame.sprite.Sprite):
    def __init__(self,board,r,c,n):
        self.game=board.game
        self.groups=self.game.all_sprites,self.game.tiles
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        #create tile image
        self.number=n
        self.board=board
        
        #get image for tile of this number. if DNE, use red square with number as text
        try:
            self.image=self.game.board.tile_imgs[int(log2(self.number))]
        except:
            img=pygame.Surface((self.board.TILE_SIZE,self.board.TILE_SIZE))
            img.fill(BLACK)
            draw_text(img,str(self.number),48,WHITE,img.get_rect().width//2,img.get_rect().height//2,'center')
            self.image=img
            
        self.rect=self.image.get_rect()
        self.rect.topleft=(10+self.board.BORDER+c*(self.board.TILE_SIZE+self.board.BORDER),10+self.board.BORDER+r*(self.board.TILE_SIZE+self.board.BORDER))
        
        self.old_loc=[0,0]
        self.new_loc=[0,0]
        self.set_old_loc(r,c)
        self.set_new_loc(r,c)
        
        self.has_combined=False
        
    def __repr__(self):
        return 'Tile('+str(self.number)+')'
        
    def update(self):
        #get image for tile of this number. if DNE, use red square with number as text
        try:
            self.image=self.game.board.tile_imgs[int(log2(self.number))]
        except:
            img=pygame.Surface((self.board.TILE_SIZE,self.board.TILE_SIZE))
            img.fill(RED)
            draw_text(img,str(self.number),48,BLACK,img.get_rect().width//2,img.get_rect().height//2,'center')
            self.image=img
        
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
