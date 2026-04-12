import threading
import time
from gamelib.data.version import print_version
from gamelib.core.model.render.render_game_window_windows import main_game_window


class Engine():
    def __init__(self, game=None):
        self.running = False
        self.game_loop_thread = None
        self.game = game
        self.loop_delay = 1.0 / 60.0
    
    def set_game(self, game):
        self.game = game
    
    def _game_loop(self):
        while self.running and self.game:
            try:
                self.game.update()
                time.sleep(self.loop_delay)
            except Exception:
                break
    
    def start_game_loop(self):
        if not self.game or self.running:
            return
        
        self.running = True
        self.game_loop_thread = threading.Thread(target=self._game_loop, daemon=True)
        self.game_loop_thread.start()
    
    def stop_game_loop(self):
        self.running = False
        if self.game_loop_thread:
            self.game_loop_thread.join(timeout=1.0)
            self.game_loop_thread = None
    
    def set_fps(self, fps):
        if fps > 0:
            self.loop_delay = 1.0 / fps
    
    def print_engine_info(self):
        print_version()
    
    def __del__(self):
        self.stop_game_loop()


class Game:
    def __init__(self, title, width, height, background_color):
        self.window = main_game_window(title, width, height, background_color)
        self.engine = None
    
    def set_engine(self, engine):
        self.engine = engine
        engine.set_game(self)
    
    def setup(self):
        pass
    
    def start(self):
        self.setup()
        if self.engine:
            self.engine.start_game_loop()
    
    def update(self):
        pass
    
    def end(self):
        pass