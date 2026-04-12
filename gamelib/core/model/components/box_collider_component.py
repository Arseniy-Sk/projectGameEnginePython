from gamelib.core.model.components.image_for_base_gameObj import Component
from gamelib.core.model.events.events_system import global_bus


class Box_collider(Component):
    def __init__(self, is_trigger: bool):
        super().__init__()
        self.is_trigger = is_trigger
        self.obj2 = None
        self.function = None
        self._checking = False
    
    def set_game_object(self, obj):
        super().set_game_object(obj)
    
    def check_collision(self, obj2, function=None):
        self.obj2 = obj2
        self.function = function
        
        if not self.obj or not self.obj.canvas:
            return
        
        if not self._checking:
            self._checking = True
            self._check_collision_loop()
    
    def _check_collision_loop(self):
        if not self._checking or not self.obj or not self.obj2 or not self.obj.canvas:
            self._checking = False
            return
        
        coords1 = self._get_coordinates(self.obj)
        coords2 = self._get_coordinates(self.obj2)
        
        if coords1 and coords2 and self._is_colliding(coords1, coords2):
            self._handle_collision()
        
        if self.obj and self.obj.canvas:
            self.obj.canvas.after(100, self._check_collision_loop)
    
    def _get_coordinates(self, obj):
        if hasattr(obj, 'get_coordinates'):
            return obj.get_coordinates()
        return None
    
    def _is_colliding(self, rect1, rect2):
        return (rect1[0] < rect2[2] and rect1[2] > rect2[0] and
                rect1[1] < rect2[3] and rect1[3] > rect2[1])
    
    def _handle_collision(self):
        global_bus.emit(self.obj, 'collision_enter', {
            'other': self.obj2,
            'is_trigger': self.is_trigger
        })
        
        if not self.is_trigger:
            self._stop_gravity_on_target()
        elif self.function:
            self.function()
    
    def _stop_gravity_on_target(self):
        if not hasattr(self.obj2, 'components'):
            return
        
        for component in self.obj2.components:
            if hasattr(component, 'stop_gravity'):
                component.stop_gravity()
                break
    
    def stop_checking(self):
        self._checking = False
        self.obj2 = None
        self.function = None