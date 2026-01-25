from gamelib.core.model.render.render_scene_obj import *
from gamelib.core.model.scenes.scene import *

class GameObject():
    def __init__(self):
        self.components = list()

class Rectangle(GameObject):
    def __init__(self, canvas, position: list, color, scene=None):
        super().__init__()
        if len(position) != 4:
            raise ValueError("coords must be a list of 4 values: [x1, y1, x2, y2]")
        
        self.x1 = position[0]
        self.y1 = position[1]
        self.x2 = position[2]
        self.y2 = position[3]
        self.canvas = canvas
        self.color = color
        
        # Create rectangle on the canvas
        self.rect_id = canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2, 
            fill=color, outline=color
        )

        self.position = position

        if scene:
            scene.add_game_obj(self)


    def get_coordinates(self):
        """Возвращает координаты прямоугольника в виде списка [x1, y1, x2, y2]"""
        return [self.x1, self.y1, self.x2, self.y2]
    
    def get_position(self):
        """Возвращает текущую позицию (левый верхний угол)"""
        return [self.x1, self.y1]
    
    def get_size(self):
        """Возвращает размеры прямоугольника [ширина, высота]"""
        return [self.x2 - self.x1, self.y2 - self.y1]
    

    def update_position(self, new_x, new_y):
        """Обновляет позицию объекта и всех его компонентов"""        
        # Calculate offset
        dx = new_x - self.x1
        dy = new_y - self.y1
        print(f"  Calculated dx={dx}, dy={dy}")
        
        # Upadte object coordinate
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        self.x1 = new_x
        self.y1 = new_y
        self.x2 = new_x + width
        self.y2 = new_y + height
        
        if hasattr(self, 'rect_id'):
            self.canvas.move(self.rect_id, dx, dy)
        
        # Moves all components behind the object
        print(f"  Updating {len(self.components)} components:")
        for i, component in enumerate(self.components):
            print(f"    Component {i}: {type(component).__name__}")
            if hasattr(component, 'update_position'):
                component.update_position(dx, dy)

    def add_component(self, component):
        self.components.append(component)
