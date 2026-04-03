# gamelib/core/model/camera/camera.py
from gamelib.core.model.events.events_system import global_bus
from gamelib.core.model.vectors.verctor2 import Vector2
import math
import random  # Добавляем импорт random

class Camera2D:
    """
    2D камера как в Unity.
    Поддерживает следование за объектом, зум, границы, шейк и плавное движение.
    """
    
    def __init__(self, scene, width, height):
        """
        Инициализация камеры.
        
        :param scene: сцена, к которой привязана камера
        :param width: ширина области просмотра камеры
        :param height: высота области просмотра камеры
        """
        self.scene = scene
        self.canvas = scene.canvas
        self.width = width
        self.height = height
        
        # Позиция камеры (центр камеры в мировых координатах)
        self.position = Vector2(width // 2, height // 2)
        
        # Целевая позиция для плавного следования
        self.target_position = None
        
        # Слежение за объектом
        self.follow_target = None
        self.follow_offset = Vector2(0, 0)
        self.follow_smooth_speed = 5.0  # Скорость плавного следования
        self.follow_deadzone = Vector2(0, 0)  # Мертвая зона
        
        # Зум
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.zoom_smooth_speed = 4.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        
        # Границы камеры
        self.bounds_enabled = False
        self.bounds_left = 0
        self.bounds_right = 0
        self.bounds_top = 0
        self.bounds_bottom = 0
        
        # Эффекты
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_timer = 0
        self.shake_offset = Vector2(0, 0)
        
        # Плавное движение
        self.smooth_movement_enabled = False
        self.smooth_speed = 8.0
        
        # Смещение камеры (ручное)
        self.offset = Vector2(0, 0)
        
        # Сохраняем исходные координаты всех объектов на сцене
        self.objects_original_positions = {}
        
        # События камеры
        global_bus.subscribe(None, 'camera_shake_started', self._on_shake_started)
        global_bus.subscribe(None, 'camera_zoom_changed', self._on_zoom_changed)
    
    def update(self, delta_time=1/60):
        """
        Обновление камеры. Вызывать каждый кадр.
        
        :param delta_time: время между кадрами
        """
        # Обновляем слежение за объектом
        if self.follow_target:
            self._update_following(delta_time)
        
        # Обновляем зум
        if self.target_zoom != self.zoom:
            diff = self.target_zoom - self.zoom
            self.zoom += diff * min(1.0, self.zoom_smooth_speed * delta_time)
            if abs(self.target_zoom - self.zoom) < 0.01:
                self.zoom = self.target_zoom
        
        # Обновляем эффект шейка
        if self.shake_timer > 0:
            self._update_shake(delta_time)
        
        # Применяем позицию камеры
        self._apply_camera_transform()
    
    def _update_following(self, delta_time):
        """Обновление слежения за объектом"""
        if not self.follow_target:
            return
        
        # Получаем позицию цели
        if hasattr(self.follow_target, 'get_center'):
            center = self.follow_target.get_center()
            target_pos = Vector2(center[0], center[1])
        elif hasattr(self.follow_target, 'get_position'):
            pos = self.follow_target.get_position()
            target_pos = Vector2(pos[0] + self.follow_target.width // 2, 
                                pos[1] + self.follow_target.height // 2)
        else:
            target_pos = Vector2(self.follow_target.x, self.follow_target.y)
        
        target_pos = target_pos + self.follow_offset
        
        # Если есть мертвая зона
        if self.follow_deadzone.x > 0 or self.follow_deadzone.y > 0:
            current_target = self.target_position if self.target_position else self.position
            diff = target_pos - current_target
            if abs(diff.x) <= self.follow_deadzone.x and abs(diff.y) <= self.follow_deadzone.y:
                return
        
        if self.smooth_movement_enabled:
            # Плавное движение
            if self.target_position is None:
                self.target_position = target_pos
            else:
                diff = target_pos - self.target_position
                self.target_position = self.target_position + diff * min(1.0, self.follow_smooth_speed * delta_time)
            
            # Обновляем позицию камеры
            diff_pos = self.target_position - self.position
            self.position = self.position + diff_pos * min(1.0, self.smooth_speed * delta_time)
        else:
            # Мгновенное движение
            self.target_position = target_pos
            self.position = target_pos
        
        # Применяем границы
        self._apply_bounds()
    
    def _apply_bounds(self):
        """Применение границ камеры"""
        if not self.bounds_enabled:
            return
        
        half_width = self.width / (2 * self.zoom)
        half_height = self.height / (2 * self.zoom)
        
        if self.position.x - half_width < self.bounds_left:
            self.position.x = self.bounds_left + half_width
        if self.position.x + half_width > self.bounds_right:
            self.position.x = self.bounds_right - half_width
        if self.position.y - half_height < self.bounds_top:
            self.position.y = self.bounds_top + half_height
        if self.position.y + half_height > self.bounds_bottom:
            self.position.y = self.bounds_bottom - half_height
        
        if self.target_position:
            self.target_position = self.position
    
    def _update_shake(self, delta_time):
        """Обновление эффекта шейка"""
        self.shake_timer -= delta_time
        
        if self.shake_timer > 0:
            intensity = self.shake_intensity * (self.shake_timer / self.shake_duration)
            self.shake_offset = Vector2(
                (random.random() - 0.5) * 2 * intensity,
                (random.random() - 0.5) * 2 * intensity
            )
        else:
            self.shake_offset = Vector2(0, 0)
            self.shake_intensity = 0
            global_bus.emit(self, 'camera_shake_finished', {})
    
    def _apply_camera_transform(self):
        """Применение трансформации камеры ко всем объектам на сцене"""
        if not self.canvas:
            return
        
        # Вычисляем смещение камеры
        screen_center = Vector2(self.width // 2, self.height // 2)
        camera_offset = screen_center - (self.position + self.offset + self.shake_offset)
        
        # Применяем смещение ко всем объектам на сцене
        for obj in self.scene.gameObj_list:
            if hasattr(obj, 'rect_id') and obj.rect_id:
                # Сохраняем оригинальную позицию если нужно
                if obj not in self.objects_original_positions:
                    self.objects_original_positions[obj] = Vector2(obj.x, obj.y)
                
                # Вычисляем новую позицию
                original_pos = self.objects_original_positions[obj]
                new_x = original_pos.x + camera_offset.x
                new_y = original_pos.y + camera_offset.y
                
                # Обновляем позицию прямоугольника
                coords = [new_x, new_y, new_x + obj.width, new_y + obj.height]
                self.canvas.coords(obj.rect_id, *coords)
    
    def set_follow_target(self, target, offset=(0, 0), smooth=True, smooth_speed=5.0):
        """
        Установить объект для слежения.
        
        :param target: объект за которым следит камера
        :param offset: смещение от центра объекта
        :param smooth: плавное ли движение
        :param smooth_speed: скорость плавного движения
        """
        self.follow_target = target
        self.follow_offset = Vector2(offset[0], offset[1])
        self.smooth_movement_enabled = smooth
        self.smooth_speed = smooth_speed
        
        # Инициализируем позицию
        if target:
            if hasattr(target, 'get_center'):
                center = target.get_center()
                self.position = Vector2(center[0] + offset[0], center[1] + offset[1])
            elif hasattr(target, 'get_position'):
                pos = target.get_position()
                self.position = Vector2(pos[0] + target.width // 2 + offset[0], 
                                       pos[1] + target.height // 2 + offset[1])
            else:
                self.position = Vector2(target.x + offset[0], target.y + offset[1])
            self.target_position = self.position
    
    def set_follow_deadzone(self, width, height):
        """Установить мертвую зону для слежения"""
        self.follow_deadzone = Vector2(width, height)
    
    def set_bounds(self, left, top, right, bottom):
        """
        Установить границы движения камеры.
        
        :param left: левая граница
        :param top: верхняя граница
        :param right: правая граница
        :param bottom: нижняя граница
        """
        self.bounds_enabled = True
        self.bounds_left = left
        self.bounds_top = top
        self.bounds_right = right
        self.bounds_bottom = bottom
    
    def disable_bounds(self):
        """Отключить границы"""
        self.bounds_enabled = False
    
    def set_zoom(self, zoom, smooth=True, smooth_speed=4.0):
        """
        Установить уровень зума.
        
        :param zoom: уровень зума (1.0 = нормальный)
        :param smooth: плавное ли изменение
        :param smooth_speed: скорость изменения
        """
        self.target_zoom = max(self.min_zoom, min(self.max_zoom, zoom))
        self.zoom_smooth_speed = smooth_speed
        
        if not smooth:
            self.zoom = self.target_zoom
        
        global_bus.emit(self, 'camera_zoom_changed', {
            'zoom': self.zoom,
            'target_zoom': self.target_zoom
        })
    
    def add_zoom(self, delta, smooth=True):
        """Добавить к зиму"""
        self.set_zoom(self.zoom + delta, smooth)
    
    def shake(self, intensity, duration):
        """
        Эффект дрожания камеры.
        
        :param intensity: интенсивность дрожания
        :param duration: длительность в секундах
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = duration
        global_bus.emit(self, 'camera_shake_started', {
            'intensity': intensity,
            'duration': duration
        })
    
    def move_to(self, position, smooth=True, speed=8.0):
        """
        Переместить камеру в указанную позицию.
        
        :param position: целевая позиция
        :param smooth: плавное ли перемещение
        :param speed: скорость перемещения
        """
        target = Vector2(position[0], position[1])
        self.target_position = target
        self.smooth_movement_enabled = smooth
        self.smooth_speed = speed
        
        if not smooth:
            self.position = target
    
    def get_world_to_screen(self, world_position):
        """
        Преобразовать мировые координаты в экранные.
        
        :param world_position: позиция в мировых координатах
        :return: позиция в экранных координатах
        """
        screen_center = Vector2(self.width // 2, self.height // 2)
        camera_offset = screen_center - (self.position + self.offset)
        return Vector2(
            world_position[0] + camera_offset.x,
            world_position[1] + camera_offset.y
        )
    
    def get_screen_to_world(self, screen_position):
        """
        Преобразовать экранные координаты в мировые.
        
        :param screen_position: позиция на экране
        :return: позиция в мировых координатах
        """
        screen_center = Vector2(self.width // 2, self.height // 2)
        camera_offset = screen_center - (self.position + self.offset)
        return Vector2(
            screen_position[0] - camera_offset.x,
            screen_position[1] - camera_offset.y
        )
    
    def _on_shake_started(self, event):
        """Обработчик начала шейка"""
        pass
    
    def _on_zoom_changed(self, event):
        """Обработчик изменения зума"""
        pass


class CameraController:
    """
    Контроллер камеры для удобного управления из игрового кода.
    """
    
    def __init__(self, camera):
        self.camera = camera
        self.zoom_speed = 2.0
        self.move_speed = 500.0
    
    def handle_input(self, input_manager, delta_time=1/60):
        """
        Обработка ввода для управления камерой.
        
        :param input_manager: менеджер ввода
        :param delta_time: время между кадрами
        """
        # Управление зумом (Q/E или колесико)
        if input_manager.is_key_down('q'):
            self.camera.add_zoom(-self.zoom_speed * delta_time)
        if input_manager.is_key_down('e'):
            self.camera.add_zoom(self.zoom_speed * delta_time)
        
        # Управление перемещением (WASD)
        move = Vector2(0, 0)
        if input_manager.is_key_down('a'):
            move.x = -self.move_speed * delta_time
        if input_manager.is_key_down('d'):
            move.x = self.move_speed * delta_time
        if input_manager.is_key_down('w'):
            move.y = -self.move_speed * delta_time
        if input_manager.is_key_down('s'):
            move.y = self.move_speed * delta_time
        
        if move.x != 0 or move.y != 0:
            new_pos = self.camera.position + move
            self.camera.move_to((new_pos.x, new_pos.y), smooth=False)
    
    def focus_on_object(self, obj, offset=(0, 0)):
        """Сфокусироваться на объекте"""
        if hasattr(obj, 'get_center'):
            center = obj.get_center()
        elif hasattr(obj, 'get_position'):
            pos = obj.get_position()
            center = (pos[0] + obj.width // 2, pos[1] + obj.height // 2)
        else:
            center = (obj.x, obj.y)
        
        self.camera.move_to((center[0] + offset[0], center[1] + offset[1]), smooth=True)
    
    def reset_zoom(self, smooth=True):
        """Сброс зума"""
        self.camera.set_zoom(1.0, smooth)