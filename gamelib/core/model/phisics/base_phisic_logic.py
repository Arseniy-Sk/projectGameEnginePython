from gamelib.core.model.render.render_scene_obj import *
from gamelib.core.model.vectors.verctor2 import *
import math

def set_position(canvas, obj, dx, dy):
    render_set_position(canvas, obj, dx, dy)

def falling(obj, mass):
    if not obj:
        return
    current_pos = obj.get_position()
    obj.update_position(current_pos[0], current_pos[1] + (mass / 2))

def impulse(obj, force, angle_or_vector, mass, on_complete=None):
    """Применяет импульс к объекту плавно"""
    if not obj:
        return None
        
    start_pos = obj.get_position()
    
    if isinstance(angle_or_vector, Vector2):
        # Новая система: используем вектор
        vector = angle_or_vector.normalized()
        
        # Расстояние зависит от силы и массы
        # Чем больше сила - тем дальше летит объект
        # Чем больше масса - тем меньше эффект
        distance = force * 10 / max(1, mass)
        
        # Скорость анимации зависит от силы (чем больше сила - тем быстрее)
        # Минимальная скорость = 50мс на шаг, максимальная = 10мс на шаг
        speed = max(10, min(50, 100 - force))
        steps = 20  # Фиксированное количество шагов для плавности
        
        # Рассчитываем смещение за каждый шаг
        step_dx = (vector.x * distance) / steps
        step_dy = (vector.y * distance) / steps
        
        # Запускаем плавную анимацию
        current_step = 0
        
        def apply_impulse_step():
            nonlocal current_step
            
            if current_step < steps:
                # Применяем шаг импульса
                current_x = start_pos[0] + step_dx * (current_step + 1)
                current_y = start_pos[1] + step_dy * (current_step + 1)
                obj.update_position(current_x, current_y)
                
                current_step += 1
                # Планируем следующий шаг с учетом скорости
                return True, speed
            else:
                # Импульс завершен
                if on_complete:
                    on_complete()
                return False, None
        
        return apply_impulse_step
    else:
        # Старая система: используем угол (для обратной совместимости)
        angle = angle_or_vector
        
        # Расстояние зависит от силы и массы
        distance = force * 10 / max(1, mass)
        
        angle_rad = math.radians(angle)
        dx_total = distance * math.sin(angle_rad)
        dy_total = distance * math.cos(angle_rad)
        
        speed = max(10, min(50, 100 - force))
        steps = 20
        
        step_dx = dx_total / steps
        step_dy = dy_total / steps
        
        current_step = 0
        
        def apply_impulse_step():
            nonlocal current_step
            
            if current_step < steps:
                current_x = start_pos[0] + step_dx * (current_step + 1)
                current_y = start_pos[1] + step_dy * (current_step + 1)
                obj.update_position(current_x, current_y)
                
                current_step += 1
                return True, speed
            else:
                if on_complete:
                    on_complete()
                return False, None
        
        return apply_impulse_step