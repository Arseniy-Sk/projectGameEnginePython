# space_collector.py
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *
from gamelib.core.model.events.events_system import global_bus

class SpaceCollector(Game):
    def __init__(self):
        super().__init__("Космический коллектор", 1024, 768, "midnight blue")
        self.scene_switcher = SceneSwitcher()
        self.frame_count = 0
        self.input_manager = None
        self.score = 0
        self.collectibles = []
        self.obstacles = []
        self.game_active = False
        self.game_over = False
        
        # Настройка игры
        self.game_scene = None
        self.menu_scene = None
        self.player = None
        
    def setup(self):
        """Инициализация игры"""
        # Создаем сцены
        self.menu_scene = Scene(self.window)
        self.game_scene = Scene(self.window)
        
        # Настраиваем меню
        self.setup_menu_scene()
        
        # Настраиваем игровую сцену
        self.setup_game_scene()
        
        # Показываем меню
        self.scene_switcher.show_scene(self.menu_scene)
        
        # Инициализируем систему ввода
        self.input_manager = InputManager(self.window.root)
        
        # Подписываемся на события
        self.setup_event_listeners()
        
        print("Игра инициализирована! Нажмите SPACE для старта")
    
    def setup_menu_scene(self):
        """Создание меню"""
        # Заголовок
        title = gameObject.Rectangle(
            self.menu_scene.canvas,
            x=312, y=200, width=400, height=80,
            color='gold',
            scene=self.menu_scene
        )
        
        # Создаем текстовый объект через компонент изображения
        # Вместо этого используем прямоугольники для создания надписей
        
        # Инструкции
        inst1 = gameObject.Rectangle(
            self.menu_scene.canvas,
            x=362, y=320, width=300, height=40,
            color='light blue',
            scene=self.menu_scene
        )
        
        inst2 = gameObject.Rectangle(
            self.menu_scene.canvas,
            x=362, y=380, width=300, height=40,
            color='light blue',
            scene=self.menu_scene
        )
        
        inst3 = gameObject.Rectangle(
            self.menu_scene.canvas,
            x=362, y=440, width=300, height=40,
            color='light blue',
            scene=self.menu_scene
        )
        
        # Анимированные звезды в меню
        for i in range(10):
            star = gameObject.Rectangle(
                self.menu_scene.canvas,
                x=random.randint(50, 974),
                y=random.randint(50, 718),
                width=5, height=5,
                color='white',
                scene=self.menu_scene
            )
            # Добавляем небольшую гравитацию для эффекта падающих звезд
            star_physics = BasePhisicComponent(mass=random.randint(1, 5), gravity=True)
            star.add_component(star_physics)
            
    def setup_game_scene(self):
        """Создание игровой сцены"""
        # Создаем игрока - космический корабль (зеленый треугольник через прямоугольник)
        self.player = gameObject.Rectangle(
            self.game_scene.canvas,
            x=512, y=684, width=40, height=40,
            color='lime green',
            scene=self.game_scene
        )
        
        # Добавляем физику игроку
        player_physics = BasePhisicComponent(mass=20, gravity=False)
        self.player.add_component(player_physics)
        
        # Добавляем коллайдер для игрока
        player_collider = Box_collider(is_trigger=True)
        self.player.add_component(player_collider)
        
        # Создаем границы экрана (невидимые стены)
        self.create_boundaries()
        
        # Создаем первоначальные объекты
        self.spawn_collectibles(5)
        self.spawn_obstacles(3)
        
        # Добавляем информацию о счете (используем прямоугольники как индикаторы)
        self.score_display = gameObject.Rectangle(
            self.game_scene.canvas,
            x=10, y=10, width=200, height=30,
            color='dark blue',
            scene=self.game_scene
        )
    
    def create_boundaries(self):
        """Создание границ экрана"""
        # Левая стена
        left_wall = gameObject.Rectangle(
            self.game_scene.canvas,
            x=-10, y=0, width=10, height=768,
            color='gray',
            scene=self.game_scene
        )
        left_wall_physics = BasePhisicComponent(mass=1000, gravity=False)
        left_wall.add_component(left_wall_physics)
        
        # Правая стена
        right_wall = gameObject.Rectangle(
            self.game_scene.canvas,
            x=1024, y=0, width=10, height=768,
            color='gray',
            scene=self.game_scene
        )
        right_wall_physics = BasePhisicComponent(mass=1000, gravity=False)
        right_wall.add_component(right_wall_physics)
        
        # Верхняя стена
        top_wall = gameObject.Rectangle(
            self.game_scene.canvas,
            x=0, y=-10, width=1024, height=10,
            color='gray',
            scene=self.game_scene
        )
        top_wall_physics = BasePhisicComponent(mass=1000, gravity=False)
        top_wall.add_component(top_wall_physics)
        
        # Нижняя стена (с ней игрок проигрывает)
        bottom_wall = gameObject.Rectangle(
            self.game_scene.canvas,
            x=0, y=768, width=1024, height=10,
            color='red',
            scene=self.game_scene
        )
        bottom_wall_physics = BasePhisicComponent(mass=1000, gravity=False)
        bottom_wall.add_component(bottom_wall_physics)
    
    def spawn_collectibles(self, count):
        """Создание собираемых объектов (золотые монеты)"""
        for i in range(count):
            x = random.randint(100, 900)
            y = random.randint(100, 600)
            
            collectible = gameObject.Rectangle(
                self.game_scene.canvas,
                x=x, y=y, width=25, height=25,
                color='gold',
                scene=self.game_scene
            )
            
            # Добавляем физику с гравитацией
            collect_physics = BasePhisicComponent(mass=5, gravity=True)
            collectible.add_component(collect_physics)
            
            # Добавляем коллайдер как триггер
            collect_collider = Box_collider(is_trigger=True)
            collectible.add_component(collect_collider)
            
            # Проверяем коллизию с игроком
            collect_collider.check_collision(self.player, 
                                           lambda obj=collectible: self.collect_item(obj))
            
            self.collectibles.append(collectible)
    
    def spawn_obstacles(self, count):
        """Создание препятствий (красные астероиды)"""
        for i in range(count):
            x = random.randint(100, 900)
            y = random.randint(100, 500)
            
            obstacle = gameObject.Rectangle(
                self.game_scene.canvas,
                x=x, y=y, width=40, height=40,
                color='red',
                scene=self.game_scene
            )
            
            # Добавляем физику
            obst_physics = BasePhisicComponent(mass=30, gravity=True)
            obstacle.add_component(obst_physics)
            
            # Добавляем коллайдер (не триггер - физическое столкновение)
            obst_collider = Box_collider(is_trigger=False)
            obstacle.add_component(obst_collider)
            
            # Проверяем коллизию с игроком
            obst_collider.check_collision(self.player, 
                                        lambda: self.hit_obstacle())
            
            self.obstacles.append(obstacle)
    
    def setup_event_listeners(self):
        """Настройка подписок на события"""
        # Следим за позицией игрока
        global_bus.subscribe(self.player, 'position_changed', self.on_player_move)
        
        # Следим за коллизиями
        global_bus.subscribe(None, 'collision_enter', self.on_collision)
        
        # Следим за завершением импульсов
        global_bus.subscribe(None, 'impulse_finished', self.on_impulse_finished)
    
    def on_player_move(self, event):
        """Обработка движения игрока"""
        # Проверяем, не упал ли игрок за нижнюю границу
        pos = event.data['new']
        if pos[1] > 750:  # Близко к нижней границе
            self.game_over = True
            self.game_active = False
            print("ИГРА ОКОНЧЕНА! Вы упали!")
    
    def on_collision(self, event):
        """Обработка столкновений"""
        if event.source == self.player:
            other = event.data.get('other')
            if other and other in self.collectibles:
                # Событие сбора обрабатывается в collect_item
                pass
    
    def on_impulse_finished(self, event):
        """Обработка завершения импульса"""
        if event.source == self.player:
            print("Импульс игрока завершен")
    
    def collect_item(self, item):
        """Сбор предмета"""
        if item in self.collectibles:
            self.collectibles.remove(item)
            self.score += 10
            print(f"Собрано! Счет: {self.score}")
            
            # Удаляем объект с канваса
            if hasattr(item, 'rect_id') and self.game_scene.canvas:
                self.game_scene.canvas.delete(item.rect_id)
            
            # Создаем новый предмет
            if len(self.collectibles) < 5:
                self.spawn_collectibles(1)
    
    def hit_obstacle(self):
        """Столкновение с препятствием"""
        self.score = max(0, self.score - 5)
        print(f"Столкновение! Счет: {self.score}")
        
        # Отбрасываем игрока
        player_physics = next(c for c in self.player.components 
                            if isinstance(c, BasePhisicComponent))
        
        # Случайное направление отскока
        angle = random.randint(0, 360)
        player_physics.impulse(20, angle)
    
    def start(self):
        """Запуск игры"""
        super().start()
        print("Космический коллектор запущен!")
    
    def update(self):
        """Обновление каждого кадра"""
        self.frame_count += 1
        
        if not self.game_active and not self.game_over:
            # В меню - проверяем пробел для старта
            if self.input_manager.is_key_down('space'):
                self.start_game()
        
        elif self.game_active:
            # Управление игроком (только если игра активна)
            self.handle_player_input()
            
            # Обновляем отображение счета
            if self.frame_count % 30 == 0:
                print(f"Текущий счет: {self.score}")
        
        elif self.game_over:
            # Обработка окончания игры
            if self.input_manager.is_key_down('r'):
                self.restart_game()
    
    def handle_player_input(self):
        """Обработка ввода игрока"""
        player_physics = next(c for c in self.player.components 
                            if isinstance(c, BasePhisicComponent))
        
        # Движение по WASD
        move_force = 15
        move_vector = Vector2(0, 0)
        
        if self.input_manager.is_key_down('w'):
            move_vector = move_vector.add(Vector2(0, -1))
        if self.input_manager.is_key_down('s'):
            move_vector = move_vector.add(Vector2(0, 1))
        if self.input_manager.is_key_down('a'):
            move_vector = move_vector.add(Vector2(-1, 0))
        if self.input_manager.is_key_down('d'):
            move_vector = move_vector.add(Vector2(1, 0))
        
        # Применяем импульс, если есть движение
        if move_vector.magnitude() > 0:
            player_physics.impulse(move_force, move_vector.normalized())
        
        # Специальные способности
        if self.input_manager.is_key_down('shift_l') or self.input_manager.is_key_down('Shift_L'):
            # Рывок
            mouse_pos = self.get_mouse_position()
            if mouse_pos:
                player_pos = self.player.get_center()
                direction = Vector2(mouse_pos[0] - player_pos[0], 
                                  mouse_pos[1] - player_pos[1])
                if direction.magnitude() > 0:
                    player_physics.impulse(40, direction.normalized())
        
        # Остановка движения
        if self.input_manager.is_key_down('x'):
            player_physics.stop_impulse()
    
    def get_mouse_position(self):
        """Получение позиции мыши (упрощенно)"""
        # В реальном проекте здесь была бы реализация получения координат мыши
        return None
    
    def start_game(self):
        """Начало игры"""
        self.game_active = True
        self.game_over = False
        self.score = 0
        self.scene_switcher.switch_scene(self.menu_scene, self.game_scene)
        print("ИГРА НАЧАЛАСЬ! Собирайте золотые монеты, избегайте красные препятствия!")
        print("Управление: WASD - движение, Shift + клик - рывок, X - стоп")
    
    def restart_game(self):
        """Перезапуск игры"""
        # Очищаем сцену
        for obj in self.collectibles + self.obstacles:
            if hasattr(obj, 'rect_id') and self.game_scene.canvas:
                self.game_scene.canvas.delete(obj.rect_id)
        
        self.collectibles = []
        self.obstacles = []
        
        # Возвращаем игрока на стартовую позицию
        self.player.update_position(512, 684)
        
        # Создаем новые объекты
        self.spawn_collectibles(5)
        self.spawn_obstacles(3)
        
        self.game_active = True
        self.game_over = False
        self.score = 0
        print("ИГРА ПЕРЕЗАПУЩЕНА!")

def main():
    """Главная функция"""
    # Создаем игру
    game = SpaceCollector()
    
    # Создаем движок
    engine = Engine(game)
    engine.set_fps(60)
    
    # Запускаем
    game.set_engine(engine)
    game.start()
    
    # Запускаем главный цикл
    game.window.root.mainloop()

if __name__ == "__main__":
    main()