
from game.component import Element, Transform
from game.ecs import System

class UiSystem(System):    
    def update(self, dt):
        for entity, [element, transform] in self.world.get_components(Element, Transform):
            transform.fixed = True

            if element.parent != None:
                pelement = self.world.component_for_entity(element.parent, Element)
                transform.position.x = pelement.position.x + element.position.x
                transform.position.y = pelement.position.y + element.position.y
            else:
                transform.position.x = element.position.x
                transform.position.y = element.position.y