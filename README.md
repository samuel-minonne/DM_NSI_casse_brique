# DM_NSI_casse_brique
</br>

Here is a quick explanation of the game:
- move the player with Q and D (made for a french keyboard, the controls can be changed at the start of the code file)
- if the ball hits the player on the edge, it will bonce at a different angle
- the ball moves faster as the games goes on

There are three types of bricks:
- blue bricks are normal, the darker the blue the more health the brick has
- orange bricks make the ball bonce in a random direction
- white bricks make the ball go faster

Use this link to play the game: https://kitao.github.io/pyxel/wasm/launcher/?run=samuel-minonne.DM_NSI_casse_brique.main3


General mechanics:
-lives system

Ball:
-randomized starting angle
</br>

class Brick:
    def __init__(self,x,y,hp:int):
        self.xpos = x
        self.ypos = y
        self.hp = hp
        self.hitbox = hb.Hitbox(self.xpos,self.ypos,bricksLength,bricksHeight)
