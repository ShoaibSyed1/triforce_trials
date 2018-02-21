import pathlib
import os

from game.game import Game

# TODO: Move to player death
if pathlib.Path('save/player.toml').exists():
    os.remove('save/player.toml')
pathlib.Path('save').mkdir(parents=True, exist_ok=True)

game = Game()
game.start()