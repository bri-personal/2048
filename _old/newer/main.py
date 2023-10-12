import pygame
import random
from os import path
from settings import *
from sprites import *
        
class Game:
    def __init__(self):
        #initialize pygame and create window
        pygame.init()
        pygame.mixer.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock=pygame.time.Clock()
        self.font_name=pygame.font.match_font(FONT_NAME)
        self.load_data()
        self.running=True
        
    #load images, sounds, etc.
    def load_data(self):
        self.dir=path.dirname(__file__)
        self.img_dir=path.join(self.dir,'img')
        self.snd_dir=path.join(self.dir,'snd')
    
    #start a new game
    def new(self):
        self.all_sprites=pygame.sprite.Group()
        self.tiles=pygame.sprite.Group()
        self.board=Board(self,BORDER,BORDER,SIDE*9//10)
        
        img=pygame.Surface((WIDTH-3*BORDER-self.board.rect.width,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'RESET',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.reset_button=Button(self,WIDTH-BORDER-(WIDTH-self.board.rect.right-2*BORDER)//2,BORDER+50,img)
        
        #start with 2 randomly placed tiles
        for _ in range(2):
            self.board.new_tile()
        
#         self.board.tiles[0][0]=Tile(self.board,0,0,1024)
#         self.board.tiles[0][1]=Tile(self.board,0,1,1024)
#         self.board.tiles[0][2]=Tile(self.board,0,2,2)

#         for i in range(len(self.board.tiles)):
#             for j in range(len(self.board.tiles[i])):
#                 self.board.tiles[i][j]=Tile(self.board,i,j,i*8+(j+1)*2)
#         self.board.tiles[0][0]=None
        
        self.score=0
        self.add_timer=0
        self.add_now=False
        self.page='start'
        self.run()

    #main loop calls other methods for specific pages
    def run(self):
        self.playing=True
        while self.playing:
            #keep loop running at correct speed
            self.clock.tick(FPS)
            if self.page=='start':
                self.start_screen()
            elif self.page=='play':
                self.play_screen()
            elif self.page=='end':
                self.end_screen(False)
            elif self.page=='win':
                self.end_screen(True)
            else:
                print("Page not found!")
                self.page='start'
            
    #default game loop method
    def play_screen(self):
        #process input (events)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    if not self.add_now and not self.board.moving:
                        self.board.move('left') #move all tiles left
                    
                if event.key==pygame.K_RIGHT:
                    if not self.add_now and not self.board.moving:
                        self.board.move('right') #move all tiles right
                    
                if event.key==pygame.K_UP:
                    if not self.add_now and not self.board.moving:
                        self.board.move('up') #move all tiles up

                if event.key==pygame.K_DOWN:
                    if not self.add_now and not self.board.moving:
                        self.board.move('down') #move all tiles down
                        
        if self.board.moving:
            done=True
            for row in self.board.tiles:
                for tile in row:
                    if tile is not None:
                        if tile.old_loc[0]<tile.new_loc[0]:
                            done=False
                            tile.old_loc[0]+=10
                            tile.rect.y=tile.old_loc[0]
                        elif tile.old_loc[0]>tile.new_loc[0]:
                            done=False
                            tile.old_loc[0]-=10
                            tile.rect.y=tile.old_loc[0]
                        if tile.old_loc[1]<tile.new_loc[1]:
                            done=False
                            tile.old_loc[1]+=10
                            tile.rect.x=tile.old_loc[1]
                        elif tile.old_loc[1]>tile.new_loc[1]:
                            done=False
                            tile.old_loc[1]-=10
                            tile.rect.x=tile.old_loc[1]
                    self.board.moving=not done
                    
        if self.add_now and not self.board.moving and pygame.time.get_ticks()-self.add_timer>DELAY:
            self.board.new_tile() #then add a new tile
            self.add_now=False
            self.add_timer=pygame.time.get_ticks()
                
        #update
        self.all_sprites.update()
        
        #draw/render
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        draw_text(self.screen,"Score: "+str(self.score),36,BLACK,self.board.rect.right+BORDER,BORDER,'topleft')
        
        if self.reset_button.draw():
            self.reset_board()
        
        pygame.display.flip()
        
#         print(self.board.tiles)

    #start screen shown when game is first opened
    def start_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                self.page='play'
        self.screen.fill(BLACK)
        draw_text(self.screen,TITLE,48,WHITE,WIDTH//2,HEIGHT//4,'midtop')
        pygame.display.flip()
        
    #end screen shown when game is over
    def end_screen(self,win):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
                
        if win:
            text="YOU WIN"
        else:
            text="GAME OVER"
            
        draw_text(self.screen,text,48,RED,self.board.rect.centerx,self.board.rect.centery,'center')
        
        if self.reset_button.draw():
            self.reset_board()
            self.page='play'
        
        pygame.display.flip()
        
    def reset_board(self):
        self.board.clear()
        self.score=0
        self.add_timer=0
        self.add_now=False
        #start with 2 randomly placed tiles
        for _ in range(2):
            self.board.new_tile()

g=Game()
while g.running:
    g.new()

pygame.quit()