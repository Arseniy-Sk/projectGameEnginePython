#!/usr/bin/env python3
import sys
import os
import argparse
from datetime import datetime


def create_game_project(game_name):
    clean_name = game_name.replace(' ', '_').replace('-', '_').lower()
    class_name = ''.join(word.capitalize() for word in clean_name.split('_'))
    filename = f"{clean_name}.py"
    
    if os.path.exists(filename):
        print(f"❌ Файл {filename} уже существует!")
        return False
    
    game_template = '''\"\"\"
{game_name}
Создано с помощью GameLib Framework
Дата: {date}
\"\"\"

import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *
from gamelib.core.model.gui.gui_factory import Label, Button, Panel


class {class_name}(Game):
    def __init__(self):
        super().__init__("{game_name}", 800, 600, "#1a1a2e")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        self.player = None
        self.objects = []
        self.score = 0
        self.game_active = True
        self.paused = False
        self.physics = None
        
    def setup(self):
        self.main_scene = Scene(self.window)
        self.create_world()
        self.create_player()
        self.create_gui()
        self.scene_switcher.show_scene(self.main_scene)
        self.input_manager = InputManager(self.window.root)
        self.window.root.after(16, self.game_loop)
    
    def create_world(self):
        self.main_scene.canvas.configure(bg='#1a1a2e')
        
        ground = gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=550,
            width=800, height=50,
            color='#2a2a3e',
            scene=self.main_scene
        )
        self.objects.append(ground)
        
        platforms = [(200, 500, 100, 20), (500, 450, 100, 20), (350, 400, 100, 20), (650, 480, 80, 20)]
        
        for x, y, w, h in platforms:
            plat = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y,
                width=w, height=h,
                color='#3a3a4e',
                scene=self.main_scene
            )
            self.objects.append(plat)
    
    def create_player(self):
        self.player = gameObject.Rectangle(
            self.main_scene.canvas,
            x=400, y=500,
            width=40, height=40,
            color='#00ff88',
            scene=self.main_scene
        )
        
        self.physics = BasePhisicComponent(mass=10, gravity=True)
        self.player.add_component(self.physics)
        
        gameObject.Rectangle(self.main_scene.canvas, x=410, y=510, width=8, height=8, color='#ffffff', scene=self.main_scene)
        gameObject.Rectangle(self.main_scene.canvas, x=422, y=510, width=8, height=8, color='#ffffff', scene=self.main_scene)
    
    def create_gui(self):
        top_panel = Panel(self.window.root, bg="#0d0d1a")
        top_panel.place(x=10, y=10)
        
        self.score_label = Label(top_panel.widget, text="СЧЕТ: 0", font=("Courier", 14, "bold"), color="#00ff88", bg="#0d0d1a")
        self.score_label.pack(padx=20, pady=10)
        
        self.status_label = Label(top_panel.widget, text="ИГРА", font=("Courier", 10, "bold"), color="#ffff00", bg="#0d0d1a")
        self.status_label.pack(padx=20, pady=5)
        
        right_panel = Panel(self.window.root, bg="#0d0d1a")
        right_panel.place(x=630, y=10)
        
        Button(right_panel.widget, text="СБРОС [R]", command=self.reset_game, font=("Courier", 10, "bold"), color="#ff8866", bg="#2a2a3e").pack(pady=3, padx=10, fill="x")
        Button(right_panel.widget, text="ПАУЗА [P]", command=self.toggle_pause, font=("Courier", 10, "bold"), color="#ffff00", bg="#2a2a3e").pack(pady=3, padx=10, fill="x")
        Button(right_panel.widget, text="ВЫХОД [ESC]", command=self.window.root.quit, font=("Courier", 10, "bold"), color="#ff6666", bg="#2a2a3e").pack(pady=3, padx=10, fill="x")
        
        Label(right_panel.widget, text="A/D - движение\\nSPACE - прыжок", font=("Courier", 8), color="#888888", bg="#0d0d1a").pack(pady=10)
    
    def game_loop(self):
        if self.game_active and not self.paused:
            self.update_game()
        self.window.root.after(16, self.game_loop)
    
    def update_game(self):
        if not self.player:
            return
        
        x, y = self.player.get_position()
        
        if self.input_manager.is_key_down('a'):
            self.player.update_position(x - 5, y)
        if self.input_manager.is_key_down('d'):
            self.player.update_position(x + 5, y)
        if self.input_manager.is_key_down('space') and hasattr(self, 'physics') and self.physics:
            self.physics.impulse(12, Vector2(0, -1))
            self.window.root.after(200, lambda: None)
    
    def toggle_pause(self):
        self.paused = not self.paused
        if hasattr(self, 'status_label'):
            self.status_label.set_text("ПАУЗА" if self.paused else "ИГРА")
    
    def reset_game(self):
        self.score = 0
        self.game_active = True
        self.paused = False
        if self.player:
            self.player.update_position(400, 500)
        if hasattr(self, 'score_label'):
            self.score_label.set_text("СЧЕТ: 0")
            self.status_label.set_text("ИГРА")
    
    def update(self):
        if self.input_manager:
            if self.input_manager.is_key_down('Escape'):
                self.window.root.quit()
            if self.input_manager.is_key_down('p'):
                self.toggle_pause()
                self.window.root.after(200, lambda: None)
            if self.input_manager.is_key_down('r'):
                self.reset_game()
                self.window.root.after(200, lambda: None)


def main():
    game = {class_name}()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()


if __name__ == "__main__":
    main()
'''
    
    game_template = game_template.format(
        game_name=game_name,
        class_name=class_name,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(game_template)
        
        print(f"\n✅ Игра '{game_name}' создана: {filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def list_projects():
    py_files = [f for f in os.listdir('.') if f.endswith('.py') and f not in ['create_game.py', 'setup.py']]
    if py_files:
        print("\n📁 Существующие игры:")
        for f in py_files:
            print(f"   • {f}")
    else:
        print("\n📁 Нет созданных игр")


def main_cli():
    parser = argparse.ArgumentParser(description='Создание игры на GameLib')
    parser.add_argument('name', nargs='?', help='Название игры')
    parser.add_argument('--list', '-l', action='store_true', help='Список игр')
    args = parser.parse_args()
    
    if args.list:
        list_projects()
    elif args.name:
        create_game_project(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main_cli()