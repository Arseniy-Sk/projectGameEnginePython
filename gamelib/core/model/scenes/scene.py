from gamelib.core.model.render.render_game_window_windows import *
from gamelib.core.model.render.render_scene_obj import show_scene, close_scene


class Scene():
    def __init__(self, window):
        self.window = window
        self.canvas = window.add_scene()
        self.gui_list = []
        self.gameObj_list = []

    @classmethod
    def create_scene(cls, window):
        return cls(window)

    def add_game_obj(self, obj):
        self.gameObj_list.append(obj)

    def show_gameObj_list(self):
        for obj in self.gameObj_list:
            print(f"Scene's gameObj_list: {obj}")


class SceneSwitcher():
    def __init__(self):
        self.scenes = []

    def show_scene(self, scene):
        show_scene(scene)
        
    def close_scene(self, scene):
        close_scene(scene)

    def switch_scene(self, scene1, scene2):
        self.close_scene(scene1)
        self.show_scene(scene2)