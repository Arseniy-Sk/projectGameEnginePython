from gamelib.core.model.components.image_for_base_gameObj import Component
from gamelib.core.model.phisics.base_phisic_logic import *
from gamelib.core.model.vectors.verctor2 import *
from gamelib.core.model.events.events_system import global_bus

class BasePhisicComponent(Component):
    def __init__(self, mass, gravity=False):
        super().__init__()
        self.mass = mass
        self.is_gravity_active = False
        self.gravity_task_id = None
        self.current_impulse_task = None
        self.auto_gravity = gravity

    def set_game_object(self, obj):
        super().set_game_object(obj)
        if self.auto_gravity and self.obj and self.obj.canvas and hasattr(self.obj, 'scene'):
            self.add_physic_enum()

    def set_position(self, dx, dy):
        if self.obj and hasattr(self.obj, 'update_position'):
            current_pos = self.obj.get_position()
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            self.obj.update_position(new_x, new_y)

    def move_by_vector(self, vector, distance=None):
        if not isinstance(vector, Vector2):
            raise TypeError("vector должен быть объектом Vector2")
        if distance is not None:
            normalized = vector.normalized()
            dx = normalized.x * distance
            dy = normalized.y * distance
        else:
            dx = vector.x
            dy = vector.y
        self.set_position(dx, dy)

    def add_physic_enum(self):
        if not self.obj or not self.obj.canvas:
            print("Error: Cannot add physics - object has no canvas")
            return
        
        self.is_gravity_active = True
        # Генерируем событие
        global_bus.emit('gravity_started', self, {'mass': self.mass})
        
        def apply_gravity():
            if not self.is_gravity_active:
                return
            falling(self.obj, self.mass)
            if self.is_gravity_active and self.obj and self.obj.canvas:
                self.gravity_task_id = self.obj.canvas.after(100, apply_gravity)
        
        apply_gravity()

    def stop_gravity(self):
        self.is_gravity_active = False
        if self.gravity_task_id and self.obj and self.obj.canvas:
            self.obj.canvas.after_cancel(self.gravity_task_id)
            self.gravity_task_id = None
        # Генерируем событие
        global_bus.emit('gravity_stopped', self, {'mass': self.mass})
        print("Gravity stopped")
    
    def stop_impulse(self):
        if self.current_impulse_task and self.obj and self.obj.canvas:
            self.obj.canvas.after_cancel(self.current_impulse_task)
            self.current_impulse_task = None
            print("Impulse stopped")
    
    def impulse(self, force, vector, on_complete=None):
        if not self.obj or not self.obj.canvas:
            print("Error: Cannot apply impulse - object has no canvas")
            return
        
        if self.current_impulse_task:
            self.stop_impulse()
        
        # Генерируем событие начала импульса
        global_bus.emit('impulse_started', self, {'force': force, 'vector': vector})
        
        impulse_step_func = impulse(self.obj, force, vector, self.mass, on_complete)
        
        def apply_impulse():
            has_next, delay = impulse_step_func()
            if has_next and delay:
                self.current_impulse_task = self.obj.canvas.after(delay, apply_impulse)
            else:
                self.current_impulse_task = None
                # Генерируем событие завершения (оно также генерируется внутри impulse, но продублируем для надёжности)
                global_bus.emit('impulse_finished', self, {'force': force, 'vector': vector})
        
        apply_impulse()