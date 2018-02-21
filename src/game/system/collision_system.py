import pygame

from game.component import CollisionComponent, EventComponent, Tag, Transform
from game.constants import COLLISION_DISTANCE
from game.ecs import System
from game.event import Event, EventType

class CollisionSystem(System):
    def __init__(self):
        self.event_bus = EventComponent([])
    
    def start(self):
        self.world.create_entity_with(self.event_bus, Tag(["system"]))
    
    def update(self, dt):
        import math

        bodies = [Body(entity, collision, transform) for entity, [collision, transform] in self.world.get_components(CollisionComponent, Transform)]
        if len(bodies) < 1:
            return
        quad_tree = QuadTree(bodies, 4)
        
        for body in bodies:
            body.collision.velocity.x *= body.collision.friction
            body.collision.velocity.y *= body.collision.friction

            if abs(body.collision.velocity.x) < 0.5:
                body.collision.velocity.x = 0
            if abs(body.collision.velocity.y) < 0.5:
                body.collision.velocity.y = 0

            if abs(body.collision.velocity.x) > body.collision.max_speed:
                body.collision.velocity.x = math.copysign(body.collision.max_speed, body.collision.velocity.x)
            if abs(body.collision.velocity.y) > body.collision.max_speed:
                body.collision.velocity.y = math.copysign(body.collision.max_speed, body.collision.velocity.y)

            if body.collision.velocity.x != 0 or body.collision.velocity.y != 0 or body.collision.persistent:
                prev_x = body.transform.position.x
                prev_y = body.transform.position.y

                sent = []

                body.transform.position.x += body.collision.velocity.x * dt

                for other_body in quad_tree.collide(body):
                    self.event_bus.send.append(Event({
                        'first': body.entity,
                        'second': other_body.entity
                    }, EventType.COLLISION))
                    sent.append(other_body.entity)
                    if body.collision.solid and other_body.collision.solid:
                        body.transform.position.x = prev_x
                        body.collision.velocity.x = 0
                
                body.transform.position.y += body.collision.velocity.y * dt

                for other_body in quad_tree.collide(body):
                    if not other_body.entity in sent:
                        self.event_bus.send.append(Event({
                            'first': body.entity,
                            'second': other_body.entity
                        }, EventType.COLLISION))
                    if body.collision.solid and other_body.collision.solid:
                        body.transform.position.y = prev_y
                        body.collision.velocity.y = 0

class Body:
    def __init__(self, entity, collision, transform):
        self.entity = entity
        self.collision = collision
        self.transform = transform
    
    def get_rect(self):
        return pygame.Rect(
            self.transform.position.x,
            self.transform.position.y,
            self.collision.size.x * self.transform.scale.x,
            self.collision.size.y * self.transform.scale.y)
    
    def get_right(self):
        return self.transform.position.x + self.collision.size.x * self.transform.scale.x
    
    def get_bottom(self):
        return self.transform.position.y + self.collision.size.y * self.transform.scale.y

class QuadTree:
    def __init__(self, bodies, depth, bounds=None):
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

        depth -= 1
        if depth <= 0:
            self.bodies = bodies
            return
        
        if bounds == None:
            left = min(body.transform.position.x for body in bodies)
            top = min(body.transform.position.y for body in bodies)
            right = max(body.get_right() for body in bodies)
            bottom = max(body.get_bottom() for body in bodies)
        else:
            left, top, right, bottom = bounds
        
        self.center_x = (left + right) / 2
        self.center_y = (top + bottom) / 2

        self.bodies = []
        nws = []
        nes = []
        sws = []
        ses = []

        for body in bodies:
            nw = (body.transform.position.x <= self.center_x and body.transform.position.y <= self.center_y) or (body.get_right() <= self.center_x and body.get_bottom() <= self.center_y)
            ne = (body.transform.position.x >= self.center_x and body.transform.position.y <= self.center_y) or (body.get_right() >= self.center_x and body.get_bottom() <= self.center_y)
            sw = (body.transform.position.x <= self.center_x and body.transform.position.y >= self.center_y) or (body.get_right() <= self.center_x and body.get_bottom() >= self.center_y)
            se = (body.transform.position.x >= self.center_x and body.transform.position.y >= self.center_y) or (body.get_right() >= self.center_x and body.get_bottom() >= self.center_y)

            if nw and ne and sw and se:
                self.bodies.append(body)
            else:
                if nw:
                    nws.append(body)
                if ne:
                    nes.append(body)
                if sw:
                    sws.append(body)
                if se:
                    ses.append(body)
        
        if len(nws) > 0:
            self.nw = QuadTree(nws, depth, (left, top, self.center_x, self.center_y))
        if len(nes) > 0:
            self.ne = QuadTree(nes, depth, (self.center_x, top, right, self.center_y))
        if len(sws) > 0:
            self.sw = QuadTree(sws, depth, (left, self.center_y, self.center_x, bottom))
        if len(ses) > 0:
            self.se = QuadTree(ses, depth, (self.center_x, self.center_y, right, bottom))
    
    def collide(self, body):
        collisions = set([self.bodies[i] for i in body.get_rect().collidelistall([body.get_rect() for body in self.bodies])])

        rect = body.get_rect()
        if self.nw != None and ((rect.left <= self.center_x and rect.top <= self.center_y) or (rect.right <= self.center_x and rect.bottom <= self.center_y)):
            collisions |= self.nw.collide(body)
        if self.ne != None and ((rect.left >= self.center_x and rect.top <= self.center_y) or (rect.right >= self.center_x and rect.bottom <= self.center_y)):
            collisions |= self.ne.collide(body)
        if self.sw != None and ((rect.left <= self.center_x and rect.top >= self.center_y) or (rect.right <= self.center_x and rect.bottom >= self.center_y)):
            collisions |= self.sw.collide(body)
        if self.se != None and ((rect.left >= self.center_x and rect.top >= self.center_y) or (rect.right >= self.center_x and rect.bottom >= self.center_y)):
            collisions |= self.se.collide(body)
        
        if body in collisions:
            collisions.remove(body)
        
        return collisions