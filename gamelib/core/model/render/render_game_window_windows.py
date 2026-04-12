import tkinter as tk
from gamelib.core.model.render.render_scene_obj import create_canvas


class main_game_window():
    def __init__(self, name, width, height, background_color):
        self.name = name
        self.width = width
        self.height = height
        self.background_color = background_color
        self.root = tk.Tk()
        self._setup_window()
    
    def _setup_window(self):
        self.root.title(self.name)
        self.root.geometry(f"{self.width}x{self.height}")
    
    def add_scene(self):
        return create_canvas(self.root, self.width, self.height, self.background_color)