import pygame

from game import constants
from game.batch import SpriteBatch
from game.component import EventComponent, Sprite, Tag, Tag, Transform
from game.ecs import System
from game.event import CameraEventType, Event, EventType

class RenderSystem(System):
    def __init__(self, screen):
        self.screen = screen

        self.buffer = pygame.Surface((constants.WIDTH, constants.HEIGHT))

        self._batch = SpriteBatch()
        
        self._cam_bounds = pygame.Rect(0, 0, 1000, 1000)
        self._cam_pos = pygame.math.Vector2(0, 0)

        self._event_bus = EventComponent([EventType.CAMERA])
    
    def start(self):
        self.world.create_entity_with(self._event_bus, Tag(["system"]))

    def update(self, dt):
        for event in self._event_bus.get_events():
            if event.ty == EventType.CAMERA:
                if event.data['type'] == CameraEventType.FOLLOW:
                    self._cam_pos = event.data.get('pos', pygame.math.Vector2(0, 0)) - event.data.get('offset', pygame.math.Vector2(0, 0))
                    
                    if self._cam_pos.x < self._cam_bounds.x:
                        self._cam_pos.x = self._cam_bounds.x
                    elif self._cam_pos.x > ((self._cam_bounds.x + self._cam_bounds.width) - self.buffer.get_width()):
                        self._cam_pos.x = self._cam_bounds.x + self._cam_bounds.width - self.buffer.get_width()
                    
                    if self._cam_pos.y < self._cam_bounds.y:
                        self._cam_pos.y = self._cam_bounds.y
                    elif self._cam_pos.y > ((self._cam_bounds.y + self._cam_bounds.height) - self.buffer.get_height()):
                        self._cam_pos.y = self._cam_bounds.y + self._cam_bounds.height - self.buffer.get_height()

                elif event.data['type'] == CameraEventType.SET_BOUNDS:
                    self._cam_bounds = pygame.Rect(event.data['x'], event.data['y'], event.data['width'], event.data['height'])
        
        self.buffer.fill((255, 255, 255))

        comps = list(self.world.get_components(Sprite, Transform))
        comps.sort(key=lambda x:
            x[1][1].layer)
        
        for (entity, (sprite, transform)) in comps:
            if not transform.fixed:
                transform = Transform(
                    position=pygame.math.Vector2(transform.position.x - self._cam_pos.x, transform.position.y - self._cam_pos.y),
                    scale=transform.scale,
                    layer=transform.layer,
                    fixed=False)
            if sprite.visible:
                self._batch.draw(entity, sprite, transform)

        self._batch.update(self.buffer)
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()