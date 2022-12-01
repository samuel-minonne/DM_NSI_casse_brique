# DM_NSI_casse_brique
</br>
Hello, this is a placeholder that will be in use until I do something with it

Have a nice day :)
 use this link to play the game:  https://kitao.github.io/pyxel/wasm/launcher/?run=samuel-minonne.DM_NSI_casse_brique.main2


General mechanics:
-lives system
-time system
-score system
-inputs with the keyboard

Level design:
-a way to store and load a specific level
-make at least one level (obviously)

Player:
-

Ball:
-always the same size
-variable speed
-randomized starting angle
-no more than one

Bricks:
-at least 3 different types
</br>

class Brick:
    def __init__(self,x,y,hp:int):
        self.xpos = x
        self.ypos = y
        self.hp = hp
        self.hitbox = hb.Hitbox(self.xpos,self.ypos,bricksLength,bricksHeight)
