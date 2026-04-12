simple_template = '''\"\"\"
{game_name} - простая игра
Создано с GameLib
\"\"\"

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *


class {class_name}(Game):
    def __init__(self):
        super().__init__("{game_name}", 800, 600, "#1a1a2e")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        self.player = None
    
    def setup(self):
        scene = Scene(self.window)
        self.scene_switcher.show_scene(scene)
        
        self.player = gameObject.Rectangle(
            scene.canvas, x=400, y=300,
            width=50, height=50,
            color='#00ff88', scene=scene
        )
        
        self.input_manager = InputManager(self.window.root)
        self.window.root.after(16, self.game_loop)
    
    def game_loop(self):
        x, y = self.player.get_position()
        
        if self.input_manager.is_key_down('a'):
            self.player.update_position(x - 5, y)
        if self.input_manager.is_key_down('d'):
            self.player.update_position(x + 5, y)
        if self.input_manager.is_key_down('w'):
            self.player.update_position(x, y - 5)
        if self.input_manager.is_key_down('s'):
            self.player.update_position(x, y + 5)
        if self.input_manager.is_key_down('Escape'):
            self.window.root.quit()
        
        self.window.root.after(16, self.game_loop)
    
    def update(self):
        pass


def main():
    game = {class_name}()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()


if __name__ == "__main__":
    main()
'''