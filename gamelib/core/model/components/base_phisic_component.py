from gamelib.core.model.components.image_for_base_gameObj import Component
from gamelib.core.model.phisics.base_phisic_logic import *

class BasePhisicComponent(Component):
    def __init__(self, canvas, obj, mass):
        super().__init__(obj)
        self.canvas = canvas
        self.mass = mass
        self.is_gravity_active = False
        self.gravity_task_id = None

        if hasattr(obj, 'add_component'):
            obj.add_component(self)


    def set_position(self, dx, dy):
        """Перемещает объект на указанное смещение"""
        if hasattr(self.obj, 'update_position'):
            # Get Current Position
            current_pos = self.obj.get_position()
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            
            # Update GameObject position
            self.obj.update_position(new_x, new_y)


    def add_physic_enum(self, root):
            """Добавляет физическое поведение"""
            self.is_gravity_active = True
            
            def apply_gravity():
                if not self.is_gravity_active:
                    return
                # Apply Gravitation
                falling(self.obj, self.mass)
                # Plan the next cadr
                if self.is_gravity_active:
                    self.gravity_task_id = root.after(100, apply_gravity)
            
            apply_gravity()


    def stop_gravity(self):
            """Останавливает гравитацию"""
            self.is_gravity_active = False
            if self.gravity_task_id:
                self.canvas.after_cancel(self.gravity_task_id)
                self.gravity_task_id = None
            print("Gravity stopped")