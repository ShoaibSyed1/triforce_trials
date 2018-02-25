from game.script.script import Script

class SwordScript(Script):
    def __init__(self, damage_data, player):
        self.damage_data = damage_data
        self.player = player