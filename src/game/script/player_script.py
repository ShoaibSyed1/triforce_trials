import pygame

from game import constants, loader, paths
from game.component import AnimationSets, CollisionComponent, EventComponent, ScriptComponent, Sprite, Tag, Transform
from game.direction import Direction
from game.drop import DropType
from game.event import CameraEventType, Event, EventType, PlayerEventType
from game.player_data import PlayerData
from game.script.script import Script
from game.script.sword_script import SwordScript

class PlayerScript(Script):
    def __init__(self, data):
        self.data = PlayerData()

        self.sound_death = pygame.mixer.Sound(paths.SOUNDS + "player/death.wav")
        self.sound_hurt = pygame.mixer.Sound(paths.SOUNDS + "player/hurt.wav")

        self.sound_pickup_arrow = pygame.mixer.Sound(paths.SOUNDS + "player/pickup/arrow.wav")
        
        self.facer = Facer(self)
        self.state = None

        self.hurt_cooldown = 0
        self.hurt_blinker = 0

        self.bomb_timer = constants.BOMB_COOLDOWN

        self.joystick = None
        if pygame.joystick.get_count() > 0 and False: # TODO: Setting to enable joystick
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
    
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

        self.event_bus.send.append(Event({
            'type': PlayerEventType.ARROWS_CHANGED,
            'original': self.data.arrows,
            'amount': 0,
            'new': self.data.arrows
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
                    self.hurt(event.data['amount'], event.data.get('knockback', pygame.math.Vector2(0, 0)))
            elif event.ty == EventType.COLLISION:
                other = None
                if event.data['first'] == self.entity:
                    other = event.data['second']
                elif event.data['second'] == self.entity:
                    other = event.data['first']
                
                if other != None:
                    if self.world.has_component(other, Tag):
                        tag = self.world.component_for_entity(other, Tag)
                        if "drop" in tag.tags:
                            script = self.world.component_for_entity(other, ScriptComponent).script
                            drop_info = script.drop

                            if drop_info.ty == DropType.ARROW:
                                amount = drop_info.data['amount']

                                original = self.data.arrows
                                self.data.arrows += amount

                                self.event_bus.send.append(Event({
                                    'type': PlayerEventType.ARROWS_CHANGED,
                                    'original': original,
                                    'amount': amount,
                                    'new': self.data.arrows
                                }, EventType.PLAYER))

                                self.sound_pickup_arrow.play()

                                script.collected()
            
            self.state.on_event(event)
        
        self.state.update(dt)

        self.hurt_cooldown -= dt
        if self.hurt_cooldown < 0:
            self.hurt_cooldown = 0
            self.sprite.visible = True

        if self.hurt_cooldown > 0:
            self.hurt_blinker += dt
            if self.hurt_blinker >= constants.HURT_BLINK:
                self.hurt_blinker = 0
                self.sprite.visible = not self.sprite.visible 

        if self.bomb_timer > 0:
            self.bomb_timer -= dt           
    
    def set_state(self, state):
        if self.state != None:
            self.state.stop()
        self.state = state
        self.state.start()
    
    def hurt(self, amount, knockback):
        if self.hurt_cooldown > 0:
            return
        self.hurt_cooldown = constants.HURT_COOLDOWN
        
        original = self.data.health

        self.data.health -= amount
        if self.data.health <= 0:
            gameover = self.world.create_entity_with(*loader.load("entity", "gameover")[0])

            script = self.world.component_for_entity(gameover, ScriptComponent).script
            script.player_pos = self.transform.position

            self.data = PlayerData()
        else:
            self.collision.velocity.x += knockback.x
            self.collision.velocity.y += knockback.y

            self.sound_hurt.play()

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

        if keys_pressed[pygame.K_w] or (self.player.joystick != None and self.player.joystick.get_axis(1) > 0.2):
            if not self.player.facer.contains(Direction.UP):
                self.player.facer.hold(Direction.UP)
        else:
            self.player.facer.release(Direction.UP)
        
        if keys_pressed[pygame.K_s] or (self.player.joystick != None and self.player.joystick.get_axis(1) < -0.2):
            if not self.player.facer.contains(Direction.DOWN):
                self.player.facer.hold(Direction.DOWN)
        else:
            self.player.facer.release(Direction.DOWN)
        
        if keys_pressed[pygame.K_a] or (self.player.joystick != None and self.player.joystick.get_axis(0) < -0.2):
            if not self.player.facer.contains(Direction.LEFT):
                self.player.facer.hold(Direction.LEFT)
        else:
            self.player.facer.release(Direction.LEFT)
        
        if keys_pressed[pygame.K_d] or (self.player.joystick != None and self.player.joystick.get_axis(0) > 0.2):
            if not self.player.facer.contains(Direction.RIGHT):
                self.player.facer.hold(Direction.RIGHT)
        else:
            self.player.facer.release(Direction.RIGHT)
    
    def on_event(self, event):
        if event.ty == EventType.PYGAME:
            if event.data.type == pygame.KEYDOWN:
                if event.data.key == pygame.K_SPACE:
                    self.player.set_state(SwingState(self.player))
                elif event.data.key == pygame.K_LSHIFT:
                    self.player.set_state(BowState(self.player))
                elif event.data.key == pygame.K_b:
                    self.spawn_bomb()
            elif event.data.type == pygame.JOYBUTTONDOWN:
                if event.data.joy == 0:
                    if event.data.button == 18:
                        self.player.set_state(SwingState(self.player))
                    elif event.data.button == 16:
                        self.player.set_state(BowState(self.player))
                    elif event.data.button == 17:
                        self.spawn_bomb()
    
    def spawn_bomb(self):
        if self.player.bomb_timer <= 0 and self.player.data.bombs > 0:
            original = self.player.data.bombs
            self.player.data.bombs -= 1
            self.player.event_bus.send.append(Event({
                'type': PlayerEventType.BOMBS_CHANGED,
                'original': original,
                'amount': -1,
                'new': self.player.data.bombs
            }, EventType.PLAYER))
                        
            self.player.bomb_timer = constants.BOMB_COOLDOWN
            bomb = self.player.world.create_entity_with(*loader.load("entity", "bomb")[0])

            transform = self.player.world.component_for_entity(bomb, Transform)
            transform.position.x = self.player.transform.position.x
            transform.position.y = self.player.transform.position.y

            script = self.player.world.component_for_entity(bomb, ScriptComponent).script
            script.damage_data = self.player.data.get_explosion_damage(transform.position)

class Facer:
    def __init__(self, player):
        self._dirs = []
        self._last_dir = None
        self.player = player
    
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
        if self.player.joystick != None:
            joy_x = self.player.joystick.get_axis(0)
            joy_y = self.player.joystick.get_axis(1)
            if joy_x < -0.9:
                joy_x = -1
            elif joy_x > 0.9:
                joy_x = 1
            elif (joy_x < 0.2 and joy_x > 0) or (joy_x > -0.2 and joy_x < 0):
                joy_x = 0
            
            if joy_y < -0.9:
                joy_y = -1
            elif joy_y > 0.9:
                joy_y = 1
            elif (joy_y < 0.2 and joy_y > 0) or (joy_y > -0.2 and joy_y < 0):
                joy_y = 0
            
            return pygame.math.Vector2(50 * joy_x, -50 * joy_y)
        elif self.is_moving():
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

        dir = self.player.facer.get_dir()
        if dir == None:
            dir = Direction.DOWN

        self.real_sword_entity = self.player.world.create_entity_with(*loader.load("entity", "sword_collision")[0])
        sword_script = SwordScript(self.player.data.get_sword_damage(dir), self.player)
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

class BowState(PlayerState):
    def __init__(self, player):
        super().__init__(player)

        self.sound = pygame.mixer.Sound(paths.SOUNDS + "bow.wav")

        self.timer = 0
    
    def start(self):
        self.setup_bow()

        self.player.collision.velocity.x = 0
        self.player.collision.velocity.y = 0

        self.sound.play()

        dir = self.player.facer.get_dir()
        animation = "bow_down"
        if dir == Direction.UP:
            animation = "bow_up"
        elif dir == Direction.LEFT:
            animation = "bow_left"
        elif dir == Direction.RIGHT:
            animation = "bow_right"
        
        self.player.animation.current = animation
    
    def setup_bow(self):
        self.bow_entity = self.player.world.create_entity_with(*loader.load("entity", "bow")[0])

        animation = self.player.world.component_for_entity(self.bow_entity, AnimationSets)
        script = self.player.world.component_for_entity(self.bow_entity, ScriptComponent)
        transform = self.player.world.component_for_entity(self.bow_entity, Transform)

        dir = self.player.facer.get_dir()
        if dir == None:
            dir = Direction.DOWN

        script.script.damage_data = self.player.data.get_bow_damage(dir)
        script.script.player = self.player

        dir = self.player.facer.get_dir()

        if dir == Direction.UP:
            transform.position.x = self.player.transform.position.x
            transform.position.y = self.player.transform.position.y
            transform.layer = 9
            animation.current = "up"
            script.script.dir = Direction.UP
        elif dir == Direction.LEFT:
            transform.position.x = self.player.transform.position.x - 8
            transform.position.y = self.player.transform.position.y
            animation.current = "left"
            script.script.dir = Direction.LEFT
        elif dir == Direction.RIGHT:
            transform.position.x = self.player.transform.position.x + self.player.sprite.bounds.width + 4
            transform.position.y = self.player.transform.position.y
            animation.current = "right"
            script.script.dir = Direction.RIGHT
        else:
            transform.position.x = self.player.transform.position.x
            transform.position.y = self.player.transform.position.y + self.player.sprite.bounds.height
            animation.current = "down"
            script.script.dir = Direction.DOWN
    
    def update(self, dt):
        self.timer += dt

        if self.timer >= constants.BOW_TIME:
            self.player.set_state(NeutralState(self.player))
    
    def stop(self):
        self.player.world.delete_entity(self.bow_entity)