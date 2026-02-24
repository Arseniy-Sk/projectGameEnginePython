from gamelib.core.model.render.render_scene_obj import *
from gamelib.core.model.vectors.verctor2 import *
from gamelib.core.model.events.events_system import global_bus
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

    # Испускаем событие начала импульса
    if isinstance(angle_or_vector, Vector2):
        global_bus.emit(obj, 'impulse_started', {
            'force': force,
            'vector': angle_or_vector.normalized()
        })
    else:
        global_bus.emit(obj, 'impulse_started', {
            'force': force,
            'angle': angle_or_vector
        })

    start_pos = obj.get_position()

    if isinstance(angle_or_vector, Vector2):
        vector = angle_or_vector.normalized()
        distance = force * 10 / max(1, mass)
        speed = max(10, min(50, 100 - force))
        steps = 20
        step_dx = (vector.x * distance) / steps
        step_dy = (vector.y * distance) / steps
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
                global_bus.emit(obj, 'impulse_finished', {
                    'force': force,
                    'vector': vector
                })
                return False, None

        return apply_impulse_step
    else:
        angle = angle_or_vector
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
                global_bus.emit(obj, 'impulse_finished', {
                    'force': force,
                    'angle': angle
                })
                return False, None

        return apply_impulse_step