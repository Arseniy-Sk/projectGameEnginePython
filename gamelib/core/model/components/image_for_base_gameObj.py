from PIL import Image, ImageTk
import tkinter as Tk
from gamelib.core.model.render.render_scene_obj import *

# Parent class for the all components
class Component():
    def __init__(self, obj):
        self.obj = obj


class ImageComponent(Component):
    def __init__(self, rectangle_obj, image_path, use_object_coords=True):
        """Компонент для добавления изображения к объекту"""
        super().__init__(rectangle_obj)
        
        self.rectangle = rectangle_obj
        self.image_path = image_path
        self.use_object_coords = use_object_coords
        
        if hasattr(rectangle_obj, 'get_coordinates'):
            coords = rectangle_obj.get_coordinates()
        else:
            return
        
        # Upload image
        try:
            print(f"\nLoading image from: {image_path}")
            self.image = Image.open(image_path)
            
            # Get object's coordinate
            obj_coords = rectangle_obj.get_coordinates()
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
            
            canvas = rectangle_obj.canvas
            if canvas:
                self.image_id = canvas.create_image(
                    image_center_x,  # X center coordinate
                    image_center_y,  # Y center coordinate
                    image=self.tk_image,
                    anchor='center'
                )
                
                canvas.tag_raise(self.image_id)
                
                rectangle_obj.tk_image = self.tk_image
                
                if hasattr(rectangle_obj, 'add_component'):
                    rectangle_obj.add_component(self)
                    print(f"✓ ImageComponent added to rectangle's components")
            else:
                print("ERROR: No canvas available!")
            
        except FileNotFoundError as e:
            print(f"✗ File not found: {e}")
        except Exception as e:
            print(f"✗ Error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()


    def update_position(self, dx, dy):
        """Обновляет позицию изображения при перемещении объекта"""        
        if hasattr(self, 'image_id') and hasattr(self.rectangle, 'canvas'):
            # Moving image
            canvas = self.rectangle.canvas
            if canvas:
                canvas.move(self.image_id, dx, dy)