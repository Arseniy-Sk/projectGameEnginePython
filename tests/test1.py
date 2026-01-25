# tests/test1.py
import sys
import os
import time 
# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import my library
from gamelib import *

# Initialization game engine
GAME_ENGINE = Engine()
# Test's Debug log
GAME_ENGINE.print_engine_info()

# Create main game window   
MAIN_GAME_WINDOW = main_game_window("TEST game 1", 800, 600)

# Create scenes using static method
MainScene = Scene(MAIN_GAME_WINDOW)
SecondScene = Scene(MAIN_GAME_WINDOW)

# Create SceneSwitcher
SCENE_SWITCHER = SceneSwitcher()

# Create test game_objects
obj1 = Rectangle(MainScene.canvas, [0, 0, 100, 100], 'red', MainScene)

obj2 = Rectangle(SecondScene.canvas, [50, 50, 150, 150], 'blue', SecondScene)
# Add Image Component
image_path = os.path.join(os.path.dirname(__file__), "resources/images/123123123.jpg")
img_comp = ImageComponent(obj2, image_path)

obj3 = Rectangle(SecondScene.canvas, [50, 200, 150, 300], 'green', SecondScene)

# Add Physic Component
physics_comp = BasePhisicComponent(SecondScene.canvas, obj2, 20)

# Show MainScene scene
SCENE_SWITCHER.show_scene(MainScene)

def debug_info():
    print("\n=== DEBUG INFO ===")
    print(f"obj2.components count: {len(obj2.components)}")
    for i, comp in enumerate(obj2.components):
        print(f"  Component {i}: {type(comp).__name__}")
    
    # Показываем статус гравитации
    if hasattr(physics_comp, 'is_gravity_active'):
        print(f"  Gravity active: {physics_comp.is_gravity_active}")
    
    print("==================\n")

def switch_after_3_seconds():
    SCENE_SWITCHER.switch_scene(MainScene, SecondScene)
    # debug_info()
    
    # Add Physic Enum for the Obj2
    physics_comp.add_physic_enum(MAIN_GAME_WINDOW.root)
    
    # Планируем перемещение через 5 секунд после запуска гравитации
    MAIN_GAME_WINDOW.root.after(5000, switch_position_after_5_seconds)

def switch_position_after_5_seconds():    
    if hasattr(physics_comp, 'stop_gravity'):
        physics_comp.stop_gravity()
    
    # Set new position Obj2
    physics_comp.set_position(300, 0)
    
    # Update canvas
    SecondScene.canvas.update()
    
    MAIN_GAME_WINDOW.root.after(2000, start_gravity_again)

def start_gravity_again():
    physics_comp.add_physic_enum(MAIN_GAME_WINDOW.root)


collider = Box_collider(obj3, MAIN_GAME_WINDOW.root, False) 
collider.check_collision(obj2, SecondScene.canvas, MAIN_GAME_WINDOW.root, print("COLISIOL COLISION"))


MAIN_GAME_WINDOW.root.after(1000, debug_info)
MAIN_GAME_WINDOW.root.after(3000, switch_after_3_seconds)

# Start the main screen event loop
MAIN_GAME_WINDOW.root.mainloop()