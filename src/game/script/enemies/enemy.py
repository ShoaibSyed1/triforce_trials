from enum import Enum

import pygame

from game import constants, loader, paths
from game.component import AnimationSets, CollisionComponent, EventComponent, ScriptComponent, Tag, Transform
from game.damage_data import ArrowDamage, ExplosionDamage, SwordDamage
from game.direction import Direction
from game.event import Event, EventType, CollisionEventType, DeleteEventType, PlayerEventType
from game.script.script import Script
from game.script.sword_script import SwordScript

class Enemy(Script):
    def __init__(self):
        self.health = 3
        self.xp_amount = 5
        self.attack_amount = 1

        self.damage_knockback = pygame.math.Vector2(0, 0)

        self._enemy_state = None
        self._dead = False
    
    def start(self, entity, world):
        self.entity = entity
        self.world = world

        self.animation = world.component_for_entity(entity, AnimationSets)
        self.collision = world.component_for_entity(entity, CollisionComponent)
        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.transform = world.component_for_entity(entity, Transform)

        self._set_state(NormalState(self))
    
    def update(self, dt):
        for event in self.event_bus.events:
            self._enemy_state.on_event(event)
        
        self._enemy_state.update(dt)
    
    def _set_state(self, state):
        if self._enemy_state != None:
            self._enemy_state.stop()
        self._enemy_state = state
        self._enemy_state.start()
    
    def e_start(self): pass
    def e_update(self, dt): pass

    def on_death(self): pass

class EnemyState:
    def __init__(self, enemy):
        self.enemy = enemy
    
    def start(self): pass
    
    def stop(self): pass
    
    def update(self, dt): pass
    
    def on_event(self, event): pass

class NormalState(EnemyState):
    def __init__(self, enemy):
        super().__init__(enemy)

        self.damage_sound = pygame.mixer.Sound(paths.SOUNDS + "/enemies/damage.wav")
        self.death_sound = pygame.mixer.Sound(paths.SOUNDS + "/enemies/death.wav")
    
    def start(self):
        self.enemy.animation.current = "default"

        self.enemy.e_start()
    
    def update(self, dt):
        self.enemy.e_update(dt)
    
    def on_event(self, event):
        if event.ty == EventType.COLLISION:
            if event.data['first'] == self.enemy.entity or event.data['second'] == self.enemy.entity:
                if event.data['first'] == self.enemy.entity:
                    other_entity = event.data['second']
                else:
                    other_entity = event.data['first']

                tag = self.enemy.world.component_for_entity(other_entity, Tag)

                if tag != None:
                    if "weapon" in tag.tags:
                        self.take_damage(other_entity)
                    
                    if "player" in tag.tags:
                        self.enemy.event_bus.send.append(Event({
                            'type': PlayerEventType.HURT,
                            'amount': self.enemy.attack_amount,
                            'knockback': self.enemy.damage_knockback
                        }, EventType.PLAYER))
    
    def take_damage(self, weapon_entity):        
        script_comp = self.enemy.world.component_for_entity(weapon_entity, ScriptComponent)
        
        damage_data = script_comp.script.damage_data

        if isinstance(damage_data, ArrowDamage):
            self.enemy.health -= damage_data.damage
            self.enemy.collision.velocity += damage_data.knockback
        elif isinstance(damage_data, ExplosionDamage):
            self.enemy.health -= damage_data.damage

            hori, vert = Direction.between(damage_data.origin, self.enemy.transform.position, 16)
            x = 0
            y = 0
            if hori != None:
                x = hori.to_vector(damage_data.knockback_m).x
            if vert != None:
                y = vert.to_vector(damage_data.knockback_m).y
            
            self.enemy.collision.velocity += pygame.math.Vector2(x, y)
        elif isinstance(damage_data, SwordDamage):
            self.enemy.health -= damage_data.damage
            self.enemy.collision.velocity += damage_data.knockback

        if self.enemy.health <= 0:
            self.death_sound.play()
            self.die()
        else:
            self.damage_sound.play()
            self.enemy._set_state(StunnedState(self.enemy))
    
    def die(self):
        if self.enemy._dead:
            return
        
        self.enemy.on_death()
        
        self.enemy._dead = True
        self.enemy.event_bus.send.append(Event({
            'type': PlayerEventType.ADD_XP,
            'amount': self.enemy.xp_amount
        }, EventType.PLAYER, True))

        poof_entity = self.enemy.world.create_entity_with(*loader.load("entity", "poof")[0])
        poof_transform = self.enemy.world.component_for_entity(poof_entity, Transform)

        poof_transform.position = self.enemy.transform.position

class StunnedState(EnemyState):
    def __init__(self, enemy):
        super().__init__(enemy)
        self.cooldown = 0.5
    
    def start(self):
        self.enemy.animation.current = "stunned"
    
    def update(self, dt):
        self.cooldown -= dt

        if self.cooldown <= 0:
            self.enemy._set_state(NormalState(self.enemy))