# tests/test_camera.py
"""
Тестовая игра для демонстрации системы камеры в стиле Unity 2D
"""

import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *
from gamelib.core.model.camera.camera import Camera2D


class CameraDemoGame(Game):
    """Демонстрационная игра с камерой"""
    
    def __init__(self):
        super().__init__("Camera Demo - Unity Style 2D Camera", 1024, 768, "#1a1a2e")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        
        # Игровые объекты
        self.player = None
        self.platforms = []
        self.coins = []
        self.enemies = []
        
        # Камера
        self.camera = None
        
        # Физика игрока
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.can_jump = True
        
        # Счет
        self.score = 0
        self.coins_collected = 0
        
        # Состояние
        self.game_active = True
        self.show_info = True
        
        # Размеры мира
        self.world_width = 3000
        self.world_height = 2000
    
    def setup(self):
        print("\n" + "="*60)
        print("CAMERA DEMO GAME - Unity Style 2D Camera")
        print("="*60)
        print("\nУПРАВЛЕНИЕ:")
        print("  [A][D] - движение влево/вправо")
        print("  [W][Space] - прыжок")
        print("  [Q][E] - зум камеры")
        print("  [R] - сброс зума")
        print("  [F] - эффект дрожания")
        print("  [C] - центрировать на игроке")
        print("  [TAB] - показать/скрыть информацию")
        print("  [ESC] - выход")
        print("="*60 + "\n")
        
        # Создаем сцену
        self.main_scene = Scene(self.window)
        self.main_scene.canvas.configure(bg='#1a1a2e')
        
        # Создаем камеру
        self.camera = Camera2D(self.main_scene, self.window.width, self.window.height)
        
        # Создаем мир
        self.create_world()
        
        # Создаем игрока
        self.create_player()
        
        # Создаем монетки
        self.create_coins()
        
        # Создаем врагов
        self.create_enemies()
        
        # Настраиваем камеру
        self.camera.follow(self.player, offset=(0, -50), smoothness=0.08)
        self.camera.set_bounds(0, 0, self.world_width, self.world_height)
        
        # Показываем сцену
        self.scene_switcher.show_scene(self.main_scene)
        
        # Настраиваем ввод
        self.input_manager = InputManager(self.window.root)
        
        # Создаем GUI
        self.create_gui()
        
        # Запускаем игровой цикл
        self.window.root.after(16, self.game_loop)
        
        print("=== ИГРА ЗАПУЩЕНА ===\n")
    
    def create_world(self):
        """Создание игрового мира"""
        # Земля
        ground = gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=self.world_height - 50,
            width=self.world_width, height=50,
            color="#2a5a2a",
            scene=self.main_scene
        )
        self.platforms.append(ground)
        
        # Платформы
        platforms_data = [
            (300, self.world_height - 150, 150, 20),
            (600, self.world_height - 250, 120, 20),
            (1000, self.world_height - 200, 200, 20),
            (1400, self.world_height - 300, 100, 20),
            (1800, self.world_height - 180, 180, 20),
            (2200, self.world_height - 350, 130, 20),
            (2600, self.world_height - 250, 160, 20),
            (2800, self.world_height - 120, 100, 20),
        ]
        
        for x, y, w, h in platforms_data:
            platform = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y, width=w, height=h,
                color="#4a8a4a",
                scene=self.main_scene
            )
            self.platforms.append(platform)
            
            # Декоративная полоска (отдельный объект)
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x + 10, y=y - 3, width=w - 20, height=3,
                color="#6aaa6a",
                scene=self.main_scene
            )
        
        # Декоративные элементы - столбики
        for x in range(100, self.world_width, 200):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=self.world_height - 80, width=10, height=30,
                color="#5a8a3a",
                scene=self.main_scene
            )
        
        # Облака
        cloud_color = "#3a3a5a"
        clouds = [
            (500, 300, 80, 40), (550, 280, 60, 35), (450, 290, 50, 30),
            (1500, 200, 100, 45), (1560, 180, 70, 35), (1440, 190, 60, 30),
            (2500, 350, 90, 40), (2560, 330, 65, 35), (2440, 340, 55, 30),
        ]
        
        for x, y, w, h in clouds:
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y, width=w, height=h,
                color=cloud_color,
                scene=self.main_scene
            )
    
    def create_player(self):
        """Создание игрока"""
        self.player = gameObject.Rectangle(
            self.main_scene.canvas,
            x=500, y=self.world_height - 100,
            width=40, height=40,
            color="#ff6a4a",
            scene=self.main_scene
        )
        
        # Глаза
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=self.player.x + 8, y=self.player.y + 10,
            width=8, height=8, color="#ffffff",
            scene=self.main_scene
        )
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=self.player.x + 24, y=self.player.y + 10,
            width=8, height=8, color="#ffffff",
            scene=self.main_scene
        )
        
        # Зрачки
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=self.player.x + 10, y=self.player.y + 12,
            width=4, height=4, color="#000000",
            scene=self.main_scene
        )
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=self.player.x + 26, y=self.player.y + 12,
            width=4, height=4, color="#000000",
            scene=self.main_scene
        )
        
        # Улыбка (используем create_arc напрямую)
        self.main_scene.canvas.create_arc(
            self.player.x + 8, self.player.y + 20,
            self.player.x + 32, self.player.y + 35,
            start=0, extent=-180, fill="#ffaa88", outline="#ffaa88"
        )
    
    def create_coins(self):
        """Создание монеток"""
        coin_positions = []
        
        # Монетки на платформах
        for platform in self.platforms:
            for x in range(platform.x + 30, platform.x + platform.width - 30, 50):
                if x + 16 < platform.x + platform.width:
                    coin_positions.append((x, platform.y - 20))
        
        # Монетки в воздухе
        for i in range(40):
            x = random.randint(100, self.world_width - 100)
            y = random.randint(100, self.world_height - 200)
            coin_positions.append((x, y))
        
        for x, y in coin_positions[:80]:
            coin = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y, width=16, height=16,
                color="#ffcc44",
                scene=self.main_scene
            )
            # Блик
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x + 3, y=y + 3, width=10, height=10,
                color="#ffaa00",
                scene=self.main_scene
            )
            self.coins.append(coin)
    
    def create_enemies(self):
        """Создание врагов"""
        enemy_positions = [
            (800, self.world_height - 180, "red"),
            (1500, self.world_height - 280, "orange"),
            (2000, self.world_height - 210, "red"),
            (2500, self.world_height - 280, "orange"),
        ]
        
        for x, y, color in enemy_positions:
            enemy = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y, width=30, height=30,
                color=color,
                scene=self.main_scene
            )
            # Глаза
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x + 6, y=y + 8, width=6, height=6, color="#ffffff",
                scene=self.main_scene
            )
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x + 18, y=y + 8, width=6, height=6, color="#ffffff",
                scene=self.main_scene
            )
            self.enemies.append({
                'obj': enemy,
                'dir': 1,
                'speed': 2,
                'start_x': x,
                'range': 100
            })
    
    def create_gui(self):
        """Создание GUI панели"""
        self.info_panel = tk.Frame(self.window.root, bg='#0a0a1a', relief='raised', bd=2)
        self.info_panel.place(x=10, y=10, width=260, height=140)
        
        tk.Label(
            self.info_panel,
            text="CAMERA DEMO",
            font=("Courier", 12, "bold"),
            bg='#0a0a1a', fg='#00ff88'
        ).pack(pady=3)
        
        tk.Label(
            self.info_panel,
            text="="*25,
            font=("Courier", 8),
            bg='#0a0a1a', fg='#00aa88'
        ).pack()
        
        self.score_label = tk.Label(
            self.info_panel,
            text=f"Монет: {self.coins_collected}",
            font=("Courier", 10),
            bg='#0a0a1a', fg='#ffcc44'
        )
        self.score_label.pack(anchor='w', padx=10)
        
        self.pos_label = tk.Label(
            self.info_panel,
            text=f"Позиция: (0, 0)",
            font=("Courier", 9),
            bg='#0a0a1a', fg='#88ff88'
        )
        self.pos_label.pack(anchor='w', padx=10)
        
        self.zoom_label = tk.Label(
            self.info_panel,
            text=f"Зум: 1.0x",
            font=("Courier", 9),
            bg='#0a0a1a', fg='#88ff88'
        )
        self.zoom_label.pack(anchor='w', padx=10)
        
        self.status_label = tk.Label(
            self.info_panel,
            text="Статус: ИГРА",
            font=("Courier", 9, "bold"),
            bg='#0a0a1a', fg='#ffff00'
        )
        self.status_label.pack(anchor='w', padx=10)
    
    def update_player(self):
        """Обновление игрока"""
        if not self.game_active:
            return
        
        # Горизонтальное движение
        speed = 6
        if self.input_manager.is_key_down('a'):
            self.velocity_x = -speed
        elif self.input_manager.is_key_down('d'):
            self.velocity_x = speed
        else:
            self.velocity_x *= 0.9
        
        # Прыжок
        if (self.input_manager.is_key_down('w') or self.input_manager.is_key_down('space')):
            if self.on_ground and self.can_jump:
                self.velocity_y = -12
                self.on_ground = False
                self.can_jump = False
                self.status_label.config(text="Статус: ПРЫЖОК!")
                self.window.root.after(200, lambda: self.status_label.config(text="Статус: ИГРА"))
        
        # Гравитация
        self.velocity_y += 0.8
        if self.velocity_y > 15:
            self.velocity_y = 15
        
        # Обновление позиции по X
        new_x = self.player.x + self.velocity_x
        new_x = max(0, min(new_x, self.world_width - self.player.width))
        
        # Обновление позиции по Y
        new_y = self.player.y + self.velocity_y
        
        # Проверка столкновений с платформами
        self.on_ground = False
        
        for platform in self.platforms:
            # По горизонтали
            if (new_x < platform.x + platform.width and 
                new_x + self.player.width > platform.x):
                
                # Падение сверху
                if (self.player.y + self.player.height <= platform.y and 
                    new_y + self.player.height > platform.y and
                    self.velocity_y >= 0):
                    
                    new_y = platform.y - self.player.height
                    self.velocity_y = 0
                    self.on_ground = True
                    self.can_jump = True
        
        self.player.update_position(new_x, new_y)
        
        # Обновляем улыбку (пересоздаем)
        self.main_scene.canvas.delete("smile")
        self.main_scene.canvas.create_arc(
            self.player.x + 8, self.player.y + 20,
            self.player.x + 32, self.player.y + 35,
            start=0, extent=-180, fill="#ffaa88", outline="#ffaa88",
            tags="smile"
        )
        
        # Обновляем глаза
        for obj in self.main_scene.gameObj_list:
            if obj != self.player and obj.x > self.player.x - 10 and obj.x < self.player.x + 50:
                pass
    
    def update_coins(self):
        """Обновление монеток"""
        for coin in self.coins[:]:
            if self.check_collision(self.player, coin):
                self.coins.remove(coin)
                self.main_scene.canvas.delete(coin.rect_id)
                self.coins_collected += 1
                self.score += 10
                self.score_label.config(text=f"Монет: {self.coins_collected}")
                self.camera.shake(intensity=3, duration=0.1)
                self.status_label.config(text="Статус: +10 МОНЕТ!")
                self.window.root.after(200, lambda: self.status_label.config(text="Статус: ИГРА"))
    
    def update_enemies(self):
        """Обновление врагов"""
        for enemy in self.enemies:
            obj = enemy['obj']
            new_x = obj.x + enemy['speed'] * enemy['dir']
            
            if new_x <= enemy['start_x'] - enemy['range']:
                new_x = enemy['start_x'] - enemy['range']
                enemy['dir'] = 1
            elif new_x >= enemy['start_x'] + enemy['range']:
                new_x = enemy['start_x'] + enemy['range']
                enemy['dir'] = -1
            
            obj.update_position(new_x, obj.y)
            
            if self.check_collision(self.player, obj):
                self.velocity_y = -8
                self.velocity_x = (self.player.x - obj.x) * 0.3
                self.score = max(0, self.score - 5)
                self.camera.shake(intensity=8, duration=0.2)
                self.status_label.config(text="Статус: УДАР!")
                self.window.root.after(300, lambda: self.status_label.config(text="Статус: ИГРА"))
    
    def check_collision(self, obj1, obj2):
        """Проверка коллизии"""
        return (obj1.x < obj2.x + obj2.width and
                obj1.x + obj1.width > obj2.x and
                obj1.y < obj2.y + obj2.height and
                obj1.y + obj1.height > obj2.y)
    
    def game_loop(self):
        """Основной игровой цикл"""
        if self.game_active:
            self.update_player()
            self.update_enemies()
            self.update_coins()
            
            # Обновляем камеру
            self.camera.update(1/60)
            
            # Обновляем GUI
            self.pos_label.config(text=f"Позиция: ({self.player.x:.0f}, {self.player.y:.0f})")
            self.zoom_label.config(text=f"Зум: {self.camera.zoom:.1f}x")
        
        # Обработка ввода для камеры
        self.handle_camera_input()
        
        self.window.root.after(16, self.game_loop)
    
    def handle_camera_input(self):
        """Обработка ввода для управления камерой"""
        if self.input_manager.is_key_down('q'):
            self.camera.zoom_in(0.05)
        
        if self.input_manager.is_key_down('e'):
            self.camera.zoom_out(0.05)
        
        if self.input_manager.is_key_down('r'):
            self.camera.set_zoom(1.0, instant=True)
            self.status_label.config(text="Статус: ЗУМ СБРОШЕН")
            self.window.root.after(200, lambda: self.status_label.config(text="Статус: ИГРА"))
        
        if self.input_manager.is_key_down('f'):
            self.camera.shake(intensity=12, duration=0.4)
            self.status_label.config(text="Статус: ДРОЖАНИЕ!")
            self.window.root.after(400, lambda: self.status_label.config(text="Статус: ИГРА"))
        
        if self.input_manager.is_key_down('c'):
            self.camera.move_to((self.player.x + 20, self.player.y + 20), instant=True)
        
        if self.input_manager.is_key_down('Tab'):
            if self.show_info:
                self.info_panel.place_forget()
                self.show_info = False
            else:
                self.info_panel.place(x=10, y=10)
                self.show_info = True
        
        if self.input_manager.is_key_down('Escape'):
            self.game_active = False
            self.window.root.quit()
    
    def update(self):
        """Метод для движка"""
        pass


def main():
    """Запуск игры"""
    game = CameraDemoGame()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()


if __name__ == "__main__":
    main()