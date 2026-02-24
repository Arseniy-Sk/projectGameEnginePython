# tests/test2.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *
from gamelib.core.model.events.events_system import global_bus

class MyGame(Game):
    def __init__(self, title="2d game", width=800, height=600, background_color="black"):
        super().__init__(title, width, height, background_color="black")
        self.sceneSwitcher = SceneSwitcher()
        self.frame_count = 0
        self.input_manager = None

    def setup(self):
        MainScene = Scene(self.window)

        self.red_obj = gameObject.Rectangle(
            MainScene.canvas,
            x=50, y=50, width=100, height=100,
            color='red',
            scene=MainScene
        ).add_component(BasePhisicComponent(mass=15, gravity=True))

        self.blue_obj = gameObject.Rectangle(
            MainScene.canvas,
            x=200, y=50, width=80, height=80,
            color='blue',
            scene=MainScene
        ).add_component(BasePhisicComponent(mass=10, gravity=False))

        image_path = os.path.join(os.path.dirname(__file__), "resources/images/123123123.jpg")
        self.green_obj = gameObject.Rectangle(
            MainScene.canvas,
            x=350, y=50, width=120, height=120,
            color='white',
            scene=MainScene
        ).add_component(ImageComponent(image_path)).add_component(BasePhisicComponent(20, False))

        self.sceneSwitcher.show_scene(MainScene)
        self.window.root.after(2000, self.apply_impulse_to_blue)
        self.input_manager = InputManager(self.window.root)

        # Подписки с указанием объекта и типа
        global_bus.subscribe(self.red_obj, None, self.on_any_red_event)
        global_bus.subscribe(self.blue_obj, 'impulse_finished', self.on_blue_impulse_finished)
        global_bus.subscribe(None, 'position_changed', self.on_any_position_changed)
        global_bus.subscribe(None, None, self.on_global_event)
        global_bus.subscribe(self.green_obj, 'custom_event', self.on_green_custom_event)

    def on_any_red_event(self, event):
        print(f"[Красный] {event.type} → {event.data}")

    def on_blue_impulse_finished(self, event):
        print(f"[Синий] Импульс завершён: {event.data}")

    def on_any_position_changed(self, event):
        if self.frame_count % 10 == 0:  # не спамим
            name = "красный" if event.source == self.red_obj else "синий" if event.source == self.blue_obj else "зелёный"
            print(f"[Позиция] {name}: {event.data['old']} → {event.data['new']}")

    def on_global_event(self, event):
        if event.type != 'position_changed':
            print(f"[Глобально] {event.type} от {event.source}")

    def on_green_custom_event(self, event):
        print(f"[Кастом] {event.data['message']}")

    def apply_impulse_to_blue(self):
        print("Применяем импульс к синему")
        blue_physics = next(c for c in self.blue_obj.components if isinstance(c, BasePhisicComponent))
        blue_physics.impulse(50, Vector2(1, -0.5).normalized(), lambda: print("Импульс (колбэк)"))

    def start(self):
        super().start()
        print("Игра запущена!")

    def update(self):
        self.frame_count += 1

        if self.frame_count % 60 == 0:
            red_physics = next(c for c in self.red_obj.components if isinstance(c, BasePhisicComponent))
            red_physics.impulse(5, Vector2(0.2, -0.8).normalized())

        # Используем новый метод is_key_down, не зависящий от раскладки
        if self.input_manager.is_key_down('e'):
            green_physics = next(c for c in self.green_obj.components if isinstance(c, BasePhisicComponent))
            green_physics.impulse(30, Vector2(0, -1).normalized(),
                                  lambda: print("Импульс зелёного (колбэк)"))
            # Не сбрасываем клавишу, так как is_key_down проверяет каждый кадр

        if self.input_manager.is_key_down('c'):
            print("Генерируем кастомное событие от зелёного")
            global_bus.emit(self.green_obj, 'custom_event', {'message': 'Привет от зелёного!'})

        # Пример для стрелок (они не зависят от раскладки)
        if self.input_manager.is_key_down('Up'):
            print("Нажата стрелка вверх")


def main():
    game = MyGame()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()

if __name__ == "__main__":
    main()
