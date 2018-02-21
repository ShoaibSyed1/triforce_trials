class Component: pass

class System:
    def __init__(self):
        self.world = None
        self._priority = 0
        self._started = False
    
    def start(self): pass
    
    def update(self, dt): pass

class World:
    def __init__(self):
        self._systems = []
        self._components = {}
        self._next_id = 0
        self._remove = []
        self._entities = []
        self._close_listeners = {}
    
    def create_entity(self):
        entity_id = self._next_id
        self._next_id += 1

        self._entities.append(entity_id)

        return entity_id
    
    def create_entity_with(self, *components):
        entity = self.create_entity()

        for component in components:
            self.add_component(entity, component)
        
        return entity
    
    def add_component(self, entity, component):
        if not type(component) in self._components.keys():
            self._components[type(component)] = {}
        
        self._components[type(component)][entity] = component
    
    def remove_component(self, entity, component):
        if not type(component) in self._components.keys():
            return False

        if entity in self._components[type(component)].keys():
            del self._components[type(component)][entity]
            return True
        
        return False
    
    def delete_entity(self, entity):
        if entity in self._close_listeners.keys():
            for cb in self._close_listeners[entity]:
                cb()
        
        self._remove.append(entity)
    
    def add_system(self, system, priority=0):
        if not system in self._systems:
            self._systems.append(system)
            system.world = self
            system._priority = priority
            system._started = False

            self._systems.sort(key=lambda x: x._priority, reverse=True)
    
    def get_system(self, system_type):
        for system in self._systems:
            if type(system) == system_type:
                return system
        
        return None
    
    def update(self, dt):
        for system in self._systems:
            if not system._started:
                system.start()
                system._started = True
            
            system.update(dt)
        
        for entity in self._remove:
            if entity in self._entities:
                self._entities.remove(entity)
            for comp_dict in self._components.values():
                if entity in comp_dict.keys():
                    del comp_dict[entity]
        
        self._remove.clear()
    
    def has_component(self, entity, component_type):
        return entity in self._components[component_type].keys()

    def component_for_entity(self, entity, component_type):
        return self._components[component_type].get(entity, None)

    def components_for_entity(self, entity):
        return map(lambda x: x[entity], filter(lambda x: entity in x.keys(), self._components.values()))
    
    def get_components(self, *component_types):
        entities = []
        for entity in self._entities:
            entities.append(entity)
        
        for component_type in component_types:
            if not component_type in self._components.keys():
                return None
            else:
                comp_entities = self._components[component_type].keys()

                remove = []
                for entity in entities:
                    if not entity in comp_entities:
                        remove.append(entity)
                
                for entity in remove:
                    entities.remove(entity)
        
        for entity in entities:
            yield entity, [self.component_for_entity(entity, ct) for ct in component_types]
    
    def get_all_entities(self):
        return self._entities
    
    def clear_entities(self):
        for cb_list in self._close_listeners.values():
            for cb in cb_list:
                cb()
        
        self._components = {}
        self._next_id = 0
        self._remove = []
        self._entities = []
    
    def add_close_listener(self, entity, listener):
        if not entity in self._close_listeners.keys():
            self._close_listeners[entity] = []
        
        self._close_listeners[entity].append(listener)