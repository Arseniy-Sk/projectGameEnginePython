import tkinter as tk
from gamelib.core.model.render.render_scene_obj import create_canvas

class main_game_window():
    def __init__(self, name, width, height, background_color):
        self.name = name
        self.width = width
        self.height = height
        __root = tk.Tk()
        self.root = __root
        self.background_color = background_color

        self.create_main_game_window(self.name, self.width, self.height, self.root)


    def create_main_game_window(self, name1, width1, height1, root1):
        root1.title(name1)
        root1.geometry(f"{width1}x{height1}")
        print(f"Game window '{name1}' created with size {width1}x{height1}.")


    def add_scene(self):
        return create_canvas(self.root, self.width, self.height, self.background_color)
    
        
