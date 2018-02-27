from game import loader
from game.component import AnimationSets, ScriptComponent, Transform
from game.direction import Direction
from game.event import Event, EventType, PlayerEventType
from game.script.script import Script

class BowScript(Script):
    def __init__(self):
        self.dir = None

        self.damage_data = None
        self.player = None
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.transform = world.component_for_entity(entity, Transform)

        self.spawn_arrow()

    def spawn_arrow(self):
        if self.player.data.arrows <= 0:
            return
        
        original = self.player.data.arrows
        self.player.data.arrows -= 1

        self.player.event_bus.send.append(Event({
            'type': PlayerEventType.ARROWS_CHANGED,
            'original': original,
            'amount': -1,
            'new': self.player.data.arrows
        }, EventType.PLAYER))
        
        arrow_entity = loader.load_entities_into("arrow", self.world)

        animation = self.world.component_for_entity(arrow_entity, AnimationSets)
        script = self.world.component_for_entity(arrow_entity, ScriptComponent)
        transform = self.world.component_for_entity(arrow_entity, Transform)

        transform.position.x = self.transform.position.x
        transform.position.y = self.transform.position.y

        animation.current = "down"
        if self.dir == Direction.UP:
            animation.current = "up"
            transform.position.y -= 32
        elif self.dir == Direction.LEFT:
            animation.current = "left"
            transform.position.x -= 32
        elif self.dir == Direction.RIGHT:
            animation.current = "right"
            transform.position.x += 16
        else:
            transform.position.y += 16

        script.script.damage_data = self.damage_data
        script.script.dir = self.dir
        script.script.player = self.player