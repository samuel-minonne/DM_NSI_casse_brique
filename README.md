# DM_NSI_casse_brique
</br>

Here is a quick explanation of the game:
- Move the player with Q and D (made for a french keyboard, the controls can be changed at the start of the code file)
- If the ball hits the player on the edge, it will bonce at a different angle
- The ball moves faster as the games goes on
- If the ball touches the bottom of the screen you loose a life

There are three types of bricks:
- Blue bricks are normal, the darker the blue the more health the brick has
- Orange bricks make the ball bonce in a random direction
- White bricks make the ball go faster

Use this link to play the oldest version of the game (with not too many bugs): https://kitao.github.io/pyxel/wasm/launcher/?run=samuel-minonne.DM_NSI_casse_brique.main

Use this link to play the latest version of the game (with lots of bugs): https://kitao.github.io/pyxel/wasm/launcher/?run=samuel-minonne.DM_NSI_casse_brique.mainv2

Know bugs:
- The lives system doesn't work properly (sometimes more than one hp is lost)
- If the player moves while the ball hits its side, the ball might get stuck inside the player
- The game crashes if multiple bricks get deleted at the same time

Things to do to improve the game:
- Fix bugs
- Change the ball movement system so that we don't have to round the speed
- Make more levels
- Do more playtesting to find more bugs
</br>
