import pygame

from game import constants, loader, paths
from game.component import AnimationSets, CollisionComponent, EventComponent, ScriptComponent, Sprite, Tag, Transform
from game.direction import Direction
from game.event import CameraEventType, Event, EventType, PlayerEventType
from game.player_data import PlayerData
from game.script.script import Script
from game.script.sword_script import SwordScript
from game.sword_data import SwordData

class PlayerScript(Script):
    def __init__(self, data):
        self.data = PlayerData()
        
        self.facer = Facer()
        self.state = None

        self.hurt_cooldown = 0
    
    def start(self, entity, world):
        self.animation = world.component_for_entity(entity, AnimationSets)
        self.collision = world.component_for_entity(entity, CollisionComponent)
        self.event_bus = world.component_for_entity(entity, EventComponent)
        self.sprite = world.component_for_entity(entity, Sprite)
        self.transform = world.component_for_entity(entity, Transform)

        self.entity = entity
        self.world = world

        self.data.load()

        self.world.add_close_listener(entity, lambda: self.data.save())

        self.event_bus.send.append(Event({
            'type': PlayerEventType.XP_ADDED,
            'original': self.data.xp,
            'amount': 0,
            'new': self.data.xp
        }, EventType.PLAYER))

        self.event_bus.send.append(Event({
            'type': PlayerEventType.HEALTH_CHANGED,
            'original': self.data.health,
            'amount': 0,
            'new': self.data.health
        }, EventType.PLAYER))

        self.set_state(NeutralState(self))
    
    def update(self, dt):
        for event in self.event_bus.get_events():
            if event.ty == EventType.PLAYER:
                if event.data['type'] == PlayerEventType.SET_POS:
                    self.transform.position.x = event.data['x']
                    self.transform.position.y = event.data['y']

                    self.event_bus.send.append(Event({
                        'type': CameraEventType.FOLLOW,
                        'pos': self.transform.position,
                        'offset': pygame.math.Vector2(320 - 16, 200 - 16)
                    }, EventType.CAMERA))
                elif event.data['type'] == PlayerEventType.ADD_XP:
                    original = self.data.xp
                    self.data.add_xp(event.data['amount'])

                    self.event_bus.send.append(Event({
                        'type': PlayerEventType.XP_ADDED,
                        'original': original,
                        'amount': event.data['amount'],
                        'new': self.data.xp
                    }, EventType.PLAYER))
                elif event.data['type'] == PlayerEventType.HURT:
                    self.hurt(event.data['amount'])
            
            self.state.on_event(event)
        
        self.state.update(dt)

        self.hurt_cooldown += dt
    
    def set_state(self, state):
        if self.state != None:
            self.state.stop()
        self.state = state
        self.state.start()
    
    def hurt(self, amount):
        if self.hurt_cooldown < constants.HURT_COOLDOWN:
            return
        
        original = self.data.health
        
        self.hurt_cooldown = 0

        self.data.health -= amount
        if self.data.health <= 0:
            print("DEAD")

        print("HURT")

        self.event_bus.send.append(Event({
            'type': PlayerEventType.HEALTH_CHANGED,
            'original': original,
            'amount': amount,
            'new': self.data.health
        }, EventType.PLAYER))

class PlayerState:
    def __init__(self, player):
        self.player = player
    
    def start(self): pass
    
    def update(self, dt): pass
    
    def stop(self): pass

    def on_event(self, event): pass

class NeutralState(PlayerState):
    def __init__(self, player):
        super().__init__(player)

        self.step_sound = pygame.mixer.Sound(paths.SOUNDS + "player/step.wav")
        self.step_timer = 0
    
    def start(self):
        self.player.event_bus.send.append(Event({
            'type': CameraEventType.FOLLOW,
            'pos': self.player.transform.position,
            'offset': pygame.math.Vector2(320 - 16, 200 - 16)
        }, EventType.CAMERA))
    
    def update(self, dt):
        self.player.collision.velocity += self.player.facer.get_movement()
        self.player.animation.current = self.player.facer.get_animation()

        if self.player.facer.is_moving():
            self.step_timer += dt

            if self.step_timer >= 0.35:
                self.step_timer = 0
                self.step_sound.play()
        else:
            self.step_timer = 0

        if self.player.collision.velocity.x != 0 or self.player.collision.velocity.y != 0:
            self.player.event_bus.send.append(Event({
                'type': CameraEventType.FOLLOW,
                'pos': self.player.transform.position,
                'offset': pygame.math.Vector2(320 - 16, 200 - 16)
            }, EventType.CAMERA))

            self.player.event_bus.send.append(Event({
                'type': PlayerEventType.PLAYER_MOVED,
                'x': self.player.transform.position.x,
                'y': self.player.transform.position.y
            }, EventType.PLAYER))
        
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_w]:
            if not self.player.facer.contains(Direction.UP):
                self.player.facer.hold(Direction.UP)
        else:
            self.player.facer.release(Direction.UP)
        
        if keys_pressed[pygame.K_s]:
            if not self.player.facer.contains(Direction.DOWN):
                self.player.facer.hold(Direction.DOWN)
        else:
            self.player.facer.release(Direction.DOWN)
        
        if keys_pressed[pygame.K_a]:
            if not self.player.facer.contains(Direction.LEFT):
                self.player.facer.hold(Direction.LEFT)
        else:
            self.player.facer.release(Direction.LEFT)
        
        if keys_pressed[pygame.K_d]:
            if not self.player.facer.contains(Direction.RIGHT):
                self.player.facer.hold(Direction.RIGHT)
        else:
            self.player.facer.release(Direction.RIGHT)
    
    def on_event(self, event):
        if event.ty == EventType.PYGAME:
            if event.data.type == pygame.KEYDOWN:
                if event.data.key == pygame.K_SPACE:
                    self.player.set_state(SwingState(self.player))

class Facer:
    def __init__(self):
        self._dirs = []
        self._last_dir = None
    
    def contains(self, dir):
        return dir in self._dirs
    
    def hold(self, dir):
        if len(self._dirs) > 0 and self._dirs[-1] == dir:
            return
        
        self.release(dir)
        
        self._dirs.append(dir)
    
    def release(self, dir):
        if dir in self._dirs:
            self._dirs.remove(dir)
    
    def get_dir(self):
        if len(self._dirs) > 0:
            self._last_dir = self._dirs[0]
            return self._dirs[0]
        else:
            return self._last_dir
    
    def is_moving(self):
        return len(self._dirs) > 0
    
    def get_movement(self):
        if self.is_moving():
            horizontal_dir = None
            vertical_dir = None

            new_dirs = self._dirs.copy()
            new_dirs.reverse()
            for dir in new_dirs:
                if dir.is_horizontal():
                    horizontal_dir = dir
                else:
                    vertical_dir = dir
            
            move = pygame.math.Vector2(0, 0)
            if horizontal_dir == Direction.LEFT:
                move.x -= 50
            elif horizontal_dir == Direction.RIGHT:
                move.x += 50
            
            if vertical_dir == Direction.UP:
                move.y -= 50
            elif vertical_dir == Direction.DOWN:
                move.y += 50
            
            return move
        else:
            return pygame.math.Vector2(0, 0)
    
    def get_animation(self):
        dir = self.get_dir()
        if len(self._dirs) > 0:
            if dir == Direction.UP:
                return "walk_up"
            elif dir == Direction.DOWN:
                return "walk_down"
            elif dir == Direction.LEFT:
                return "walk_left"
            else:
                return "walk_right"
        else:
            if dir == Direction.UP:
                return "idle_up"
            elif dir == Direction.LEFT:
                return "idle_left"
            elif dir == Direction.RIGHT:
                return "idle_right"
            else:
                return "idle_down"

class SwingState(PlayerState):
    def __init__(self, player):
        super().__init__(player)

        self.sound = pygame.mixer.Sound(paths.SOUNDS + "player/sword_attack.wav")

        self.timer = 0

        self.real_sword_entity = self.player.world.create_entity_with(*loader.load("entity", "sword_collision")[0])
        sword_script = SwordScript(SwordData(1), self.player)
        self.player.world.add_component(self.real_sword_entity, ScriptComponent(sword_script))
        self.sword_entity = self.player.world.create_entity_with(*loader.load("entity", "sword")[0])
    
    def start(self):
        self.setup_sword()

        self.sound.play()

        self.player.collision.velocity.x = 0
        self.player.collision.velocity.y = 0

        dir = self.player.facer.get_dir()
        animation = "sword_down"
        if dir == Direction.DOWN:
            animation = "sword_down"
        elif dir == Direction.RIGHT:
            animation = "sword_right"
        elif dir == Direction.LEFT:
            animation = "sword_left"
        elif dir == Direction.UP:
            animation = "sword_up"
        
        self.player.animation.current = animation
    
    def setup_sword(self):
        animation = self.player.world.component_for_entity(self.sword_entity, AnimationSets)
        transform = self.player.world.component_for_entity(self.sword_entity, Transform)
        
        transform.position.x = self.player.transform.position.x - 16 * transform.scale.x - self.player.sprite.offset.x
        transform.position.y = self.player.transform.position.y - 16 * transform.scale.y - self.player.sprite.offset.y

        real_collision = self.player.world.component_for_entity(self.real_sword_entity, CollisionComponent)
        real_transform = self.player.world.component_for_entity(self.real_sword_entity, Transform)

        dir = self.player.facer.get_dir()

        if dir == Direction.DOWN or dir == None:
            animation.current = "swing_down"
            real_collision.size.x = 32
            real_collision.size.y = 16
            real_transform.position.x = self.player.transform.position.x + self.player.sprite.offset.x - 8 * real_transform.scale.x
            real_transform.position.y = self.player.transform.position.y + self.player.sprite.offset.y + self.player.sprite.frame_height * self.player.transform.scale.y // 2
        elif dir == Direction.RIGHT:
            animation.current = "swing_right"
            real_collision.size.x = 20
            real_collision.size.y = 32
            real_transform.position.x = self.player.transform.position.x + self.player.sprite.offset.x + self.player.sprite.frame_width * self.player.transform.scale.x // 2
            real_transform.position.y = self.player.transform.position.y + self.player.sprite.offset.y - 8 * real_transform.scale.y
        elif dir == Direction.LEFT:
            animation.current = "swing_left"
            real_collision.size.x = 20
            real_collision.size.y = 32
            real_transform.position.x = -20 * real_transform.scale.x + self.player.transform.position.x + self.player.sprite.offset.x + self.player.sprite.frame_width * self.player.transform.scale.x // 2
            real_transform.position.y = self.player.transform.position.y + self.player.sprite.offset.y - 8 * real_transform.scale.y
        elif dir == Direction.UP:
            real_collision.size.x = 32
            real_collision.size.y = 16
            real_transform.position.x = self.player.transform.position.x + self.player.sprite.offset.x - 8 * real_transform.scale.x
            real_transform.position.y = -32 * real_transform.scale.y + self.player.transform.position.y + self.player.sprite.offset.y + self.player.sprite.frame_height * self.player.transform.scale.y // 2
            animation.current = "swing_up"
    
    def stop(self):
        self.player.world.delete_entity(self.real_sword_entity)
        self.player.world.delete_entity(self.sword_entity)

    def update(self, dt):
        self.timer += dt

        if self.timer >= constants.SWING_TIME:
            self.player.set_state(NeutralState(self.player))