import pyxel
import hitboxes as hb
import math

#========================================================================parameters===================================================================
gameTitle = "Casse Briques"
gameHeight = 200
gameWidth = 128
gameScale = 4

minX = 0
maxX = gameWidth
minY = 0
maxY = gameHeight

playerStartX = 64
playerStartY = 128
playerLength = 32
playerHeight = 8
playerSpeed = 2
playerColor = 1

ballStartX = 64
ballStartY = 64
ballSize = 4
ballStartAngle = 15 #warning, the y axis is the wrong way
ballStartSpeed = 2
ballColor = 10

bricksLength = 16
bricksHeight = 4
bricksXSpacing = bricksLength + 1 
bricksYSpacing = bricksHeight + 1

key_up = pyxel.KEY_Z
key_down = pyxel.KEY_S
key_left = pyxel.KEY_Q
key_right = pyxel.KEY_D


#==================================================================classes================================================================
class Player:
    def __init__(self):
        self.xpos = playerStartX
        self.ypos = playerStartY
        self.length = playerLength
        self.height = playerHeight
        self.hitbox = hb.Hitbox(self.xpos,self.ypos,self.length,self.height)
        
    def playerMovement(self):
        """modifies the values of xspeed and yspeed based on key imputs"""
        # reading the imputs and converting them to speed
        if pyxel.btn(key_right) and self.xpos+self.length<maxX:
            self.xpos += playerSpeed
            
        if pyxel.btn(key_left) and self.xpos>minX:
            self.xpos -= playerSpeed
            
        self.hitbox.moveTo(self.xpos,self.ypos)
        
class Ball:
    def __init__(self) -> None:
        self.xpos = ballStartX 
        self.ypos = ballStartY
        self.angle = ballStartAngle
        self.speed = ballStartSpeed
        self.length = ballSize
        self.height = ballSize
        self.hitbox = hb.Hitbox(self.xpos,self.ypos,self.length,self.height)
        
    def bounce(self,wallAngle):
        """changes the trajectory of the ball as if it bounced on a wall with the specified angle"""
        self.angle = wallAngle+(wallAngle-self.angle)

        
    def ballMovement(self):
        ball.xpos += math.cos(math.radians(self.angle))*self.speed
        ball.ypos += math.sin(math.radians(self.angle))*self.speed
        if self.xpos <= minX:
            self.bounce(90)
        if self.xpos + ballSize >= maxX:
            self.bounce(90)
        if self.ypos <= minY:
            self.bounce(0)
        if self.ypos + ballSize >= maxY:
            self.bounce(0)
        

class Brick:
    def __init__(self,x,y,hp:int):
        self.xpos = x
        self.ypos = y
        self.hp = hp
        self.color = 3
        self.hitbox = hb.Hitbox(self.xpos,self.ypos,bricksLength,bricksHeight)


            
pyxel.init(gameWidth, gameHeight, title=gameTitle, display_scale=gameScale)

player = Player()
ball = Ball()
bricksList = []
for i in range(3):
    bricksList.append(Brick(8*i,20,1))

def update():
    player.playerMovement()
    ball.ballMovement()
    
def draw():
    pyxel.cls(0)
    pyxel.rect(player.xpos,player.ypos,player.length,player.height,playerColor)
    pyxel.rect(ball.xpos,ball.ypos,ball.length,ball.height,ballColor)
    for i in range(len(bricksList)):
        pyxel.rect(bricksList[i].xpos,bricksList[i].ypos,bricksLength,bricksHeight,bricksList[i].color)
    
    
pyxel.run(update, draw)
