import threading
import time
from gamelib.data.version import print_version
from gamelib.core.model.render.render_game_window_windows import *

#main lib class
class Engine():
    #Function at initialization engine in project
    def __init__(self, game=None):
        print("Engine was Started!")
        self.running = False
        self.game_loop_thread = None
        self.game = game  # Ссылка на игру
        self.loop_delay = 1.0 / 60.0  # 60 FPS по умолчанию
    
    def set_game(self, game):
        """Установить игру для обновления"""
        self.game = game
    
    def _game_loop(self):
        """Основной игровой цикл в отдельном потоке"""
        while self.running and self.game:
            try:
                # Вызываем метод update игры
                self.game.update()
                time.sleep(self.loop_delay)  # Задержка для контроля FPS
            except Exception as e:
                print(f"Error in game loop: {e}")
                break
    
    def start_game_loop(self):
        """Запустить игровой цикл в отдельном потоке"""
        if self.game is None:
            print("Error: No game set for engine")
            return
        
        if self.running:
            print("Game loop is already running")
            return
        
        self.running = True
        self.game_loop_thread = threading.Thread(target=self._game_loop, daemon=True)
        self.game_loop_thread.start()
        print("Game loop started in separate thread")
    
    def stop_game_loop(self):
        """Остановить игровой цикл"""
        self.running = False
        if self.game_loop_thread:
            self.game_loop_thread.join(timeout=1.0)
            self.game_loop_thread = None
        print("Game loop stopped")
    
    def set_fps(self, fps):
        """Установить желаемое количество кадров в секунду"""
        if fps > 0:
            self.loop_delay = 1.0 / fps
            print(f"FPS set to {fps}")
    
    def print_engine_info(self):
        print_version()
    
    #Function at the end of the game
    def __del__(self):
        self.stop_game_loop()
        print("Engine ended his worked!")


class Game:
    def __init__(self, title, width, height, background_color):
        MAIN_GAME_WINDOW = main_game_window(title, width, height, background_color)
        self.window = MAIN_GAME_WINDOW
        self.engine = None  # Ссылка на движок
    
    def set_engine(self, engine):
        """Установить движок для игры"""
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