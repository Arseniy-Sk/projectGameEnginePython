# create_game.py
#!/usr/bin/env python3
"""
Скрипт для создания нового игрового проекта
Использование: python create_game.py <имя_игры>
"""

import sys
import os
import argparse
from datetime import datetime


def create_game_project(game_name):
    """
    Создает новый игровой проект с указанным именем
    
    :param game_name: имя игры (используется для названия файла и класса)
    """
    
    # Очищаем имя для использования в коде
    clean_name = game_name.replace(' ', '_').replace('-', '_').lower()
    class_name = ''.join(word.capitalize() for word in clean_name.split('_'))
    
    # Создаем имя файла
    filename = f"{clean_name}.py"
    
    # Проверяем, существует ли уже файл
    if os.path.exists(filename):
        print(f"❌ Файл {filename} уже существует!")
        return False
    
    # Содержимое файла (используем тройные кавычки и экранирование)
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
    \"\"\"Главный класс игры {game_name}\"\"\"
    
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
        print("\\n" + "="*60)
        print(f"🚀 ЗАПУСК ИГРЫ: {game_name}")
        print("="*60)
        print("\\nУПРАВЛЕНИЕ:")
        print("  [A][D] - движение влево/вправо")
        print("  [SPACE] - прыжок")
        print("  [P] - пауза")
        print("  [R] - сброс")
        print("  [ESC] - выход")
        print("="*60 + "\\n")
        
        # Создаем сцену
        self.main_scene = Scene(self.window)
        
        # Создаем мир
        self.create_world()
        
        # Создаем игрока
        self.create_player()
        
        # Создаем GUI
        self.create_gui()
        
        # Показываем сцену
        self.scene_switcher.show_scene(self.main_scene)
        
        # Настраиваем ввод
        self.input_manager = InputManager(self.window.root)
        
        # Запускаем игровой цикл
        self.window.root.after(16, self.game_loop)
        
        print("✅ ИГРА ГОТОВА! ИСПОЛЬЗУЙТЕ A/D И ПРОБЕЛ")
    
    def create_world(self):
        \"\"\"Создание игрового мира\"\"\"
        self.main_scene.canvas.configure(bg='#1a1a2e')
        
        # Земля
        ground = gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=550,
            width=800, height=50,
            color='#2a2a3e',
            scene=self.main_scene
        )
        self.objects.append(ground)
        
        # Платформы
        platforms = [
            (200, 500, 100, 20),
            (500, 450, 100, 20),
            (350, 400, 100, 20),
            (650, 480, 80, 20)
        ]
        
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
        \"\"\"Создание игрока\"\"\"
        self.player = gameObject.Rectangle(
            self.main_scene.canvas,
            x=400, y=500,
            width=40, height=40,
            color='#00ff88',
            scene=self.main_scene
        )
        
        # Добавляем физику
        self.physics = BasePhisicComponent(mass=10, gravity=True)
        self.player.add_component(self.physics)
        
        # Глаза
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=410, y=510,
            width=8, height=8,
            color='#ffffff',
            scene=self.main_scene
        )
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=422, y=510,
            width=8, height=8,
            color='#ffffff',
            scene=self.main_scene
        )
    
    def create_gui(self):
        \"\"\"Создание интерфейса\"\"\"
        # Верхняя панель
        top_panel = Panel(self.window.root, bg="#0d0d1a")
        top_panel.place(x=10, y=10)
        
        # Счет
        self.score_label = Label(
            top_panel.widget,
            text="СЧЕТ: 0",
            font=("Courier", 14, "bold"),
            color="#00ff88",
            bg="#0d0d1a"
        )
        self.score_label.pack(padx=20, pady=10)
        
        # Статус
        self.status_label = Label(
            top_panel.widget,
            text="ИГРА",
            font=("Courier", 10, "bold"),
            color="#ffff00",
            bg="#0d0d1a"
        )
        self.status_label.pack(padx=20, pady=5)
        
        # Правая панель с кнопками
        right_panel = Panel(self.window.root, bg="#0d0d1a")
        right_panel.place(x=630, y=10)
        
        # Кнопка сброса
        Button(
            right_panel.widget,
            text="СБРОС [R]",
            command=self.reset_game,
            font=("Courier", 10, "bold"),
            color="#ff8866",
            bg="#2a2a3e"
        ).pack(pady=3, padx=10, fill="x")
        
        # Кнопка паузы
        Button(
            right_panel.widget,
            text="ПАУЗА [P]",
            command=self.toggle_pause,
            font=("Courier", 10, "bold"),
            color="#ffff00",
            bg="#2a2a3e"
        ).pack(pady=3, padx=10, fill="x")
        
        # Кнопка выхода
        Button(
            right_panel.widget,
            text="ВЫХОД [ESC]",
            command=self.window.root.quit,
            font=("Courier", 10, "bold"),
            color="#ff6666",
            bg="#2a2a3e"
        ).pack(pady=3, padx=10, fill="x")
        
        # Инструкция
        Label(
            right_panel.widget,
            text="A/D - движение\\nSPACE - прыжок",
            font=("Courier", 8),
            color="#888888",
            bg="#0d0d1a"
        ).pack(pady=10)
    
    def game_loop(self):
        \"\"\"Игровой цикл\"\"\"
        if self.game_active and not self.paused:
            self.update_game()
        
        self.window.root.after(16, self.game_loop)
    
    def update_game(self):
        \"\"\"Обновление игровой логики\"\"\"
        if not self.player:
            return
        
        # Движение влево-вправо
        x, y = self.player.get_position()
        
        if self.input_manager.is_key_down('a'):
            self.player.update_position(x - 5, y)
        
        if self.input_manager.is_key_down('d'):
            self.player.update_position(x + 5, y)
        
        # Прыжок
        if self.input_manager.is_key_down('space'):
            if hasattr(self, 'physics') and self.physics:
                self.physics.impulse(12, Vector2(0, -1))
                self.window.root.after(200, lambda: None)
    
    def toggle_pause(self):
        \"\"\"Пауза\"\"\"
        self.paused = not self.paused
        if hasattr(self, 'status_label'):
            self.status_label.set_text("ПАУЗА" if self.paused else "ИГРА")
        print("⏸ ПАУЗА" if self.paused else "▶ ПРОДОЛЖЕНИЕ")
    
    def reset_game(self):
        \"\"\"Сброс игры\"\"\"
        self.score = 0
        self.game_active = True
        self.paused = False
        if self.player:
            self.player.update_position(400, 500)
        if hasattr(self, 'score_label'):
            self.score_label.set_text("СЧЕТ: 0")
            self.status_label.set_text("ИГРА")
        print("🔄 ИГРА СБРОШЕНА")
    
    def update(self):
        \"\"\"Метод для движка\"\"\"
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
    \"\"\"Запуск игры\"\"\"
    game = {class_name}()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()


if __name__ == "__main__":
    main()
'''
    
    # Заменяем переменные в шаблоне
    game_template = game_template.format(
        game_name=game_name,
        class_name=class_name,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # Записываем файл
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(game_template)
        
        print(f"\n✅ Игра '{game_name}' успешно создана!")
        print(f"📁 Файл: {filename}")
        print(f"🏷️  Класс: {class_name}")
        print(f"📂 Путь: {os.path.abspath(filename)}")
        print("\n📝 Как запустить:")
        print(f"   python {filename}")
        print("\n🎮 Игра содержит:")
        print("   - Игрока с физикой и прыжками")
        print("   - Платформы для прыжков")
        print("   - GUI панель со счетом")
        print("   - Управление A/D + Пробел")
        print("   - Кнопки паузы и сброса")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании файла: {e}")
        return False


def list_projects():
    """Показывает список существующих проектов"""
    py_files = [f for f in os.listdir('.') if f.endswith('.py') and f not in ['create_game.py', 'setup.py']]
    
    if py_files:
        print("\n📁 Существующие игровые проекты:")
        for f in py_files:
            size = os.path.getsize(f)
            print(f"   • {f} ({size} байт)")
    else:
        print("\n📁 Нет созданных игр")


def main_cli():
    """Консольный интерфейс"""
    parser = argparse.ArgumentParser(
        description='Создание нового игрового проекта на GameLib',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры:
  python create_game.py MyGame          - создать игру MyGame
  python create_game.py "Space Shooter" - создать игру с пробелом в названии
  python create_game.py --list          - показать все игры
        '''
    )
    
    parser.add_argument('name', nargs='?', help='Название игры')
    parser.add_argument('--list', '-l', action='store_true', help='Показать список игр')
    
    args = parser.parse_args()
    
    if args.list:
        list_projects()
    elif args.name:
        create_game_project(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main_cli()