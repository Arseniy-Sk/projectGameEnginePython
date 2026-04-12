# GameLib Framework - Полная документация

## Оглавление
1. [Введение](#введение)
2. [Быстрый старт](#быстрый-старт)
3. [Ядро фреймворка](#ядро-фреймворка)
4. [Игровые объекты](#игровые-объекты)
5. [Компоненты](#компоненты)
6. [Сцены](#сцены)
7. [Физика](#физика)
8. [Аудиосистема](#аудиосистема)
9. [Векторная математика](#векторная-математика)
10. [Система событий](#система-событий)
11. [Камера](#камера)
12. [GUI система](#gui-система)
13. [Ввод с клавиатуры](#ввод-с-клавиатуры)
14. [Создание игры - полный гайд](#создание-игры-полный-гайд)
15. [Примеры](#примеры)

---

## Введение

GameLib - это легковесный фреймворк для создания 2D игр на Python с использованием Tkinter. Фреймворк предоставляет все необходимые инструменты для быстрой разработки: систему компонентов, физику, аудио, работу с камерой, GUI и многое другое.

### Особенности
- Компонентно-ориентированная архитектура
- Встроенная физика и гравитация
- Система сцен и переключения между ними
- Аудиосистема с поддержкой MP3/WAV
- 2D камера с слежением и эффектами
- Система событий
- GUI виджеты
- Векторная математика

---

## Быстрый старт

### Установка

```python
# Установка через pip
pip install gamelib

# Или клонирование репозитория
git clone https://github.com/yourusername/gamelib.git
cd gamelib
python setup.py install
```

### Создание первой игры

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *

class MyFirstGame(Game):
    def __init__(self):
        super().__init__("Моя игра", 800, 600, "#1a1a2e")
        self.scene_switcher = SceneSwitcher()
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
        
        self.window.root.after(16, self.game_loop)
    
    def update(self):
        pass

def main():
    game = MyFirstGame()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()

if __name__ == "__main__":
    main()
```

---

## Ядро фреймворка

### Класс Engine

Основной движок игры, управляет игровым циклом.

```python
class Engine:
    def __init__(self, game=None)
    def set_game(self, game)
    def start_game_loop(self)
    def stop_game_loop(self)
    def set_fps(self, fps)
    def print_engine_info(self)
```

**Атрибуты:**
- `running` - флаг работы движка
- `game_loop_thread` - поток игрового цикла
- `game` - ссылка на объект игры
- `loop_delay` - задержка между кадрами (1/FPS)

**Методы:**

```python
# Создание движка
engine = Engine(game_object)

# Установка игры
engine.set_game(my_game)

# Запуск игрового цикла
engine.start_game_loop()

# Остановка игрового цикла
engine.stop_game_loop()

# Установка FPS
engine.set_fps(60)  # 60 кадров в секунду

# Вывод информации о движке
engine.print_engine_info()
```

### Класс Game

Базовый класс для всех игр.

```python
class Game:
    def __init__(self, title, width, height, background_color)
    def set_engine(self, engine)
    def setup(self)
    def start(self)
    def update(self)
    def end(self)
```

**Атрибуты:**
- `window` - главное окно игры (main_game_window)
- `engine` - ссылка на движок

**Методы:**

```python
class MyGame(Game):
    def __init__(self):
        super().__init__("Название", 1024, 768, "#000000")
    
    def setup(self):
        """Вызывается при старте игры, инициализация"""
        # Создание сцен, объектов, GUI
        pass
    
    def update(self):
        """Вызывается каждый кадр движком"""
        # Обновление игровой логики
        pass
    
    def end(self):
        """Вызывается при завершении игры"""
        # Очистка ресурсов
        pass
```

### Класс main_game_window

Управление главным окном игры.

```python
class main_game_window:
    def __init__(self, name, width, height, background_color)
    def add_scene(self)
```

**Атрибуты:**
- `name` - название окна
- `width` - ширина
- `height` - высота
- `root` - корневой виджет Tkinter
- `background_color` - цвет фона

**Методы:**

```python
# Создание окна
window = main_game_window("Моя игра", 800, 600, "#1a1a2e")

# Создание холста для сцены
canvas = window.add_scene()
```

---

## Игровые объекты

### Класс GameObject

Базовый класс для всех игровых объектов.

```python
class GameObject:
    def __init__(self, x=0, y=0, width=50, height=50, canvas=None, scene=None)
    def add_component(self, component)
    def get_coordinates(self)
    def get_position(self)
    def get_size(self)
    def get_center(self)
    def update_position(self, new_x, new_y)
```

**Атрибуты:**
- `x, y` - позиция (левый верхний угол)
- `width, height` - размеры
- `canvas` - холст Tkinter
- `scene` - родительская сцена
- `components` - список компонентов
- `rect_id` - ID прямоугольника на холсте

**Методы:**

```python
# Создание объекта
obj = GameObject(x=100, y=100, width=50, height=50)

# Добавление компонента
obj.add_component(physics_component)

# Получение координат [x1, y1, x2, y2]
coords = obj.get_coordinates()

# Получение позиции [x, y]
pos = obj.get_position()

# Получение размеров [width, height]
size = obj.get_size()

# Получение центра [center_x, center_y]
center = obj.get_center()

# Обновление позиции
obj.update_position(200, 200)  # перемещает объект и все компоненты
```

### Класс gameObject.Rectangle

Прямоугольный объект для отрисовки.

```python
class gameObject.Rectangle(GameObject):
    def __init__(self, canvas, x=0, y=0, width=50, height=50, color="red", scene=None)
```

**Пример:**

```python
# Создание прямоугольника
player = gameObject.Rectangle(
    canvas=scene.canvas,
    x=400, y=300,
    width=50, height=50,
    color="#00ff88",
    scene=main_scene
)
```

---

## Компоненты

### Базовый класс Component

```python
class Component:
    def __init__(self)
    def set_game_object(self, obj)
```

### AudioSource - аудиокомпонент

```python
class AudioSource(Component):
    def __init__(self)
    def add_sound(self, name, file_path)
    def play(self, sound_name, volume=None)
    def set_collision_sound(self, sound_name)
    def on_collision(self, other)
```

**Методы:**

```python
# Создание аудиоисточника
audio = AudioSource()
player.add_component(audio)

# Добавление звука
audio.add_sound("jump", "sounds/jump.wav")
audio.add_sound("coin", "sounds/coin.mp3")

# Воспроизведение
audio.play("jump", volume=0.8)

# Привязка к коллизии
audio.set_collision_sound("coin")

# Обработка коллизии
def on_collision(self, other):
    audio.on_collision(other)
```

### AudioListener - слушатель событий

```python
class AudioListener(Component):
    def __init__(self)
    def bind_event(self, event_type, sound_name)
    def unbind_event(self, event_type)
    def on_event(self, event)
```

**Пример:**

```python
listener = AudioListener()
listener.bind_event("player_death", "sounds/death.wav")
listener.bind_event("level_complete", "sounds/win.mp3")
```

### BasePhisicComponent - физика

```python
class BasePhisicComponent(Component):
    def __init__(self, mass, gravity=False)
    def set_position(self, dx, dy)
    def move_by_vector(self, vector, distance=None)
    def add_physic_enum(self)
    def stop_gravity(self)
    def stop_impulse(self)
    def impulse(self, force, vector, on_complete=None)
```

**Атрибуты:**
- `mass` - масса объекта
- `is_gravity_active` - активна ли гравитация
- `auto_gravity` - автоматическая гравитация

**Методы:**

```python
# Создание физики
physics = BasePhisicComponent(mass=10, gravity=True)
player.add_component(physics)

# Перемещение по вектору
vector = Vector2(1, 0)
physics.move_by_vector(vector, distance=50)

# Включение гравитации
physics.add_physic_enum()

# Остановка гравитации
physics.stop_gravity()

# Применение импульса
physics.impulse(force=12, vector=Vector2(0, -1))
# Или с углом
physics.impulse(force=12, angle_or_vector=45, mass=10)

# Остановка импульса
physics.stop_impulse()
```

### ImageComponent - отображение изображений

```python
class ImageComponent(Component):
    def __init__(self, image_path, use_object_coords=True)
    def update_position(self, dx, dy)
```

**Пример:**

```python
# Создание компонента изображения
image_comp = ImageComponent("assets/player.png")
player.add_component(image_comp)

# Изображение автоматически масштабируется под размер объекта
```

### Box_collider - коллизии

```python
class Box_collider(Component):
    def __init__(self, is_trigger: bool)
    def check_collision(self, obj2, function=None)
    def stop_checking(self)
```

**Атрибуты:**
- `is_trigger` - триггер (не останавливает движение)
- `obj2` - объект для проверки
- `function` - функция обратного вызова

**Методы:**

```python
# Создание коллайдера
collider = Box_collider(is_trigger=False)
player.add_component(collider)

# Проверка коллизии с объектом
def on_collision():
    print("Столкновение!")

collider.check_collision(enemy, on_collision)

# Остановка проверки
collider.stop_checking()
```

---

## Сцены

### Класс Scene

```python
class Scene:
    def __init__(self, window)
    @classmethod
    def create_scene(cls, window)
    def add_game_obj(self, obj)
    def show_gameObj_list(self)
```

**Атрибуты:**
- `window` - главное окно
- `canvas` - холст для отрисовки
- `gui_list` - список GUI элементов
- `gameObj_list` - список игровых объектов

**Методы:**

```python
# Создание сцены
scene = Scene(window)
# Или
scene = Scene.create_scene(window)

# Добавление объекта
scene.add_game_obj(player)

# Показать все объекты (отладка)
scene.show_gameObj_list()
```

### Класс SceneSwitcher

```python
class SceneSwitcher:
    def __init__(self)
    def show_scene(self, scene)
    def close_scene(self, scene)
    def switch_scene(self, scene1, scene2)
```

**Методы:**

```python
switcher = SceneSwitcher()

# Показать сцену
switcher.show_scene(main_scene)

# Скрыть сцену
switcher.close_scene(main_scene)

# Переключить сцены
switcher.switch_scene(scene1, scene2)
```

---

## Физика

### Функции физики

```python
def set_position(canvas, obj, dx, dy)
def falling(obj, mass)
def impulse(obj, force, angle_or_vector, mass, on_complete=None)
```

**Примеры:**

```python
# Установка позиции
set_position(canvas, player, 10, 10)

# Применение гравитации
falling(player, mass=10)

# Импульс по вектору
impulse(player, force=15, angle_or_vector=Vector2(1, -1), mass=10)

# Импульс с углом и колбэком
def on_finish():
    print("Импульс завершен")

impulse(player, force=20, angle_or_vector=45, mass=10, on_complete=on_finish)
```

---

## Аудиосистема

### Класс AudioSystem

```python
class AudioSystem:
    def __init__(self)
    def load_sound(self, name, file_path)
    def play_sound(self, name, volume=None)
    def play_music(self, file_path, loop=True, volume=None)
    def stop_music(self)
    def set_sound_volume(self, volume)
    def set_music_volume(self, volume)
    def mute(self)
    def unmute(self)
    def toggle_mute(self)
```

**Атрибуты:**
- `sounds` - словарь загруженных звуков
- `sound_volume` - громкость звуков (0-1)
- `music_volume` - громкость музыки (0-1)
- `muted` - флаг отключения звука

**Методы:**

```python
# Получение глобального экземпляра
audio = global_audio

# Загрузка звуков
audio.load_sound("jump", "sounds/jump.wav")
audio.load_sound("coin", "sounds/coin.mp3")

# Воспроизведение
audio.play_sound("jump", volume=0.8)

# Музыка
audio.play_music("music/background.mp3", loop=True, volume=0.5)
audio.stop_music()

# Управление громкостью
audio.set_sound_volume(0.7)
audio.set_music_volume(0.3)

# Mute
audio.mute()
audio.unmute()
audio.toggle_mute()
```

---

## Векторная математика

### Класс Vector2

```python
class Vector2:
    def __init__(self, x=0, y=0)
    @classmethod
    def from_angle(cls, magnitude, angle_degrees)
    @classmethod
    def from_points(cls, start_x, start_y, end_x, end_y)
    def magnitude(self)
    def normalized(self)
    def angle(self)
    def scale(self, scalar)
    def add(self, other)
    def dot(self, other)
```

**Арифметические операции:**
- `+` - сложение векторов
- `-` - вычитание
- `*` - умножение на скаляр или поэлементное умножение
- `/` - деление на скаляр
- `-` - унарный минус
- `==` / `!=` - сравнение

**Методы:**

```python
# Создание вектора
v1 = Vector2(10, 20)
v2 = Vector2(5, 5)

# Из угла
v = Vector2.from_angle(magnitude=10, angle_degrees=45)

# Из точек
v = Vector2.from_points(0, 0, 10, 10)

# Длина вектора
length = v1.magnitude()

# Нормализация
normalized = v1.normalized()

# Угол вектора
angle = v1.angle()  # в градусах

# Скалярное произведение
dot = v1.dot(v2)

# Масштабирование
scaled = v1.scale(2)

# Сложение
sum_v = v1.add(v2)

# Использование операторов
v3 = v1 + v2
v4 = v1 * 2
v5 = v1 - v2

# Доступ по индексу
x = v1[0]
y = v1[1]
v1[0] = 100

# Распаковка
x, y = v1
```

---

## Система событий

### Класс Event

```python
class Event:
    def __init__(self, source, event_type, data=None)
```

**Атрибуты:**
- `source` - источник события
- `type` - тип события (строка)
- `data` - данные события

### Класс EventBus

```python
class EventBus:
    def __init__(self)
    def subscribe(self, source, event_type, callback)
    def unsubscribe(self, source, event_type, callback)
    def emit(self, source, event_type, data=None)
```

**Методы:**

```python
# Получение глобальной шины
bus = global_bus

# Подписка на события
def on_player_death(event):
    print(f"Игрок умер: {event.data}")

bus.subscribe(player, "death", on_player_death)
bus.subscribe(None, "game_over", on_game_over)  # все источники
bus.subscribe(None, None, on_any_event)  # все события

# Отписка
bus.unsubscribe(player, "death", on_player_death)

# Отправка событий
bus.emit(player, "death", {"score": 100, "position": (x, y)})
bus.emit(None, "level_complete", {"level": 2})
```

---

## Камера

### Класс Camera2D

```python
class Camera2D:
    def __init__(self, scene, width, height)
    def update(self, delta_time=1/60)
    def follow(self, target, offset=(0, 0), smoothness=0.1)
    def stop_follow(self)
    def set_zoom(self, zoom, instant=False)
    def zoom_in(self, delta=0.2)
    def zoom_out(self, delta=0.2)
    def set_bounds(self, left, top, right, bottom)
    def remove_bounds(self)
    def shake(self, intensity=10, duration=0.3)
    def move_to(self, position, instant=False)
    def world_to_screen(self, world_pos)
    def screen_to_world(self, screen_pos)
```

**Атрибуты:**
- `position` - позиция камеры
- `zoom` - уровень зума
- `follow_target` - объект слежения
- `bounds` - границы мира

**Методы:**

```python
# Создание камеры
camera = Camera2D(scene, width=800, height=600)

# Обновление (вызывать каждый кадр)
camera.update(delta_time=1/60)

# Слежение за игроком
camera.follow(player, offset=(0, -50), smoothness=0.1)

# Остановка слежения
camera.stop_follow()

# Управление зумом
camera.set_zoom(2.0, instant=False)
camera.zoom_in(0.1)
camera.zoom_out(0.1)

# Установка границ
camera.set_bounds(left=0, top=0, right=2000, bottom=2000)

# Эффект дрожания
camera.shake(intensity=15, duration=0.5)

# Перемещение камеры
camera.move_to((500, 500), instant=False)

# Преобразование координат
screen_pos = camera.world_to_screen((1000, 500))
world_pos = camera.screen_to_world((400, 300))
```

---

## GUI система

### Класс Label

```python
class Label:
    def __init__(self, parent, text="", font=("Arial", 12), color="white", bg=None)
    def set_text(self, text)
    def set_color(self, color)
    def set_font(self, font)
    def pack(self, **kwargs)
    def place(self, x, y)
```

### Класс Button

```python
class Button:
    def __init__(self, parent, text="", command=None, font=("Arial", 12), 
                 color="white", bg="#333333")
    def set_text(self, text)
    def set_color(self, color)
    def set_bg(self, bg)
    def set_command(self, command)
    def pack(self, **kwargs)
    def place(self, x, y)
```

### Класс CheckBox

```python
class CheckBox:
    def __init__(self, parent, text="", default=False, on_change=None,
                 color="white", bg=None)
    def is_checked(self)
    def set_checked(self, checked)
    def set_text(self, text)
    def set_color(self, color)
    def pack(self, **kwargs)
```

### Класс Slider

```python
class Slider:
    def __init__(self, parent, from_=0, to=100, default=50, on_change=None,
                 length=200, bg=None)
    def get_value(self)
    def set_value(self, value)
    def pack(self, **kwargs)
```

### Класс DropDown

```python
class DropDown:
    def __init__(self, parent, items=[], default=None, on_select=None,
                 color="white", bg="#333333")
    def get_selected(self)
    def set_items(self, items)
    def set_color(self, color)
    def pack(self, **kwargs)
```

### Класс TextInput

```python
class TextInput:
    def __init__(self, parent, placeholder="", width=20, on_change=None,
                 color="white", bg="#333333", placeholder_color="gray")
    def get_text(self)
    def set_text(self, text)
    def set_color(self, color)
    def set_bg(self, bg)
    def clear(self)
    def pack(self, **kwargs)
```

### Класс Panel

```python
class Panel:
    def __init__(self, parent, bg=None)
    def pack(self, **kwargs)
    def place(self, x, y)
```

**Примеры GUI:**

```python
from gamelib.core.model.gui.gui_factory import Label, Button, Panel, TextInput

# Панель
panel = Panel(root, bg="#1a1a2e")
panel.place(x=10, y=10)

# Метка
label = Label(panel.widget, text="Привет!", font=("Arial", 14), color="#ffffff")
label.pack(pady=5)

# Кнопка
def on_click():
    print("Нажата кнопка!")

button = Button(panel.widget, text="Нажми", command=on_click)
button.pack(pady=5)

# Поле ввода
def on_text_change(text):
    print(f"Введено: {text}")

text_input = TextInput(panel.widget, placeholder="Введите имя", on_change=on_text_change)
text_input.pack(pady=5)

# Ползунок
def on_slider_change(value):
    print(f"Значение: {value}")

slider = Slider(panel.widget, from_=0, to=100, default=50, on_change=on_slider_change)
slider.pack(pady=5)
```

---

## Ввод с клавиатуры

### Класс InputManager

```python
class InputManager:
    def __init__(self, root)
    def is_key_down(self, expected_key)
```

**Методы:**

```python
# Создание менеджера ввода
input_manager = InputManager(window.root)

# Проверка нажатия клавиши
if input_manager.is_key_down('w'):
    # Движение вверх

# Поддерживаемые клавиши:
# - Буквы: 'a', 'b', 'c', ... 'z'
# - Стрелки: 'up', 'down', 'left', 'right'
# - Специальные: 'space', 'return', 'escape'
# - По коду: is_key_down(65)  # Код клавиши A
```

---

## Создание игры - полный гайд

### Шаг 1: Структура проекта

```
my_game/
├── main.py
├── assets/
│   ├── images/
│   ├── sounds/
│   └── music/
└── README.md
```

### Шаг 2: Базовый шаблон

```python
# main.py
import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *
from gamelib.core.model.gui.gui_factory import Label, Button, Panel

class MyGame(Game):
    def __init__(self):
        super().__init__("Название игры", 1024, 768, "#1a1a2e")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        self.main_scene = None
        self.player = None
        
    def setup(self):
        # Инициализация игры
        pass
    
    def update(self):
        # Игровая логика
        pass
    
    def create_gui(self):
        # Создание интерфейса
        pass

def main():
    game = MyGame()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()

if __name__ == "__main__":
    main()
```

### Шаг 3: Создание игрока

```python
def setup(self):
    # Создание сцены
    self.main_scene = Scene(self.window)
    self.scene_switcher.show_scene(self.main_scene)
    
    # Создание игрока
    self.player = gameObject.Rectangle(
        self.main_scene.canvas,
        x=400, y=500,
        width=50, height=50,
        color="#00ff88",
        scene=self.main_scene
    )
    
    # Добавление физики
    physics = BasePhisicComponent(mass=10, gravity=True)
    self.player.add_component(physics)
    
    # Добавление аудио
    audio = AudioSource()
    audio.add_sound("jump", "assets/sounds/jump.wav")
    self.player.add_component(audio)
    
    # Добавление коллайдера
    collider = Box_collider(is_trigger=False)
    self.player.add_component(collider)
    
    # Настройка ввода
    self.input_manager = InputManager(self.window.root)
    
    # Запуск игрового цикла
    self.window.root.after(16, self.game_loop)
```

### Шаг 4: Управление игроком

```python
def game_loop(self):
    if not self.paused and self.game_active:
        self.update_player()
    
    self.window.root.after(16, self.game_loop)

def update_player(self):
    x, y = self.player.get_position()
    
    # Движение
    if self.input_manager.is_key_down('a'):
        self.player.update_position(x - 5, y)
    if self.input_manager.is_key_down('d'):
        self.player.update_position(x + 5, y)
    
    # Прыжок
    if self.input_manager.is_key_down('space'):
        physics = self.get_physics_component()
        if physics:
            physics.impulse(12, Vector2(0, -1))
            audio = self.get_audio_component()
            if audio:
                audio.play("jump")

def get_physics_component(self):
    for comp in self.player.components:
        if isinstance(comp, BasePhisicComponent):
            return comp
    return None
```

### Шаг 5: Создание врагов

```python
class Enemy(gameObject.Rectangle):
    def __init__(self, canvas, x, y, scene):
        super().__init__(canvas, x=x, y=y, width=40, height=40, 
                        color="#ff4444", scene=scene)
        self.speed = 2
        self.direction = 1
        
    def update(self):
        x, y = self.get_position()
        new_x = x + self.speed * self.direction
        self.update_position(new_x, y)
        
        # Смена направления у границ
        if new_x <= 0 or new_x >= 800 - self.width:
            self.direction *= -1

# В классе игры
def setup(self):
    # ...
    self.enemies = []
    for i in range(5):
        enemy = Enemy(self.main_scene.canvas, 100 + i * 100, 200, self.main_scene)
        self.enemies.append(enemy)

def update(self):
    for enemy in self.enemies:
        enemy.update()
```

### Шаг 6: Система очков

```python
def __init__(self):
    # ...
    self.score = 0
    self.score_label = None

def create_gui(self):
    panel = Panel(self.window.root, bg="#0a0a1a")
    panel.place(x=10, y=10)
    
    self.score_label = Label(
        panel.widget,
        text=f"СЧЕТ: {self.score}",
        font=("Courier", 14, "bold"),
        color="#00ff88",
        bg="#0a0a1a"
    )
    self.score_label.pack(pady=5)

def add_score(self, points):
    self.score += points
    if self.score_label:
        self.score_label.set_text(f"СЧЕТ: {self.score}")
```

### Шаг 7: Коллизии и сбор предметов

```python
class Coin(gameObject.Rectangle):
    def __init__(self, canvas, x, y, scene):
        super().__init__(canvas, x=x, y=y, width=20, height=20, 
                        color="#ffff00", scene=scene)
        self.collected = False

def check_collisions(self):
    for coin in self.coins:
        if not coin.collected:
            if self.check_collision(self.player, coin):
                coin.collected = True
                self.main_scene.canvas.delete(coin.rect_id)
                self.add_score(10)
                self.play_sound("coin")

def check_collision(self, obj1, obj2):
    coords1 = obj1.get_coordinates()
    coords2 = obj2.get_coordinates()
    
    return (coords1[0] < coords2[2] and coords1[2] > coords2[0] and
            coords1[1] < coords2[3] and coords1[3] > coords2[1])
```

### Шаг 8: Камера

```python
def setup(self):
    # ...
    self.camera = Camera2D(self.main_scene, self.window.width, self.window.height)
    self.camera.follow(self.player, offset=(0, -100), smoothness=0.05)
    self.camera.set_bounds(0, 0, 2000, 2000)

def update(self):
    self.camera.update(1/60)
```

### Шаг 9: Музыка и звуки

```python
def setup(self):
    # Загрузка музыки
    global_audio.play_music("assets/music/background.mp3", loop=True, volume=0.5)
    global_audio.set_sound_volume(0.7)
    
    # Загрузка звуков
    global_audio.load_sound("jump", "assets/sounds/jump.wav")
    global_audio.load_sound("coin", "assets/sounds/coin.wav")
    global_audio.load_sound("death", "assets/sounds/death.wav")

def play_sound(self, sound_name):
    global_audio.play_sound(sound_name)
```

### Шаг 10: Состояния игры

```python
class GameState:
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

def __init__(self):
    # ...
    self.state = GameState.MENU

def update(self):
    if self.state == GameState.PLAYING:
        self.update_game()
    elif self.state == GameState.PAUSED:
        self.update_paused()
    elif self.state == GameState.GAME_OVER:
        self.update_game_over()

def toggle_pause(self):
    if self.state == GameState.PLAYING:
        self.state = GameState.PAUSED
        global_audio.play_music("", loop=False)  # Пауза музыки
    elif self.state == GameState.PAUSED:
        self.state = GameState.PLAYING
        global_audio.play_music("assets/music/background.mp3", loop=True)

def game_over(self):
    self.state = GameState.GAME_OVER
    global_audio.stop_music()
    global_audio.play_sound("death")
```

### Шаг 11: Полный пример игры

```python
import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *
from gamelib.core.model.gui.gui_factory import Label, Button, Panel

class PlatformerGame(Game):
    def __init__(self):
        super().__init__("Платформер", 1024, 768, "#1a1a2e")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        self.player = None
        self.platforms = []
        self.coins = []
        self.score = 0
        self.state = "playing"
        
    def setup(self):
        # Сцена
        self.main_scene = Scene(self.window)
        self.scene_switcher.show_scene(self.main_scene)
        
        # Земля
        ground = gameObject.Rectangle(
            self.main_scene.canvas, x=0, y=700,
            width=1024, height=68, color="#4a4a5e", scene=self.main_scene
        )
        self.platforms.append(ground)
        
        # Платформы
        platforms_data = [(200, 600, 100, 20), (500, 550, 100, 20), 
                          (800, 500, 100, 20), (350, 450, 100, 20),
                          (650, 400, 100, 20)]
        
        for x, y, w, h in platforms_data:
            plat = gameObject.Rectangle(
                self.main_scene.canvas, x=x, y=y, width=w, height=h,
                color="#5a5a7e", scene=self.main_scene
            )
            self.platforms.append(plat)
        
        # Игрок
        self.player = gameObject.Rectangle(
            self.main_scene.canvas, x=400, y=600,
            width=40, height=40, color="#00ff88", scene=self.main_scene
        )
        
        # Физика
        physics = BasePhisicComponent(mass=10, gravity=True)
        self.player.add_component(physics)
        
        # Коллайдер
        collider = Box_collider(is_trigger=False)
        self.player.add_component(collider)
        
        # Монетки
        for i in range(10):
            coin = gameObject.Rectangle(
                self.main_scene.canvas, x=100 + i * 80, y=300,
                width=20, height=20, color="#ffff00", scene=self.main_scene
            )
            self.coins.append(coin)
        
        # GUI
        self.create_gui()
        
        # Ввод
        self.input_manager = InputManager(self.window.root)
        
        # Звуки
        global_audio.load_sound("jump", "assets/sounds/jump.wav")
        global_audio.load_sound("coin", "assets/sounds/coin.wav")
        global_audio.play_music("assets/music/game.mp3", loop=True, volume=0.5)
        
        # Камера
        self.camera = Camera2D(self.main_scene, self.window.width, self.window.height)
        self.camera.follow(self.player, offset=(0, -100), smoothness=0.1)
        
        # Игровой цикл
        self.window.root.after(16, self.game_loop)
    
    def create_gui(self):
        panel = Panel(self.window.root, bg="#0a0a1a")
        panel.place(x=10, y=10)
        
        self.score_label = Label(
            panel.widget, text=f"СЧЕТ: {self.score}",
            font=("Courier", 14, "bold"), color="#00ff88", bg="#0a0a1a"
        )
        self.score_label.pack(pady=5)
    
    def game_loop(self):
        if self.state == "playing":
            self.update_game()
        
        self.camera.update(1/60)
        self.window.root.after(16, self.game_loop)
    
    def update_game(self):
        x, y = self.player.get_position()
        
        # Движение
        if self.input_manager.is_key_down('a'):
            self.player.update_position(x - 5, y)
        if self.input_manager.is_key_down('d'):
            self.player.update_position(x + 5, y)
        
        # Прыжок
        if self.input_manager.is_key_down('space'):
            physics = self.get_component(self.player, BasePhisicComponent)
            if physics and self.is_on_ground():
                physics.impulse(12, Vector2(0, -1))
                global_audio.play_sound("jump")
                self.window.root.after(200, lambda: None)
        
        # Сбор монет
        for coin in self.coins[:]:
            if self.check_collision(self.player, coin):
                self.coins.remove(coin)
                self.main_scene.canvas.delete(coin.rect_id)
                self.score += 10
                self.score_label.set_text(f"СЧЕТ: {self.score}")
                global_audio.play_sound("coin")
        
        # Проверка падения
        if y > 800:
            self.reset_game()
    
    def get_component(self, obj, component_type):
        for comp in obj.components:
            if isinstance(comp, component_type):
                return comp
        return None
    
    def is_on_ground(self):
        x, y = self.player.get_position()
        player_bottom = y + self.player.height
        
        for platform in self.platforms:
            px, py = platform.get_position()
            if (x + self.player.width > px and x < px + platform.width and
                abs(player_bottom - py) < 10):
                return True
        return False
    
    def check_collision(self, obj1, obj2):
        c1 = obj1.get_coordinates()
        c2 = obj2.get_coordinates()
        return (c1[0] < c2[2] and c1[2] > c2[0] and
                c1[1] < c2[3] and c1[3] > c2[1])
    
    def reset_game(self):
        self.player.update_position(400, 600)
        self.score = 0
        self.score_label.set_text(f"СЧЕТ: {self.score}")
        
        physics = self.get_component(self.player, BasePhisicComponent)
        if physics:
            physics.stop_gravity()
            physics.add_physic_enum()
    
    def update(self):
        pass

def main():
    game = PlatformerGame()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()

if __name__ == "__main__":
    main()
```

---

## Примеры

### Пример 1: Движение игрока

```python
class PlayerController(Component):
    def __init__(self, speed=5):
        super().__init__()
        self.speed = speed
        self.input_manager = None
    
    def set_game_object(self, obj):
        super().set_game_object(obj)
        self.input_manager = InputManager(obj.canvas.winfo_toplevel())
    
    def update(self):
        x, y = self.obj.get_position()
        
        if self.input_manager.is_key_down('a'):
            self.obj.update_position(x - self.speed, y)
        if self.input_manager.is_key_down('d'):
            self.obj.update_position(x + self.speed, y)

# Использование
player = gameObject.Rectangle(canvas, x=400, y=300, width=50, height=50, color="red")
player.add_component(PlayerController(speed=8))
```

### Пример 2: Патрулирующий враг

```python
class PatrolEnemy(gameObject.Rectangle):
    def __init__(self, canvas, x, y, width, height, color, scene, left_bound, right_bound):
        super().__init__(canvas, x=x, y=y, width=width, height=height, color=color, scene=scene)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = 2
        self.direction = 1
    
    def update(self):
        x, y = self.get_position()
        new_x = x + self.speed * self.direction
        
        if new_x <= self.left_bound or new_x + self.width >= self.right_bound:
            self.direction *= -1
        else:
            self.update_position(new_x, y)

# Использование
enemy = PatrolEnemy(scene.canvas, x=500, y=500, width=40, height=40, 
                    color="#ff4444", scene=scene, left_bound=300, right_bound=700)
```

### Пример 3: Пул объектов (оптимизация)

```python
class ObjectPool:
    def __init__(self, factory_method, size=10):
        self.pool = [factory_method() for _ in range(size)]
        self.active = []
    
    def get(self):
        if self.pool:
            obj = self.pool.pop()
            self.active.append(obj)
            return obj
        return None
    
    def release(self, obj):
        if obj in self.active:
            self.active.remove(obj)
            self.pool.append(obj)
    
    def update_all(self):
        for obj in self.active:
            obj.update()

# Использование
def create_bullet():
    return gameObject.Rectangle(scene.canvas, x=0, y=0, width=5, height=5, 
                                color="#ffff00", scene=scene)

bullet_pool = ObjectPool(create_bullet, size=20)

# Выстрел
bullet = bullet_pool.get()
if bullet:
    bullet.update_position(player_x, player_y)
```

### Пример 4: Анимация

```python
class Animation(Component):
    def __init__(self, frames, frame_duration=0.1, loop=True):
        super().__init__()
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.time = 0
    
    def update(self, delta_time):
        self.time += delta_time
        if self.time >= self.frame_duration:
            self.time = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
            
            self.update_frame()
    
    def update_frame(self):
        if hasattr(self.obj, 'image_comp'):
            self.obj.image_comp.set_image(self.frames[self.current_frame])

# Использование
frames = ["frame1.png", "frame2.png", "frame3.png"]
animation = Animation(frames, frame_duration=0.1, loop=True)
player.add_component(animation)
```

---

## Заключение

GameLib предоставляет все необходимые инструменты для создания 2D игр на Python. Фреймворк прост в использовании, но достаточно мощный для создания сложных проектов.

### Полезные советы:

1. **Оптимизация**: Используйте пулы объектов для часто создаваемых объектов
2. **Звуки**: Загружайте звуки при старте игры, а не во время игры
3. **Камера**: Используйте границы камеры для ограничения мира
4. **События**: Используйте систему событий для слабой связанности компонентов
5. **Физика**: Для простых игр достаточно встроенной физики

### Ресурсы:

- GitHub: https://github.com/yourusername/gamelib
- Примеры: /examples
- Документация: /docs

---

**© GameLib Framework - Создавайте игры с удовольствием!**