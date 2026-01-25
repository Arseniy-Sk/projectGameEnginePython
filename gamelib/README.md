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

Компонент с базовой физикой (передвижение) - ошибка.