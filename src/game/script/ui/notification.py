import pygame

from game import constants, loader, paths
from game.component import EventComponent, Sprite, Transform
from game.event import Event, EventType, NotifyEventType
from game.script.script import Script

class Notification(Script):
    def __init__(self):
        self.state = NeutralState(self)

        self.queue = []

        self.title_entity = None
        self.text_entity = None
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.sprite = world.component_for_entity(entity, Sprite)
        self.transform = world.component_for_entity(entity, Transform)

        self.state.start()
    
    def update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.NOTIFY:
                if event.data['type'] == NotifyEventType.NOTIFY:
                    time = event.data['time']
                    title = event.data['title']
                    text = event.data['text']
                    sound_path = event.data.get('sound_path', None)

                    self.add_notification(time, title, text, sound_path)
        
        self.state.update(dt)
    
    def set_state(self, state):
        if self.state != None:
            self.state.stop()
        
        self.state = state
        self.state.start()
    
    def add_notification(self, time, title, text, sound_path=None):
        self.queue.append(NotifyInfo(time, title, text, sound_path))

class NotifyInfo:
    def __init__(self, time, title, text, sound_path=None):
        self.time = time
        self.title = title
        self.text = text
        self.sound_path = sound_path

class NotificationState:
    def __init__(self, notify):
        self.notify = notify
    
    def start(self): pass
    def update(self, dt): pass
    def stop(self): pass

class NeutralState(NotificationState):
    def start(self):
        self.notify.sprite.visible = False
    
    def update(self, dt):
        if len(self.notify.queue) > 0:
            info = self.notify.queue[0]
            if info.sound_path != None:
                pygame.mixer.Sound(paths.SOUNDS + info.sound_path).play()
            self.notify.set_state(DownState(self.notify))

class DownState(NotificationState):
    def __init__(self, notify):
        super().__init__(notify)

        self.velocity = 20
    
    def start(self):
        self.notify.sprite.visible = True
        self.notify.transform.position.x = constants.WIDTH / 2 - (self.notify.sprite.texture.get_width() * self.notify.transform.scale.x) / 2
        self.notify.transform.position.y = -(self.notify.sprite.texture.get_height() * self.notify.transform.scale.y)
        
        self.create_title()
        self.create_text()
    
    def create_title(self):
        self.notify.title_entity = self.notify.world.create_entity_with(*loader.load("entity", "ui/overworld/notification_text")[0])

        self.notify.world.remove_component(self.notify.title_entity, Sprite)
        sprite = Sprite.new_text(self.notify.queue[0].title, (120, 232, 133), 24)
        self.notify.world.add_component(self.notify.title_entity, sprite)

        self.title_transform = self.notify.world.component_for_entity(self.notify.title_entity, Transform)

        self.title_transform.position.x = constants.WIDTH / 2 - (sprite.texture.get_width() * self.title_transform.scale.x) / 2
        self.title_transform.position.y = self.notify.transform.position.y + constants.NOTIFY_TITLE_DISTANCE
    
    def create_text(self):
        self.notify.text_entity = self.notify.world.create_entity_with(*loader.load("entity", "ui/overworld/notification_text")[0])

        self.notify.world.remove_component(self.notify.text_entity, Sprite)
        sprite = Sprite.new_text(self.notify.queue[0].text, (255, 255, 255), 16)
        self.notify.world.add_component(self.notify.text_entity, sprite)

        self.text_transform = self.notify.world.component_for_entity(self.notify.text_entity, Transform)

        self.text_transform.position.x = constants.WIDTH / 2 - (sprite.texture.get_width() * self.text_transform.scale.x) / 2
        self.text_transform.position.y = self.notify.transform.position.y + constants.NOTIFY_TEXT_DISTANCE
    
    def update(self, dt):
        self.notify.transform.position.y += self.velocity
        self.velocity -= 2
        if self.velocity < 3:
            self.velocity = 3
        
        self.title_transform.position.y = self.notify.transform.position.y + constants.NOTIFY_TITLE_DISTANCE
        self.text_transform.position.y = self.notify.transform.position.y + constants.NOTIFY_TEXT_DISTANCE

        if self.notify.transform.position.y >= 0:
            self.notify.transform.position.y = 0
            self.title_transform.position.y = self.notify.transform.position.y + constants.NOTIFY_TITLE_DISTANCE
            self.text_transform.position.y = self.notify.transform.position.y + constants.NOTIFY_TEXT_DISTANCE

            self.notify.set_state(DisplayState(self.notify))

class DisplayState(NotificationState):
    def __init__(self, notify):
        super().__init__(notify)

        self.timer = 0
    
    def update(self, dt):
        self.timer += dt

        if self.timer >= self.notify.queue[0].time:
            self.notify.set_state(CloseState(self.notify))

class CloseState(NotificationState):
    def __init__(self, notify):
        super().__init__(notify)

        self.velocity = 1
    
    def start(self):
        del self.notify.queue[0]

        self.title_transform = self.notify.world.component_for_entity(self.notify.title_entity, Transform)
        self.text_transform = self.notify.world.component_for_entity(self.notify.text_entity, Transform)
    
    def update(self, dt):
        self.notify.transform.position.y -= self.velocity
        self.velocity += 2

        self.title_transform.position.y = self.notify.transform.position.y + constants.NOTIFY_TITLE_DISTANCE
        self.text_transform.position.y = self.notify.transform.position.y + constants.NOTIFY_TEXT_DISTANCE

        if self.notify.transform.position.y <= -(self.notify.sprite.texture.get_height() * self.notify.transform.scale.y):
            self.notify.set_state(NeutralState(self.notify))
    
    def stop(self):
        self.notify.world.delete_entity(self.notify.title_entity)
        self.notify.world.delete_entity(self.notify.text_entity)