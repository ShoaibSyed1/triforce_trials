from game.script.enemies.mini_moldorm import MiniMoldorm
from game.script.tiles.entrance import EntranceScript
from game.script.tiles.exit import Exit
from game.script.ui.action_script import ActionScript
from game.script.ui.bottom_bar import BottomBar
from game.script.ui.hearts import HeartsScript
from game.script.ui.player_level import PlayerLevel
from game.script.ui.xp_bar import XpBar
from game.script.load_script import LoadScript
from game.script.player_script import PlayerScript
from game.script.poof import Poof
from game.script.sword_script import SwordScript

_SCRIPTS = {
    "enemies/mini_moldorm": MiniMoldorm,
    "tiles/entrance": EntranceScript,
    "tiles/exit": Exit,
    "ui/action_script": ActionScript,
    "ui/bottom_bar": BottomBar,
    "ui/hearts": HeartsScript,
    "ui/player_level": PlayerLevel,
    "ui/xp_bar": XpBar,
    "load_script": LoadScript,
    "player_script": PlayerScript,
    "poof": Poof,
    "sword_script": SwordScript
}

def get(path):
    return _SCRIPTS.get(path, None)