# tests/test1.py
import sys
import os
import time 
import math

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import my library
from gamelib import *

# Initialization game engine
GAME_ENGINE = Engine()
# Test's Debug log
GAME_ENGINE.print_engine_info()

# Create main game window   
MAIN_GAME_WINDOW = main_game_window("TEST game 1 - Smooth Impulse", 800, 600, 'white')

# Create scenes using static method
MainScene = Scene(MAIN_GAME_WINDOW)
SecondScene = Scene(MAIN_GAME_WINDOW)

# Create SceneSwitcher
SCENE_SWITCHER = SceneSwitcher()

# Create test game_objects (новый синтаксис)
obj1 = gameObject.Rectangle(
    MainScene.canvas, 
    x=0, y=0, width=100, height=100, 
    color='red', 
    scene=MainScene
)

obj2 = gameObject.Rectangle(
    SecondScene.canvas, 
    x=50, y=50, width=100, height=100, 
    color='blue', 
    scene=SecondScene
)

# Add Image Component (новый синтаксис)
image_path = os.path.join(os.path.dirname(__file__), "resources/images/123123123.jpg")
if os.path.exists(image_path):
    img_comp = ImageComponent(image_path)
    obj2.add_component(img_comp)
else:
    print(f"Warning: Image not found at {image_path}")

obj3 = gameObject.Rectangle(
    SecondScene.canvas, 
    x=50, y=200, width=100, height=100, 
    color='green', 
    scene=SecondScene
)

obj4 = gameObject.Rectangle(
    SecondScene.canvas, 
    x=300, y=50, width=100, height=100, 
    color='purple', 
    scene=SecondScene
)

# Add Physic Component to obj2 and obj4 (НОВЫЙ СИНТАКСИС)
physics_comp = BasePhisicComponent(mass=20, gravity=True)
obj2.add_component(physics_comp)

physics_comp_obj4 = BasePhisicComponent(mass=15, gravity=False)
obj4.add_component(physics_comp_obj4)

# Show MainScene scene
SCENE_SWITCHER.show_scene(MainScene)

def debug_info():
    print("\n=== DEBUG INFO ===")
    print(f"obj2.components count: {len(obj2.components)}")
    for i, comp in enumerate(obj2.components):
        print(f"  Component {i}: {type(comp).__name__}")
    
    # Показываем статус гравитации
    print(f"  obj2 Gravity active: {physics_comp.is_gravity_active}")
    print(f"  obj4 Gravity active: {physics_comp_obj4.is_gravity_active}")
    
    # Показываем позиции объектов
    print(f"\n  Object positions:")
    print(f"  obj2 position: {obj2.get_position()}")
    print(f"  obj4 position: {obj4.get_position()}")
    
    print("==================\n")

def switch_after_3_seconds():
    SCENE_SWITCHER.switch_scene(MainScene, SecondScene)
    debug_info()
    
    # Запускаем тесты плавного импульса
    MAIN_GAME_WINDOW.root.after(1000, test_smooth_impulse)

def test_smooth_impulse():
    """Тестирование плавного импульса"""
    print("\n" + "="*50)
    print("TESTING SMOOTH IMPULSE")
    print("="*50)
    
    def on_impulse_complete(obj_name):
        print(f"\n✓ Импульс для {obj_name} завершен!")
    
    # Тест 1: Слабый импульс вправо (медленный)
    print("\n1. Слабый импульс (сила=20) вправо - должен быть медленным:")
    print(f"   Начальная позиция obj2: {obj2.get_position()}")
    
    physics_comp.impulse(20, Vector2(1, 0), 
                         lambda: on_impulse_complete("obj2 (слабый)"))
    
    # Тест 2: Сильный импульс вверх-вправо (быстрый)
    MAIN_GAME_WINDOW.root.after(1500, lambda: 
        print("\n2. Сильный импульс (сила=80) по диагонали - должен быть быстрым:"))
    
    MAIN_GAME_WINDOW.root.after(1600, lambda: 
        print(f"   Начальная позиция obj4: {obj4.get_position()}"))
    
    MAIN_GAME_WINDOW.root.after(1700, lambda:
        physics_comp_obj4.impulse(80, Vector2(1, -1).normalized(),
                                  lambda: on_impulse_complete("obj4 (сильный)")))
    
    # Тест 3: Очень сильный импульс (очень быстрый)
    MAIN_GAME_WINDOW.root.after(3500, lambda:
        print("\n3. Очень сильный импульс (сила=150) влево - должен быть очень быстрым:"))
    
    MAIN_GAME_WINDOW.root.after(3600, test_sequential_impulses)

def test_sequential_impulses():
    """Тестирование последовательных импульсов"""
    print("\n" + "="*50)
    print("TESTING SEQUENTIAL IMPULSES")
    print("="*50)
    
    # Создаем новый объект для теста
    test_obj = gameObject.Rectangle(
        SecondScene.canvas, 
        x=100, y=400, width=50, height=50, 
        color='orange', 
        scene=SecondScene
    )
    
    test_physics = BasePhisicComponent(mass=10, gravity=False)
    test_obj.add_component(test_physics)
    
    print(f"\nСоздан тестовый объект в позиции: {test_obj.get_position()}")
    print("Будет выполнен квадрат из 4 импульсов...")
    
    impulse_sequence = [
        {"force": 40, "vector": Vector2(1, 0), "name": "вправо"},
        {"force": 40, "vector": Vector2(0, 1), "name": "вниз"},
        {"force": 40, "vector": Vector2(-1, 0), "name": "влево"},
        {"force": 40, "vector": Vector2(0, -1), "name": "вверх"}
    ]
    
    current_step = 0
    
    def apply_next_impulse():
        nonlocal current_step
        
        if current_step < len(impulse_sequence):
            step = impulse_sequence[current_step]
            print(f"\n  Импульс {current_step + 1}: {step['name']} (сила={step['force']})")
            print(f"  Позиция перед импульсом: {test_obj.get_position()}")
            
            test_physics.impulse(
                step["force"], 
                step["vector"],
                lambda: MAIN_GAME_WINDOW.root.after(500, apply_next_impulse)
            )
            
            current_step += 1
        else:
            print(f"\n✓ Все импульсы завершены!")
            print(f"  Финальная позиция: {test_obj.get_position()}")
            print("  (Должна быть близка к начальной)")
            
            # Финальный тест - импульс разной силы
            MAIN_GAME_WINDOW.root.after(1000, test_various_forces)
    
    # Запускаем последовательность импульсов
    apply_next_impulse()

def test_various_forces():
    """Тестирование импульсов разной силы"""
    print("\n" + "="*50)
    print("TESTING VARIOUS FORCE LEVELS")
    print("="*50)
    
    # Создаем объекты для теста разной силы
    forces = [10, 30, 60, 100, 150]
    colors = ['red', 'blue', 'green', 'purple', 'orange']
    
    print(f"\nСоздаем {len(forces)} объектов с импульсами разной силы:")
    print("Чем больше сила - тем дальше и быстрее летит объект")
    
    objects = []
    
    for i, (force, color) in enumerate(zip(forces, colors)):
        # Создаем объект
        obj = gameObject.Rectangle(
            SecondScene.canvas, 
            x=50 + i*30, y=300, width=30, height=30, 
            color=color, 
            scene=SecondScene
        )
        
        phys = BasePhisicComponent(mass=15, gravity=False)
        obj.add_component(phys)
        objects.append((obj, phys, force, color))
        
        print(f"  Объект {i+1}: сила={force}, цвет={color}")
    
    # Применяем импульсы одновременно
    print("\nПрименяем импульсы одновременно (все вправо):")
    
    for obj, phys, force, color in objects:
        phys.impulse(force, Vector2(1, 0),
                    lambda f=force, c=color: 
                    print(f"    ✓ Импульс {c} (сила={f}) завершен"))
    
    # Финальное сообщение
    MAIN_GAME_WINDOW.root.after(5000, lambda:
        print("\n" + "="*50 +
              "\nALL TESTS COMPLETE!\n" +
              "Observe how different forces affect speed and distance.\n" +
              "Small force = slow movement\n" +
              "Large force = fast movement\n" +
              "="*50))

# Добавляем коллайдер к obj3 (НОВЫЙ СИНТАКСИС)
collider = Box_collider(is_trigger=False)
obj3.add_component(collider)
collider.check_collision(obj2, lambda: print("COLISION DETECTED!"))

MAIN_GAME_WINDOW.root.after(1000, debug_info)
MAIN_GAME_WINDOW.root.after(3000, switch_after_3_seconds)

# Start the main screen event loop
MAIN_GAME_WINDOW.root.mainloop()