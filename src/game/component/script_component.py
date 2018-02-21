from game.ecs import Component
from game.from_dict import FromDict

class ScriptComponent(Component, FromDict):
    def __init__(self, script):
        self.script = script
        self.started = False
    
    @staticmethod
    def from_dict(data):
        from game import scripts

        script_class = scripts.get(data['path'])
        script = script_class(*data.get('args', []))
        
        return ScriptComponent(script)