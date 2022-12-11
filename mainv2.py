import pyxel
import math
import random
#voir le redme sur github pour les infos générales: https://github.com/samuel-minonne/DM_NSI_casse_brique
#========================================================================parameters===================================================================
gameTitle = "Casse Briques"
gameHeight = 200
gameWidth = 201
gameScale = 4

minX = 0
maxX = gameWidth
minY = 0
maxY = gameHeight

playerStartHP = 5

playerStartX = 64
playerStartY = 150
playerLength = 32
playerHeight = 8
playerSpeed = 3.0
playerColor = 11

ballStartX = 100
ballStartY = 50
ballSize = 4
ballStartAngle = 45 #warning, the y axis is the wrong way
ballStartSpeed = 2.0
ballColor = 10
ballSpeedIncrementation = 0.0003
brickSpeedIncrementation = 0.5

bricksLength = 32
bricksHeight = 8
bricksXSpacing = bricksLength + 1
bricksYSpacing = bricksHeight + 1

scoreIncrementation = 10
scoreMultiplier = 2
scoreMultiplierTime = 60 #in frames, 1sec = 30 frames

key_left = pyxel.KEY_Q
key_right = pyxel.KEY_D

level_line0 = [[1,1],[3,1],[1,2],[1,2],[3,1],[1,1]]#la 1ere ligne du dessin, le premier chiffre est le type de brique (0=pas de brique) et le deuxième ses hp
level_line1 = [[2,1],[1,3],[3,2],[3,2],[1,3],[2,1]]#la 2eme ligne du dessin, le premier chiffre est le type de brique (0=pas de brique) et le deuxième ses hp
level_line2 = [[1,1],[1,2],[0,0],[0,0],[1,2],[1,1]]#la 3eme ligne du dessin, le premier chiffre est le type de brique (0=pas de brique) et le deuxième ses hp
level_line3 = [[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]]#la 4eme ligne du dessin, le premier chiffre est le type de brique (0=pas de brique) et le deuxième ses hp

#==================================================================classes================================================================
#============the hitboxes module============
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
        if pyxel.btn(key_right) and self.xpos+self.length<maxX:
            self.xpos += playerSpeed
            
        if pyxel.btn(key_left) and self.xpos>minX:
            self.xpos -= playerSpeed
            
        self.hitbox.moveTo(self.getX(),self.getY())
        
#=======================================================================the ball class====================================================
class Ball:
    def __init__(self):
        self.randomAngle = random.randint(45,135)
        
        self.xpos = float(ballStartX)
        self.ypos = float(ballStartY)
        self.angle = self.randomAngle
        self.speed = ballStartSpeed
        self.length = ballSize
        self.height = ballSize
        self.hitbox = Hitbox(self.xpos,self.ypos,self.length,self.height)
        
        self.positivex = (math.cos(math.radians(self.angle)) > 0.0) #True si on va vers la droite (il faut ajouter à x) est positif, sinon false 
        self.positivey = (math.sin(math.radians(self.angle)) > 0.0) #True si on va vers le bas (il faut ajouter à y) est positif, sinon false
        self.bounceList = [] #pour éviter de rebondir plusieurs fois en même temps sur le même mur (et donc être bloqué)
        self.bouncedX = False #pour éviter des problèmes de plusieurs rebonds hors des limites du terrain
        self.bricksTouched = [] #pour éviter d'enlever plusieurs hp à une seule brique par coup
        self.predicted_angle = 0
        self.predicted_positivex = (math.cos(math.radians(self.predicted_angle)) > 0.0)
        self.predicted_positivey = (math.sin(math.radians(self.predicted_angle)) > 0.0)
        self.haveWeLostHP = False
        
    def getX(self):
        """Returns the x coordinate of the ball as an int"""
        return int(round(self.xpos))
    
    def getY(self):
        """Returns the y coordinate of the ball as an int"""
        return int(round(self.ypos))

    def bounce(self,wallAngle,is_pred = False):
        """changes the trajectory of the ball as if it bounced on a wall with the specified angle"""
        print("bounce")
        if wallAngle not in self.bounceList:
            if not is_pred:
                self.angle = wallAngle+(wallAngle-self.angle)
                self.bounceList.append(wallAngle)
                print("bounced")
            else:
                self.predicted_angle = wallAngle+(wallAngle-self.angle) #nous permet de faire des prédictions sans bouger la balle
                print("predicted_angle:",self.predicted_angle)

    def ballMovement(self):
        """Moves the ball"""
        self.bounceList = [] #Toujours le bug de la balle qui se bloque sur les bords
        self.bricksTouched = []
        self.haveWeLostHP = False
        self.randomAngle = random.randint(45,135)
        xspeed = math.cos(math.radians(self.angle))*self.speed
        yspeed = math.sin(math.radians(self.angle))*self.speed
        xspeedDifference = abs(xspeed - math.floor(xspeed))
        yspeedDifference = abs(yspeed - math.floor(yspeed))
        print(xspeedDifference,yspeedDifference)
        self.positivex = (math.cos(math.radians(self.angle)) > 0.0) #True si on va vers la droite (il faut ajouter à x) est positif, sinon false
        self.positivey = (math.sin(math.radians(self.angle)) > 0.0) #True si on va vers le bas (il faut ajouter à y) est positif, sinon false

        
        print("ball movement-------------------------------------------------------------------")
        
        def collisions(isPrediction = False):
            """Checks for collisions and modifies the values accordingly"""
            # On regarde d'abord les briques
            print("collisions")
            for brick in bricksList:
                status = doHitboxesTouch(self.hitbox,brick.hitbox) #une variable staut pour éviter d'appeler la fonction plusieurs fois
                if (not (status == ['f','f'] or status == ['o','o'])) and brick.type == 2 and brick not in self.bricksTouched:
                    self.speed += brickSpeedIncrementation
                if status == ['y','+']:
                    if brick.type == 3:
                        self.angle = self.randomAngle
                    else:
                        self.bounce(360,is_pred=isPrediction)
                    if brick not in self.bricksTouched: #pour éviter de taper plusieurs fois la même brique (oui je sais le copier-coller c'est pas bien j'aurais du créer une fonction)
                        brick.hp -= 1
                        self.bricksTouched.append(brick)
                elif status == ['y','-']:
                    self.bounce(0,is_pred=isPrediction)
                    if brick not in self.bricksTouched: #pour éviter de taper plusieurs fois la même brique
                        brick.hp -= 1
                        self.bricksTouched.append(brick)
                elif status == ['x','+']:
                    self.bounce(270,is_pred=isPrediction)
                    if brick not in self.bricksTouched: #pour éviter de taper plusieurs fois la même brique
                        brick.hp -= 1
                        self.bricksTouched.append(brick)
                elif status == ['x','-']:
                    self.bounce(90,is_pred=isPrediction)
                    if brick not in self.bricksTouched: #pour éviter de taper plusieurs fois la même brique
                        brick.hp -= 1
                        self.bricksTouched.append(brick)
                    
            # On vérifie si on est toujours dans l'écran
            print('ball cords',self.xpos,self.ypos)  
            print('angle and speed',self.angle,self.speed)
            if self.hitbox.left <= minX:
                if not self.bouncedX:
                    self.bounce(90,is_pred=isPrediction)
                self.bouncedX = True
            elif self.hitbox.right + ballSize >= maxX:
                if not self.bouncedX:
                    self.bounce(270,is_pred=isPrediction)
                self.bouncedX = True
            elif self.hitbox.top <= minY:
                self.bounce(360,is_pred=isPrediction)
            elif self.hitbox.bottom + ballSize >= maxY:
                if not self.haveWeLostHP:
                    game_values.hp -= 1
                self.bounce(0,is_pred=isPrediction)
            print(self.xpos,self.ypos)
            # On fait les collisions avec le plateau
            playerStatus = doHitboxesTouch(ball.hitbox,player.hitbox)
            if playerStatus == ['y','-']: #ATTENTION, il bounce 2 fois (car son ordonné ne change pas) c'est pour ça qu'on a bounceList
                if ball.xpos < player.xpos+4:
                    self.bounce(350,is_pred=isPrediction)
                elif ball.xpos > player.xpos + playerLength - 4:
                    self.bounce(10,is_pred=isPrediction)
                else:
                    self.bounce(0,is_pred=isPrediction)
            elif playerStatus == ['y','+']:
                self.bounce(360,is_pred=isPrediction)
            elif playerStatus == ['x','+']:
                if not self.bouncedX:
                    self.bounce(270,is_pred=isPrediction)
                self.bouncedX = True
            elif playerStatus == ['x','-']:
                if not self.bouncedX:
                    self.bounce(90,is_pred=isPrediction)
                self.bouncedX = True
            
            self.positivex = (math.cos(math.radians(self.angle)) > 0.0) #True si on va vers la droite (il faut ajouter à x) est positif, sinon false 
            self.positivey = (math.sin(math.radians(self.angle)) > 0.0) #True si on va vers le bas (il faut ajouter à y) est positif, sinon false
            if isPrediction:
                self.predicted_positivex = (math.cos(math.radians(self.predicted_angle)) > 0.0)
                self.predicted_positivey = (math.sin(math.radians(self.predicted_angle)) > 0.0)
            print(self.bounceList)

        for i in range (abs(round(xspeed))):#pour pouvoir gérer des vitesses supérieures à 1, on avance de 1, puis on vérifie les colisions, puis on répète autant de fois que nécéssaire
            print("x")
            collisions()
            if self.positivex == True:
                self.xpos += 1
                self.hitbox.moveTo(self.getX(),self.getY())
                print("moved right")
            elif self.positivex == False :
                self.xpos -= 1
                self.hitbox.moveTo(self.getX(),self.getY())
                print("moved left")
                print("end x")
        collisions(isPrediction=True)
        if (self.predicted_positivex and round(self.xpos + xspeedDifference) != self.getX()) or (not self.predicted_positivex and round(self.xpos - xspeedDifference) != self.getX()):
            collisions()#on refait ça une dernière fois pour gérer l'arrondi 
        if self.positivex == True:
            self.xpos += xspeedDifference
            self.hitbox.moveTo(self.getX(),self.getY())
            print("moved right",xspeedDifference)
        elif self.positivex == False :
            self.xpos -= xspeedDifference
            self.hitbox.moveTo(self.getX(),self.getY())
            print("moved left",xspeedDifference)
        self.bouncedX = False
           
           
        for i in range (abs(round(yspeed))): #on fait la même chose sur l'axe y
            print("y")
            collisions()
            if self.positivey == True :
                self.ypos += 1
                self.hitbox.moveTo(self.getX(),self.getY())
                print("moved down")
            elif self.positivey == False :
                self.ypos -= 1
                self.hitbox.moveTo(self.getX(),self.getY())
                print("moved up")
                print("end y")
        collisions(isPrediction=True)
        #if round(self.ypos + yspeedDifference) != self.getY():
        if (self.predicted_positivey and round(self.ypos + yspeedDifference) != self.getY()) or (not self.predicted_positivey and round(self.ypos - yspeedDifference) != self.getY()):
            collisions()#ne doit s'exécuter que si on change de position (la hitbox en tout cas)
        if self.positivey == True:
            self.ypos += yspeedDifference
            self.hitbox.moveTo(self.getX(),self.getY())
            print("moved down",yspeedDifference)
        elif self.positivey == False :
            self.ypos -= yspeedDifference
            self.hitbox.moveTo(self.getX(),self.getY())
            print("moved up",yspeedDifference)# il bounce deux fois car il a pas move (il move pas assez pour faire bouger la hitbox et donc rebondit deux fois), comme il bouge après avoir rebondi les valeurs de direction sont différentes et donc il bounce quand même même si il ne bougeras pas
        

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
                self.colour = 6
            elif self.hp == 2:
                self.colour = 12
            elif self.hp == 3:
                self.colour = 5
            else:
                self.colour = 13
        elif self.type == 3:
            if self.hp == 2:
                self.colour = 9
            else:
                self.colour = 15

class GameValues:
    """A class that handles the score and the HP of the player"""
    def __init__(self):
        self.score = 0
        self.score_multiplier = 1
        self.score_timer = 0
        self.hp = playerStartHP
        
    def updatev(self):
        """Updates the score timer and the score multiplier"""
        self.score_timer -= 1
        if self.score_timer < 0:
            self.score_multiplier = 1
                
def createBrickLine(line:list,lineNumber:int):
    """Creates a line of bricks, with a list of tuples as the line pattern and an int as the line number"""
    for i in range (len(line)):
        if line[i][0] != 0:
            bricksList.append(Brick(bricksXSpacing*i+2,bricksYSpacing*lineNumber+1,line[i][1],line[i][0]))


#==============================================================================starting the game================================================
            
pyxel.init(gameWidth, gameHeight, title=gameTitle, display_scale=gameScale)

player = Player()
ball = Ball()
game_values = GameValues()
bricksList = []
createBrickLine(level_line0,0)
createBrickLine(level_line1,1)
createBrickLine(level_line2,2)
createBrickLine(level_line3,3)

#================================================================running the game===================================================
def update():
    player.playerMovement()
    ball.ballMovement()
    for brick in bricksList:
        brick.brickUpdate()
    if pyxel.btnp(pyxel.KEY_B):
        ball.bounce(90)
    listBricksToRemove = []
    for brick in bricksList: #enlève les briques qui sont mortes
        if brick.hp <= 0:
            listBricksToRemove.append(brick)
    for i in range (len(listBricksToRemove)):
        bricksList.remove(listBricksToRemove[i])
        game_values.score += scoreIncrementation*game_values.score_multiplier
        game_values.score_multiplier = scoreMultiplier
        game_values.score_timer = scoreMultiplierTime
        print("removed brick")
      
    game_values.updatev()  
    ball.speed += ballSpeedIncrementation #augmente la vitesse de la balle de 0.9 toutes les 100 secondes


def draw():
    pyxel.cls(0)
    pyxel.rect(player.getX(),player.getY(),player.length,player.height,playerColor)
    pyxel.rect(ball.getX(),ball.getY(),ball.length,ball.height,ballColor)
    for i in range(len(bricksList)):
        pyxel.rect(bricksList[i].xpos,bricksList[i].ypos,bricksLength,bricksHeight,bricksList[i].colour)
    pyxel.text(3,11,'Score:'+str(game_values.score),4)
    if game_values.score_multiplier != 1:
        pyxel.text(3,20,'Score x'+str(game_values.score_multiplier),4)
    pyxel.text(3,3,'HP:'+str(game_values.hp),4)
    if bricksList == [] and game_values.hp >0:
        pyxel.text(65,90,'Well done: YOU WON',4)
    if game_values.hp <= 0:
        pyxel.text(70,90,'YOU LOST',4)
    
pyxel.run(update, draw)
