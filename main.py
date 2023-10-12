import pygame
from os import path
from settings import *
from sprites import *

#project by Brian Slonim
#Music: https://www.bensound.com
        
class Game:
    def __init__(self):
        #initialize pygame and create window
        pygame.mixer.pre_init(44100, -16, 1, 512)
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
        
        #use 2048 tile image from TILE_SET if it exists
        if TILE_SET:
            try:
                icon_img=pygame.image.load(path.join(self.img_dir,TILE_SET+"\\2048.png")).convert()
            except:
                try:
                    icon_img=pygame.image.load(path.join(self.img_dir,TILE_SET+"\\2048.jpg")).convert()
                except:
                    icon_img=pygame.image.load(path.join(self.img_dir,"icon.png")).convert()
        else:
            icon_img=pygame.image.load(path.join(self.img_dir,"icon.png")).convert()
        pygame.display.set_icon(icon_img)
        
        self.start_img=pygame.image.load(path.join(self.img_dir,"start.jpg")).convert()
        self.start_img=pygame.transform.scale(self.start_img,(WIDTH,HEIGHT))
        
        pygame.mixer.music.load(path.join(self.snd_dir,'bensound-jazzyfrenchy.mp3'))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    
    #start a new game
    def new(self):
        self.all_sprites=pygame.sprite.Group()
        self.tiles=pygame.sprite.Group()
        self.board=Board(self,BORDER,BORDER,SIDE*9//10)
        self.reset_board(True)
        
        img=pygame.Surface((WIDTH-3*BORDER-self.board.rect.width,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'START',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.start_button=Button(self,WIDTH//2-BORDER*2-img_rect.width//2,HEIGHT-(BORDER+img_rect.height*5//2),img)
        
        img=pygame.Surface((WIDTH-3*BORDER-self.board.rect.width,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'RULES',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.rules_button=Button(self,WIDTH//2+BORDER*2+img_rect.width//2,HEIGHT-(BORDER+img_rect.height*5//2),img)
        
        img=pygame.Surface((WIDTH-3*BORDER-self.board.rect.width,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'BACK',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.back_button=Button(self,WIDTH//2,HEIGHT-(BORDER+img_rect.height*3//2),img)
        
        img=pygame.Surface((WIDTH-3*BORDER-self.board.rect.width,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'RESET',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.reset_button=Button(self,WIDTH-BORDER-(WIDTH-self.board.rect.right-2*BORDER)//2,BORDER*2+50*2,img)
        
        img=pygame.Surface((WIDTH-3*BORDER-self.board.rect.width,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'BACK',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.back_button_2=Button(self,WIDTH-BORDER-(WIDTH-self.board.rect.right-2*BORDER)//2,BORDER*3+50*2+img_rect.height,img)
        
        img=pygame.Surface((WIDTH-3*BORDER-self.board.rect.width,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'TILES',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.tiles_button=Button(self,WIDTH-BORDER-(WIDTH-self.board.rect.right-2*BORDER)//2,BORDER*4+50*2+img_rect.height*2,img)
        
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
            elif self.page=='rules':
                self.rules_screen()
            elif self.page=='play':
                self.play_screen()
            elif self.page=='tiles':
                self.tiles_screen()
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
                self.board.save() #save board before closing program
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
                        
                        
        #slide tiles
        if self.board.moving:
            done=True
            for row in self.board.tiles:
                for tile in row:
                    if tile is not None:
                        if tile.old_loc[0]<tile.new_loc[0]:
                            done=False
                            tile.old_loc[0]+=TILE_MARGIN
                            tile.rect.y=tile.old_loc[0]
                            if abs(tile.rect.y-tile.new_loc[0])<TILE_MARGIN:
                                tile.rect.y=tile.new_loc[0]
                                tile.old_loc[0]=tile.new_loc[0]
                        elif tile.old_loc[0]>tile.new_loc[0]:
                            done=False
                            tile.old_loc[0]-=TILE_MARGIN
                            tile.rect.y=tile.old_loc[0]
                            if abs(tile.rect.y-tile.new_loc[0])<TILE_MARGIN:
                                tile.rect.y=tile.new_loc[0]
                                tile.old_loc[0]=tile.new_loc[0]
                        if tile.old_loc[1]<tile.new_loc[1]:
                            done=False
                            tile.old_loc[1]+=TILE_MARGIN
                            tile.rect.x=tile.old_loc[1]
                            if abs(tile.rect.x-tile.new_loc[1])<TILE_MARGIN:
                                tile.rect.x=tile.new_loc[1]
                                tile.old_loc[1]=tile.new_loc[1]
                        elif tile.old_loc[1]>tile.new_loc[1]:
                            done=False
                            tile.old_loc[1]-=TILE_MARGIN
                            tile.rect.x=tile.old_loc[1]
                            if abs(tile.rect.x-tile.new_loc[1])<TILE_MARGIN:
                                tile.rect.x=tile.new_loc[1]
                                tile.old_loc[1]=tile.new_loc[1]
                        self.board.moving=not done
                                
            #slide combined tiles
            for tile in self.board.combined_tiles:
                if tile is not None:
                    if tile.old_loc[0]<tile.new_loc[0]:
                        done=False
                        tile.old_loc[0]+=TILE_MARGIN
                        tile.rect.y=tile.old_loc[0]
                        if abs(tile.rect.y-tile.new_loc[0])<TILE_MARGIN:
                            tile.rect.y=tile.new_loc[0]
                            tile.old_loc[0]=tile.new_loc[0]
                    elif tile.old_loc[0]>tile.new_loc[0]:
                        done=False
                        tile.old_loc[0]-=TILE_MARGIN
                        tile.rect.y=tile.old_loc[0]
                        if abs(tile.rect.y-tile.new_loc[0])<TILE_MARGIN:
                            tile.rect.y=tile.new_loc[0]
                            tile.old_loc[0]=tile.new_loc[0]
                    if tile.old_loc[1]<tile.new_loc[1]:
                        done=False
                        tile.old_loc[1]+=TILE_MARGIN
                        tile.rect.x=tile.old_loc[1]
                        if abs(tile.rect.x-tile.new_loc[1])<TILE_MARGIN:
                            tile.rect.x=tile.new_loc[1]
                            tile.old_loc[1]=tile.new_loc[1]
                    elif tile.old_loc[1]>tile.new_loc[1]:
                        done=False
                        tile.old_loc[1]-=TILE_MARGIN
                        tile.rect.x=tile.old_loc[1]
                        if abs(tile.rect.x-tile.new_loc[1])<TILE_MARGIN:
                            tile.rect.x=tile.new_loc[1]
                            tile.old_loc[1]=tile.new_loc[1]
                            
                    self.board.moving=not done
            
            #combine tiles (kill one tile and update number on other)
            if not self.board.moving:
                for tile in self.board.combined_tiles:
                    tile.kill()
                for row in self.board.tiles:
                    for tile in row:
                        if tile is not None and tile.has_combined:
                            tile.number*=2
                            self.score+=tile.number
                            tile.has_combined=False
                    
        if self.add_now and not self.board.moving and pygame.time.get_ticks()-self.add_timer>DELAY:
            self.board.new_tile(True) #then add a new tile
            self.add_now=False
            self.add_timer=pygame.time.get_ticks()
                
        #update
        self.all_sprites.update()
        
        #draw/render
        self.screen.fill(WHITE)
        
        self.all_sprites.draw(self.screen)
        draw_text(self.screen,"Score: "+str(self.score),32,BLACK,self.board.rect.right+BORDER,BORDER,'topleft')
        draw_text(self.screen,"Highscore: "+str(self.highscore),32,BLACK,self.board.rect.right+BORDER,BORDER+50,'topleft')
        
        if self.reset_button.draw():
            self.reset_board(False) #save is included in method
        if self.back_button_2.draw():
            self.board.save() #save board before going back to start screen
            self.page='start'
            pygame.mixer.music.play(-1)
        if self.tiles_button.draw():
            self.page='tiles'
        
        pygame.display.flip()

    #start screen shown when game is first opened
    def start_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
        
        self.screen.fill(WHITE)
        self.screen.blit(self.start_img,(0,0,WIDTH,HEIGHT))
        
        if self.start_button.draw():
            self.page='play'
        if self.rules_button.draw():
            self.page='rules'
        
        pygame.display.flip()
          
    #page that shows how to play
    def rules_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
        
        self.screen.fill(WHITE)
        
        draw_text(self.screen,'RULES',96,RED,WIDTH//2,BORDER*2,'midtop')
        draw_text(self.screen,'Use the arrow keys to slide the tiles.',24,BLACK,WIDTH//2,HEIGHT//4+50,'midtop')
        draw_text(self.screen,'When two tiles of the same number meet, they combine.',24,BLACK,WIDTH//2,HEIGHT//4+50*2,'midtop')
        draw_text(self.screen,'If the board fills up and there are no more possible moves, you lose.',24,BLACK,WIDTH//2,HEIGHT//4+50*3,'midtop')
        draw_text(self.screen,'Press the reset button to reset the board if you lose, or if you want to start over.',24,BLACK,WIDTH//2,HEIGHT//4+50*4,'midtop')
        draw_text(self.screen,'Form a 2048 tile to win!',24,BLACK,WIDTH//2,HEIGHT//4+50*5,'midtop')
        
        
        if self.back_button.draw():
            self.page='start'
            
        pygame.display.flip()
        
    #page that shows which tiles are which number
    def tiles_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.board.save() #save board before closing game
                self.playing=False
                self.running=False
        
        self.screen.fill(WHITE)
        
        draw_text(self.screen,'TILES',96,RED,WIDTH//2,BORDER*2,'midtop')
        
        x=BORDER
        y=BORDER*3+100
        for i in range(1,min(14,len(self.board.tile_imgs))): #up to 2^13, or 8192
            self.screen.blit(self.board.tile_imgs[i],(x,y))
            pygame.draw.rect(self.screen,BLACK,(x,y+self.board.TILE_SIZE-self.board.TILE_SIZE//4,self.board.TILE_SIZE,self.board.TILE_SIZE//4))
            draw_text(self.screen,str(2**i),32,WHITE,x+self.board.TILE_SIZE//2,y+self.board.TILE_SIZE-self.board.TILE_SIZE//8,'center')
            x+=self.board.TILE_SIZE+BORDER
            if x>=WIDTH:
                x=BORDER
                y+=BORDER+self.board.TILE_SIZE
        
        if self.back_button.draw():
            self.page='play'
            
        pygame.display.flip()
        
    #end screen shown when game is over
    def end_screen(self,win):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.board.save() #save board before closing program
                self.playing=False
                self.running=False
        
        if not self.updated_highscore:
            self.updated_highscore=True
            o_f = open('highscore.txt', 'w')
            if self.score>self.highscore:
                o_f.write(str(self.score))
                self.highscore=self.score
            else:
                o_f.write(str(self.highscore))
            o_f.close()
                
        if win:
            text="YOU WIN"
        else:
            text="GAME OVER"
            
        draw_text(self.screen,text,48,RED,self.board.rect.centerx,self.board.rect.centery,'center')
        
        if self.reset_button.draw():
            self.reset_board(False) #save is included in method
            self.page='play'
        if self.back_button_2.draw():
            self.board.save() #save board because why not
            if win:
                self.page='play' #go back to play screen to keep playing if you won
                self.updated_highscore=False
            else:
                self.page='start' #if you lost, go back to start screen and have a reset board ready
                self.reset_board(False)
                pygame.mixer.music.play(-1)
        if self.tiles_button.draw():
            self.page='tiles'
        
        pygame.display.flip()
        
    #resets board and score for new game. should_load is True if loading a previous game
    def reset_board(self, should_load):
        if should_load:
            self.board.load()
            
        else:
            self.board.clear()
            #start with 2 randomly placed tiles
            for _ in range(2):
                self.board.new_tile(True) #new tiles can be 2 or 4
            self.score=0
            
        self.add_timer=0
        self.add_now=False
        self.moved=True
        
        try:
            i_f=open('highscore.txt','r')
            self.highscore=int(i_f.read())
            i_f.close()
        except:
            self.highscore=0
            
        self.updated_highscore=False
        
        
        ###TEST CASES###
#         self.board.tiles[0][0]=Tile(self.board,0,0,1024)
#         self.board.tiles[1][0]=Tile(self.board,1,0,1024)
#         self.board.tiles[2][0]=Tile(self.board,2,0,2)
#         self.board.tiles[3][0]=Tile(self.board,3,0,2)
#         for i in range(1,15):
#             self.board.tiles[i//4][i%4]=Tile(self.board,i//4,i%4,2**i)
            
        self.board.save()

g=Game()
while g.running:
    g.new()

pygame.quit()