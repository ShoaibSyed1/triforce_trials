from game.component import EventComponent
from game.ecs import System

class EventBusSystem(System):
    def update(self, dt):
        events = []
        for entity, [event_component] in self.world.get_components(EventComponent):
            for event in event_component.send:
                events.append(event)
                event_component.send.remove(event)
                if event.delete_after:
                    self.world.delete_entity(entity)
        
        for entity, [event_component] in self.world.get_components(EventComponent):
            for event in event_component.to_remove:
                event_component.events.remove(event)
            
            for event in events:
                if event.ty in event_component.listen:
                    event_component.events.append(event)