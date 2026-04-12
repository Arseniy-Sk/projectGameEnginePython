from PIL import Image, ImageTk
from gamelib.core.model.render.render_scene_obj import *
from gamelib.core.model.events.events_system import global_bus


class Component():
    def __init__(self):
        self.obj = None

    def set_game_object(self, obj):
        self.obj = obj


class ImageComponent(Component):
    def __init__(self, image_path, use_object_coords=True):
        super().__init__()
        self.image_path = image_path
        self.use_object_coords = use_object_coords
        self.image_id = None
        self.tk_image = None
        
    def set_game_object(self, obj):
        super().set_game_object(obj)
        self._initialize_image()
    
    def _initialize_image(self):
        if not self.obj or not hasattr(self.obj, 'get_coordinates') or not self.obj.canvas:
            return
        
        try:
            self.image = Image.open(self.image_path)
            
            obj_coords = self.obj.get_coordinates()
            obj_width = obj_coords[2] - obj_coords[0]
            obj_height = obj_coords[3] - obj_coords[1]
            
            self.image = self.image.resize((obj_width, obj_height))
            self.tk_image = ImageTk.PhotoImage(self.image)
            
            self.image_id = self.obj.canvas.create_image(
                obj_coords[0] + obj_width // 2,
                obj_coords[1] + obj_height // 2,
                image=self.tk_image,
                anchor='center'
            )
            
            self.obj.canvas.tag_raise(self.image_id)
            self.obj.tk_image = self.tk_image
            
            global_bus.emit('image_loaded', self, {
                'image_path': self.image_path,
                'width': obj_width,
                'height': obj_height
            })
            
        except Exception:
            pass

    def update_position(self, dx, dy):
        if self.image_id and self.obj and self.obj.canvas:
            self.obj.canvas.move(self.image_id, dx, dy)