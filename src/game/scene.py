import pygame

from game.ecs import World

class Scene:
    def __init__(self, game):
        self.game = game
        self.world = World()
    
    def start(self):
        from game import loader
        from game.system import AnimationSystem, CollisionSystem, EventBusSystem, EventSystem, MusicSystem, RenderSystem, ScriptSystem, UiSystem

        for entity_info in loader.load("scene", "overworld"):
            self.world.create_entity_with(*entity_info)

        self.world.add_system(AnimationSystem(), 1)
        self.world.add_system(CollisionSystem())
        self.world.add_system(EventBusSystem())
        self.world.add_system(EventSystem())
        self.world.add_system(MusicSystem())
        self.world.add_system(RenderSystem(self.game.window))
        self.world.add_system(ScriptSystem())
        self.world.add_system(UiSystem())

    def update(self, dt):
        from game.system import EventSystem
        
        self.world.update(dt)

        if self.world.get_system(EventSystem).should_quit:
            self.game.running = False