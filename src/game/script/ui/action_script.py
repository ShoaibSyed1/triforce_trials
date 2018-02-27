import pygame

from game import constants, loader
from game.component import EventComponent, Sprite, Transform
from game.event import Event, EventType, ActionEventType
from game.script.script import Script

class ActionScript(Script):
    def __init__(self):
        self.cur_id = None
        self.cur_text = None
        self.cur_callback = None
        self.cur_timeout = None

        self.timer = 0

        self.text_entity = None
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.sprite = world.component_for_entity(entity, Sprite)

        self.reset()
    
    def update(self, dt):
        if self.cur_timeout != None:
            self.timer += dt
            if self.timer >= self.cur_timeout:
                self.timer = 0
                self.reset()
        
        for event in self.event_bus.get_events():
            if event.ty == EventType.ACTION:
                if event.data['type'] == ActionEventType.SET_INFO:
                    self.cur_id = event.data['id']
                    self.cur_text = event.data['text']
                    self.cur_callback = event.data['callback']
                    self.cur_timeout = event.data.get('timeout', None)
                    self.update_action()
                elif event.data['type'] == ActionEventType.DELETE_INFO:
                    if event.data['id'] == self.cur_id:
                        self.reset()
            elif event.ty == EventType.PYGAME:
                if event.data.type == pygame.KEYDOWN:
                    if event.data.key == pygame.K_e:
                        if self.cur_callback != None:
                            if self.cur_callback() == True:
                                self.reset()
                elif event.data.type == pygame.JOYBUTTONDOWN:
                    if event.data.joy == 0:
                        if event.data.button == 19:
                            if self.cur_callback != None:
                                if self.cur_callback() == True:
                                    self.reset()
    
    def reset(self):
        self.cur_id = None
        self.cur_text = None
        self.cur_callback = None
        self.cur_timeout = None

        self.sprite.visible = False

        if self.text_entity != None:
            self.world.delete_entity(self.text_entity)
            self.text_entity = None
    
    def update_action(self):
        if self.text_entity != None:
            self.world.delete_entity(self.text_entity)
            self.text_entity = None
        
        self.sprite.visible = True
        
        self.text_entity = self.world.create_entity_with(*loader.load("entity", "ui/overworld/action_text")[0])
        sprite = Sprite.new_text(self.cur_text, (255, 255, 255), 20)
        self.world.add_component(self.text_entity, sprite)
        transform = self.world.component_for_entity(self.text_entity, Transform)
        transform.position.x = constants.WIDTH / 2 - sprite.texture.get_width() / 2
        transform.position.y = 320