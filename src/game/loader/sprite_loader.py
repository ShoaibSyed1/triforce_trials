import pygame

from game import paths
from game.component import Sprite
from game.loader.loader import Loader

class SpriteLoader(Loader):
    @staticmethod
    def load(data, path):
        if 'text' in data.keys():
            text = data['text']
            text_val = text['text']
            color = text['color']
            size = text['size']
            fontname = text.get('font', pygame.font.get_default_font())

            return Sprite.new_text(text_val, color, size, fontname)
        
        image_path = paths.IMAGES + data['image'] + ".png"
        texture = pygame.image.load(image_path)

        bounds = data.get('bounds', None)
        if bounds != None:
            bounds = pygame.Rect(bounds[0], bounds[1], bounds[2], bounds[3])
        
        visible = data.get('visible', True)

        offset = pygame.math.Vector2(data.get('offset', [0, 0])[0], data.get('offset', [0, 0])[1])
        
        sprite = Sprite(texture, bounds, visible, offset)

        if 'animation' in data.keys():
            animation = data['animation']
            frame_width = animation['frame_width']
            frame_height = animation['frame_height']
            delay = animation.get('delay', -1)
            start = animation.get('start', 0)
            end = animation.get('end', None)

            sprite.with_animation(frame_width, frame_height, delay, start, end)

        return sprite

    @staticmethod
    def get_full_path(part_path):
        return paths.SPRITES + part_path