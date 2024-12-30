from kandinsky import *
from ion import *
from time import sleep,monotonic
from random import *

global all

#Settings
baseSnakeSize=4
speed=1
snakeColor=color(0,255,0)
snakeInnerEyesColor="black"
snakeOuterEyesColor="white"
backgroundColor=color(0,0,0)
appleColor=color(255,0,0)
appleStemColor=color(0,250,0)
mainMenuInstColor='red'
mainMenuBackgroundColor=color(50,50,50)
deathScreenBackgroundColor=color(50,50,50)
deathScreenTextColor='white'
deathScreenInstColor='red'
deathScreenScoreColor='orange'
gameFooterColor=color(50,50,50)
gameFooterTextColor="white"

# -------------------------------------
# DO NOT EDIT THE CODE AFTER THIS LINE!
# -------------------------------------

#Variables for the game
applePresence=False
justDied=False
start=monotonic()
score=0
bestScore=0


def centerString(s):
  return " " * int((32-len(s))/2) + s + " " * int((32-len(s))/2)

def score(start):
  score=int(round(monotonic()-start,0))+(len(player.tiles)-4)*100
  return score
    
def resetScore():
  global start
  start=monotonic()
  score(monotonic())
 
def setBestScore(score):
  global bestScore
  bestScore=score

#The snake class
class Snake():
  def __init__(self):
    self.x=150
    self.y=101
    self.di=0
    self.moves=[]
    self.tiles=[]
    for i in range(1,baseSnakeSize+1):
      tile=Tile(i,self.x,self.y,self.di)
      self.tiles.append(tile)
  def move(self,px):    
    for tile in self.tiles:
      tile.move(px)
  def draw(self):
    for tile in self.tiles:
      tile.draw()
  def setDi(self,di):
    self.di=di
    for tile in self.tiles:
      tile.di=di
  def addTile(self):
    tilesNum=len(self.tiles)
    tile=Tile(tilesNum+1,self.tiles[tilesNum-1].x,self.tiles[tilesNum-1].y,self.di)
    self.tiles.append(tile)
  def reset(self):
    self.__init__()
    self.setDi(0)

#Class the chunks of the 
#tail/head of the snake
class Tile():
  def __init__(self,n,x,y,di):
    self.x=x #screen center = 160, 111
    self.y=y
    self.di=di
    self.rectx=10
    self.recty=10
    self.n=n
    fill_rect(self.x,self.y,self.rectx,self.recty,snakeColor)
  def move(self,px):
    n=self.n
    if(n==1):
      if self.di==0:
        self.y-=px
        player.moves.append([self.x,self.y])
      if self.di==1:
        self.x+=px
        player.moves.append([self.x,self.y])
      if self.di==2:
        self.y+=px
        player.moves.append([self.x,self.y])
      if self.di==3:
        self.x-=px
        player.moves.append([self.x,self.y])
      if len(player.moves) > (len(player.tiles)+1):
        player.moves.reverse()
        player.moves.pop()
        player.moves.reverse()
    else:
      totMoves=len(player.moves)
      moveN=int(totMoves-n)
      if(moveN >= 0):
        move=player.moves[moveN]
        self.x=move[0]
        self.y=move[1]
  def draw(self):
    if self.n==1:
      fill_rect(self.x,self.y,self.rectx,self.recty,snakeColor)
      if(self.di==0):
        fill_rect(self.x+2,self.y+2,3,3,snakeOuterEyesColor)
        fill_rect(self.x+6,self.y+2,3,3,snakeOuterEyesColor)
        set_pixel(self.x+3,self.y+2,snakeInnerEyesColor)
        set_pixel(self.x+7,self.y+2,snakeInnerEyesColor)
      if(self.di==1):
        fill_rect(self.x+6,self.y+2,3,3,snakeOuterEyesColor)
        fill_rect(self.x+6,self.y+6,3,3,snakeOuterEyesColor)
        set_pixel(self.x+8,self.y+3,snakeInnerEyesColor)
        set_pixel(self.x+8,self.y+7,snakeInnerEyesColor)
      if(self.di==2):
        fill_rect(self.x+6,self.y+6,3,3,snakeOuterEyesColor)
        fill_rect(self.x+2,self.y+6,3,3,snakeOuterEyesColor)
        set_pixel(self.x+7,self.y+8,snakeInnerEyesColor)
        set_pixel(self.x+3,self.y+8,snakeInnerEyesColor)
      if(self.di==3):
        fill_rect(self.x+2,self.y+6,3,3,snakeOuterEyesColor)
        fill_rect(self.x+2,self.y+2,3,3,snakeOuterEyesColor)
        set_pixel(self.x+2,self.y+7,snakeInnerEyesColor)
        set_pixel(self.x+2,self.y+3,snakeInnerEyesColor)
    else:
      fill_rect(self.x,self.y,self.rectx,self.recty,snakeColor)
  def reset(self):
    self.x=160
    self.y=111
    self.di=0
    
#Class for the apple 
#(placing logic here)
class Apple():
  def __init__(self):
    self.x=randint(0,31)*10
    self.y=randint(0,19)*10
    self.rectx=10
    self.recty=11
  def draw(self):
    fill_rect(self.x,self.y+1,10,10,appleColor)
    set_pixel(self.x+4,self.y,appleStemColor)
    set_pixel(self.x+5,self.y+1,appleStemColor)
    set_pixel(self.x,self.y+1,backgroundColor)
    set_pixel(self.x,self.y+10,backgroundColor)
    set_pixel(self.x+9,self.y+1,backgroundColor)
    set_pixel(self.x+9,self.y+10,backgroundColor)
  def reset(self):
    applePresence=False
    self.__init__()

#Get the color of the pixels
#around the player
def getPixelFront():
  return get_pixel(player.tiles[0].x+5,player.tiles[0].y-5)
def getPixelBehind():
  return get_pixel(player.tiles[0].x+5,player.tiles[0].y+15)
def getPixelLeft():
  return get_pixel(player.tiles[0].x-5,player.tiles[0].y+5)
def getPixelRight():
  return get_pixel(player.tiles[0].x+15,player.tiles[0].y+5)

#Check if player shall die
def testDeath(score,bestScore):
  #hit walls
  if player.tiles[0].x<0 or player.tiles[0].y>=200 or player.tiles[0].x>320 or player.tiles[0].y<0:
      endGame(score,bestScore)
  #eat self
  pixelFront=getPixelFront()
  pixelBehind=getPixelBehind()
  pixelLeft=getPixelLeft()
  pixelRight=getPixelRight()
  if player.di==0 and pixelFront==snakeColor:
    endGame(score,bestScore)
  if player.di==1 and pixelRight==snakeColor:
    endGame(score,bestScore)
  if player.di==2 and pixelBehind==snakeColor:
    endGame(score,bestScore)
  if player.di==3 and pixelLeft==snakeColor:
    endGame(score,bestScore)

#Check if snake can eat
#an apple
def testAppleEaten():
  head=player.tiles[0]
  if (head.x+5 >= apple.x and head.x+5 <= apple.x+apple.rectx) and (head.y+5 >= apple.y and head.y+5 <= apple.y+apple.recty):
    player.addTile()
    apple.reset()

#The animation on death
def animation(color):
  l=monotonic()+0.58;
  while monotonic()<l:
    x=randint(0,107)
    y=randint(0,74)
    fill_rect(x*3,y*3,3,3,color)
  setScreenColor(color)

def setScreenColor(color):
  fill_rect(0,0,320,222,color)

#Game screen
def resetScreen():
  #screen = 32 char
  fill_rect(0,0,320,201,backgroundColor)
  fill_rect(0,201,320,20,gameFooterColor)
  s="SCORE: %s - LENGTH: %s" %(score(start),len(player.tiles))
  draw_string(centerString(s),0,204,gameFooterTextColor,gameFooterColor)

#When player dies
def endGame(score,bestScore):
  #Animation
  animation(deathScreenBackgroundColor)
  #Other animation
  #for i in range(0,223):
  #  fill_rect(0,0,320,i,deathScreenBackgroundColor)
  #  sleep(0.001)
  
  #Set best score
  if score > bestScore:
    setBestScore(score)
    bestScore=score
  #sleep(0.1)
  
  #Animate descending text
  for i in range(0,15):
    i=i*6
    offsetx=160-115//2
    offsety=i-70
    drawLogo(offsetx,offsety)
    draw_string(centerString("YOU LOST!"),0,i,deathScreenTextColor,mainMenuBackgroundColor)
    sleep(0.05)
  s3="Score: %s - Best Score: %s" %(score,bestScore)
  draw_string(centerString(s3),0,111,deathScreenScoreColor,deathScreenBackgroundColor)
  run=0
  died=1
  
  #Wait for keypress OK to 
  #restart game
  while died==1:
    if int(monotonic())%2==1:
      draw_string("Press <OK>",215,201,deathScreenInstColor,deathScreenBackgroundColor)
    else:
      fill_rect(215,201,105,21,deathScreenBackgroundColor)
    if keydown(KEY_OK) or keydown(KEY_EXE):
      resetScore()
      player.reset()
      animation(backgroundColor)
      died=0
      run=1

#Draw the game logo
def drawLogo(offsetx,offsety):
  setScreenColor(mainMenuBackgroundColor)
  #LOGO = x:0->115px, 
  #y:0->45px
  
  logoColor=snakeColor
  #Logo
  #S
  fill_rect(offsetx+5,offsety+0,15,5,logoColor)
  fill_rect(offsetx+5,offsety+5,5,5,logoColor)
  fill_rect(offsetx+15,offsety+5,5,5,logoColor)
  fill_rect(offsetx+20,offsety+5,5,5,logoColor)
  fill_rect(offsetx+0,offsety+5,5,15,logoColor)
  fill_rect(offsetx+5,offsety+20,15,5,logoColor)
  fill_rect(offsetx+5,offsety+15,5,5,logoColor)
  fill_rect(offsetx+20,offsety+25,5,15,logoColor)
  fill_rect(offsetx+15,offsety+25,5,5,logoColor)
  fill_rect(offsetx+5,offsety+40,15,5,logoColor)
  fill_rect(offsetx+15,offsety+35,5,5,logoColor)
  fill_rect(offsetx+5,offsety+35,5,5,logoColor)
  fill_rect(offsetx+0,offsety+35,5,5,logoColor)
  fill_rect(offsetx+22,offsety+5,2,2,'white')
  fill_rect(offsetx+22,offsety+8,2,2,'white')
  fill_rect(offsetx+23,offsety+6,1,1,'black')
  fill_rect(offsetx+23,offsety+8,1,1,'black')
  fill_rect(offsetx+25,offsety+7,2,1,'red')
  fill_rect(offsetx+27,offsety+6,1,1,'red')
  fill_rect(offsetx+27,offsety+8,1,1,'red')
  #n
  fill_rect(offsetx+30,offsety+25,5,20,logoColor)
  fill_rect(offsetx+30,offsety+25,15,5,logoColor)
  fill_rect(offsetx+45,offsety+30,5,15,logoColor)
  #a
  fill_rect(offsetx+57,offsety+25,10,5,logoColor)
  fill_rect(offsetx+57,offsety+35,10,3,logoColor)
  fill_rect(offsetx+57,offsety+42,10,3,logoColor)
  fill_rect(offsetx+54,offsety+38,3,4,logoColor)
  fill_rect(offsetx+67,offsety+30,5,15,logoColor)
  #k
  fill_rect(offsetx+75,offsety+10,5,35,logoColor)
  fill_rect(offsetx+80,offsety+30,5,5,logoColor)
  fill_rect(offsetx+85,offsety+25,5,5,logoColor)
  fill_rect(offsetx+85,offsety+35,5,10,logoColor)
  #e
  fill_rect(offsetx+95,offsety+30,5,12,logoColor)
  fill_rect(offsetx+100,offsety+27,10,3,logoColor)
  fill_rect(offsetx+100,offsety+35,10,3,logoColor)
  fill_rect(offsetx+110,offsety+30,3,5,logoColor)
  fill_rect(offsetx+100,offsety+42,10,3,logoColor)
  

##MAIN MENU
menu=1
#Animation for descending text and logo
for i in range(0,20):
  i=i*6
  offsetx=160-115//2
  offsety=i-61
  drawLogo(offsetx,offsety)
  draw_string(centerString("Coded by mattmunich"),0,i,'white',mainMenuBackgroundColor)
  sleep(0.05)
  
while menu==1:
  #Wait for start keypress (OK or EXE)
  if keydown(KEY_OK) or keydown(KEY_EXE):
    menu=0
  if int(monotonic())%2==1:
    draw_string("Press <OK>",215,201,mainMenuInstColor,mainMenuBackgroundColor)
  else:
    fill_rect(215,201,105,21,mainMenuBackgroundColor)

##GAME
#-> The game itself

#Some code pre-game loop
player=Snake()
t=monotonic()
resetScreen()
player.draw()
run=1

##GAME LOOP 
while run==1:
  #Update score
  score(start)
  
  #Apple drawing
  if applePresence==False:
    apple=Apple()
    applePresence=True
  apple.draw()
  
  #Set direction
  #UP=0;RIGHT=1;DOWN=2;LEFT=3
  if keydown(KEY_UP):
    player.setDi(0)
  if keydown(KEY_RIGHT):
    player.setDi(1)
  if keydown(KEY_DOWN):
    player.setDi(2)
  if keydown(KEY_LEFT):
    player.setDi(3)     
  
  ##Clock and drawing player
  tilesNum=len(player.tiles)
  divider=tilesNum/speed
  if monotonic()-t>speed/divider:
    resetScreen()
    player.move(10)
    player.draw()  
    t=monotonic()

  # Death check
  testDeath(score(start),bestScore)

  # Apple eating check
  testAppleEaten()
