Проект библиотеки для создания 2д (и возможно 3д) игр на языке программирования Python3.

Метод factory;
MVVM Model; 
Компонентная структура объектов;

Документация:

01. Подключение библиотеки
'''
from gamelib import *
'''

02. Инициализация движка
'''
GAME_ENGINE = Engine()
'''

03. Создание главного игрового окна
'''
MAIN_GAME_WINDOW = main_game_window("TEST game 1", 800, 600)
'''

04. Запуск главного цикла событий Tkinter
'''
MAIN_GAME_WINDOW.root.mainloop() #после описания создания всех объектов и gui
'''

05. Создание сцен
'''
SCENE_SWITCHER = SceneSwitcher()
'''

06. Создание базовых объектов
'''
obj1 = Rectangle(MainScene.canvas, [0, 0, 100, 100], 'red')
'''

07. Скрыть/показать сцену
'''
SCENE_SWITCHER.show_scene(MainScene)
'''

'''
SCENE_SWITCHER.close_scene(MainScene)
'''

08. Переключение активных сцен
'''
SCENE_SWITCHER.switch_scene(MainScene, SecondScene)
'''

09. Добавление изображения к base_gameObj
'''
obj2 = Rectangle(SecondScene.canvas, [0, 0, 100, 100], 'blue')
image_path = os.path.join(os.path.dirname(__file__), "resources/images/123123123.jpg")
ImageComponent(SecondScene.canvas, image_path)
'''

10. 





Пояснения
Теперь при подписке нужно указывать источник (конкретный объект или компонент) и тип события. Можно также подписаться на все события данного типа от любых объектов, передав source=None.

Встроенные события:

Физика: gravity_started, gravity_stopped, impulse_started, impulse_finished

Коллайдер: collision_enter, collision_exit, trigger_enter, trigger_exit

GameObject: position_changed, destroyed

ImageComponent: image_loaded

Пример кастомного события custom_event генерируется по таймеру.

Подписка на события от конкретных компонентов позволяет точно реагировать только на нужные объекты.

Эта система проста и легко расширяема. Можно добавлять новые типы событий в любом месте, просто вызывая global_bus.emit().


Отличная библиотека! Вижу, что вы создаете компонентно-ориентированный игровой движок на Tkinter. Вот полная документация:

# **Документация игрового движка GameLib**

## **Обзор архитектуры**

GameLib - это компонентно-ориентированный 2D игровой движок, построенный на базе Tkinter. Архитектура следует паттерну MVVM (Model-View-ViewModel) с использованием компонентной системы для игровых объектов.

### **Ключевые особенности:**
- Компонентная архитектура игровых объектов
- Система сцен и переключения между ними
- Физический движок с гравитацией и импульсами
- Система коллизий с триггерами
- Событийно-ориентированная архитектура (EventBus)
- Векторная математика
- Система ввода с поддержкой клавиатуры

---

## **01. Подключение библиотеки**

```python
from gamelib import *
```

Импортирует все основные компоненты библиотеки.

---

## **02. Инициализация движка**

### **Класс Engine**

```python
GAME_ENGINE = Engine(game=None)
```

**Параметры:**
- `game` (Game, optional): Экземпляр игры для управления

**Методы:**

| Метод | Описание | Параметры |
|-------|----------|-----------|
| `set_game(game)` | Устанавливает игру для обновления | `game`: экземпляр Game |
| `start_game_loop()` | Запускает игровой цикл в отдельном потоке | - |
| `stop_game_loop()` | Останавливает игровой цикл | - |
| `set_fps(fps)` | Устанавливает желаемый FPS | `fps`: кадров в секунду |
| `print_engine_info()` | Выводит информацию о версии движка | - |

**Пример:**
```python
engine = Engine()
engine.set_fps(60)
engine.print_engine_info()  # gamelib version: 0.1
```

---

## **03. Создание главного игрового окна**

### **Класс main_game_window**

```python
MAIN_GAME_WINDOW = main_game_window(name, width, height, background_color)
```

**Параметры:**
- `name` (str): Заголовок окна
- `width` (int): Ширина окна в пикселях
- `height` (int): Высота окна в пикселях
- `background_color` (str): Цвет фона (например, 'white', '#FF0000')

**Атрибуты:**
- `root`: Основной экземпляр Tkinter
- `width`/`height`: Размеры окна

**Методы:**
- `add_scene()`: Создает и возвращает новый canvas для сцены

**Пример:**
```python
window = main_game_window("My Game", 1024, 768, "black")
```

---

## **04. Запуск главного цикла событий Tkinter**

```python
MAIN_GAME_WINDOW.root.mainloop()
```

Запускает главный цикл обработки событий Tkinter. Должен вызываться после настройки всех игровых объектов.

---

## **05. Работа со сценами**

### **Класс Scene**

```python
scene = Scene(window)
# или
scene = Scene.create_scene(window)  # альтернативный конструктор
```

**Параметры:**
- `window`: Экземпляр главного игрового окна

**Атрибуты:**
- `canvas`: Canvas для отрисовки объектов сцены
- `gameObj_list`: Список игровых объектов на сцене
- `gui_list`: Список GUI элементов

**Методы:**
- `add_game_obj(obj)`: Добавляет игровой объект на сцену
- `show_gameObj_list()`: Выводит список объектов в консоль

### **Класс SceneSwitcher**

```python
switcher = SceneSwitcher()
```

**Методы:**

| Метод | Описание |
|-------|----------|
| `show_scene(scene)` | Показывает указанную сцену |
| `close_scene(scene)` | Скрывает указанную сцену |
| `switch_scene(scene1, scene2)` | Переключает с scene1 на scene2 |

**Пример:**
```python
switcher = SceneSwitcher()
main_scene = Scene(window)
game_scene = Scene(window)

switcher.show_scene(main_scene)
# ... через 3 секунды
switcher.switch_scene(main_scene, game_scene)
```

---

## **06. Создание игровых объектов**

### **Класс GameObject и gameObject.Rectangle**

```python
obj = gameObject.Rectangle(canvas, x, y, width, height, color, scene)
```

**Параметры:**
- `canvas`: Canvas для отрисовки
- `x`, `y` (int): Координаты левого верхнего угла
- `width`, `height` (int): Размеры прямоугольника
- `color` (str): Цвет заливки
- `scene` (Scene, optional): Сцена, на которую добавляется объект

**Методы GameObject:**

| Метод | Описание | Возвращает |
|-------|----------|------------|
| `get_coordinates()` | Координаты [x1, y1, x2, y2] | list |
| `get_position()` | Позиция [x, y] | list |
| `get_size()` | Размеры [width, height] | list |
| `get_center()` | Центр объекта [x, y] | list |
| `update_position(new_x, new_y)` | Обновляет позицию | - |
| `add_component(component)` | Добавляет компонент | self |

**Пример:**
```python
player = gameObject.Rectangle(
    scene.canvas,
    x=100, y=100,
    width=50, height=50,
    color='blue',
    scene=scene
)
```

---

## **07-08. Управление видимостью сцен**

```python
# Показать сцену
SCENE_SWITCHER.show_scene(MainScene)

# Скрыть сцену
SCENE_SWITCHER.close_scene(MainScene)

# Переключить сцены
SCENE_SWITCHER.switch_scene(MainScene, SecondScene)
```

---

## **09. Компонентная система**

### **Базовый класс Component**

```python
class Component:
    def __init__(self):
        self.obj = None
    
    def set_game_object(self, obj):
        self.obj = obj
```

### **ImageComponent - компонент изображения**

```python
img_comp = ImageComponent(image_path, use_object_coords=True)
obj.add_component(img_comp)
```

**Параметры:**
- `image_path` (str): Путь к файлу изображения
- `use_object_coords` (bool): Использовать координаты объекта

**Особенности:**
- Автоматически подгоняет изображение под размер объекта
- Создает изображение на canvas
- Генерирует событие 'image_loaded'

### **BasePhisicComponent - физический компонент**

```python
physics = BasePhisicComponent(mass, gravity=False)
obj.add_component(physics)
```

**Параметры:**
- `mass` (float): Масса объекта
- `gravity` (bool): Автоматически включить гравитацию

**Методы:**

| Метод | Описание | Параметры |
|-------|----------|-----------|
| `add_physic_enum()` | Включает гравитацию | - |
| `stop_gravity()` | Останавливает гравитацию | - |
| `impulse(force, vector, on_complete)` | Применяет импульс | `force`: сила, `vector`: Vector2 или угол, `on_complete`: callback |
| `stop_impulse()` | Останавливает текущий импульс | - |
| `set_position(dx, dy)` | Смещает объект | относительное смещение |
| `move_by_vector(vector, distance)` | Движение по вектору | |

**Пример:**
```python
# Включение гравитации
physics = BasePhisicComponent(mass=10, gravity=True)

# Импульс с вектором
physics.impulse(50, Vector2(1, 0), lambda: print("Готово!"))

# Импульс с углом
physics.impulse(30, 45)  # 45 градусов
```

### **Box_collider - компонент коллизий**

```python
collider = Box_collider(is_trigger=False)
obj.add_component(collider)
collider.check_collision(other_obj, callback_function)
```

**Параметры:**
- `is_trigger` (bool): True - только триггер (без остановки), False - физическое столкновение

**Методы:**
- `check_collision(obj2, function)`: Начинает проверку коллизий с obj2

**События:**
- Генерирует 'collision_enter' при столкновении

---

## **10. Система событий (EventBus)**

### **Классы Event и EventBus**

```python
from gamelib.core.model.events.events_system import global_bus
```

**Методы EventBus:**

| Метод | Описание |
|-------|----------|
| `subscribe(source, event_type, callback)` | Подписаться на события |
| `unsubscribe(source, event_type, callback)` | Отписаться |
| `emit(source, event_type, data)` | Сгенерировать событие |

**Пример подписки:**
```python
# На все события от конкретного объекта
global_bus.subscribe(player, None, my_callback)

# На конкретный тип события от любых объектов
global_bus.subscribe(None, 'collision_enter', on_collision)

# На все события вообще
global_bus.subscribe(None, None, on_any_event)
```

**Встроенные события:**

| Категория | События |
|-----------|---------|
| Физика | 'gravity_started', 'gravity_stopped', 'impulse_started', 'impulse_finished' |
| Коллизии | 'collision_enter' |
| GameObject | 'position_changed', 'destroyed' |
| Изображения | 'image_loaded' |

---

## **11. Векторная математика**

### **Класс Vector2**

```python
v = Vector2(x, y)
```

**Методы создания:**

| Метод | Описание |
|-------|----------|
| `from_angle(magnitude, angle_degrees)` | Создает вектор из угла |
| `from_points(x1, y1, x2, y2)` | Создает вектор из двух точек |

**Методы:**

| Метод | Описание |
|-------|----------|
| `magnitude()` | Длина вектора |
| `normalized()` | Нормализованный вектор |
| `angle()` | Угол в градусах |
| `scale(scalar)` | Умножение на скаляр |
| `add(other)` | Сложение векторов |
| `dot(other)` | Скалярное произведение |

**Пример:**
```python
v1 = Vector2(3, 4)
print(v1.magnitude())  # 5.0

v2 = Vector2.from_angle(10, 45)  # вектор длиной 10 под 45°
v3 = v1.normalized()  # (0.6, 0.8)
```

---

## **12. Система ввода**

### **Класс InputManager**

```python
input_manager = InputManager(root)
```

**Методы:**
- `is_key_down(expected_key)`: Проверяет, нажата ли клавиша

**Поддерживаемые форматы клавиш:**
- Буквы: 'a', 'b', ... 'z'
- Специальные: 'space', 'return', 'escape', 'up', 'down', 'left', 'right'
- Коды клавиш: 65 (A), 66 (B), ...

**Пример:**
```python
if input_manager.is_key_down('space'):
    player.jump()

if input_manager.is_key_down('left'):
    player.move_left()
```

---

## **13. Базовый класс Game**

```python
class MyGame(Game):
    def __init__(self):
        super().__init__("Title", 800, 600, "white")
    
    def setup(self):
        # Инициализация объектов
        pass
    
    def update(self):
        # Логика каждого кадра
        pass
    
    def end(self):
        # Очистка ресурсов
        pass
```

---

## **Разбор тестового примера test1.py**

### **Полный анализ примера**

```python
# Импорт и настройка путей
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gamelib import *
```

### **Этап 1: Инициализация движка и окна**
```python
GAME_ENGINE = Engine()
GAME_ENGINE.print_engine_info()  # Вывод версии

MAIN_GAME_WINDOW = main_game_window("TEST game 1", 800, 600, 'white')
```
Создается экземпляр движка и главное окно размером 800x600 с белым фоном.

### **Этап 2: Создание сцен**
```python
MainScene = Scene(MAIN_GAME_WINDOW)
SecondScene = Scene(MAIN_GAME_WINDOW)
SCENE_SWITCHER = SceneSwitcher()
```
Создаются две сцены и переключатель между ними.

### **Этап 3: Создание игровых объектов**
```python
obj1 = gameObject.Rectangle(MainScene.canvas, x=0, y=0, width=100, height=100, 
                            color='red', scene=MainScene)

obj2 = gameObject.Rectangle(SecondScene.canvas, x=50, y=50, width=100, height=100,
                            color='blue', scene=SecondScene)
```
Создаются прямоугольники на разных сценах.

### **Этап 4: Добавление компонентов**
```python
# Изображение
image_path = os.path.join(os.path.dirname(__file__), "resources/images/123123123.jpg")
img_comp = ImageComponent(image_path)
obj2.add_component(img_comp)

# Физика
physics_comp = BasePhisicComponent(mass=20, gravity=True)
obj2.add_component(physics_comp)

# Коллайдер
collider = Box_collider(is_trigger=False)
obj3.add_component(collider)
collider.check_collision(obj2, lambda: print("COLISION DETECTED!"))
```
Демонстрируется компонентная архитектура: объекты получают новые возможности через компоненты.

### **Этап 5: Тестирование физики**
Пример содержит три теста физической системы:

**Тест 1: Импульсы разной силы**
```python
physics_comp.impulse(20, Vector2(1, 0))  # Слабый, медленный
physics_comp_obj4.impulse(80, Vector2(1, -1).normalized())  # Сильный, быстрый
```
Демонстрирует, что сила импульса влияет на скорость движения.

**Тест 2: Последовательные импульсы**
```python
# Квадратное движение: вправо → вниз → влево → вверх
impulse_sequence = [
    {"force": 40, "vector": Vector2(1, 0)},
    {"force": 40, "vector": Vector2(0, 1)},
    {"force": 40, "vector": Vector2(-1, 0)},
    {"force": 40, "vector": Vector2(0, -1)}
]
```
Объект движется по квадрату, демонстрируя работу последовательных импульсов.

**Тест 3: Сравнение сил**
Создаются 5 объектов с разной силой импульса (10, 30, 60, 100, 150) для наглядного сравнения.

### **Этап 6: Таймеры и управление**
```python
MAIN_GAME_WINDOW.root.after(1000, debug_info)
MAIN_GAME_WINDOW.root.after(3000, switch_after_3_seconds)
MAIN_GAME_WINDOW.root.mainloop()
```
Используются таймеры Tkinter для отложенного выполнения функций.

---

## **Разбор тестового примера test2.py**

Этот пример демонстрирует более сложное использование библиотеки с наследованием от Game и системой событий.

### **Класс MyGame**
```python
class MyGame(Game):
    def __init__(self):
        super().__init__("2d game", 800, 600, background_color="black")
        self.frame_count = 0
        self.input_manager = None
```

### **Система событий в действии**
```python
# Подписка на события
global_bus.subscribe(self.red_obj, None, self.on_any_red_event)
global_bus.subscribe(self.blue_obj, 'impulse_finished', self.on_blue_impulse_finished)
global_bus.subscribe(None, 'position_changed', self.on_any_position_changed)

# Обработчики событий
def on_any_red_event(self, event):
    print(f"[Красный] {event.type} → {event.data}")

def on_blue_impulse_finished(self, event):
    print(f"[Синий] Импульс завершён: {event.data}")
```

### **Управление с клавиатуры**
```python
def update(self):
    if self.input_manager.is_key_down('e'):
        # Применить импульс к зеленому объекту
        green_physics.impulse(30, Vector2(0, -1))
    
    if self.input_manager.is_key_down('c'):
        # Генерация кастомного события
        global_bus.emit(self.green_obj, 'custom_event', 
                       {'message': 'Привет от зелёного!'})
```

---

## **Лучшие практики**

1. **Компонентный подход**: Группируйте функциональность в компоненты
2. **Событийная архитектура**: Используйте EventBus для слабой связанности
3. **Разделение на сцены**: Организуйте игру логическими блоками (меню, уровни)
4. **Обработка ошибок**: Проверяйте существование файлов и компонентов
5. **Оптимизация**: Не создавайте объекты каждый кадр, используйте пулы

---

## **Ограничения и особенности**

- Движок построен на Tkinter, что ограничивает производительность
- Однопоточная модель с отдельным потоком для игрового цикла
- Подходит для простых 2D игр и прототипов
- Встроенная система событий позволяет расширять функциональность

---

## **Заключение**

GameLib предоставляет гибкую компонентно-ориентированную архитектуру для создания 2D игр на Python. Благодаря системе событий, компонентам и векторной математике, библиотека подходит для обучения и создания небольших игровых проектов.





























```markdown
# GameLib - Игровой фреймворк на Python

GameLib - это простой и понятный фреймворк для создания 2D игр на Python с использованием Tkinter. Фреймворк построен на компонентной архитектуре и предоставляет все необходимые инструменты для быстрой разработки игр.

## Особенности

- 🎮 **Компонентная архитектура** - гибкая система компонентов для игровых объектов
- 🎬 **Система сцен** - удобное переключение между игровыми сценами
- ⚡ **Физический движок** - гравитация, импульсы, коллизии
- 🎯 **Система коллизий** - обнаружение столкновений с триггерами
- 📡 **Событийная система** - EventBus для слабой связанности компонентов
- 📐 **Векторная математика** - класс Vector2 для удобной работы с координатами
- ⌨️ **Система ввода** - обработка клавиатурного ввода
- 🎨 **GUI система** - простые и стильные элементы интерфейса
- 🖼️ **Работа с изображениями** - загрузка и отображение спрайтов
- 🎵 **Аудио система** - поддержка звуков и музыки (WAV, MP3)

## Установка

```bash
pip install -e .
```

### Требования

- Python 3.7+
- Tkinter (входит в стандартную установку Python)
- Pillow (для работы с изображениями)
- pydub (для аудио, опционально)

## Быстрый старт

```python
from gamelib import *

class MyGame(Game):
    def setup(self):
        # Создаем сцену
        scene = Scene(self.window)
        SceneSwitcher().show_scene(scene)
        
        # Создаем игрока
        self.player = gameObject.Rectangle(
            scene.canvas,
            x=100, y=100,
            width=50, height=50,
            color='red',
            scene=scene
        )
        
        # Добавляем физику
        physics = BasePhisicComponent(mass=10, gravity=True)
        self.player.add_component(physics)
        
        # Настраиваем ввод
        self.input_manager = InputManager(self.window.root)
    
    def update(self):
        # Движение игрока
        if self.input_manager.is_key_down('a'):
            x, y = self.player.get_position()
            self.player.update_position(x - 5, y)

# Запуск игры
game = MyGame()
engine = Engine(game)
game.set_engine(engine)
game.start()
game.window.root.mainloop()
```

## Основные компоненты

### 1. Создание игрового окна

```python
window = main_game_window("Название игры", 800, 600, "black")
```

### 2. Сцены

```python
# Создание сцены
scene = Scene(window)

# Переключение между сценами
switcher = SceneSwitcher()
switcher.show_scene(scene)
switcher.close_scene(scene)
switcher.switch_scene(scene1, scene2)
```

### 3. Игровые объекты

```python
# Создание прямоугольника
obj = gameObject.Rectangle(
    canvas,
    x=0, y=0,           # позиция
    width=100, height=100,  # размер
    color='red',        # цвет
    scene=scene
)

# Методы объекта
obj.get_position()      # получить позицию
obj.update_position(x, y)  # изменить позицию
obj.get_center()        # получить центр
obj.add_component(component)  # добавить компонент
```

### 4. Компоненты

#### Физический компонент

```python
physics = BasePhisicComponent(mass=20, gravity=True)
obj.add_component(physics)

# Применение импульса
physics.impulse(50, Vector2(1, 0))  # сила, направление
physics.stop_gravity()  # остановить гравитацию
```

#### Компонент изображения

```python
image = ImageComponent("путь/к/изображению.png")
obj.add_component(image)
```

#### Компонент коллизий

```python
collider = Box_collider(is_trigger=False)
obj.add_component(collider)
collider.check_collision(other_obj, on_collision)
```

### 5. GUI система

```python
from gamelib.core.model.gui.gui_factory import Label, Button, Panel

# Создание панели
panel = Panel(parent, bg="#1a1a2e")
panel.pack(pady=10)

# Текстовая метка
label = Label(panel.widget, text="Привет!", font=("Arial", 12), color="white", bg="#1a1a2e")
label.pack()

# Кнопка
def on_click():
    label.set_text("Нажато!")

button = Button(panel.widget, text="Нажми", command=on_click, color="white", bg="#333344")
button.pack()

# Чекбокс
checkbox = CheckBox(panel.widget, text="Опция", on_change=lambda checked: print(checked))

# Слайдер
slider = Slider(panel.widget, from_=0, to=100, on_change=lambda val: print(val))

# Выпадающий список
dropdown = DropDown(panel.widget, items=["1", "2", "3"], on_select=lambda item: print(item))

# Поле ввода
text_input = TextInput(panel.widget, placeholder="Введите текст...", on_change=lambda text: print(text))
```

### 6. Векторная математика

```python
from gamelib.core.model.vectors.verctor2 import Vector2

v = Vector2(10, 20)
v2 = Vector2.from_angle(100, 45)  # длина, угол
v3 = v.normalized()  # нормализация
length = v.magnitude()  # длина
angle = v.angle()  # угол в градусах
result = v + v2  # сложение
result = v * 2  # умножение на скаляр
```

### 7. Система событий

```python
from gamelib.core.model.events.events_system import global_bus

# Подписка на события
def on_collision(event):
    print(f"Столкновение: {event.data}")

global_bus.subscribe(player, 'collision_enter', on_collision)

# Генерация события
global_bus.emit(player, 'custom_event', {'data': 'value'})
```

### 8. Система ввода

```python
input_manager = InputManager(window.root)

# Проверка нажатия клавиш
if input_manager.is_key_down('w'):
    move_up()
if input_manager.is_key_down('space'):
    jump()
if input_manager.is_key_down('Escape'):
    quit_game()
```

### 9. Аудио система

```python
from gamelib.core.model.audio.audio_system import global_audio
from gamelib.core.model.components.audio_component import AudioSource

# Загрузка звука
audio = AudioSource()
audio.add_sound("jump", "sound.wav")
audio.play("jump")

# Фоновая музыка
global_audio.play_music("music.mp3", loop=True)
global_audio.stop_music()
global_audio.set_music_volume(0.5)
```

## Примеры

### Простая игра с платформером

```python
class Platformer(Game):
    def setup(self):
        scene = Scene(self.window)
        SceneSwitcher().show_scene(scene)
        
        # Игрок
        self.player = gameObject.Rectangle(
            scene.canvas, 100, 500, 30, 30, 'red', scene
        )
        self.physics = BasePhisicComponent(10, True)
        self.player.add_component(self.physics)
        
        # Земля
        ground = gameObject.Rectangle(
            scene.canvas, 0, 550, 800, 50, 'green', scene
        )
        
        self.input = InputManager(self.window.root)
    
    def update(self):
        if self.input.is_key_down('a'):
            x, y = self.player.get_position()
            self.player.update_position(x - 5, y)
        if self.input.is_key_down('d'):
            x, y = self.player.get_position()
            self.player.update_position(x + 5, y)
        if self.input.is_key_down('space'):
            self.physics.impulse(15, Vector2(0, -1))
```

## Структура проекта

```
gamelib/
├── core/
│   └── model/
│       ├── audio/          # Аудио система
│       ├── camera/         # Камера
│       ├── components/     # Компоненты (физика, коллизии, изображения)
│       ├── engine.py       # Основной движок
│       ├── events/         # Система событий
│       ├── factory/        # Фабрика объектов
│       ├── gui/            # GUI система
│       ├── input/          # Система ввода
│       ├── phisics/        # Физическая логика
│       ├── render/         # Рендеринг
│       ├── scenes/         # Система сцен
│       └── vectors/        # Векторная математика
└── data/                   # Данные и версии
```

## Горячие клавиши в примерах

- **W/A/S/D** - движение
- **Пробел** - прыжок/подача
- **P** - пауза
- **R** - сброс
- **ESC** - выход
- **Q/E** - зум камеры
- **F** - эффект дрожания камеры

## Лицензия

MIT License

## Автор

Zubanov A.S

## Благодарности

Фреймворк создан для обучения и быстрой разработки 2D игр на Python.
```