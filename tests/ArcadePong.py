# arcade_pong_gui.py
import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gamelib import *
from gamelib.core.model.gui.gui_factory import Label, Button, Panel


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


class ArcadePongGUI(Game):
    def __init__(self):
        super().__init__("ARCADEPONG 9000", SCREEN_WIDTH + 200, SCREEN_HEIGHT, "#000000")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        
        # Счет
        self.left_score = 0
        self.right_score = 0
        
        # Состояние
        self.game_active = True
        self.paused = False
        self.serving = True
        self.server = "left"
        self.vs_ai = True
        
        # Объекты
        self.left_paddle = None
        self.right_paddle = None
        self.ball = None
        
        # Физика
        self.ball_dx = 0
        self.ball_dy = 0
        self.ball_speed = BALL_SPEED
        self.last_hit = None
        self.rally_count = 0
        
        # GUI элементы
        self.left_score_label = None
        self.right_score_label = None
        self.status_label = None
        self.mode_label = None
        self.speed_label = None
        self.rally_label = None
    
    def setup(self):
        print("\n" + "="*60)
        print("ARCADEPONG 9000 - НОВАЯ GUI СИСТЕМА")
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
        
        # Создаем игровое поле
        self.create_arena()
        self.create_paddles()
        self.create_ball()
        
        # Создаем GUI панель
        self.create_gui_panel()
        
        # Показываем сцену
        self.scene_switcher.show_scene(self.main_scene)
        
        # Настраиваем ввод
        self.input_manager = InputManager(self.window.root)
        
        # Запускаем игровой цикл
        self.window.root.after(16, self.game_loop)
        
        print("=== ИГРА ЗАПУЩЕНА ===\n")
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
    
    def create_gui_panel(self):
        """Создание панели управления с новой GUI системой"""
        # Основная панель справа
        self.gui_panel = Panel(self.window.root, bg="#0a0a1a")
        self.gui_panel.place(x=SCREEN_WIDTH + 10, y=10)
        
        # Заголовок
        title = Label(self.gui_panel.widget, text="PONG 9000", 
                      font=("Courier", 16, "bold"), color="#00ff88", bg="#0a0a1a")
        title.pack(pady=10)
        
        # Панель счета
        score_panel = Panel(self.gui_panel.widget, bg="#1a1a2e")
        score_panel.pack(pady=5, padx=10, fill="x")
        
        score_title = Label(score_panel.widget, text="СЧЕТ", 
                           font=("Courier", 10), color="#00aa88", bg="#1a1a2e")
        score_title.pack()
        
        # Счет в одну строку
        score_row = Panel(score_panel.widget, bg="#1a1a2e")
        score_row.pack(pady=5)
        
        self.left_score_label = Label(score_row.widget, text="00", 
                                       font=("Courier", 24, "bold"), 
                                       color="#00ff88", bg="#1a1a2e")
        self.left_score_label.pack(side="left", padx=10)
        
        colon = Label(score_row.widget, text=":", 
                     font=("Courier", 20, "bold"), 
                     color="#ffffff", bg="#1a1a2e")
        colon.pack(side="left")
        
        self.right_score_label = Label(score_row.widget, text="00", 
                                        font=("Courier", 24, "bold"), 
                                        color="#00ff88", bg="#1a1a2e")
        self.right_score_label.pack(side="left", padx=10)
        
        # Информационная панель
        info_panel = Panel(self.gui_panel.widget, bg="#1a1a2e")
        info_panel.pack(pady=5, padx=10, fill="x")
        
        # Режим
        mode_row = Panel(info_panel.widget, bg="#1a1a2e")
        mode_row.pack(fill="x", pady=2)
        
        mode_text = Label(mode_row.widget, text="РЕЖИМ:", 
                         font=("Courier", 9), color="#00aa88", bg="#1a1a2e")
        mode_text.pack(side="left")
        
        self.mode_label = Label(mode_row.widget, text="ИИ", 
                                font=("Courier", 10, "bold"), 
                                color="#00ff88", bg="#1a1a2e")
        self.mode_label.pack(side="right")
        
        # Скорость
        speed_row = Panel(info_panel.widget, bg="#1a1a2e")
        speed_row.pack(fill="x", pady=2)
        
        speed_text = Label(speed_row.widget, text="СПИД:", 
                          font=("Courier", 9), color="#00aa88", bg="#1a1a2e")
        speed_text.pack(side="left")
        
        self.speed_label = Label(speed_row.widget, text="4.0", 
                                 font=("Courier", 10, "bold"), 
                                 color="#00ff88", bg="#1a1a2e")
        self.speed_label.pack(side="right")
        
        # Розыгрыш
        rally_row = Panel(info_panel.widget, bg="#1a1a2e")
        rally_row.pack(fill="x", pady=2)
        
        rally_text = Label(rally_row.widget, text="РОЗЫГР:", 
                          font=("Courier", 9), color="#00aa88", bg="#1a1a2e")
        rally_text.pack(side="left")
        
        self.rally_label = Label(rally_row.widget, text="0", 
                                 font=("Courier", 10, "bold"), 
                                 color="#00ff88", bg="#1a1a2e")
        self.rally_label.pack(side="right")
        
        # Кнопки управления
        btn_serve = Button(self.gui_panel.widget, text="ПОДАЧА", 
                          command=self.serve_ball,
                          font=("Courier", 10, "bold"), 
                          color="#00ff88", bg="#2a2a3e")
        btn_serve.pack(pady=3, padx=10, fill="x")
        
        btn_pause = Button(self.gui_panel.widget, text="ПАУЗА", 
                          command=self.toggle_pause,
                          font=("Courier", 10, "bold"), 
                          color="#ffff00", bg="#2a2a3e")
        btn_pause.pack(pady=3, padx=10, fill="x")
        
        btn_reset = Button(self.gui_panel.widget, text="СБРОС", 
                          command=self.reset_score,
                          font=("Courier", 10, "bold"), 
                          color="#ff8866", bg="#2a2a3e")
        btn_reset.pack(pady=3, padx=10, fill="x")
        
        btn_mode = Button(self.gui_panel.widget, text="ИИ/2P", 
                         command=self.toggle_mode,
                         font=("Courier", 10, "bold"), 
                         color="#88aaff", bg="#2a2a3e")
        btn_mode.pack(pady=3, padx=10, fill="x")
        
        # Статус
        self.status_label = Label(self.gui_panel.widget, text="ГОТОВ", 
                                   font=("Courier", 12, "bold"), 
                                   color="#ffff00", bg="#0a0a1a")
        self.status_label.pack(pady=10)
        
        # Инструкция
        instr = Label(self.gui_panel.widget, 
                      text="W/S - ЛЕВЫЙ\n↑/↓ - ПРАВЫЙ\nESC - ВЫХОД",
                      font=("Courier", 8), color="#888888", bg="#0a0a1a")
        instr.pack(pady=5)
    
    def game_loop(self):
        """Основной игровой цикл"""
        if not self.paused and self.game_active and not self.serving:
            self.update_ball_position()
        
        # Обновляем GUI
        self.update_gui()
        
        # Следующий кадр
        self.window.root.after(16, self.game_loop)
    
    def update_gui(self):
        """Обновление GUI элементов"""
        if self.left_score_label:
            self.left_score_label.set_text(f"{self.left_score:02d}")
            self.right_score_label.set_text(f"{self.right_score:02d}")
            self.speed_label.set_text(f"{self.ball_speed:.1f}")
            self.rally_label.set_text(str(self.rally_count))
            self.mode_label.set_text("ИИ" if self.vs_ai else "2P")
    
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
        
        if new_y >= SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE:
            new_y = SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE
            self.ball_dy = -abs(self.ball_dy) * 0.95
        
        # Проверка коллизий
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
        if self.ball_dx < 0:
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
                
                self.last_hit = "left"
                self.rally_count += 1
                self.flash_paddle(self.left_paddle)
        
        # Правая ракетка
        right_x, right_y = self.right_paddle.get_position()
        if self.ball_dx > 0:
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
                
                self.last_hit = "right"
                self.rally_count += 1
                self.flash_paddle(self.right_paddle)
    
    def normalize_speed(self):
        """Нормализация скорости"""
        current_speed = math.sqrt(self.ball_dx**2 + self.ball_dy**2)
        if current_speed > 0:
            factor = self.ball_speed / current_speed
            self.ball_dx *= factor
            self.ball_dy *= factor
    
    def flash_paddle(self, paddle):
        """Эффект мигания"""
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
        self.status_label.set_text("ИГРА")
        print(f"🎾 ПОДАЧА! Угол: {base_angle:.1f}°")
    
    def score_point(self, side):
        """Начисление очка"""
        # Эффект
        goal_text = self.main_scene.canvas.create_text(
            SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
            text="GOAL!",
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
            self.server = "right"
            print(f"\n⚡ ГОЛ ЛЕВОГО! Счет: {self.left_score}:{self.right_score}")
        else:
            self.right_score += 1
            self.server = "left"
            print(f"\n⚡ ГОЛ ПРАВОГО! Счет: {self.left_score}:{self.right_score}")
        
        # Проверка победы
        if self.left_score >= WIN_SCORE:
            self.game_over("ЛЕВЫЙ")
        elif self.right_score >= WIN_SCORE:
            self.game_over("ПРАВЫЙ")
        else:
            self.status_label.set_text("ПОДАЧА")
            print("🟢 НАЖМИТЕ [SPACE] ДЛЯ ПОДАЧИ")
    
    def game_over(self, winner):
        """Конец игры"""
        self.game_active = False
        
        self.main_scene.canvas.create_text(
            SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50,
            text=f"{winner} WINS!",
            font=("Courier", 32, "bold"),
            fill='#00FF00'
        )
        
        self.status_label.set_text("GAME OVER")
        print(f"\n🏆 ПОБЕДИТЕЛЬ: {winner}!")
    
    def update_ai(self):
        """Обновление ИИ"""
        if not self.vs_ai or self.paused or self.serving:
            return
        
        ball_x, ball_y = self.ball.get_position()
        paddle_x, paddle_y = self.right_paddle.get_position()
        
        if self.ball_dx > 0:
            time_to_reach = (paddle_x - ball_x) / self.ball_dx if self.ball_dx > 0 else 1000
            predicted_y = ball_y + self.ball_dy * time_to_reach
            
            while predicted_y < WALL_SIZE or predicted_y > SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE:
                if predicted_y < WALL_SIZE:
                    predicted_y = WALL_SIZE + (WALL_SIZE - predicted_y)
                if predicted_y > SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE:
                    predicted_y = (SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE) - (predicted_y - (SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE))
            
            target_y = predicted_y - PADDLE_HEIGHT//2
            target_y = max(WALL_SIZE, min(target_y, SCREEN_HEIGHT - PADDLE_HEIGHT - WALL_SIZE))
            
            diff = target_y - paddle_y
            move = diff * AI_DIFFICULTY
            if abs(move) > PADDLE_SPEED * 0.5:
                move = PADDLE_SPEED * 0.5 if move > 0 else -PADDLE_SPEED * 0.5
            
            self.right_paddle.update_position(paddle_x, paddle_y + move)
    
    def toggle_pause(self):
        """Пауза"""
        if self.game_active:
            self.paused = not self.paused
            self.status_label.set_text("ПАУЗА" if self.paused else "ИГРА")
            print("⏸ ПАУЗА" if self.paused else "▶ ПРОДОЛЖЕНИЕ")
    
    def toggle_mode(self):
        """Переключение режима"""
        self.vs_ai = not self.vs_ai
        mode = "ИИ" if self.vs_ai else "2P"
        print(f"\n🔄 РЕЖИМ: {mode}")
    
    def reset_score(self):
        """Сброс"""
        print("\n🔄 СБРОС")
        
        self.left_score = 0
        self.right_score = 0
        
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
        
        self.status_label.set_text("ГОТОВ")
        print("🟢 НАЖМИТЕ [SPACE] ДЛЯ НАЧАЛА")
    
    def update(self):
        """Игровой цикл"""
        if not self.game_active or self.paused:
            return
        
        # Левая ракетка
        left_x, left_y = self.left_paddle.get_position()
        
        if self.input_manager.is_key_down('w'):
            new_y = max(WALL_SIZE, left_y - PADDLE_SPEED)
            self.left_paddle.update_position(left_x, new_y)
        
        if self.input_manager.is_key_down('s'):
            new_y = min(SCREEN_HEIGHT - PADDLE_HEIGHT - WALL_SIZE, left_y + PADDLE_SPEED)
            self.left_paddle.update_position(left_x, new_y)
        
        # Правая ракетка
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
        
        # Клавиши
        if self.input_manager.is_key_down('space') and self.serving and self.game_active:
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
    game = ArcadePongGUI()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()


if __name__ == "__main__":
    main()