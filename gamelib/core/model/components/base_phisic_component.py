from gamelib.core.model.components.image_for_base_gameObj import Component
from gamelib.core.model.phisics.base_phisic_logic import *
from gamelib.core.model.vectors.verctor2 import *

class BasePhisicComponent(Component):
    def __init__(self, mass, gravity=False):
        super().__init__()
        self.mass = mass
        self.is_gravity_active = False
        self.gravity_task_id = None
        self.current_impulse_task = None  # Для отслеживания текущего импульса
        
        # Автоматически включаем гравитацию если указано
        self.auto_gravity = gravity

    def set_game_object(self, obj):
        """Устанавливает ссылку на игровой объект"""
        super().set_game_object(obj)
        # Автоматически включаем гравитацию после привязки к объекту
        if self.auto_gravity and self.obj and self.obj.canvas and hasattr(self.obj, 'scene'):
            self.add_physic_enum()

    def set_position(self, dx, dy):
        """Перемещает объект на указанное смещение"""
        if self.obj and hasattr(self.obj, 'update_position'):
            # Get Current Position
            current_pos = self.obj.get_position()
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            
            # Update GameObject position
            self.obj.update_position(new_x, new_y)

    def move_by_vector(self, vector, distance=None):
        """
        Перемещает объект по вектору.
        
        Args:
            vector: Vector2 - вектор направления
            distance: float - расстояние для перемещения (если None, использует длину вектора)
        """
        if not isinstance(vector, Vector2):
            raise TypeError("vector должен быть объектом Vector2")
        
        # Если указано расстояние, нормализуем вектор и умножаем на расстояние
        if distance is not None:
            normalized = vector.normalized()
            dx = normalized.x * distance
            dy = normalized.y * distance
        else:
            # Используем сам вектор как смещение
            dx = vector.x
            dy = vector.y
        
        self.set_position(dx, dy)

    def add_physic_enum(self):
        """Добавляет физическое поведение (гравитацию)"""
        if not self.obj or not self.obj.canvas:
            print("Error: Cannot add physics - object has no canvas")
            return
        
        self.is_gravity_active = True
        
        def apply_gravity():
            if not self.is_gravity_active:
                return
            # Apply Gravitation
            falling(self.obj, self.mass)
            # Plan the next cadr
            if self.is_gravity_active and self.obj and self.obj.canvas:
                self.gravity_task_id = self.obj.canvas.after(100, apply_gravity)
        
        apply_gravity()

    def stop_gravity(self):
        """Останавливает гравитацию"""
        self.is_gravity_active = False
        if self.gravity_task_id and self.obj and self.obj.canvas:
            self.obj.canvas.after_cancel(self.gravity_task_id)
            self.gravity_task_id = None
        print("Gravity stopped")
    
    def stop_impulse(self):
        """Останавливает текущий импульс"""
        if self.current_impulse_task and self.obj and self.obj.canvas:
            self.obj.canvas.after_cancel(self.current_impulse_task)
            self.current_impulse_task = None
            print("Impulse stopped")
    
    def impulse(self, force, vector, on_complete=None):
        """
        Применяет импульс к объекту плавно
        
        Args:
            force: float - сила импульса (влияет на расстояние и скорость)
            vector: Vector2 или угол - направление импульса
            on_complete: function - функция, вызываемая по завершении импульса
        """
        if not self.obj or not self.obj.canvas:
            print("Error: Cannot apply impulse - object has no canvas")
            return
        
        # Останавливаем предыдущий импульс, если он есть
        if self.current_impulse_task:
            self.stop_impulse()
        
        # Получаем функцию для шага импульса
        impulse_step_func = impulse(self.obj, force, vector, self.mass, on_complete)
        
        def apply_impulse():
            """Рекурсивно применяет импульс шаг за шагом"""
            has_next, delay = impulse_step_func()
            
            if has_next and delay:
                # Планируем следующий шаг с заданной задержкой
                self.current_impulse_task = self.obj.canvas.after(delay, apply_impulse)
            else:
                # Импульс завершен
                self.current_impulse_task = None
        
        # Запускаем импульс
        apply_impulse()