from gamelib.core.model.render.render_scene_obj import *
from gamelib.core.model.scenes.scene import *
from gamelib.core.model.events.events_system import global_bus


class GameObject():
    def __init__(self, x=0, y=0, width=50, height=50, canvas=None, scene=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas = canvas
        self.scene = scene
        self.components = []
        self.rect_id = None

    def add_component(self, component):
        if hasattr(component, 'set_game_object'):
            component.set_game_object(self)
        self.components.append(component)
        return self

    def get_coordinates(self):
        return [self.x, self.y, self.x + self.width, self.y + self.height]
    
    def get_position(self):
        return [self.x, self.y]
    
    def get_size(self):
        return [self.width, self.height]
    
    def get_center(self):
        return [self.x + self.width / 2, self.y + self.height / 2]

    def update_position(self, new_x, new_y):
        dx = new_x - self.x
        dy = new_y - self.y
        old_pos = (self.x, self.y)
        
        self.x = new_x
        self.y = new_y
        
        if self.rect_id and self.canvas:
            self.canvas.move(self.rect_id, dx, dy)
        
        for component in self.components:
            if hasattr(component, 'update_position'):
                component.update_position(dx, dy)

        global_bus.emit(self, 'position_changed', {
            'old': old_pos,
            'new': (new_x, new_y),
            'dx': dx,
            'dy': dy
        })

    def AddListener(self):
        pass


class gameObject():
    class Rectangle(GameObject):
        def __init__(self, canvas, x=0, y=0, width=50, height=50, color="red", scene=None):
            super().__init__(x, y, width, height, canvas, scene)
            self.color = color
            
            self.rect_id = canvas.create_rectangle(
                self.x, self.y, self.x + self.width, self.y + self.height, 
                fill=color, outline=color
            )

            if scene:
                scene.add_game_obj(self)