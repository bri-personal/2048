#game options/settings
TITLE="2048"
WIDTH= 800
HEIGHT=600
SIDE=min(WIDTH,HEIGHT) #use for measurements based on smaller side of window
FPS=60

DELAY=150 #delay when tiles are shifted before new tile appears, in ms
BORDER=10 #px
TILE_MARGIN=35

#define fonts
FONT_NAME='Arial'

#define tileset (cupcake or sus). use empty string for numbers only
TILE_SET='cupcake'

#define colors
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)

BG_COLOR_1=(91,91,91)
BG_COLOR_2=(153,153,153)

TILE_COLORS=[WHITE,(219,229,241),(250,239,211),(242,200,160),(255,114,0),(255,85,17),(255,69,0),(245,207,90),(241,194,50),(233,177,9),(237,178,0),(255,192,0),RED]