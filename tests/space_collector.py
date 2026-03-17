# space_collector_fixed.py
import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gamelib import *

# Константы игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
CRYSTAL_SIZE = 15
ASTEROID_SIZE = 25
WALL_SIZE = 10

class SpaceCollector(Game):
    def __init__(self):
        super().__init__("Space Collector", SCREEN_WIDTH, SCREEN_HEIGHT, "#000033")  # Темно-синий фон
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        
        # Списки объектов
        self.crystals = []
        self.asteroids = []
        
        # Для отладки
        self.debug_mode = True
        
    def setup(self):
        print("\n" + "="*50)
        print("SPACE COLLECTOR - ИСПРАВЛЕННАЯ ВЕРСИЯ")
        print("="*50)
        print("\nУПРАВЛЕНИЕ:")
        print("  ← → ↑ ↓ - движение")
        print("  SPACE - выстрел (остановка астероидов)")
        print("  P - пауза")
        print("  R - рестарт")
        print("  ESC - выход")
        print("\nЦЕЛЬ: Собирать зеленые кристаллы, избегать красных астероидов!")
        print("="*50 + "\n")
        
        # Создаем главную сцену
        self.main_scene = Scene(self.window)
        
        # Создаем игрока
        self.create_player()
        
        # Создаем стены
        self.create_walls()
        
        # Создаем GUI в отдельном фрейме
        self.setup_gui()
        
        # Показываем сцену
        self.scene_switcher.show_scene(self.main_scene)
        
        # Настраиваем ввод
        self.input_manager = InputManager(self.window.root)
        
        # Подписываемся на события
        self.setup_events()
        
        # Запускаем спавн объектов
        self.spawn_crystal()
        self.spawn_asteroid()
        
        print("=== ИГРА ЗАПУЩЕНА! ===\n")
    
    def create_player(self):
        """Создание игрока с компонентами"""
        # Основной объект - космический корабль (ромб)
        self.player = gameObject.Rectangle(
            self.main_scene.canvas,
            x=SCREEN_WIDTH//2 - PLAYER_SIZE//2,
            y=SCREEN_HEIGHT//2 - PLAYER_SIZE//2,
            width=PLAYER_SIZE,
            height=PLAYER_SIZE,
            color='cyan',
            scene=self.main_scene
        )
        
        # Добавляем физику с очень маленькой массой для быстрого движения
        self.player_physics = BasePhisicComponent(mass=5, gravity=False)
        self.player.add_component(self.player_physics)
        
        # Добавляем коллайдер
        self.player_collider = Box_collider(is_trigger=False)
        self.player.add_component(self.player_collider)
        
        print(f"✓ Игрок создан в позиции {self.player.get_position()}")
    
    def create_walls(self):
        """Создание стен по краям экрана"""
        wall_color = '#666666'
        
        # Верхняя стена
        self.top_wall = gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=0,
            width=SCREEN_WIDTH,
            height=WALL_SIZE,
            color=wall_color,
            scene=self.main_scene
        )
        
        # Нижняя стена
        self.bottom_wall = gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=SCREEN_HEIGHT - WALL_SIZE,
            width=SCREEN_WIDTH,
            height=WALL_SIZE,
            color=wall_color,
            scene=self.main_scene
        )
        
        # Левая стена
        self.left_wall = gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=0,
            width=WALL_SIZE,
            height=SCREEN_HEIGHT,
            color=wall_color,
            scene=self.main_scene
        )
        
        # Правая стена
        self.right_wall = gameObject.Rectangle(
            self.main_scene.canvas,
            x=SCREEN_WIDTH - WALL_SIZE, y=0,
            width=WALL_SIZE,
            height=SCREEN_HEIGHT,
            color=wall_color,
            scene=self.main_scene
        )
        
        # Добавляем коллайдеры к стенам
        for wall in [self.top_wall, self.bottom_wall, self.left_wall, self.right_wall]:
            collider = Box_collider(is_trigger=False)
            wall.add_component(collider)
            collider.check_collision(self.player, lambda: self.on_wall_collision())
    
    def setup_gui(self):
        """Настройка интерфейса"""
        # Создаем фрейм для GUI справа
        self.gui_frame = tk.Frame(self.window.root, bg='#222222', relief='raised', bd=3)
        self.gui_frame.place(x=SCREEN_WIDTH + 10, y=10, width=180, height=300)
        
        # Заголовок
        title_label = Label(self.gui_frame, "SPACE COLLECTOR", ("Arial", 12, "bold"))
        title_label.pack(pady=10)
        
        # Счет
        self.score_label = Label(
            self.gui_frame,
            f"Счет: {self.score}",
            ("Arial", 14, "bold")
        )
        self.score_label.pack(pady=5)
        
        # Жизни
        self.lives_label = Label(
            self.gui_frame,
            f"Жизни: {self.lives}",
            ("Arial", 14)
        )
        self.lives_label.pack(pady=5)
        
        # Статус
        self.status_label = Label(
            self.gui_frame,
            "ИГРА",
            ("Arial", 12, "bold")
        )
        self.status_label.pack(pady=10)
        
        # Кнопки управления
        pause_btn = Button(
            self.gui_frame,
            "Пауза (P)",
            self.toggle_pause,
            ("Arial", 10)
        )
        pause_btn.pack(pady=5, fill='x', padx=10)
        
        restart_btn = Button(
            self.gui_frame,
            "Рестарт (R)",
            self.restart_game,
            ("Arial", 10)
        )
        restart_btn.pack(pady=5, fill='x', padx=10)
        
        # Инструкция
        instr_text = "← → ↑ ↓ - движение\nSPACE - стоп\nESC - выход"
        instr_label = Label(
            self.gui_frame,
            instr_text,
            ("Arial", 9)
        )
        instr_label.pack(pady=10)
        
        # Сообщение Game Over (изначально скрыто)
        self.game_over_label = Label(
            self.window.root,
            "GAME OVER",
            ("Arial", 32, "bold")
        )
    
    def setup_events(self):
        """Подписка на события"""
        global_bus.subscribe(self.player, 'collision_enter', self.on_player_collision)
        global_bus.subscribe(self.player, 'position_changed', self.on_player_move)
        
        if self.debug_mode:
            global_bus.subscribe(None, None, self.debug_event)
    
    def debug_event(self, event):
        """Отладка событий"""
        if event.type in ['collision_enter', 'impulse_finished']:
            print(f"Событие: {event.type} от {type(event.source).__name__}")
    
    def spawn_crystal(self):
        """Создание кристалла"""
        if self.game_over:
            self.window.root.after(1000, self.spawn_crystal)
            return
        
        if not self.paused and len(self.crystals) < 5:  # Максимум 5 кристаллов
            # Случайная позиция
            x = random.randint(WALL_SIZE + 10, SCREEN_WIDTH - WALL_SIZE - CRYSTAL_SIZE - 10)
            y = random.randint(WALL_SIZE + 10, SCREEN_HEIGHT - WALL_SIZE - CRYSTAL_SIZE - 10)
            
            # Создаем кристалл
            crystal = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y,
                width=CRYSTAL_SIZE,
                height=CRYSTAL_SIZE,
                color='#00FF00',  # Ярко-зеленый
                scene=self.main_scene
            )
            
            # Добавляем коллайдер-триггер
            collider = Box_collider(is_trigger=True)
            crystal.add_component(collider)
            collider.check_collision(self.player, lambda c=crystal: self.collect_crystal(c))
            
            # Добавляем в список
            self.crystals.append(crystal)
            
            print(f"✨ Кристалл создан в позиции ({x}, {y})")
        
        # Планируем следующий спавн
        interval = random.randint(2000, 4000)
        self.window.root.after(interval, self.spawn_crystal)
    
    def spawn_asteroid(self):
        """Создание астероида"""
        if self.game_over:
            self.window.root.after(1000, self.spawn_asteroid)
            return
        
        if not self.paused and len(self.asteroids) < 3:  # Максимум 3 астероида
            # Выбираем сторону для спавна
            side = random.randint(0, 3)
            
            if side == 0:  # сверху
                x = random.randint(WALL_SIZE, SCREEN_WIDTH - WALL_SIZE - ASTEROID_SIZE)
                y = -ASTEROID_SIZE - 10
            elif side == 1:  # справа
                x = SCREEN_WIDTH + 10
                y = random.randint(WALL_SIZE, SCREEN_HEIGHT - WALL_SIZE - ASTEROID_SIZE)
            elif side == 2:  # снизу
                x = random.randint(WALL_SIZE, SCREEN_WIDTH - WALL_SIZE - ASTEROID_SIZE)
                y = SCREEN_HEIGHT + 10
            else:  # слева
                x = -ASTEROID_SIZE - 10
                y = random.randint(WALL_SIZE, SCREEN_HEIGHT - WALL_SIZE - ASTEROID_SIZE)
            
            # Создаем астероид
            asteroid = gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=y,
                width=ASTEROID_SIZE,
                height=ASTEROID_SIZE,
                color='#FF4444',  # Красный
                scene=self.main_scene
            )
            
            # Добавляем физику
            physics = BasePhisicComponent(mass=10, gravity=False)
            asteroid.add_component(physics)
            
            # Добавляем коллайдер
            collider = Box_collider(is_trigger=False)
            asteroid.add_component(collider)
            collider.check_collision(self.player, lambda a=asteroid: self.hit_by_asteroid(a))
            
            # Направление к центру экрана
            center_x, center_y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
            direction = Vector2(center_x - x, center_y - y).normalized()
            
            # Применяем импульс
            physics.impulse(random.randint(15, 25), direction)
            
            # Добавляем в список
            self.asteroids.append(asteroid)
            
            print(f"💫 Астероид создан")
        
        # Планируем следующий спавн
        interval = random.randint(3000, 5000)
        self.window.root.after(interval, self.spawn_asteroid)
    
    def collect_crystal(self, crystal):
        """Сбор кристалла"""
        if crystal in self.crystals and not self.game_over:
            self.crystals.remove(crystal)
            
            # Удаляем с канваса
            if hasattr(crystal, 'rect_id'):
                self.main_scene.canvas.delete(crystal.rect_id)
            
            # Обновляем счет
            self.score += 10
            
            # Обновляем GUI
            self.score_label.set_text(f"Счет: {self.score}")
            
            print(f"✓ Кристалл собран! Счет: {self.score}")
    
    def hit_by_asteroid(self, asteroid):
        """Столкновение с астероидом"""
        if self.game_over or self.paused:
            return
        
        self.lives -= 1
        self.lives_label.set_text(f"Жизни: {self.lives}")
        
        print(f"💥 Попадание! Осталось жизней: {self.lives}")
        
        if self.lives <= 0:
            self.game_over = True
            print("\n=== GAME OVER ===")
            self.status_label.set_text("GAME OVER")
            
            # Показываем сообщение
            self.game_over_label.pack(pady=200)
            
            # Останавливаем все импульсы
            for obj in self.asteroids:
                for comp in obj.components:
                    if isinstance(comp, BasePhisicComponent):
                        comp.stop_impulse()
        else:
            # Визуальный эффект попадания (мигание)
            self.flash_player()
    
    def flash_player(self):
        """Эффект мигания при попадании"""
        if hasattr(self.player, 'rect_id'):
            original_color = 'cyan'
            self.main_scene.canvas.itemconfig(self.player.rect_id, fill='white')
            self.window.root.after(100, lambda: self.main_scene.canvas.itemconfig(
                self.player.rect_id, fill=original_color))
    
    def on_wall_collision(self):
        """Столкновение со стеной"""
        # Просто отладочное сообщение
        pass
    
    def on_player_collision(self, event):
        """Обработчик столкновений игрока"""
        pass  # Обрабатываем в отдельных функциях
    
    def on_player_move(self, event):
        """Отслеживание движения игрока"""
        pass
    
    def toggle_pause(self):
        """Пауза/продолжение игры"""
        if not self.game_over:
            self.paused = not self.paused
            self.status_label.set_text("ПАУЗА" if self.paused else "ИГРА")
            print("⏸ Игра на паузе" if self.paused else "▶ Игра продолжена")
    
    def restart_game(self):
        """Рестарт игры"""
        print("\n🔄 Рестарт игры...")
        
        # Убираем сообщение Game Over
        self.game_over_label.pack_forget()
        
        # Очищаем кристаллы
        for crystal in self.crystals:
            if hasattr(crystal, 'rect_id'):
                self.main_scene.canvas.delete(crystal.rect_id)
        self.crystals.clear()
        
        # Очищаем астероиды
        for asteroid in self.asteroids:
            if hasattr(asteroid, 'rect_id'):
                self.main_scene.canvas.delete(asteroid.rect_id)
        self.asteroids.clear()
        
        # Сбрасываем игрока в центр
        self.player.update_position(
            SCREEN_WIDTH//2 - PLAYER_SIZE//2,
            SCREEN_HEIGHT//2 - PLAYER_SIZE//2
        )
        
        # Сбрасываем параметры
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        
        # Обновляем GUI
        self.score_label.set_text(f"Счет: {self.score}")
        self.lives_label.set_text(f"Жизни: {self.lives}")
        self.status_label.set_text("ИГРА")
        
        print("✓ Игра перезапущена!\n")
    
    def shoot(self):
        """Выстрел - останавливает ближайший астероид"""
        if self.game_over or self.paused:
            return
        
        player_x, player_y = self.player.get_center()
        closest_asteroid = None
        min_distance = float('inf')
        
        # Ищем ближайший астероид
        for asteroid in self.asteroids:
            ast_x, ast_y = asteroid.get_center()
            distance = math.sqrt((ast_x - player_x)**2 + (ast_y - player_y)**2)
            if distance < min_distance:
                min_distance = distance
                closest_asteroid = asteroid
        
        # Останавливаем ближайший астероид
        if closest_asteroid and min_distance < 200:
            for comp in closest_asteroid.components:
                if isinstance(comp, BasePhisicComponent):
                    comp.stop_impulse()
                    print(f"🎯 Астероид остановлен!")
                    break
    
    def update(self):
        """Игровой цикл"""
        if self.game_over or self.paused:
            return
        
        # Скорость движения игрока
        move_speed = 8
        
        # Управление с клавиатуры
        dx, dy = 0, 0
        
        if self.input_manager.is_key_down('Left'):
            dx = -move_speed
        if self.input_manager.is_key_down('Right'):
            dx = move_speed
        if self.input_manager.is_key_down('Up'):
            dy = -move_speed
        if self.input_manager.is_key_down('Down'):
            dy = move_speed
        
        # Применяем движение
        if dx != 0 or dy != 0:
            current_x, current_y = self.player.get_position()
            new_x = current_x + dx
            new_y = current_y + dy
            
            # Проверка границ
            new_x = max(WALL_SIZE, min(new_x, SCREEN_WIDTH - PLAYER_SIZE - WALL_SIZE))
            new_y = max(WALL_SIZE, min(new_y, SCREEN_HEIGHT - PLAYER_SIZE - WALL_SIZE))
            
            self.player.update_position(new_x, new_y)
        
        # Обработка клавиш
        if self.input_manager.is_key_down('space'):
            self.shoot()
        
        if self.input_manager.is_key_down('p'):
            self.toggle_pause()
            # Небольшая задержка чтобы не спамить
            self.window.root.after(200, lambda: None)
        
        if self.input_manager.is_key_down('r'):
            self.restart_game()
        
        if self.input_manager.is_key_down('Escape'):
            self.window.root.quit()
        
        # Проверка коллизий со стенами для астероидов
        for asteroid in self.asteroids[:]:
            x, y = asteroid.get_position()
            
            # Удаляем астероиды, улетевшие далеко
            if (x < -100 or x > SCREEN_WIDTH + 100 or 
                y < -100 or y > SCREEN_HEIGHT + 100):
                self.asteroids.remove(asteroid)
                self.main_scene.canvas.delete(asteroid.rect_id)

def main():
    # Создаем окно с правильными размерами (с учетом места для GUI)
    window_width = SCREEN_WIDTH + 200  # Добавляем место для GUI
    window_height = SCREEN_HEIGHT
    
    class CustomGame(SpaceCollector):
        def __init__(self):
            super().__init__()
            # Переопределяем размер окна
            self.window.width = window_width
            self.window.height = window_height
            self.window.root.geometry(f"{window_width}x{window_height}")
    
    # Создаем игру
    game = CustomGame()
    
    # Создаем движок
    engine = Engine(game)
    game.set_engine(engine)
    
    # Запускаем игру
    game.start()
    
    # Запускаем главный цикл
    game.window.root.mainloop()

if __name__ == "__main__":
    main()