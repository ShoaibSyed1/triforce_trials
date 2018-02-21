import random

import pygame

from game import loader, paths
from game.component import EventComponent, Tag
from game.ecs import System
from game.event import Event, EventType, MusicEventType
from game.music import MusicInfo, RepeatType

class MusicSystem(System):
    def __init__(self):
        self.event_bus = EventComponent([EventType.MUSIC, EventType.PYGAME])
        self.cur_slot = None

        self.stopping = False
        self.stop_counter = 0
    
    def start(self):
        self.world.create_entity_with(self.event_bus, Tag(["system"]))

        pygame.mixer.music.set_endevent(32)
    
    def update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.MUSIC:
                if event.data['type'] == MusicEventType.PLAY:
                    if self.cur_slot == None or event.data['id'] != self.cur_slot.id:
                        info = loader.load("music", event.data['path'])
                        self.cur_slot = MusicSlot(event.data['id'], info, event.data.get('lifetime', None))
                        self.cur_slot.play()
                    elif self.cur_slot != None and event.data['id'] == self.cur_slot.id:
                        if event.data.get('lifetime', None) != None:
                            self.cur_slot.lifetime = event.data.get('lifetime', None)
                    
                elif event.data['type'] == MusicEventType.PUSH:
                    if self.cur_slot == None or event.data['id'] != self.cur_slot.id:
                        info = loader.load("music", event.data['path'])
                        if self.cur_slot != None:
                            self.cur_slot.stamp = pygame.mixer.music.get_pos()
                        
                        self.cur_slot = MusicSlot(event.data['id'], info, event.data.get('lifetime', None), self.cur_slot)
                        self.cur_slot.play()
                    elif self.cur_slot != None and event.data['id'] == self.cur_slot.id:
                        if event.data.get('lifetime', None) != None:
                            self.cur_slot.lifetime = event.data.get('lifetime', None)
                    
                elif event.data['type'] == MusicEventType.POP:
                    if self.cur_slot == None or event.data['id'] == self.cur_slot.id:
                        self.stopping = True
                        if event.data.get('fade', False):
                            pygame.mixer.music.fadeout(event.data['fade_time'])
                        else:
                            pygame.mixer.music.stop()
                        
                        self.cur_slot = self.cur_slot.prev
                        if self.cur_slot != None:
                            self.cur_slot.play()
                            
                            if self.cur_slot.stamp != None:
                                pygame.mixer.music.rewind()
                                pygame.mixer.music.set_pos(self.cur_slot.stamp / 1000)
            elif event.ty == EventType.PYGAME:
                if event.data.type == 32:
                    if self.cur_slot != None and not self.stopping:
                        self.cur_slot.next()
                        self.cur_slot.play()
        
        if self.stopping:
            self.stop_counter -= dt
            if self.stop_counter <= 0:
                self.stopping = False
                self.stop_counter = 1
        else:
            self.stop_counter = 1
        
        if self.cur_slot != None and self.cur_slot.lifetime != None:
            self.cur_slot.lifetime -= dt

            if self.cur_slot.lifetime <= 0:
                self.event_bus.send.append(Event({
                    'type': MusicEventType.POP,
                    'id': self.cur_slot.id
                }, EventType.MUSIC))

class MusicSlot:
    def __init__(self, id, info, lifetime, prev=None):
        self.id = id
        self.info = info
        self.lifetime = lifetime

        self.prev = prev
        self.stamp = None
        self.choice = None
    
    def play(self):
        if self.choice == None:
            self.next()

        choice = self.info.choices[self.choice]

        pygame.mixer.music.load(paths.MUSIC + choice['path'] + ".mp3")
        pygame.mixer.music.play()
    
    def next(self):
        weights = map(lambda x: x.get('chance', 1), self.info.choices)
        self.choice = random.choices(list(range(len(self.info.choices))), weights)[0]

"""
class MusicSystem(System):
    def __init__(self):
        self._event_bus = EventComponent([EventType.MUSIC, EventType.PYGAME])
        self._music_info = None
        self._cur_id = None
        self.paused = False
        self.stopped = False

    def start(self):
        self.world.create_entity_with(self._event_bus, Tag(["system"]))

        pygame.mixer.music.set_endevent(32)
    
    def update(self, dt):
        for event in self._event_bus.get_events():
            if event.ty == EventType.MUSIC:
                if event.data['type'] == MusicEventType.LOAD:
                    new_id = event.data.get('id', None)
                    if self._cur_id == None or new_id != self._cur_id:
                        self._cur_id = new_id
                        self._music_info = loader.load("music", event.data['path'])
                elif event.data['type'] == MusicEventType.PLAY:
                    if self._cur_id != None and self._cur_id == event.data.get('id', None):
                        continue
                    
                    if self.paused:
                        pygame.mixer.music.unpause()
                        self.paused = False
                    elif self._music_info != None:
                        self.stopped = False

                        # TODO: Other repeat types
                        weights = map(lambda x: x.get('chance', 1), self._music_info.choices)
                        choice = random.choices(self._music_info.choices, weights)[0]

                        pygame.mixer.music.load(paths.MUSIC + choice['path'] + ".mp3")
                        pygame.mixer.music.play()
                elif event.data['type'] == MusicEventType.PAUSE:
                    pygame.mixer.music.pause()
                    self.paused = True
                elif event.data['type'] == MusicEventType.STOP:
                    if event.data['fade']:
                        pygame.mixer.music.fadeout(event.data['fade_time'])
                    else:
                        pygame.mixer.music.stop()
                    
                    self.stopped = True
            elif event.ty == EventType.PYGAME:
                if event.data.type == 32:
                    if not self.stopped:
                        if self._music_info != None and self._music_info.repeat_type != RepeatType.NONE:
                            self._event_bus.events.append(Event({
                                'type': MusicEventType.PLAY
                            }, EventType.MUSIC))
"""