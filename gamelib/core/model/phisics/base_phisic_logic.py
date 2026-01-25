from gamelib.core.model.render.render_scene_obj import *

def set_position(canvas, obj, dx, dy):
    render_set_position(canvas, obj, dx, dy)


def falling(obj, mass):
    current_pos = obj.get_position()
    obj.update_position(current_pos[0], current_pos[1] + (mass / 2))


# def impulse(obj, force, vector, mass):
#         coords = obj.get_position()
#         obj.update_position(coords[0]+force / mass, coords[1]+force / mass)




import math

def calculate_impulse_toward_object(source_pos, target_pos, mass, speed):
    """
    Вычисляет импульс (и вектор направления), направленный от источника к цели
    
    Parameters:
    -----------
    source_pos : tuple/list
        Позиция источника (x, y[, z]) в системе координат
    target_pos : tuple/list
        Позиция цели (x, y[, z]) в системе координат
    mass : float
        Масса объекта
    speed : float
        Желаемая скорость/величина импульса
    
    Returns:
    --------
    tuple: (impulse_vector, impulse_magnitude, direction_vector)
        impulse_vector - вектор импульса с компонентами
        impulse_magnitude - величина импульса
        direction_vector - единичный вектор направления
    """
    
    # Преобразуем в numpy-подобные массивы для удобства вычислений
    src = list(source_pos)
    tgt = list(target_pos)
    
    # Проверяем совпадение размерностей
    if len(src) != len(tgt):
        raise ValueError("Размерности позиций источника и цели должны совпадать")
    
    # Вычисляем вектор направления от источника к цели
    direction = [tgt[i] - src[i] for i in range(len(src))]
    
    # Вычисляем расстояние до цели
    distance = math.sqrt(sum(d**2 for d in direction))
    
    # Нормализуем вектор направления (делаем единичным)
    if distance > 0:
        direction_unit = [d / distance for d in direction]
    else:
        # Если источник и цель в одной точке, импульс не имеет направления
        direction_unit = [0] * len(src)
    
    # Вычисляем вектор импульса
    impulse_vector = [mass * speed * du for du in direction_unit]
    
    # Вычисляем величину импульса
    impulse_magnitude = mass * speed
    
    return impulse_vector, impulse_magnitude, direction_unit


def apply_impulse_to_object(obj_position, impulse_vector, obj_mass=None, dt=1.0):
    """
    Применяет импульс к объекту и обновляет его скорость/позицию
    
    Parameters:
    -----------
    obj_position : list/tuple
        Текущая позиция объекта
    impulse_vector : list/tuple
        Вектор импульса
    obj_mass : float, optional
        Масса объекта (если None, возвращается только изменение скорости)
    dt : float
        Шаг времени
    
    Returns:
    --------
    tuple: (new_velocity, new_position)
        new_velocity - новая скорость объекта
        new_position - новая позиция объекта
    """
    
    pos = list(obj_position)
    impulse = list(impulse_vector)
    
    # Вычисляем изменение скорости
    if obj_mass is not None and obj_mass > 0:
        delta_v = [imp / obj_mass for imp in impulse]
    else:
        delta_v = impulse  # Если масса не указана, считаем импульс как изменение скорости
    
    # Вычисляем новую позицию (простая интеграция)
    new_position = [pos[i] + delta_v[i] * dt for i in range(len(pos))]
    
    return delta_v, new_position


# Пример использования:
if __name__ == "__main__":
    # Позиция источника (игрока/пушки)
    player_pos = (0, 0)
    # Позиция цели
    enemy_pos = (10, 5)
    # Масса снаряда
    bullet_mass = 0.5
    # Желаемая скорость
    bullet_speed = 20.0
    
    # Вычисляем импульс, направленный к врагу
    impulse_vec, impulse_mag, direction = calculate_impulse_toward_object(
        player_pos, enemy_pos, bullet_mass, bullet_speed
    )
    
    print(f"Направление к цели: {direction}")
    print(f"Вектор импульса: {impulse_vec}")
    print(f"Величина импульса: {impulse_mag:.2f} кг·м/с")
    
    # Применяем импульс к снаряду
    bullet_pos = player_pos
    delta_v, new_pos = apply_impulse_to_object(
        bullet_pos, impulse_vec, bullet_mass
    )
    
    print(f"\nСнаряд получил скорость: {delta_v}")
    print(f"Новая позиция снаряда: {new_pos}")