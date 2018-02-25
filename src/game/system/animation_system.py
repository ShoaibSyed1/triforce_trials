import pygame

from game.component import AnimationSets, Sprite
from game.ecs import System

class AnimationSystem(System):
    def update(self, dt):
        for entity, [animation_sets, sprite] in self.world.get_components(AnimationSets, Sprite):
            if animation_sets.current != None:
                current_set = animation_sets.sets[animation_sets.current]
                sprite.delay = current_set.delay
                sprite.start = current_set.start
                sprite.end = current_set.end
                if sprite.current_frame >= sprite.end or sprite.current_frame < sprite.start:
                    sprite.current_frame = sprite.start
            if animation_sets.last != animation_sets.current:
                sprite.change = True
                animation_sets.last = animation_sets.current

        for entity, [sprite] in self.world.get_components(Sprite):
            if sprite.has_animation:
                sprite.delay_counter += dt
                if sprite.delay_counter >= sprite.delay or sprite.change:
                    sprite.change = False

                    sprite.delay_counter = 0

                    sprite.current_frame += 1
                    if sprite.current_frame >= sprite.end or sprite.current_frame >= sprite.max_frames or sprite.current_frame < sprite.start:
                        sprite.current_frame = sprite.start
                    
                    frame_x = sprite.current_frame
                    frame_y = 0
                    while frame_x >= sprite.frames_x:
                        frame_x -= sprite.frames_x
                        frame_y += 1
                    
                    frame_x *= sprite.frame_width
                    frame_y *= sprite.frame_height

                    sprite.bounds = pygame.Rect(frame_x, frame_y, sprite.frame_width, sprite.frame_height)