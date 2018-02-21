import pygame

from game.component import EventComponent
from game.ecs import System
from game.event import Event, EventType

class EventSystem(System):
    def __init__(self):
        self.should_quit = False
    
    def update(self, dt):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.should_quit = True
            
            for entity, [event_component] in self.world.get_components(EventComponent):
                if EventType.PYGAME in event_component.listen:
                    event_component.send.append(Event(ev, EventType.PYGAME))