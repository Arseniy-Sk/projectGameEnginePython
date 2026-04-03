# tests/test_gui_minimal.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gamelib import *
from gamelib.core.model.gui.gui_factory import *


class MinimalGuiTest(Game):
    def __init__(self):
        super().__init__("GUI Minimal", 500, 500, "#1a1a2e")
    
    def setup(self):
        scene = Scene(self.window)
        SceneSwitcher().show_scene(scene)
        
        # Панель
        panel = Panel(scene.canvas, bg="#1a1a2e")
        panel.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Метка
        self.label = Label(panel.widget, text="Привет!", font=("Arial", 14), color="#00ff88")
        self.label.pack(pady=5)
        
        # Кнопка
        def on_click():
            self.label.set_text("Нажато!")
            self.label.set_color("#ff6688")
        
        Button(panel.widget, text="Нажми", command=on_click, color="white", bg="#333344").pack(pady=5)
        
        # Чекбокс
        def on_check(checked):
            print(f"Чекбокс: {checked}")
        
        CheckBox(panel.widget, text="Опция", on_change=on_check, color="#88aaff").pack(pady=5)
        
        # Слайдер
        def on_slider(val):
            print(f"Значение: {val}")
        
        Slider(panel.widget, from_=0, to=100, default=50, on_change=on_slider).pack(pady=5)
        
        # Выпадающий список
        def on_select(item):
            self.label.set_text(f"Выбрано: {item}")
        
        DropDown(panel.widget, items=["Пункт 1", "Пункт 2", "Пункт 3"], 
                 on_select=on_select, color="white", bg="#333344").pack(pady=5)
        
        # Поле ввода
        def on_text(text):
            print(f"Ввод: {text}")
        
        TextInput(panel.widget, placeholder="Введите текст...", on_change=on_text,
                  color="#00ff88", bg="#222244", placeholder_color="#666688").pack(pady=5)
        
        print("\n=== Готово! ===")
    
    def start(self):
        super().start()
        InputManager(self.window.root)


def main():
    game = MinimalGuiTest()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()


if __name__ == "__main__":
    main()