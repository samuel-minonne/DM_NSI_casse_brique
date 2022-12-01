import pyxel
import math

#========================================================================parameters===================================================================
gameTitle = "Casse Briques"
gameHeight = 256
gameWidth = 256
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
playerColor = 11

ballStartX = 64
ballStartY = 64
ballSize = 4
ballStartAngle = 45 #warning, the y axis is the wrong way
ballStartSpeed = 2
ballColor = 10

bricksLength = 16
bricksHeight = 4
bricksXSpacing = bricksLength + 1 
bricksYSpacing = bricksHeight + 1

key_left = pyxel.KEY_Q
key_right = pyxel.KEY_D


#==================================================================classes================================================================
#=====the hitboxes module=====
class Hitbox:
    """a hitbox with a postion, a length and a height"""
    def __init__(self,xpos:int,ypos:int,length:int,height:int):
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.height = height
        self.top = ypos
        self.bottom = ypos + height
        self.left = xpos
        self.right = xpos + length
        
    def moveTo(self,x:int,y:int):
        """Moves the hitbox to the specified coordinates"""
        self.xpos = x
        self.ypos = y
        self.top = self.ypos
        self.bottom = self.ypos + self.height
        self.left = self.xpos
        self.right = self.xpos + self.length
        
def doHitboxesCollide(hitbox1:Hitbox,hitbox2:Hitbox):
    """Checks if 2 hitboxes collide, takes two hitboxes as parameters, returns True if they collide and False if they don't"""
    if ((hitbox1.bottom>=hitbox2.top and hitbox1.bottom<=hitbox2.bottom) or (hitbox1.top>=hitbox2.top and hitbox1.top<=hitbox2.bottom)) and ((hitbox1.left>=hitbox2.left and hitbox1.left<=hitbox2.right ) or (hitbox1.right>=hitbox2.left and hitbox1.right<=hitbox2.right)):
        return True
    else:
        return False
    
def doHitboxesTouch(hitbox1:Hitbox,hitbox2:Hitbox):
    """takes two hitboxes as inputs and checks if they are touching, 
    returns a tuple of str containig ['f','f'] if not, ['x','+'] if hitbox1 is left of hitbox2, ['x','-'] if hitbox1 is left of hitbox2, 
    ['y','+'] if hitbox1 is under hitbox2, ['y','-'] if hitbox1 is above hitbox2 and ['o','o'] if they overlap"""
    if hitbox1.bottom==hitbox2.top and ((hitbox1.left>=hitbox2.left and hitbox1.left<=hitbox2.right ) or (hitbox1.right>=hitbox2.left and hitbox1.right<=hitbox2.right)):
        return ['y','-']
    elif hitbox1.top==hitbox2.bottom and ((hitbox1.left>=hitbox2.left and hitbox1.left<=hitbox2.right ) or (hitbox1.right>=hitbox2.left and hitbox1.right<=hitbox2.right)):
        return ['y','+']
    elif hitbox1.right==hitbox2.left and ((hitbox1.bottom>=hitbox2.top and hitbox1.bottom<=hitbox2.bottom) or (hitbox1.top>=hitbox2.top and hitbox1.top<=hitbox2.bottom)):
        return ['x','+']
    elif hitbox1.left==hitbox2.right and ((hitbox1.bottom>=hitbox2.top and hitbox1.bottom<=hitbox2.bottom) or (hitbox1.top>=hitbox2.top and hitbox1.top<=hitbox2.bottom)):
        return ['x','-']
    elif ((hitbox1.bottom>=hitbox2.top and hitbox1.bottom<=hitbox2.bottom) or (hitbox1.top>=hitbox2.top and hitbox1.top<=hitbox2.bottom)) and ((hitbox1.left>=hitbox2.left and hitbox1.left<=hitbox2.right ) or (hitbox1.right>=hitbox2.left and hitbox1.right<=hitbox2.right)):
        return ['o','o']
    else:
        return ['f','f']
    
#===============================================================================the other classes====================================================
class Player:
    def __init__(self):
        self.xpos = float(playerStartX)
        self.ypos = float(playerStartY)
        self.length = playerLength
        self.height = playerHeight
        self.hitbox = Hitbox(self.xpos,self.ypos,self.length,self.height)
    
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
        self.hitbox = Hitbox(self.xpos,self.ypos,self.length,self.height)
        
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
        positivex = xspeed	> 0 #True si xspeed est positif, sinon false
        positivey = yspeed	> 0 #True si yspeed est positif, sinon false
        
        def collisions():
            """Checks for collisions and modifies the values accordingly"""
            global xspeed, yspeed, positivex, positivey
            
            if self.xpos <= minX:
                self.bounce(90)
            elif self.xpos + ballSize >= maxX:
                self.bounce(90)
            elif self.ypos <= minY:
                self.bounce(0)
            elif self.ypos + ballSize >= maxY:
                self.bounce(0)
            if doHitboxesTouch(ball.hitbox,player.hitbox) == ['y','-']:
                if ball.xpos < player.xpos:
                    self.bounce(350)
                elif ball.xpos > player.xpos + playerLength:
                    self.bounce(10)
                else:
                    self.bounce(0)
                
            xspeed = math.cos(math.radians(self.angle))*self.speed
            yspeed = math.sin(math.radians(self.angle))*self.speed
            positivex = xspeed	> 0 #True si xspeed est positif, sinon false
            positivey = yspeed	> 0 #True si yspeed est positif, sinon false
            print(xspeed)
        for i in range (0,round(xspeed),1): #pourquoi i il vaut toujours 0? parceque il le round à 1 et que 1 est exclu
            print(i)
            collisions()
            if xspeed > 0 :
                self.xpos += 1
                self.hitbox.moveTo(self.getX(),self.getY())
            elif xspeed < 0 :
                self.xpos -= 1
                self.hitbox.moveTo(self.getX(),self.getY())
                
        for i in range (0,round(yspeed),1):
            print(i)
            collisions()
            if yspeed > 0 :
                self.ypos += 1
                self.hitbox.moveTo(self.getX(),self.getY())
            elif yspeed < 0 :
                self.ypos -= 1
                self.hitbox.moveTo(self.getX(),self.getY())
        #ball.xpos += math.cos(math.radians(self.angle))*self.speed
        #ball.ypos += math.sin(math.radians(self.angle))*self.speed

class Brick:
    def __init__(self,x,y,hp:int):
        self.xpos = x
        self.ypos = y
        self.hp = hp
        self.colour = 3
        self.hitbox = Hitbox(self.xpos,self.ypos,bricksLength,bricksHeight)
        
    def brickUpdate(self):
        if self.hp == 1:
            self.colour = 5
        elif self.hp == 2:
            self.colour = 12
        elif self.hp == 3:
            self.colour = 6
        else:
            self.colour = 13
        

#==============================================================================starting the game================================================
            
pyxel.init(gameWidth, gameHeight, title=gameTitle, display_scale=gameScale)

player = Player()
ball = Ball()
bricksList = []
for i in range(3):
    bricksList.append(Brick(bricksXSpacing*i,bricksYSpacing-bricksHeight,1))
for i in range(3):
    bricksList.append(Brick(bricksXSpacing*i,bricksYSpacing+1,1))

#================================================================running the game===================================================
def update():
    player.playerMovement()
    ball.ballMovement()
    for brick in bricksList:
        brick.brickUpdate()
    if pyxel.btnp(pyxel.KEY_B):
        ball.bounce(90)
    print("letmeprintplease")

    
def draw():
    pyxel.cls(0)
    pyxel.rect(player.getX(),player.getY(),player.length,player.height,playerColor)
    pyxel.rect(ball.getX(),ball.getY(),ball.length,ball.height,ballColor)
    for i in range(len(bricksList)):
        pyxel.rect(bricksList[i].xpos,bricksList[i].ypos,bricksLength,bricksHeight,bricksList[i].color)
    
    
pyxel.run(update, draw)
