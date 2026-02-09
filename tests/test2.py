# tests/test2.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *


class MyGame(Game):
    def __init__(self, title="2d game", width=800, height=600):
        super().__init__(title, width, height)
        
        SCENE_SWITCHER = SceneSwitcher()
        self.sceneSwitcher = SCENE_SWITCHER
        self.frame_count = 0

    def setup(self):
        # Создаем главную сцену
        MainScene = Scene(self.window)
        
        # Создаем объекты с цепочным добавлением компонентов
        self.red_obj = gameObject.Rectangle(
            MainScene.canvas, 
            x=50, y=50, width=100, height=100, 
            color='red', 
            scene=MainScene
        ).add_component(
            BasePhisicComponent(mass=15, gravity=True)
        )
        
        self.blue_obj = gameObject.Rectangle(
            MainScene.canvas, 
            x=200, y=50, width=80, height=80, 
            color='blue', 
            scene=MainScene
        ).add_component(
            BasePhisicComponent(mass=10, gravity=False)
        )
        
        self.green_obj = gameObject.Rectangle(
            MainScene.canvas, 
            x=350, y=50, width=60, height=120, 
            color='green', 
            scene=MainScene
        )
        
        # Показываем сцену
        self.sceneSwitcher.show_scene(MainScene)
        
        # Запускаем импульс для синего объекта через 2 секунды
        self.window.root.after(2000, self.apply_impulse_to_blue)

    def apply_impulse_to_blue(self):
        """Применяет импульс к синему объекту"""
        print("Применяем импульс к синему объекту!")
        
        # Получаем физический компонент синего объекта
        blue_physics = None
        for comp in self.blue_obj.components:
            if isinstance(comp, BasePhisicComponent):
                blue_physics = comp
                break
        
        if blue_physics:
            blue_physics.impulse(
                50, 
                Vector2(1, -0.5).normalized(),
                lambda: print("Импульс завершен!")
            )

    def start(self):
        super().start()
        print("Игра запущена!")

    def update(self):
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            print(f"Update: кадр {self.frame_count}")
            
            # Каждые 60 кадров применяем небольшой импульс к красному объекту
            red_physics = None
            for comp in self.red_obj.components:
                if isinstance(comp, BasePhisicComponent):
                    red_physics = comp
                    break
            
            if red_physics:
                red_physics.impulse(5, Vector2(0.2, -0.8).normalized())


def main():
    # Создаем игру
    game = MyGame(title="Тестовая игра 2", width=800, height=600)
    
    # Создаем движок и связываем его с игрой
    GAME_ENGINE = Engine(game)
    game.set_engine(GAME_ENGINE)
    
    # Запускаем игру (это запустит игровой цикл)
    game.start()
    
    # Запускаем главный цикл Tkinter
    game.window.root.mainloop()


if __name__ == "__main__":
    main()