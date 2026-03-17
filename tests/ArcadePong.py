# arcade_pong_90s_fixed.py
import sys
import os
import random
import math
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gamelib import *

# Константы
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120
BALL_SIZE = 10
WALL_SIZE = 15
PADDLE_SPEED = 10
BALL_SPEED = 4
BALL_MAX_SPEED = 12
WIN_SCORE = 7
AI_DIFFICULTY = 0.04
SPEED_BOOST = 0.2

class ArcadePong90s(Game):
    def __init__(self):
        super().__init__("ARCADEPONG 9000", SCREEN_WIDTH, SCREEN_HEIGHT, "#000000")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        
        # Счет
        self.left_score = 0
        self.right_score = 0
        
        # Состояние игры
        self.game_active = True
        self.paused = False
        self.serving = True
        self.server = "left"
        self.vs_ai = True
        
        # Объекты
        self.left_paddle = None
        self.right_paddle = None
        self.ball = None
        
        # Физика мяча
        self.ball_dx = 0
        self.ball_dy = 0
        self.ball_speed = BALL_SPEED
        self.last_hit = None
        self.rally_count = 0
        self.effects = []
        
    def setup(self):
        print("\n" + "="*60)
        print("ARCADEPONG 9000 - РЕТРО 90-х")
        print("="*60)
        print("\nУПРАВЛЕНИЕ:")
        print("  [W][S] - левый игрок")
        print("  [↑][↓] - правый игрок (режим 2 игроков)")
        print("  [SPACE] - подача")
        print("  [A] - переключить ИИ")
        print("  [P] - пауза")
        print("  [R] - сброс")
        print("  [ESC] - выход")
        print("="*60 + "\n")
        
        # Создаем сцену
        self.main_scene = Scene(self.window)
        
        # Создаем объекты
        self.create_arena()
        self.create_paddles()
        self.create_ball()
        self.setup_gui()
        
        # Показываем сцену
        self.scene_switcher.show_scene(self.main_scene)
        
        # Настраиваем ввод
        self.input_manager = InputManager(self.window.root)
        
        # Запускаем игровой цикл
        self.window.root.after(16, self.game_loop)
        
        print("\n=== ARCADEPONG 9000 АКТИВИРОВАН ===\n")
        print("🟢 НАЖМИТЕ [SPACE] ДЛЯ ПОДАЧИ!")
    
    def create_arena(self):
        """Создание игрового поля"""
        self.main_scene.canvas.configure(bg='#001100')
        wall_color = '#00FF00'
        
        # Верхняя стена
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=0,
            width=SCREEN_WIDTH,
            height=WALL_SIZE,
            color=wall_color,
            scene=self.main_scene
        )
        
        # Нижняя стена
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=SCREEN_HEIGHT - WALL_SIZE,
            width=SCREEN_WIDTH,
            height=WALL_SIZE,
            color=wall_color,
            scene=self.main_scene
        )
        
        # Центральная линия
        for y in range(WALL_SIZE + 10, SCREEN_HEIGHT - WALL_SIZE - 10, 25):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=SCREEN_WIDTH//2 - 3, y=y,
                width=6, height=12,
                color=wall_color,
                scene=self.main_scene
            )
        
        # Декоративные элементы
        for x in range(0, SCREEN_WIDTH, 30):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=WALL_SIZE + 2,
                width=10, height=2,
                color='#00AA00',
                scene=self.main_scene
            )
            
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=x, y=SCREEN_HEIGHT - WALL_SIZE - 4,
                width=10, height=2,
                color='#00AA00',
                scene=self.main_scene
            )
        
        # Голевые зоны
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=0, y=WALL_SIZE,
            width=20, height=SCREEN_HEIGHT - WALL_SIZE*2,
            color='#002200',
            scene=self.main_scene
        )
        
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=SCREEN_WIDTH-20, y=WALL_SIZE,
            width=20, height=SCREEN_HEIGHT - WALL_SIZE*2,
            color='#002200',
            scene=self.main_scene
        )
        
        # Score панели слева
        for i in range(5):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=30, y=30 + i*15,
                width=4, height=8,
                color='#00AA00',
                scene=self.main_scene
            )
        
        # Score панели справа
        for i in range(5):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=SCREEN_WIDTH-34, y=30 + i*15,
                width=4, height=8,
                color='#00AA00',
                scene=self.main_scene
            )
    
    def create_paddles(self):
        """Создание ракеток"""
        # Левая ракетка
        self.left_paddle = gameObject.Rectangle(
            self.main_scene.canvas,
            x=40,
            y=SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            color='#00FFFF',
            scene=self.main_scene
        )
        
        # Полоски на левой ракетке
        for i in range(4):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=42,
                y=SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2 + i*30 + 5,
                width=3, height=10,
                color='#FFFFFF',
                scene=self.main_scene
            )
        
        # Правая ракетка
        self.right_paddle = gameObject.Rectangle(
            self.main_scene.canvas,
            x=SCREEN_WIDTH - 40 - PADDLE_WIDTH,
            y=SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            color='#FF00FF',
            scene=self.main_scene
        )
        
        # Полоски на правой ракетке
        for i in range(4):
            gameObject.Rectangle(
                self.main_scene.canvas,
                x=SCREEN_WIDTH - 37 - PADDLE_WIDTH,
                y=SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2 + i*30 + 5,
                width=3, height=10,
                color='#FFFFFF',
                scene=self.main_scene
            )
    
    def create_ball(self):
        """Создание мяча"""
        self.ball = gameObject.Rectangle(
            self.main_scene.canvas,
            x=SCREEN_WIDTH//2 - BALL_SIZE//2,
            y=SCREEN_HEIGHT//2 - BALL_SIZE//2,
            width=BALL_SIZE,
            height=BALL_SIZE,
            color='#FFFFFF',
            scene=self.main_scene
        )
        
        # Внутренний квадратик
        gameObject.Rectangle(
            self.main_scene.canvas,
            x=SCREEN_WIDTH//2 - 2,
            y=SCREEN_HEIGHT//2 - 2,
            width=4, height=4,
            color='#AAAAAA',
            scene=self.main_scene
        )
    
    def setup_gui(self):
        """Настройка интерфейса"""
        # Фрейм для счета
        self.score_frame = tk.Frame(
            self.window.root, 
            bg='#000000', 
            relief='sunken', 
            bd=4
        )
        self.score_frame.place(x=SCREEN_WIDTH//2 - 200, y=15, width=400, height=70)
        
        # Левый счет - ВАЖНО: сохраняем ссылку до pack()
        self.left_score_label = tk.Label(
            self.score_frame,
            text=f"{self.left_score:02d}",
            font=("Courier", 36, "bold"),
            bg='#000000',
            fg='#00FF00'
        )
        self.left_score_label.pack(side='left', padx=40)
        
        # Разделитель
        separator = tk.Label(
            self.score_frame,
            text=":",
            font=("Courier", 36, "bold"),
            bg='#000000',
            fg='#00FF00'
        )
        separator.pack(side='left')
        
        # Правый счет - ВАЖНО: сохраняем ссылку до pack()
        self.right_score_label = tk.Label(
            self.score_frame,
            text=f"{self.right_score:02d}",
            font=("Courier", 36, "bold"),
            bg='#000000',
            fg='#00FF00'
        )
        self.right_score_label.pack(side='left', padx=40)
        
        # Фрейм управления
        self.control_frame = tk.Frame(
            self.window.root, 
            bg='#222222', 
            relief='raised', 
            bd=5
        )
        self.control_frame.place(x=SCREEN_WIDTH + 10, y=10, width=180, height=380)
        
        # Заголовок
        title = tk.Label(
            self.control_frame,
            text="PONG 9000",
            font=("Courier", 14, "bold"),
            bg='#222222',
            fg='#00FF00'
        )
        title.pack(pady=10)
        
        # LED панели
        self.leds = {}
        
        # Режим
        mode_frame = tk.Frame(self.control_frame, bg='#111111', relief='sunken', bd=2)
        mode_frame.pack(pady=2, padx=10, fill='x')
        tk.Label(mode_frame, text="РЕЖИМ", font=("Courier", 8), bg='#111111', fg='#00AA00').pack(side='left', padx=5)
        self.leds["РЕЖИМ"] = tk.Label(mode_frame, text="ИИ", font=("Courier", 10, "bold"), bg='#111111', fg='#00FF00')
        self.leds["РЕЖИМ"].pack(side='right', padx=5)
        
        # Счет
        score_frame = tk.Frame(self.control_frame, bg='#111111', relief='sunken', bd=2)
        score_frame.pack(pady=2, padx=10, fill='x')
        tk.Label(score_frame, text="СЧЕТ", font=("Courier", 8), bg='#111111', fg='#00AA00').pack(side='left', padx=5)
        self.leds["СЧЕТ"] = tk.Label(score_frame, text="0:0", font=("Courier", 10, "bold"), bg='#111111', fg='#00FF00')
        self.leds["СЧЕТ"].pack(side='right', padx=5)
        
        # Скорость
        speed_frame = tk.Frame(self.control_frame, bg='#111111', relief='sunken', bd=2)
        speed_frame.pack(pady=2, padx=10, fill='x')
        tk.Label(speed_frame, text="СПИД", font=("Courier", 8), bg='#111111', fg='#00AA00').pack(side='left', padx=5)
        self.leds["СПИД"] = tk.Label(speed_frame, text="4.0", font=("Courier", 10, "bold"), bg='#111111', fg='#00FF00')
        self.leds["СПИД"].pack(side='right', padx=5)
        
        # Розыгрыш
        rally_frame = tk.Frame(self.control_frame, bg='#111111', relief='sunken', bd=2)
        rally_frame.pack(pady=2, padx=10, fill='x')
        tk.Label(rally_frame, text="РОЗЫГР", font=("Courier", 8), bg='#111111', fg='#00AA00').pack(side='left', padx=5)
        self.leds["РОЗЫГР"] = tk.Label(rally_frame, text="0", font=("Courier", 10, "bold"), bg='#111111', fg='#00FF00')
        self.leds["РОЗЫГР"].pack(side='right', padx=5)
        
        # Кнопки
        tk.Button(
            self.control_frame,
            text="ПОДАЧА [SPACE]",
            font=("Courier", 10, "bold"),
            bg='#333333',
            fg='#00FF00',
            activebackground='#00AA00',
            command=self.serve_ball
        ).pack(pady=3, padx=10, fill='x')
        
        tk.Button(
            self.control_frame,
            text="ПАУЗА [P]",
            font=("Courier", 10, "bold"),
            bg='#333333',
            fg='#00FF00',
            command=self.toggle_pause
        ).pack(pady=3, padx=10, fill='x')
        
        tk.Button(
            self.control_frame,
            text="СБРОС [R]",
            font=("Courier", 10, "bold"),
            bg='#333333',
            fg='#00FF00',
            command=self.reset_score
        ).pack(pady=3, padx=10, fill='x')
        
        tk.Button(
            self.control_frame,
            text="ИИ/2P [A]",
            font=("Courier", 10, "bold"),
            bg='#333333',
            fg='#00FF00',
            command=self.toggle_mode
        ).pack(pady=3, padx=10, fill='x')
        
        # Инструкция
        instr = tk.Label(
            self.control_frame,
            text="W/S - ЛЕВЫЙ\n↑/↓ - ПРАВЫЙ\nESC - ВЫХОД",
            font=("Courier", 9),
            bg='#222222',
            fg='#AAAAAA',
            justify='left'
        )
        instr.pack(pady=10)
        
        # LED статуса
        self.status_led = tk.Label(
            self.control_frame,
            text="ГОТОВ",
            font=("Courier", 12, "bold"),
            bg='#000000',
            fg='#00FF00',
            relief='sunken',
            bd=2
        )
        self.status_led.pack(pady=5, padx=10, fill='x')
    
    def game_loop(self):
        """Основной игровой цикл"""
        if not self.paused and self.game_active and not self.serving:
            self.update_ball_position()
        
        # Очищаем старые эффекты
        self.clear_effects()
        
        # Обновляем LED индикаторы
        if "РЕЖИМ" in self.leds:
            self.leds["РЕЖИМ"].config(text="ИИ" if self.vs_ai else "2P")
        if "СЧЕТ" in self.leds:
            self.leds["СЧЕТ"].config(text=f"{self.left_score}:{self.right_score}")
        if "СПИД" in self.leds:
            self.leds["СПИД"].config(text=f"{self.ball_speed:.1f}")
        if "РОЗЫГР" in self.leds:
            self.leds["РОЗЫГР"].config(text=str(self.rally_count))
        
        # Следующий кадр
        self.window.root.after(16, self.game_loop)
    
    def clear_effects(self):
        """Очистка старых эффектов"""
        current_time = time.time()
        self.effects = [e for e in self.effects if e[1] > current_time]
    
    def update_ball_position(self):
        """Обновление позиции мяча"""
        if self.ball_dx == 0 and self.ball_dy == 0:
            return
        
        x, y = self.ball.get_position()
        new_x = x + self.ball_dx
        new_y = y + self.ball_dy
        
        # Столкновения со стенами
        if new_y <= WALL_SIZE:
            new_y = WALL_SIZE
            self.ball_dy = abs(self.ball_dy) * 0.95
            self.add_effect(new_x, new_y, "wall")
        
        if new_y >= SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE:
            new_y = SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE
            self.ball_dy = -abs(self.ball_dy) * 0.95
            self.add_effect(new_x, new_y, "wall")
        
        # Проверка коллизий с ракетками
        self.check_paddle_collisions(x, y)
        
        # Проверка голов
        if new_x <= 0:
            self.score_point("right")
            return
        if new_x >= SCREEN_WIDTH - BALL_SIZE:
            self.score_point("left")
            return
        
        # Обновляем позицию
        self.ball.update_position(new_x, new_y)
        
        # Эффект вращения
        if random.random() < 0.01:
            self.ball_dy += random.uniform(-0.2, 0.2)
            self.normalize_speed()
    
    def check_paddle_collisions(self, bx, by):
        """Проверка столкновений с ракетками"""
        ball_center_x = bx + BALL_SIZE//2
        ball_center_y = by + BALL_SIZE//2
        
        # Левая ракетка
        left_x, left_y = self.left_paddle.get_position()
        if self.ball_dx < 0:  # Мяч движется влево
            if (bx < left_x + PADDLE_WIDTH and 
                bx + BALL_SIZE > left_x and 
                by < left_y + PADDLE_HEIGHT and 
                by + BALL_SIZE > left_y):
                
                hit_pos = (ball_center_y - (left_y + PADDLE_HEIGHT//2)) / (PADDLE_HEIGHT//2)
                hit_pos = max(-1, min(1, hit_pos))
                angle = hit_pos * 75
                
                self.ball_speed = min(self.ball_speed + SPEED_BOOST, BALL_MAX_SPEED)
                self.ball_dx = abs(self.ball_speed * math.cos(math.radians(angle)))
                self.ball_dy = self.ball_speed * math.sin(math.radians(angle))
                
                if self.last_hit == "left":
                    self.ball_dy += random.uniform(-0.5, 0.5)
                
                self.last_hit = "left"
                self.rally_count += 1
                self.flash_paddle(self.left_paddle)
                self.add_effect(bx, by, "paddle")
        
        # Правая ракетка
        right_x, right_y = self.right_paddle.get_position()
        if self.ball_dx > 0:  # Мяч движется вправо
            if (bx < right_x + PADDLE_WIDTH and 
                bx + BALL_SIZE > right_x and 
                by < right_y + PADDLE_HEIGHT and 
                by + BALL_SIZE > right_y):
                
                hit_pos = (ball_center_y - (right_y + PADDLE_HEIGHT//2)) / (PADDLE_HEIGHT//2)
                hit_pos = max(-1, min(1, hit_pos))
                angle = hit_pos * 75
                
                self.ball_speed = min(self.ball_speed + SPEED_BOOST, BALL_MAX_SPEED)
                self.ball_dx = -abs(self.ball_speed * math.cos(math.radians(angle)))
                self.ball_dy = self.ball_speed * math.sin(math.radians(angle))
                
                if self.last_hit == "right":
                    self.ball_dy += random.uniform(-0.5, 0.5)
                
                self.last_hit = "right"
                self.rally_count += 1
                self.flash_paddle(self.right_paddle)
                self.add_effect(bx, by, "paddle")
    
    def normalize_speed(self):
        """Нормализация скорости"""
        current_speed = math.sqrt(self.ball_dx**2 + self.ball_dy**2)
        if current_speed > 0:
            factor = self.ball_speed / current_speed
            self.ball_dx *= factor
            self.ball_dy *= factor
    
    def add_effect(self, x, y, effect_type):
        """Добавление ретро-эффектов"""
        if effect_type == "paddle":
            for _ in range(3):
                spark_x = x + random.randint(-5, 5)
                spark_y = y + random.randint(-5, 5)
                spark = self.main_scene.canvas.create_oval(
                    spark_x, spark_y,
                    spark_x + 2, spark_y + 2,
                    fill='#FFFF00',
                    outline=''
                )
                self.effects.append((spark, time.time() + 0.05))
                self.window.root.after(50, lambda s=spark: self.main_scene.canvas.delete(s))
        
        elif effect_type == "wall":
            line = self.main_scene.canvas.create_line(
                x, y, x + BALL_SIZE, y + BALL_SIZE,
                fill='#00FF00',
                width=1
            )
            self.effects.append((line, time.time() + 0.05))
            self.window.root.after(50, lambda l=line: self.main_scene.canvas.delete(l))
    
    def flash_paddle(self, paddle):
        """Эффект мигания ракетки"""
        if hasattr(paddle, 'rect_id'):
            original = self.main_scene.canvas.itemcget(paddle.rect_id, 'fill')
            self.main_scene.canvas.itemconfig(paddle.rect_id, fill='#FFFFFF')
            self.window.root.after(50, lambda: self.main_scene.canvas.itemconfig(paddle.rect_id, fill=original))
    
    def serve_ball(self):
        """Подача"""
        if not self.game_active or self.paused:
            return
        
        self.ball.update_position(
            SCREEN_WIDTH//2 - BALL_SIZE//2,
            SCREEN_HEIGHT//2 - BALL_SIZE//2
        )
        
        self.ball_speed = BALL_SPEED
        self.rally_count = 0
        self.last_hit = None
        
        if self.server == "left":
            base_angle = random.uniform(-20, 20)
        else:
            base_angle = random.uniform(160, 200)
        
        self.ball_dx = self.ball_speed * math.cos(math.radians(base_angle))
        self.ball_dy = self.ball_speed * math.sin(math.radians(base_angle))
        
        self.serving = False
        self.status_led.config(text="ИГРА")
        print(f"🎾 ПОДАЧА! Угол: {base_angle:.1f}°")
    
    def score_point(self, side):
        """Начисление очка"""
        # Эффект "GOAL"
        goal_text = self.main_scene.canvas.create_text(
            SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
            text="⚡ GOAL! ⚡",
            font=("Courier", 24, "bold"),
            fill='#00FF00'
        )
        self.window.root.after(500, lambda: self.main_scene.canvas.delete(goal_text))
        
        # Останавливаем мяч
        self.ball_dx = 0
        self.ball_dy = 0
        self.serving = True
        self.ball_speed = BALL_SPEED
        self.rally_count = 0
        self.last_hit = None
        
        if side == "left":
            self.left_score += 1
            self.left_score_label.config(text=f"{self.left_score:02d}")
            self.server = "right"
            print(f"\n⚡ ГОЛ ЛЕВОГО! Счет: {self.left_score}:{self.right_score}")
        else:
            self.right_score += 1
            self.right_score_label.config(text=f"{self.right_score:02d}")
            self.server = "left"
            print(f"\n⚡ ГОЛ ПРАВОГО! Счет: {self.left_score}:{self.right_score}")
        
        # Проверка победы
        if self.left_score >= WIN_SCORE:
            self.game_over("ЛЕВЫЙ")
        elif self.right_score >= WIN_SCORE:
            self.game_over("ПРАВЫЙ")
        else:
            self.status_led.config(text="ПОДАЧА")
            print("🟢 НАЖМИТЕ [SPACE] ДЛЯ ПОДАЧИ")
    
    def game_over(self, winner):
        """Конец игры"""
        self.game_active = False
        print(f"\n🏆 ПОБЕДИТЕЛЬ: {winner}!")
        
        self.main_scene.canvas.create_text(
            SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50,
            text=f"{winner} WINS!",
            font=("Courier", 32, "bold"),
            fill='#00FF00'
        )
        
        self.status_led.config(text="GAME OVER")
    
    def update_ai(self):
        """Обновление ИИ"""
        if not self.vs_ai or self.paused or self.serving:
            return
        
        ball_x, ball_y = self.ball.get_position()
        paddle_x, paddle_y = self.right_paddle.get_position()
        
        if self.ball_dx > 0:  # Мяч летит к ИИ
            # Время до достижения
            time_to_reach = (paddle_x - ball_x) / self.ball_dx if self.ball_dx > 0 else 1000
            
            # Предсказанная позиция Y
            predicted_y = ball_y + self.ball_dy * time_to_reach
            
            # Учитываем отскоки от стен
            while predicted_y < WALL_SIZE or predicted_y > SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE:
                if predicted_y < WALL_SIZE:
                    predicted_y = WALL_SIZE + (WALL_SIZE - predicted_y)
                if predicted_y > SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE:
                    predicted_y = (SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE) - (predicted_y - (SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE))
            
            # Цель для ракетки
            target_y = predicted_y - PADDLE_HEIGHT//2
            
            # Случайность для реализма
            if random.random() < 0.3:
                target_y += random.randint(-20, 20)
            
            # Ограничиваем
            target_y = max(WALL_SIZE, min(target_y, SCREEN_HEIGHT - PADDLE_HEIGHT - WALL_SIZE))
            
            # Плавное движение
            diff = target_y - paddle_y
            move = diff * AI_DIFFICULTY
            if abs(move) > PADDLE_SPEED * 0.5:
                move = PADDLE_SPEED * 0.5 if move > 0 else -PADDLE_SPEED * 0.5
            
            self.right_paddle.update_position(paddle_x, paddle_y + move)
    
    def toggle_pause(self):
        """Пауза"""
        if self.game_active:
            self.paused = not self.paused
            self.status_led.config(text="ПАУЗА" if self.paused else "ИГРА")
            print("⏸ ПАУЗА" if self.paused else "▶ ПРОДОЛЖЕНИЕ")
    
    def toggle_mode(self):
        """Переключение режима"""
        self.vs_ai = not self.vs_ai
        mode = "ИИ" if self.vs_ai else "2P"
        print(f"\n🔄 РЕЖИМ: {mode}")
    
    def reset_score(self):
        """Сброс счета"""
        print("\n🔄 СБРОС")
        
        self.left_score = 0
        self.right_score = 0
        self.left_score_label.config(text="00")
        self.right_score_label.config(text="00")
        
        self.game_active = True
        self.serving = True
        self.server = "left"
        self.ball_speed = BALL_SPEED
        self.ball_dx = 0
        self.ball_dy = 0
        self.rally_count = 0
        self.last_hit = None
        
        self.ball.update_position(
            SCREEN_WIDTH//2 - BALL_SIZE//2,
            SCREEN_HEIGHT//2 - BALL_SIZE//2
        )
        
        self.status_led.config(text="ГОТОВ")
        print("🟢 НАЖМИТЕ [SPACE] ДЛЯ НАЧАЛА")
    
    def update(self):
        """Игровой цикл (вызывается движком)"""
        if not self.game_active or self.paused:
            return
        
        # Управление левой ракеткой
        left_x, left_y = self.left_paddle.get_position()
        
        if self.input_manager.is_key_down('w'):
            new_y = max(WALL_SIZE, left_y - PADDLE_SPEED)
            self.left_paddle.update_position(left_x, new_y)
        
        if self.input_manager.is_key_down('s'):
            new_y = min(SCREEN_HEIGHT - PADDLE_HEIGHT - WALL_SIZE, left_y + PADDLE_SPEED)
            self.left_paddle.update_position(left_x, new_y)
        
        # Управление правой ракеткой
        if not self.vs_ai:
            right_x, right_y = self.right_paddle.get_position()
            
            if self.input_manager.is_key_down('Up'):
                new_y = max(WALL_SIZE, right_y - PADDLE_SPEED)
                self.right_paddle.update_position(right_x, new_y)
            
            if self.input_manager.is_key_down('Down'):
                new_y = min(SCREEN_HEIGHT - PADDLE_HEIGHT - WALL_SIZE, right_y + PADDLE_SPEED)
                self.right_paddle.update_position(right_x, new_y)
        else:
            self.update_ai()
        
        # Обработка клавиш
        if self.input_manager.is_key_down('space'):
            if self.serving and self.game_active:
                self.serve_ball()
        
        if self.input_manager.is_key_down('p'):
            self.toggle_pause()
            self.window.root.after(200, lambda: None)
        
        if self.input_manager.is_key_down('r'):
            self.reset_score()
            self.window.root.after(200, lambda: None)
        
        if self.input_manager.is_key_down('a'):
            self.toggle_mode()
            self.window.root.after(200, lambda: None)
        
        if self.input_manager.is_key_down('Escape'):
            self.window.root.quit()

def main():
    # Создаем окно
    window_width = SCREEN_WIDTH + 200
    window_height = SCREEN_HEIGHT
    
    class CustomPong(ArcadePong90s):
        def __init__(self):
            super().__init__()
            self.window.width = window_width
            self.window.height = window_height
            self.window.root.geometry(f"{window_width}x{window_height}")
            self.window.root.configure(bg='#000000')
            self.window.root.title("ARCADEPONG 9000")
    
    # Создаем игру
    game = CustomPong()
    
    # Создаем движок
    engine = Engine(game)
    game.set_engine(engine)
    
    # Запускаем
    game.start()
    game.window.root.mainloop()

if __name__ == "__main__":
    main()