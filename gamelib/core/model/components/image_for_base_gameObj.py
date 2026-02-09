from PIL import Image, ImageTk
import tkinter as Tk
from gamelib.core.model.render.render_scene_obj import *

# Parent class for the all components
class Component():
    def __init__(self):
        self.obj = None

    def set_game_object(self, obj):
        """Устанавливает ссылку на игровой объект"""
        self.obj = obj


class ImageComponent(Component):
    def __init__(self, image_path, use_object_coords=True):
        """Компонент для добавления изображения к объекту"""
        super().__init__()
        self.image_path = image_path
        self.use_object_coords = use_object_coords
        
    def set_game_object(self, obj):
        """Переопределяем для инициализации изображения после привязки к объекту"""
        super().set_game_object(obj)
        self._initialize_image()
    
    def _initialize_image(self):
        """Инициализирует изображение после привязки к объекту"""
        if not self.obj or not hasattr(self.obj, 'get_coordinates'):
            return
        
        try:
            print(f"\nLoading image from: {self.image_path}")
            self.image = Image.open(self.image_path)
            
            # Get object's coordinate
            obj_coords = self.obj.get_coordinates()
            obj_x1, obj_y1, obj_x2, obj_y2 = obj_coords
            
            # Object size
            obj_width = obj_x2 - obj_x1
            obj_height = obj_y2 - obj_y1
            
            # Scale image for object
            self.image = self.image.resize((obj_width, obj_height))
            self.tk_image = ImageTk.PhotoImage(self.image)
            print(f"Resized image to: {obj_width}x{obj_height}")
            
            # Save size
            self.obj_width = obj_width
            self.obj_height = obj_height
            
            # Get center
            image_center_x = obj_x1 + obj_width // 2
            image_center_y = obj_y1 + obj_height // 2
            
            if self.obj.canvas:
                self.image_id = self.obj.canvas.create_image(
                    image_center_x,  # X center coordinate
                    image_center_y,  # Y center coordinate
                    image=self.tk_image,
                    anchor='center'
                )
                
                self.obj.canvas.tag_raise(self.image_id)
                self.obj.tk_image = self.tk_image
                
                print(f"✓ ImageComponent added to rectangle's components")
            else:
                print("ERROR: No canvas available!")
            
        except FileNotFoundError as e:
            print(f"✗ File not found: {e}")
        except Exception as e:
            print(f"✗ Error: {type(e).__name__}: {e}")

    def update_position(self, dx, dy):
        """Обновляет позицию изображения при перемещении объекта"""        
        if hasattr(self, 'image_id') and self.obj and self.obj.canvas:
            self.obj.canvas.move(self.image_id, dx, dy)