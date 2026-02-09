from gamelib.core.model.render.render_scene_obj import *
from gamelib.core.model.scenes.scene import *

class GameObject():
    def __init__(self, x=0, y=0, width=50, height=50, canvas=None, scene=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas = canvas
        self.scene = scene
        self.components = list()

    def add_component(self, component):
        # Передаем self в компонент, если компонент поддерживает это
        if hasattr(component, 'set_game_object'):
            component.set_game_object(self)
        self.components.append(component)
        return self  # Для цепочного вызова

    def get_coordinates(self):
        """Возвращает координаты прямоугольника в виде списка [x1, y1, x2, y2]"""
        return [self.x, self.y, self.x + self.width, self.y + self.height]
    
    def get_position(self):
        """Возвращает текущую позицию (левый верхний угол)"""
        return [self.x, self.y]
    
    def get_size(self):
        """Возвращает размеры прямоугольника [ширина, высота]"""
        return [self.width, self.height]
    
    def get_center(self):
        """Возвращает центр объекта"""
        return [self.x + self.width/2, self.y + self.height/2]

    def update_position(self, new_x, new_y):
        """Обновляет позицию объекта и всех его компонентов"""        
        # Calculate offset
        dx = new_x - self.x
        dy = new_y - self.y
        
        # Update object coordinates
        self.x = new_x
        self.y = new_y
        
        if hasattr(self, 'rect_id') and self.canvas:
            self.canvas.move(self.rect_id, dx, dy)
        
        # Moves all components behind the object
        for component in self.components:
            if hasattr(component, 'update_position'):
                component.update_position(dx, dy)


class gameObject():
    class Rectangle(GameObject):
        def __init__(self, canvas, x=0, y=0, width=50, height=50, color="red", scene=None):
            super().__init__(x, y, width, height, canvas, scene)
            self.canvas = canvas
            self.color = color
            
            # Create rectangle on the canvas
            self.rect_id = canvas.create_rectangle(
                self.x, self.y, self.x + self.width, self.y + self.height, 
                fill=color, outline=color
            )

            if scene:
                scene.add_game_obj(self)