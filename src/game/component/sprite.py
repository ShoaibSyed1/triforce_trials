import pygame

from game.ecs import Component

class Sprite(Component):
    def __init__(self, texture, bounds=None, visible=True, offset=pygame.math.Vector2(0, 0)):
        self.texture = texture
        self.bounds = bounds
        self.visible = visible
        
        self._redraw = False

        self.has_animation = False

        self.offset = offset

        self.change = True

        if self.bounds == None:
            self.bounds = pygame.Rect(0, 0, texture.get_width(), texture.get_height())
    
    @staticmethod
    def new_text(text, color, size, fontname=pygame.font.get_default_font()):
        font = pygame.font.Font(fontname, size)
        
        texture = font.render(text, True, color)

        return Sprite(texture)
    
    def with_animation(self, frame_width, frame_height, delay=-1, start=0, end=None):
        self.has_animation = True

        self.frame_width = frame_width
        self.frame_height = frame_height

        self.frames_x = int(self.texture.get_width() / self.frame_width)
        self.frames_y = int(self.texture.get_height() / self.frame_height)

        self.max_frames = self.frames_x * self.frames_y

        self.delay = delay
        self.delay_counter = delay

        self.start = start
        self.end = end

        if self.end == None:
            self.end = self.max_frames
        
        self.current_frame = self.start

        return self
    
    def repeated(self, xtimes, ytimes):
        xtimes = int(xtimes)
        ytimes = int(ytimes)

        new_texture = pygame.Surface((self.bounds.width * xtimes, self.bounds.height * xtimes))
        for y in range(ytimes):
            for x in range(xtimes):
                new_texture.blit(self.texture, (x * self.bounds.width, y * self.bounds.height), self.bounds)
        
        self.__init__(new_texture)

        return self