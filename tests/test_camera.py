# tests/test_camera.py
"""
Тестовая игра для демонстрации системы камеры.
Особенности:
- Следование камеры за игроком
- Зум (Q/E)
- Эффект дрожания при столкновениях
- Границы мира
- Платформер с физикой
"""

import sys
import os
import random
import math
import time


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *
from gamelib.core.model.camera.camera import Camera2D, CameraController

# Константы
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
WORLD_WIDTH = 3000
WORLD_HEIGHT = 2000
PLAYER_SIZE = 40
PLATFORM_HEIGHT = 30
COIN_SIZE = 20

class CameraTestGame(Game):
    """Тестовая игра для демонстрации камеры"""
    
    def __init__(self):
        super().__init__("Camera Test Game - 2D Camera Demo", SCREEN_WIDTH, SCREEN_HEIGHT, "#0a0a2a")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        
        # Игровые объекты
        self.player = None
        self.platforms = []
        self.coins = []
        self.enemies = []
        
        # Камера
        self.camera = None
        self.camera_controller = None
        
        # Физика игрока
        self.player_velocity_y = 0
        self.player_velocity_x = 0
        self.is_on_ground = False
        self.can_double_jump = True
        self.has_double_jumped = False
        
        # Счет и статистика
        self.score = 0
        self.coins_collected = 0
        self.frame_count = 0
        
        # Состояние игры
        self.game_active = True
        self.show_debug = True
        
    def setup(self):
        """Настройка игры"""
        print("\n" + "="*60)
        print("CAMERA TEST GAME - 2D Camera System Demo")
        print("="*60)
        print("\nУПРАВЛЕНИЕ:")
        print("  [A][D] - движение влево/вправо")
        print("  [W][Space] - прыжок (двойной прыжок доступен)")
        print("  [Q][E] - зум камеры")
        print("  [R] - сброс камеры")
        print("  [F] - дрожание камеры")
        print("  [C] - центрировать камеру на игроке")
        print("  [TAB] - показать/скрыть отладку")
        print("  [ESC] - выход")
        print("="*60 + "\n")
        
        # Создаем сцену
        self.main_scene = Scene(self.window)
        
        # Создаем камеру
        self.camera = Camera2D(self.main_scene, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Создаем контроллер камеры
        self.camera_controller = CameraController(self.camera)
        
        # Создаем игровой мир
        self.create_world()
        
        # Создаем игрока
        self.create_player()
        
        # Создаем врагов
        self.create_enemies()
        
        # Создаем монетки
        self.create_coins()
        
        # Настраиваем GUI
        self.setup_gui()
        
        # Настраиваем камеру
        self.camera.set_follow_target(self.player, offset=(0, 0), smooth=True, smooth_speed=4.0)
        self.camera.set_bounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
        self.camera.set_zoom(1.0, smooth=False)
        
        # Показываем сцену
        self.scene_switcher.show_scene(self.main_scene)
        
        # Настраиваем ввод
        self.input_manager = InputManager(self.window.root)
        
        # Запускаем игровой цикл
        self.window.root.after(16, self.game_loop)
        
        print("=== ИГРА ЗАПУЩЕНА ===\n")
        print("🟢 ИСПОЛЬЗУЙТЕ A/D ДЛЯ ДВИЖЕНИЯ, W/SPACE ДЛЯ ПРЫЖКА")
        print("🟢 КАМЕРА СЛЕДУЕТ ЗА ИГРОКОМ")
    
    def create_world(self):
        """Создание игрового мира"""
        # Фон (сетка для наглядности движения камеры)
        grid_color = "#2a2a4a"
        for x in range(0, WORLD_WIDTH, 100):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=0,
                width=2, height=WORLD_HEIGHT,
                color=grid_color,
                scene=self.main_scene
            )
        
        for y in range(0, WORLD_HEIGHT, 100):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=0, y=y,
                width=WORLD_WIDTH, height=2,
                color=grid_color,
                scene=self.main_scene
            )
        
        # Земля (основная платформа)
        ground = gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=WORLD_HEIGHT - 50,
            width=WORLD_WIDTH, height=50,
            color="#4a6a3a",
            scene=self.main_scene
        )
        self.platforms.append(ground)
        
        # Декоративные элементы на земле
        for x in range(50, WORLD_WIDTH, 150):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=WORLD_HEIGHT - 70,
                width=20, height=20,
                color="#6a8a5a",
                scene=self.main_scene
            )
        
        # Платформы разного уровня
        platforms_positions = [
            (300, WORLD_HEIGHT - 150, 200, PLATFORM_HEIGHT),
            (600, WORLD_HEIGHT - 250, 150, PLATFORM_HEIGHT),
            (1000, WORLD_HEIGHT - 200, 180, PLATFORM_HEIGHT),
            (1400, WORLD_HEIGHT - 300, 120, PLATFORM_HEIGHT),
            (1800, WORLD_HEIGHT - 180, 250, PLATFORM_HEIGHT),
            (2200, WORLD_HEIGHT - 350, 150, PLATFORM_HEIGHT),
            (2600, WORLD_HEIGHT - 280, 200, PLATFORM_HEIGHT),
            (2800, WORLD_HEIGHT - 120, 100, PLATFORM_HEIGHT),
        ]
        
        for x, y, w, h in platforms_positions:
            platform = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y,
                width=w, height=h,
                color="#5a7a4a",
                scene=self.main_scene
            )
            self.platforms.append(platform)
            
            # Добавляем полоски на платформы
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x + 10, y=y - 3,
                width=w - 20, height=3,
                color="#8aaa6a",
                scene=self.main_scene
            )
        
        # Декоративные столбы
        for x in [500, 1200, 1900, 2500]:
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=WORLD_HEIGHT - 200,
                width=30, height=150,
                color="#8a6a4a",
                scene=self.main_scene
            )
            
            # Верхушка столба
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x - 10, y=WORLD_HEIGHT - 210,
                width=50, height=15,
                color="#caaa7a",
                scene=self.main_scene
            )
    
    def create_player(self):
        """Создание игрока"""
        self.player = gameObject.Rectangle(
            self.main_scene.canvas,
            x=SCREEN_WIDTH//2 - PLAYER_SIZE//2,
            y=WORLD_HEIGHT - 100,
            width=PLAYER_SIZE,
            height=PLAYER_SIZE,
            color="#ff6a4a",
            scene=self.main_scene
        )
        
        # Глаза игрока
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=self.player.x + 8, y=self.player.y + 10,
            width=8, height=8,
            color="#ffffff",
            scene=self.main_scene
        )
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=self.player.x + 24, y=self.player.y + 10,
            width=8, height=8,
            color="#ffffff",
            scene=self.main_scene
        )
        
        # Зрачки
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=self.player.x + 10, y=self.player.y + 12,
            width=4, height=4,
            color="#000000",
            scene=self.main_scene
        )
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=self.player.x + 26, y=self.player.y + 12,
            width=4, height=4,
            color="#000000",
            scene=self.main_scene
        )
        
        # Улыбка
        self.main_scene.canvas.create_arc(
            self.player.x + 8, self.player.y + 20,
            self.player.x + 32, self.player.y + 32,
            start=0, extent=-180,
            fill="#ffaa88", outline="#ffaa88"
        )
    
    def create_enemies(self):
        """Создание врагов"""
        enemies_positions = [
            (500, WORLD_HEIGHT - 180, "red"),
            (1100, WORLD_HEIGHT - 230, "orange"),
            (1500, WORLD_HEIGHT - 330, "red"),
            (1900, WORLD_HEIGHT - 210, "orange"),
            (2300, WORLD_HEIGHT - 380, "red"),
            (2700, WORLD_HEIGHT - 310, "orange"),
        ]
        
        for x, y, color in enemies_positions:
            enemy = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y,
                width=30, height=30,
                color=color,
                scene=self.main_scene
            )
            self.enemies.append({
                'obj': enemy,
                'direction': 1,
                'speed': random.uniform(1, 2),
                'start_x': x,
                'move_range': 100
            })
            
            # Глаза врага
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x + 6, y=y + 8,
                width=6, height=6,
                color="#ffffff",
                scene=self.main_scene
            )
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x + 18, y=y + 8,
                width=6, height=6,
                color="#ffffff",
                scene=self.main_scene
            )
    
    def create_coins(self):
        """Создание монеток"""
        coins_positions = []
        
        # Монетки на платформах
        for platform in self.platforms:
            for x_offset in range(platform.x + 30, platform.x + platform.width - 30, 50):
                coins_positions.append((x_offset, platform.y - COIN_SIZE))
        
        # Дополнительные монетки в воздухе
        for i in range(30):
            x = random.randint(100, WORLD_WIDTH - 100)
            y = random.randint(100, WORLD_HEIGHT - 200)
            coins_positions.append((x, y))
        
        for x, y in coins_positions[:60]:  # Ограничиваем количество
            coin = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y,
                width=COIN_SIZE, height=COIN_SIZE,
                color="#ffcc44",
                scene=self.main_scene
            )
            
            # Внутренний блик
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x + 4, y=y + 4,
                width=COIN_SIZE - 8, height=COIN_SIZE - 8,
                color="#ffaa00",
                scene=self.main_scene
            )
            
            self.coins.append(coin)
    
    def setup_gui(self):
        """Настройка GUI"""
        # Фрейм для информации
        self.info_frame = tk.Frame(self.window.root, bg='#000000', relief='raised', bd=2)
        self.info_frame.place(x=10, y=10, width=250, height=120)
        
        # Заголовок
        tk.Label(
            self.info_frame,
            text="CAMERA TEST GAME",
            font=("Courier", 12, "bold"),
            bg='#000000', fg='#00ff00'
        ).pack(pady=2)
        
        tk.Label(
            self.info_frame,
            text="="*25,
            font=("Courier", 8),
            bg='#000000', fg='#00aa00'
        ).pack()
        
        # Счет
        self.score_label = tk.Label(
            self.info_frame,
            text=f"Монет: {self.coins_collected}",
            font=("Courier", 10),
            bg='#000000', fg='#ffff00'
        )
        self.score_label.pack(anchor='w', padx=10)
        
        # Позиция
        self.pos_label = tk.Label(
            self.info_frame,
            text=f"Позиция: (0, 0)",
            font=("Courier", 9),
            bg='#000000', fg='#00ff00'
        )
        self.pos_label.pack(anchor='w', padx=10)
        
        # Зум
        self.zoom_label = tk.Label(
            self.info_frame,
            text=f"Зум: 1.0x",
            font=("Courier", 9),
            bg='#000000', fg='#00ff00'
        )
        self.zoom_label.pack(anchor='w', padx=10)
        
        # Статус
        self.status_label = tk.Label(
            self.info_frame,
            text="Статус: ИГРА",
            font=("Courier", 9),
            bg='#000000', fg='#ffff00'
        )
        self.status_label.pack(anchor='w', padx=10)
        
        # Фрейм для отладки
        self.debug_frame = tk.Frame(self.window.root, bg='#000000', relief='sunken', bd=1)
        self.debug_frame.place(x=10, y=140, width=250, height=100)
        
        self.debug_label = tk.Label(
            self.debug_frame,
            text="[ОТЛАДКА]\nFPS: --\nОбъектов: --",
            font=("Courier", 8),
            bg='#000000', fg='#888888',
            justify='left'
        )
        self.debug_label.pack(pady=5, padx=5)
    
    def update_player_movement(self):
        """Обновление движения игрока"""
        if not self.game_active:
            return
        
        # Горизонтальное движение
        move_speed = 5
        if self.input_manager.is_key_down('a'):
            self.player_velocity_x = -move_speed
        elif self.input_manager.is_key_down('d'):
            self.player_velocity_x = move_speed
        else:
            self.player_velocity_x *= 0.9  # Трение
        
        # Прыжок
        if (self.input_manager.is_key_down('w') or self.input_manager.is_key_down('space')):
            if self.is_on_ground:
                self.player_velocity_y = -12
                self.is_on_ground = False
                self.has_double_jumped = False
                self.status_label.config(text="Статус: ПРЫЖОК!")
                self.window.root.after(200, lambda: self.status_label.config(text="Статус: ИГРА"))
            elif not self.has_double_jumped and self.can_double_jump:
                self.player_velocity_y = -10
                self.has_double_jumped = True
                self.status_label.config(text="Статус: ДВОЙНОЙ ПРЫЖОК!")
                self.window.root.after(200, lambda: self.status_label.config(text="Статус: ИГРА"))
        
        # Гравитация
        self.player_velocity_y += 0.8
        if self.player_velocity_y > 15:
            self.player_velocity_y = 15
        
        # Обновление позиции по X
        new_x = self.player.x + self.player_velocity_x
        new_x = max(0, min(new_x, WORLD_WIDTH - PLAYER_SIZE))
        
        # Обновление позиции по Y
        new_y = self.player.y + self.player_velocity_y
        
        # Проверка столкновений с платформами
        self.is_on_ground = False
        
        for platform in self.platforms:
            # Проверка коллизии по X
            if (new_x < platform.x + platform.width and 
                new_x + PLAYER_SIZE > platform.x):
                
                # Проверка коллизии по Y (падение сверху)
                if (self.player.y + PLAYER_SIZE <= platform.y and 
                    new_y + PLAYER_SIZE > platform.y and
                    self.player_velocity_y >= 0):
                    
                    new_y = platform.y - PLAYER_SIZE
                    self.player_velocity_y = 0
                    self.is_on_ground = True
                    self.has_double_jumped = False
                
                # Проверка коллизии по Y (прыжок снизу)
                elif (self.player.y >= platform.y + platform.height and
                      new_y < platform.y + platform.height):
                    
                    new_y = platform.y + platform.height
                    if self.player_velocity_y < 0:
                        self.player_velocity_y = 0
        
        # Обновляем позицию игрока
        self.player.update_position(new_x, new_y)
        
        # Обновляем глаза
        for comp in self.player.components:
            if hasattr(comp, 'update_position'):
                comp.update_position(self.player_velocity_x, self.player_velocity_y)
    
    def update_enemies(self):
        """Обновление врагов"""
        for enemy in self.enemies:
            obj = enemy['obj']
            new_x = obj.x + enemy['speed'] * enemy['direction']
            
            # Проверка границ движения
            if new_x <= enemy['start_x'] - enemy['move_range']:
                new_x = enemy['start_x'] - enemy['move_range']
                enemy['direction'] = 1
            elif new_x >= enemy['start_x'] + enemy['move_range']:
                new_x = enemy['start_x'] + enemy['move_range']
                enemy['direction'] = -1
            
            obj.update_position(new_x, obj.y)
            
            # Проверка столкновения с игроком
            if self.check_collision(self.player, obj):
                self.camera.shake(intensity=10, duration=0.3)
                self.player_velocity_y = -8
                self.player_velocity_x = (self.player.x - obj.x) * 0.5
                self.score = max(0, self.score - 5)
                self.status_label.config(text="Статус: УДАР!")
                self.window.root.after(300, lambda: self.status_label.config(text="Статус: ИГРА"))
    
    def update_coins(self):
        """Обновление монеток"""
        for coin in self.coins[:]:
            if self.check_collision(self.player, coin):
                self.coins.remove(coin)
                self.main_scene.canvas.delete(coin.rect_id)
                self.coins_collected += 1
                self.score += 10
                self.score_label.config(text=f"Монет: {self.coins_collected}")
                self.status_label.config(text=f"Статус: +10 МОНЕТ!")
                self.window.root.after(200, lambda: self.status_label.config(text="Статус: ИГРА"))
                self.camera.shake(intensity=3, duration=0.1)
    
    def check_collision(self, obj1, obj2):
        """Проверка коллизии двух объектов"""
        return (obj1.x < obj2.x + obj2.width and
                obj1.x + obj1.width > obj2.x and
                obj1.y < obj2.y + obj2.height and
                obj1.y + obj1.height > obj2.y)
    
    def game_loop(self):
        """Основной игровой цикл"""
        if self.game_active:
            self.update_player_movement()
            self.update_enemies()
            self.update_coins()
            
            # Обновляем камеру
            self.camera.update(1/60)
            
            # Обновляем GUI
            self.pos_label.config(text=f"Позиция: ({self.player.x:.0f}, {self.player.y:.0f})")
            self.zoom_label.config(text=f"Зум: {self.camera.zoom:.1f}x")
            
            if self.show_debug:
                self.debug_label.config(
                    text=f"[ОТЛАДКА]\n"
                         f"Камера: ({self.camera.position.x:.0f}, {self.camera.position.y:.0f})\n"
                         f"Скорость: ({self.player_velocity_x:.1f}, {self.player_velocity_y:.1f})\n"
                         f"На земле: {self.is_on_ground}\n"
                         f"Объектов: {len(self.platforms) + len(self.coins) + len(self.enemies) + 1}"
                )
        
        # Обработка ввода для камеры
        self.handle_camera_input()
        
        # Следующий кадр
        self.window.root.after(16, self.game_loop)
    
    def handle_camera_input(self):
        """Обработка ввода для управления камерой"""
        if self.input_manager.is_key_down('q'):
            self.camera.add_zoom(-0.05)
        
        if self.input_manager.is_key_down('e'):
            self.camera.add_zoom(0.05)
        
        if self.input_manager.is_key_down('r'):
            self.camera.set_zoom(1.0, smooth=True)
            self.camera.position = Vector2(self.player.x + PLAYER_SIZE//2, self.player.y + PLAYER_SIZE//2)
        
        if self.input_manager.is_key_down('f'):
            self.camera.shake(intensity=15, duration=0.5)
            self.status_label.config(text="Статус: ДРОЖАНИЕ!")
            self.window.root.after(500, lambda: self.status_label.config(text="Статус: ИГРА"))
        
        if self.input_manager.is_key_down('c'):
            self.camera_controller.focus_on_object(self.player)
        
        if self.input_manager.is_key_down('Tab'):
            self.show_debug = not self.show_debug
            if self.show_debug:
                self.debug_frame.place(x=10, y=140, width=250, height=100)
            else:
                self.debug_frame.place_forget()
        
        if self.input_manager.is_key_down('Escape'):
            self.game_active = False
            self.window.root.quit()
    
    def update(self):
        """Игровой цикл (вызывается движком)"""
        self.frame_count += 1

def main():
    """Запуск игры"""
    game = CameraTestGame()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()

if __name__ == "__main__":
    main()