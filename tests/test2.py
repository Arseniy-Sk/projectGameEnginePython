# tests/test2.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *


class MyGame(Game):
    def __init__(self, title="2d game", width=800, height=600, background_color="black"):
        super().__init__(title, width, height, background_color="black")
        
        SCENE_SWITCHER = SceneSwitcher()
        self.sceneSwitcher = SCENE_SWITCHER
        self.frame_count = 0
        self.input_manager = None

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
        
        image_path = os.path.join(os.path.dirname(__file__), "resources/images/123123123.jpg")

        self.green_obj = gameObject.Rectangle(
            MainScene.canvas, 
            x=350, y=50, width=120, height=120, 
            color='white', 
            scene=MainScene
        ).add_component(ImageComponent(image_path))
        self.green_obj.add_component(BasePhisicComponent(20, False))
        
        # Показываем сцену
        self.sceneSwitcher.show_scene(MainScene)
        
        # Запускаем импульс для синего объекта через 2 секунды
        self.window.root.after(2000, self.apply_impulse_to_blue)
        
        # Инициализируем InputManager
        self.input_manager = InputManager(self.window.root)

    def apply_impulse_to_blue(self):
        """Применяет импульс к синему объекту"""
        print("Применяем импульс к синему объекту!")
        
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
        
        # Проверяем нажатие клавиши E
        if self.input_manager and self.input_manager.key == 'e':
            green_physics = None
            for comp in self.green_obj.components:
                if isinstance(comp, BasePhisicComponent):
                    green_physics = comp
                    break
                
            if green_physics:
                green_physics.impulse(30, Vector2(0, -1).normalized(), 
                                    lambda: print("Импульс зеленого объекта завершен!"))
                
            # Сбрасываем клавишу после обработки
            self.input_manager.key = ' '


def main():
    # Создаем игру
    game = MyGame()
    
    # Создаем движок и связываем его с игрой
    GAME_ENGINE = Engine(game)
    game.set_engine(GAME_ENGINE)
    
    # Запускаем игру (это запустит игровой цикл)
    game.start()
    
    # Запускаем главный цикл Tkinter
    game.window.root.mainloop()


if __name__ == "__main__":
    main()