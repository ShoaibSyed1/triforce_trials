from game.component import ScriptComponent
from game.ecs import System

class ScriptSystem(System):
    def update(self, dt):
        for (entity, [script_component]) in self.world.get_components(ScriptComponent):
            if script_component.script != None:
                if not script_component.started:
                    script_component.script.start(entity, self.world)
                    script_component.started = True
            
            script_component.script.update(dt)