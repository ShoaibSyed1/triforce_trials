import pygame

from game.constants import WIDTH, HEIGHT

class SpriteBatch:
    def __init__(self):
        self._sprites = {}
        self._marked = []
    
    def draw(self, entity, sprite, transform):
        self._marked.append(entity)
        if entity in self._sprites.keys():            
            if transform.scale != self._sprites[entity].scale or sprite._redraw:
                sprite._redraw = False
                self._sprites[entity].scale = transform.scale
                self._sprites[entity].texture = pygame.transform.scale(
                    sprite.texture,
                    (int(sprite.texture.get_width() * transform.scale.x),
                    int(sprite.texture.get_height() * transform.scale.y)))
            
            self._sprites[entity].bounds = pygame.Rect(
                sprite.bounds.x * transform.scale.x,
                sprite.bounds.y * transform.scale.y,
                sprite.bounds.width * transform.scale.x,
                sprite.bounds.height * transform.scale.y)
            
            self._sprites[entity].position = transform.position
            self._sprites[entity].layer = transform.layer
        else:
            self._sprites[entity] = SpriteData(sprite.texture, sprite.bounds.copy(), transform.scale, transform.position, transform.layer, sprite.offset)
            self._sprites[entity].texture = pygame.transform.scale(
                sprite.texture,
                (int(sprite.texture.get_width() * transform.scale.x),
                int(sprite.texture.get_height() * transform.scale.y)))
            self._sprites[entity].bounds = pygame.Rect(
                sprite.bounds.x * transform.scale.x,
                sprite.bounds.y * transform.scale.y,
                sprite.bounds.width * transform.scale.x,
                sprite.bounds.height * transform.scale.y)
    
    def update(self, surface):
        remove = []
        for entity in self._sprites.keys():
            if not entity in self._marked:
                remove.append(entity)
        
        for entity in remove:
            del self._sprites[entity]

        for entity in self._marked:
            sprite_data = self._sprites[entity]
            surface.blit(sprite_data.texture, (sprite_data.position.x - sprite_data.offset.x, sprite_data.position.y - sprite_data.offset.y), sprite_data.bounds)
        
        self._marked.clear()

class SpriteData:
    def __init__(self, texture, bounds, scale, position, layer, offset):
        self.texture = texture
        self.bounds = bounds
        self.scale = scale
        self.position = position
        self.layer = layer
        self.offset = offset