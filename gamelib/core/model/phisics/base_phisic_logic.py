from gamelib.core.model.render.render_scene_obj import render_set_position
from gamelib.core.model.vectors.verctor2 import Vector2
from gamelib.core.model.events.events_system import global_bus
import math


def set_position(canvas, obj, dx, dy):
    render_set_position(canvas, obj, dx, dy)


def falling(obj, mass):
    if not obj:
        return
    current_pos = obj.get_position()
    obj.update_position(current_pos[0], current_pos[1] + mass / 2)


def impulse(obj, force, angle_or_vector, mass, on_complete=None):
    if not obj:
        return None
    
    start_pos = obj.get_position()
    is_vector = isinstance(angle_or_vector, Vector2)
    
    # Определяем параметры движения
    if is_vector:
        vector = angle_or_vector.normalized()
        distance = force * 10 / max(1, mass)
        dx_total = vector.x * distance
        dy_total = vector.y * distance
        finish_data = {'force': force, 'vector': vector}
    else:
        angle_rad = math.radians(angle_or_vector)
        distance = force * 10 / max(1, mass)
        dx_total = distance * math.sin(angle_rad)
        dy_total = distance * math.cos(angle_rad)
        finish_data = {'force': force, 'angle': angle_or_vector}
    
    # Испускаем событие начала
    global_bus.emit(obj, 'impulse_started', finish_data)
    
    # Параметры анимации
    steps = 20
    speed = max(10, min(50, 100 - force))
    step_dx = dx_total / steps
    step_dy = dy_total / steps
    current_step = 0
    
    def apply_impulse_step():
        nonlocal current_step
        if current_step >= steps:
            if on_complete:
                on_complete()
            global_bus.emit(obj, 'impulse_finished', finish_data)
            return False, None
        
        new_x = start_pos[0] + step_dx * (current_step + 1)
        new_y = start_pos[1] + step_dy * (current_step + 1)
        obj.update_position(new_x, new_y)
        current_step += 1
        return True, speed
    
    return apply_impulse_step