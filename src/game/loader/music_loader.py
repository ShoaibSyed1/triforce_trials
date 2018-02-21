import random

from game import paths
from game.loader.loader import Loader
from game.music import MusicInfo, RepeatType

class MusicLoader(Loader):
    @staticmethod
    def load(data, path):
        repeat_type = RepeatType[data['repeat']]
        choices = data['choices']

        return MusicInfo(choices, repeat_type)

    @staticmethod
    def get_full_path(part_path):
        return paths.MUSIC + part_path