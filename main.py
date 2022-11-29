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
ballStartAngle = 45 #warning, the y axis is the wrong way
ballStartSpeed = 4
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
        self.xpos = float(playerStartX)
        self.ypos = float(playerStartY)
        self.length = playerLength
        self.height = playerHeight
        self.hitbox = hb.Hitbox(self.xpos,self.ypos,self.length,self.height)
    
    def getX(self):
        """Returns the x coordinate of the player as an int"""
        return int(round(self.xpos))
    
    def getY(self):
        """Returns the y coordinate of the player as an int"""
        return int(round(self.ypos))
    
    def playerMovement(self):
        """Moves the player"""
        # reading the imputs and converting them to speed
        if pyxel.btn(key_right) and self.xpos+self.length<maxX:
            self.xpos += playerSpeed
            
        if pyxel.btn(key_left) and self.xpos>minX:
            self.xpos -= playerSpeed
            
        self.hitbox.moveTo(self.getX(),self.getY())
        
class Ball:
    def __init__(self) -> None:
        self.xpos = float(ballStartX)
        self.ypos = float(ballStartY)
        self.angle = ballStartAngle
        self.speed = ballStartSpeed
        self.length = ballSize
        self.height = ballSize
        self.hitbox = hb.Hitbox(self.xpos,self.ypos,self.length,self.height)
        
    def getX(self):
        """Returns the x coordinate of the ball as an int"""
        return int(round(self.xpos))
    
    def getY(self):
        """Returns the y coordinate of the ball as an int"""
        return int(round(self.ypos))
        
    def bounce(self,wallAngle):
        """changes the trajectory of the ball as if it bounced on a wall with the specified angle"""
        self.angle = wallAngle+(wallAngle-self.angle)

    def ballMovement(self):
        """Moves the ball"""
        xspeed = math.cos(math.radians(self.angle))*self.speed
        yspeed = math.sin(math.radians(self.angle))*self.speed
        
        def collisions():
            """Checks for collisions and modifies the values accordingly"""
            global xspeed, yspeed
            
            if self.xpos <= minX:
                self.bounce(90)
            elif self.xpos + ballSize >= maxX:
                self.bounce(90)
            elif self.ypos <= minY:
                self.bounce(0)
            elif self.ypos + ballSize >= maxY:
                self.bounce(0)
            if hb.doHitboxesTouch(ball.hitbox,player.hitbox) == ['y','-']:
                self.bounce(0)
                
            xspeed = math.cos(math.radians(self.angle))*self.speed
            yspeed = math.sin(math.radians(self.angle))*self.speed
                
        for i in range (xspeed):
            collisions()
            if xspeed > 0 :
                self.xpos += 1
                self.hitbox.moveTo(self.getX(),self.getY())
            elif xspeed < 0 :
                self.xpos -= 1
                self.hitbox.moveTo(self.getX(),self.getY())
                
        for i in range (yspeed):
            collisions()
            if yspeed > 0 :
                self.ypos += 1
                self.hitbox.moveTo(self.getX(),self.getY())
            elif yspeed < 0 :
                self.ypos -= 1
                self.hitbox.moveTo(self.getX(),self.getY())
        #ball.xpos += math.cos(math.radians(self.angle))*self.speed
        #ball.ypos += math.sin(math.radians(self.angle))*self.speed
        collisions()

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
    print(hb.doHitboxesTouch(ball.hitbox,player.hitbox) == ['y','-'])
    
def draw():
    pyxel.cls(0)
    pyxel.rect(player.getX(),player.getY(),player.length,player.height,playerColor)
    pyxel.rect(ball.getX(),ball.getY(),ball.length,ball.height,ballColor)
    for i in range(len(bricksList)):
        pyxel.rect(bricksList[i].xpos,bricksList[i].ypos,bricksLength,bricksHeight,bricksList[i].color)
    
    
pyxel.run(update, draw)
