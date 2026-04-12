# gamelib/core/model/camera/camera.py
import math
import random
from gamelib.core.model.events.events_system import global_bus
from gamelib.core.model.vectors.verctor2 import Vector2


class Camera2D:
    """2D камера"""
    
    def __init__(self, scene, width, height):
        self.scene = scene
        self.canvas = scene.canvas
        self.width = width
        self.height = height
        
        self.position = Vector2(width // 2, height // 2)
        
        self.follow_target = None
        self.follow_offset = Vector2(0, 0)
        self.follow_smoothness = 0.1
        
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.zoom_speed = 2.0
        self.min_zoom = 0.25
        self.max_zoom = 4.0
        
        self.bounds = None
        
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_timer = 0
        self.shake_offset = Vector2(0, 0)
        
        self._half_w = width / 2
        self._half_h = height / 2
        self._original_positions = {}
    
    def update(self, delta_time=1/60):
        self._update_following()
        self._update_zoom(delta_time)
        self._update_shake(delta_time)
        self._apply_transform()
    
    def _update_following(self):
        if not self.follow_target:
            return
        
        target_pos = self._get_target_position()
        target_pos += self.follow_offset
        
        self.position += (target_pos - self.position) * self.follow_smoothness
        self._apply_bounds()
    
    def _get_target_position(self):
        target = self.follow_target
        if hasattr(target, 'get_center'):
            center = target.get_center()
            return Vector2(center[0], center[1])
        elif hasattr(target, 'get_position'):
            pos = target.get_position()
            return Vector2(pos[0] + target.width // 2, pos[1] + target.height // 2)
        return Vector2(target.x, target.y)
    
    def _apply_bounds(self):
        if not self.bounds:
            return
        
        left, top, right, bottom = self.bounds
        half_w = self._half_w / self.zoom
        half_h = self._half_h / self.zoom
        
        self.position.x = max(left + half_w, min(right - half_w, self.position.x))
        self.position.y = max(top + half_h, min(bottom - half_h, self.position.y))
    
    def _update_zoom(self, delta_time):
        if self.target_zoom == self.zoom:
            return
        
        diff = self.target_zoom - self.zoom
        step = diff * min(1.0, self.zoom_speed * delta_time * 10)
        self.zoom += step
        
        if abs(self.target_zoom - self.zoom) < 0.01:
            self.zoom = self.target_zoom
    
    def _update_shake(self, delta_time):
        if self.shake_timer <= 0:
            if self.shake_offset.x != 0:
                self.shake_offset = Vector2(0, 0)
            return
        
        self.shake_timer -= delta_time
        
        if self.shake_timer > 0:
            intensity = self.shake_intensity * (self.shake_timer / self.shake_duration)
            self.shake_offset = Vector2(
                (random.random() - 0.5) * intensity * 2,
                (random.random() - 0.5) * intensity * 2
            )
        else:
            self.shake_offset = Vector2(0, 0)
            self.shake_intensity = 0
    
    def _apply_transform(self):
        if not self.canvas:
            return
        
        screen_center = Vector2(self._half_w, self._half_h)
        camera_offset = screen_center - (self.position + self.shake_offset)
        
        for obj in self.scene.gameObj_list:
            if not hasattr(obj, 'rect_id') or not obj.rect_id:
                continue
            
            if obj not in self._original_positions:
                self._original_positions[obj] = Vector2(obj.x, obj.y)
            
            original = self._original_positions[obj]
            self.canvas.coords(
                obj.rect_id,
                original.x + camera_offset.x,
                original.y + camera_offset.y,
                original.x + camera_offset.x + obj.width,
                original.y + camera_offset.y + obj.height
            )
            
            for comp in obj.components:
                if hasattr(comp, 'update_position'):
                    comp.update_position(camera_offset.x, camera_offset.y)
    
    def follow(self, target, offset=(0, 0), smoothness=0.1):
        self.follow_target = target
        self.follow_offset = Vector2(offset[0], offset[1])
        self.follow_smoothness = smoothness
    
    def stop_follow(self):
        self.follow_target = None
    
    def set_zoom(self, zoom, instant=False):
        self.target_zoom = max(self.min_zoom, min(self.max_zoom, zoom))
        if instant:
            self.zoom = self.target_zoom
    
    def zoom_in(self, delta=0.2):
        self.set_zoom(self.zoom + delta)
    
    def zoom_out(self, delta=0.2):
        self.set_zoom(self.zoom - delta)
    
    def set_bounds(self, left, top, right, bottom):
        self.bounds = (left, top, right, bottom)
    
    def remove_bounds(self):
        self.bounds = None
    
    def shake(self, intensity=10, duration=0.3):
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = duration
        global_bus.emit(self, 'camera_shake', {'intensity': intensity, 'duration': duration})
    
    def move_to(self, position, instant=False):
        target = Vector2(position[0], position[1])
        if instant:
            self.position = target
        else:
            self.position += (target - self.position) * 0.1
    
    def world_to_screen(self, world_pos):
        return Vector2(
            world_pos[0] - self.position.x + self._half_w,
            world_pos[1] - self.position.y + self._half_h
        )
    
    def screen_to_world(self, screen_pos):
        return Vector2(
            screen_pos[0] - self._half_w + self.position.x,
            screen_pos[1] - self._half_h + self.position.y
        )