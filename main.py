import pyxel
import math
#vitesse augmente avec le temps? , angle de départ alléatoire
#========================================================================parameters===================================================================
gameTitle = "Casse Briques"
gameHeight = 200
gameWidth = 201
gameScale = 4

minX = 0
maxX = gameWidth
minY = 0
maxY = gameHeight

playerHP = 3

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

bricksLength = 32
bricksHeight = 8
bricksXSpacing = bricksLength + 1
bricksYSpacing = bricksHeight + 1

key_left = pyxel.KEY_Q
key_right = pyxel.KEY_D

level_line0 = [[],[],[],[],[],[]]#la 1ere ligne du dessin, le premier chiffre est le type de brique (0=pas de brique) et le deuxième ses hp
level_line1 = [[],[],[],[],[],[]]#la 1ere ligne du dessin, le premier chiffre est le type de brique (0=pas de brique) et le deuxième ses hp
level_line2 = [[],[],[],[],[],[]]#la 1ere ligne du dessin, le premier chiffre est le type de brique (0=pas de brique) et le deuxième ses hp

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
        
        self.positivex = (math.cos(math.radians(self.angle)) > 0.0) #True si on va vers la droite (il faut ajouter à x) est positif, sinon false 
        self.positivey = (math.sin(math.radians(self.angle)) > 0.0) #True si on va vers le bas (il faut ajouter à y) est positif, sinon false
        self.bounceList = [] #pour éviter de rebondir plusieurs fois en même temps sur le même mur (et donc être bloqué)
        self.bricksTouched = [] #pour éviter d'enlever plusieurs hp à une seule brique par coup
        
    def getX(self):
        """Returns the x coordinate of the ball as an int"""
        return int(round(self.xpos))
    
    def getY(self):
        """Returns the y coordinate of the ball as an int"""
        return int(round(self.ypos))
        
    def bounce(self,wallAngle):
        """changes the trajectory of the ball as if it bounced on a wall with the specified angle"""
        print("bounce")
        print(self.xpos,self.ypos)
        if wallAngle not in self.bounceList:
            self.angle = wallAngle+(wallAngle-self.angle)
            self.bounceList.append(wallAngle)
            print("bounced")

    def ballMovement(self):
        """Moves the ball"""
        self.bounceList = [] #Toujours le bug de la balle qui se bloque sur les bords
        self.bricksTouched = []
        xspeed = math.cos(math.radians(self.angle))*self.speed
        yspeed = math.sin(math.radians(self.angle))*self.speed
        self.positivex = (math.cos(math.radians(self.angle)) > 0.0) #True si on va vers la droite (il faut ajouter à x) est positif, sinon false
        self.positivey = (math.sin(math.radians(self.angle)) > 0.0) #True si on va vers le bas (il faut ajouter à y) est positif, sinon false
        
        print("ball movement------------------")
        def collisions():
            """Checks for collisions and modifies the values accordingly"""
            # On regarde d'abord les briques
            for brick in bricksList:
                status = doHitboxesTouch(self.hitbox,brick.hitbox)
                if status == ['y','+']:
                    self.bounce(360)
                    if i not in self.bricksTouched: #pour éviter de taper plusieurs fois la même brique (oui je sais le copier-coller c'est pas bien j'aurais du créer une fonction)
                        brick.hp -= 1
                        self.bricksTouched.append(i)
                if status == ['y','-']:
                    self.bounce(0)
                    if i not in self.bricksTouched: #pour éviter de taper plusieurs fois la même brique
                        brick.hp -= 1
                        self.bricksTouched.append(i)
                if status == ['x','+']:
                    self.bounce(270)
                    if i not in self.bricksTouched: #pour éviter de taper plusieurs fois la même brique
                        brick.hp -= 1
                        self.bricksTouched.append(i)
                if status == ['x','-']:
                    self.bounce(90)
                    if i not in self.bricksTouched: #pour éviter de taper plusieurs fois la même brique
                        brick.hp -= 1
                        self.bricksTouched.append(i)
            # On vérifie si on est toujours dans l'écran    
            if self.xpos <= minX:
                self.bounce(90)
            elif self.xpos + ballSize >= maxX:
                self.bounce(270)
            elif self.ypos <= minY:
                self.bounce(360)
            elif self.ypos + ballSize >= maxY:
                self.bounce(0)
            # On fait les collisions avec le plateau
            playerStatus = doHitboxesTouch(ball.hitbox,player.hitbox)
            if playerStatus == ['y','-']: #ATTENTION, il bounce 2 fois (car son ordonné ne change pas) c'est pour ça qu'on a bounceList
                if ball.xpos < player.xpos:
                    self.bounce(350)
                elif ball.xpos > player.xpos + playerLength:
                    self.bounce(10)
                else:
                    self.bounce(0)
            elif playerStatus == ['y','+']:
                    self.bounce(360)
            elif playerStatus == ['x','+']:
                    self.bounce(270)
            elif playerStatus == ['x','-']:
                    self.bounce(90)
            
            self.positivex = (math.cos(math.radians(self.angle)) > 0.0) #True si on va vers la droite (il faut ajouter à x) est positif, sinon false 
            self.positivey = (math.sin(math.radians(self.angle)) > 0.0) #True si on va vers le bas (il faut ajouter à y) est positif, sinon false
            print(self.positivex,self.positivey)
            print(self.bounceList)

        for i in range (abs(round(xspeed))): #pourquoi i il vaut toujours 0? parceque il le round à 1 et que 1 est exclu xspeed passe en négatif et donc on entre plus dans la boucle
            print("x")
            collisions()
            if self.positivex == True:
                self.xpos += 1
                self.hitbox.moveTo(self.getX(),self.getY())
            elif self.positivex == False :
                self.xpos -= 1
                self.hitbox.moveTo(self.getX(),self.getY())
                
        for i in range (abs(round(yspeed))):
            print("y")
            collisions()
            if self.positivey == True :
                self.ypos += 1
                self.hitbox.moveTo(self.getX(),self.getY())
            elif self.positivey == False :
                self.ypos -= 1
                self.hitbox.moveTo(self.getX(),self.getY())
        #ball.xpos += math.cos(math.radians(self.angle))*self.speed
        #ball.ypos += math.sin(math.radians(self.angle))*self.speed

class Brick:
    def __init__(self,x,y,hp:int,type:int):
        self.xpos = x
        self.ypos = y
        self.hp = hp
        self.type = type #1 = brique normale, 2=brique qui accélère la balle, 3=brique qui fait rebondire dans une direction alléatoire
        self.colour = 13
        self.hitbox = Hitbox(self.xpos,self.ypos,bricksLength,bricksHeight)
        if self.type == 2:
            self.colour = 7
        elif self.type == 3:
            self.colour = 9
        
    def brickUpdate(self):
        """Changes the color according to the HP of the brick"""
        if self.type == 1:
            if self.hp == 1:
                self.colour = 5
            elif self.hp == 2:
                self.colour = 12
            elif self.hp == 3:
                self.colour = 6
            else:
                self.colour = 13
            
def createBrickLine(line:list,lineNumber:int):
    """Creates a line of bricks, with a list of tuples as the line pattern and an int as the line number"""
    for i in range (len(line)):
        if line[i][0] != 0:
            bricksList.append(Brick(bricksXSpacing*i+2,bricksYSpacing*lineNumber+1,line[i][1],line[i][0]))


#==============================================================================starting the game================================================
            
pyxel.init(gameWidth, gameHeight, title=gameTitle, display_scale=gameScale)

player = Player()
ball = Ball()
bricksList = []
for i in range(6):
    bricksList.append(Brick(bricksXSpacing*i+2,bricksYSpacing,1,0))
for i in range(6):
    bricksList.append(Brick(bricksXSpacing*i+2,2*bricksYSpacing,1,0))



#================================================================running the game===================================================
def update():
    player.playerMovement()
    ball.ballMovement()
    for brick in bricksList:
        brick.brickUpdate()
    if pyxel.btnp(pyxel.KEY_B):
        ball.bounce(90)
    listBricksToRemove = []
    for i in range (len(bricksList)): #enlève les briques qui sont mortes
        if bricksList[i].hp <= 0:
            listBricksToRemove.append(i)
    for i in range (len(listBricksToRemove)):
        bricksList.pop(listBricksToRemove[i])

def draw():
    pyxel.cls(0)
    pyxel.rect(player.getX(),player.getY(),player.length,player.height,playerColor)
    pyxel.rect(ball.getX(),ball.getY(),ball.length,ball.height,ballColor)
    for i in range(len(bricksList)):
        pyxel.rect(bricksList[i].xpos,bricksList[i].ypos,bricksLength,bricksHeight,bricksList[i].colour)
    
pyxel.run(update, draw)
