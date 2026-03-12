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
        self.gui_elements = []  # Список для хранения GUI элементов

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

        # === ТЕСТ GUI ===
        self.setup_gui()

    def setup_gui(self):
        """Настройка GUI элементов для тестирования"""
        print("\n=== ТЕСТИРОВАНИЕ GUI ===")
        
        # Создаем фрейм для организации GUI элементов
        self.gui_frame = tk.Frame(self.window.root, bg='lightgray', relief='raised', bd=2)
        self.gui_frame.place(x=600, y=10, width=180, height=250)  # Размещаем справа
        
        # 1. Тест Label (метка)
        self.label1 = Label(self.window.root, "Обычная метка", ("Arial", 12))
        self.label1.pack()  # Размещаем в главном окне
        self.gui_elements.append(self.label1)
        
        # Создаем метку внутри фрейма
        self.label2 = Label(self.gui_frame, "Метка во фрейме", ("Arial", 10))
        self.label2.pack(pady=5)
        self.gui_elements.append(self.label2)
        
        # 2. Тест Button (кнопки)
        self.button1 = Button(
            self.window.root,
            text="Нажми меня!",
            command=self.on_button_click,
            font=("Arial", 12)
        )
        self.button1.pack(pady=5)
        self.gui_elements.append(self.button1)
        
        # Кнопка для применения импульса к красному
        self.button2 = Button(
            self.gui_frame,
            text="Импульс красному",
            command=self.apply_impulse_to_red,
            font=("Arial", 10)
        )
        self.button2.pack(pady=5)
        self.gui_elements.append(self.button2)
        
        # Кнопка для остановки гравитации
        self.button3 = Button(
            self.gui_frame,
            text="Стоп гравитация",
            command=self.stop_gravity,
            font=("Arial", 10)
        )
        self.button3.pack(pady=5)
        self.gui_elements.append(self.button3)
        
        # Кнопка для генерации события
        self.button4 = Button(
            self.gui_frame,
            text="Событие от зеленого",
            command=self.emit_custom_event,
            font=("Arial", 10)
        )
        self.button4.pack(pady=5)
        self.gui_elements.append(self.button4)
        
        # 3. Тест изменения свойств GUI
        self.update_label_button = Button(
            self.gui_frame,
            text="Обновить метку",
            command=self.update_label,
            font=("Arial", 10)
        )
        self.update_label_button.pack(pady=5)
        self.gui_elements.append(self.update_label_button)
        
        # 4. Информационная метка для отображения счета/статуса
        self.status_label = Label(
            self.gui_frame,
            "Статус: Готов",
            ("Arial", 9)
        )
        self.status_label.pack(pady=5)
        self.gui_elements.append(self.status_label)
        
        print("✓ GUI элементы успешно созданы")
        print("=== ТЕСТ GUI ЗАВЕРШЕН ===\n")

    def on_button_click(self):
        """Обработчик нажатия на тестовую кнопку"""
        print("[GUI] Кнопка нажата!")
        self.status_label.set_text("Статус: Кнопка нажата!")
        
        # Меняем текст кнопки
        self.button1.set_text("Нажато!")
        
        # Через секунду возвращаем обратно
        self.window.root.after(1000, lambda: self.button1.set_text("Нажми меня!"))

    def apply_impulse_to_red(self):
        """Применение импульса к красному объекту через GUI"""
        print("[GUI] Применяем импульс к красному")
        red_physics = next(c for c in self.red_obj.components if isinstance(c, BasePhisicComponent))
        red_physics.impulse(30, Vector2(0.5, -1).normalized())
        self.status_label.set_text("Статус: Импульс красному")

    def stop_gravity(self):
        """Остановка гравитации для всех объектов"""
        print("[GUI] Останавливаем гравитацию")
        for obj in [self.red_obj, self.blue_obj, self.green_obj]:
            for component in obj.components:
                if isinstance(component, BasePhisicComponent):
                    component.stop_gravity()
        self.status_label.set_text("Статус: Гравитация остановлена")

    def emit_custom_event(self):
        """Генерация кастомного события"""
        print("[GUI] Генерируем кастомное событие")
        global_bus.emit(self.green_obj, 'custom_event', {'message': 'Событие от GUI!'})
        self.status_label.set_text("Статус: Событие отправлено")

    def update_label(self):
        """Обновление текста метки"""
        import random
        messages = [
            "Привет из GUI!",
            "Тестирование...",
            "GUI работает!",
            "Счет: 42",
            "Нажми кнопку!"
        ]
        new_text = random.choice(messages)
        print(f"[GUI] Обновляем метку: {new_text}")
        self.label2.set_text(new_text)
        self.status_label.set_text(f"Статус: Метка обновлена")

    def on_any_red_event(self, event):
        print(f"[Красный] {event.type} → {event.data}")

    def on_blue_impulse_finished(self, event):
        print(f"[Синий] Импульс завершён: {event.data}")
        self.status_label.set_text("Статус: Импульс синего завершен")

    def on_any_position_changed(self, event):
        if self.frame_count % 10 == 0:  # не спамим
            name = "красный" if event.source == self.red_obj else "синий" if event.source == self.blue_obj else "зелёный"
            print(f"[Позиция] {name}: {event.data['old']} → {event.data['new']}")

    def on_global_event(self, event):
        if event.type != 'position_changed':
            print(f"[Глобально] {event.type} от {event.source}")

    def on_green_custom_event(self, event):
        print(f"[Кастом] {event.data['message']}")
        self.status_label.set_text(f"Статус: {event.data['message']}")

    def apply_impulse_to_blue(self):
        print("Применяем импульс к синему")
        blue_physics = next(c for c in self.blue_obj.components if isinstance(c, BasePhisicComponent))
        blue_physics.impulse(50, Vector2(1, -0.5).normalized(), lambda: print("Импульс (колбэк)"))

    def start(self):
        super().start()
        print("Игра запущена!")
        print("\n=== ИНСТРУКЦИЯ ПО ТЕСТИРОВАНИЮ GUI ===")
        print("1. Нажмите кнопку 'Нажми меня!' - проверит базовую функциональность")
        print("2. Кнопка 'Импульс красному' - применит импульс к красному объекту")
        print("3. Кнопка 'Стоп гравитация' - остановит гравитацию у всех объектов")
        print("4. Кнопка 'Событие от зеленого' - сгенерирует кастомное событие")
        print("5. Кнопка 'Обновить метку' - меняет текст метки случайным образом")
        print("=====================================\n")

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