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
        
        self.left_score = 0
        self.right_score = 0
        
        self.game_active = True
        self.paused = False
        self.serving = True
        self.server = "left"
        self.vs_ai = True
        
        self.left_paddle = None
        self.right_paddle = None
        self.ball = None
        
        self.ball_dx = 0
        self.ball_dy = 0
        self.ball_speed = BALL_SPEED
        self.last_hit = None
        self.rally_count = 0
        
        self.left_score_label = None
        self.right_score_label = None
        self.status_label = None
        self.mode_label = None
        self.speed_label = None
        self.rally_label = None
    
    def setup(self):
        self.main_scene = Scene(self.window)
        self.create_arena()
        self.create_paddles()
        self.create_ball()
        self.create_gui_panel()
        self.scene_switcher.show_scene(self.main_scene)
        self.input_manager = InputManager(self.window.root)
        self.window.root.after(16, self.game_loop)
    
    def create_arena(self):
        self.main_scene.canvas.configure(bg='#001100')
        wall_color = '#00FF00'
        
        gameObject.Rectangle(self.main_scene.canvas, x=0, y=0, width=SCREEN_WIDTH, height=WALL_SIZE, color=wall_color, scene=self.main_scene)
        gameObject.Rectangle(self.main_scene.canvas, x=0, y=SCREEN_HEIGHT - WALL_SIZE, width=SCREEN_WIDTH, height=WALL_SIZE, color=wall_color, scene=self.main_scene)
        
        for y in range(WALL_SIZE + 10, SCREEN_HEIGHT - WALL_SIZE - 10, 25):
            gameObject.Rectangle(self.main_scene.canvas, x=SCREEN_WIDTH//2 - 3, y=y, width=6, height=12, color=wall_color, scene=self.main_scene)
        
        gameObject.Rectangle(self.main_scene.canvas, x=0, y=WALL_SIZE, width=20, height=SCREEN_HEIGHT - WALL_SIZE*2, color='#002200', scene=self.main_scene)
        gameObject.Rectangle(self.main_scene.canvas, x=SCREEN_WIDTH-20, y=WALL_SIZE, width=20, height=SCREEN_HEIGHT - WALL_SIZE*2, color='#002200', scene=self.main_scene)
    
    def create_paddles(self):
        self.left_paddle = gameObject.Rectangle(
            self.main_scene.canvas, x=40, y=SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2,
            width=PADDLE_WIDTH, height=PADDLE_HEIGHT, color='#00FFFF', scene=self.main_scene
        )
        self.right_paddle = gameObject.Rectangle(
            self.main_scene.canvas, x=SCREEN_WIDTH - 40 - PADDLE_WIDTH, y=SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2,
            width=PADDLE_WIDTH, height=PADDLE_HEIGHT, color='#FF00FF', scene=self.main_scene
        )
    
    def create_ball(self):
        self.ball = gameObject.Rectangle(
            self.main_scene.canvas, x=SCREEN_WIDTH//2 - BALL_SIZE//2, y=SCREEN_HEIGHT//2 - BALL_SIZE//2,
            width=BALL_SIZE, height=BALL_SIZE, color='#FFFFFF', scene=self.main_scene
        )
    
    def create_gui_panel(self):
        self.gui_panel = Panel(self.window.root, bg="#0a0a1a")
        self.gui_panel.place(x=SCREEN_WIDTH + 10, y=10)
        
        Label(self.gui_panel.widget, text="PONG 9000", font=("Courier", 16, "bold"), color="#00ff88", bg="#0a0a1a").pack(pady=10)
        
        score_panel = Panel(self.gui_panel.widget, bg="#1a1a2e")
        score_panel.pack(pady=5, padx=10, fill="x")
        Label(score_panel.widget, text="СЧЕТ", font=("Courier", 10), color="#00aa88", bg="#1a1a2e").pack()
        
        score_row = Panel(score_panel.widget, bg="#1a1a2e")
        score_row.pack(pady=5)
        
        self.left_score_label = Label(score_row.widget, text="00", font=("Courier", 24, "bold"), color="#00ff88", bg="#1a1a2e")
        self.left_score_label.pack(side="left", padx=10)
        Label(score_row.widget, text=":", font=("Courier", 20, "bold"), color="#ffffff", bg="#1a1a2e").pack(side="left")
        self.right_score_label = Label(score_row.widget, text="00", font=("Courier", 24, "bold"), color="#00ff88", bg="#1a1a2e")
        self.right_score_label.pack(side="left", padx=10)
        
        info_panel = Panel(self.gui_panel.widget, bg="#1a1a2e")
        info_panel.pack(pady=5, padx=10, fill="x")
        
        mode_row = Panel(info_panel.widget, bg="#1a1a2e")
        mode_row.pack(fill="x", pady=2)
        Label(mode_row.widget, text="РЕЖИМ:", font=("Courier", 9), color="#00aa88", bg="#1a1a2e").pack(side="left")
        self.mode_label = Label(mode_row.widget, text="ИИ", font=("Courier", 10, "bold"), color="#00ff88", bg="#1a1a2e")
        self.mode_label.pack(side="right")
        
        speed_row = Panel(info_panel.widget, bg="#1a1a2e")
        speed_row.pack(fill="x", pady=2)
        Label(speed_row.widget, text="СПИД:", font=("Courier", 9), color="#00aa88", bg="#1a1a2e").pack(side="left")
        self.speed_label = Label(speed_row.widget, text="4.0", font=("Courier", 10, "bold"), color="#00ff88", bg="#1a1a2e")
        self.speed_label.pack(side="right")
        
        rally_row = Panel(info_panel.widget, bg="#1a1a2e")
        rally_row.pack(fill="x", pady=2)
        Label(rally_row.widget, text="РОЗЫГР:", font=("Courier", 9), color="#00aa88", bg="#1a1a2e").pack(side="left")
        self.rally_label = Label(rally_row.widget, text="0", font=("Courier", 10, "bold"), color="#00ff88", bg="#1a1a2e")
        self.rally_label.pack(side="right")
        
        Button(self.gui_panel.widget, text="ПОДАЧА", command=self.serve_ball, font=("Courier", 10, "bold"), color="#00ff88", bg="#2a2a3e").pack(pady=3, padx=10, fill="x")
        Button(self.gui_panel.widget, text="ПАУЗА", command=self.toggle_pause, font=("Courier", 10, "bold"), color="#ffff00", bg="#2a2a3e").pack(pady=3, padx=10, fill="x")
        Button(self.gui_panel.widget, text="СБРОС", command=self.reset_score, font=("Courier", 10, "bold"), color="#ff8866", bg="#2a2a3e").pack(pady=3, padx=10, fill="x")
        Button(self.gui_panel.widget, text="ИИ/2P", command=self.toggle_mode, font=("Courier", 10, "bold"), color="#88aaff", bg="#2a2a3e").pack(pady=3, padx=10, fill="x")
        
        self.status_label = Label(self.gui_panel.widget, text="ГОТОВ", font=("Courier", 12, "bold"), color="#ffff00", bg="#0a0a1a")
        self.status_label.pack(pady=10)
        
        Label(self.gui_panel.widget, text="W/S - ЛЕВЫЙ\n↑/↓ - ПРАВЫЙ\nESC - ВЫХОД", font=("Courier", 8), color="#888888", bg="#0a0a1a").pack(pady=5)
    
    def game_loop(self):
        if not self.paused and self.game_active and not self.serving:
            self.update_ball_position()
        self.update_gui()
        self.window.root.after(16, self.game_loop)
    
    def update_gui(self):
        if self.left_score_label:
            self.left_score_label.set_text(f"{self.left_score:02d}")
            self.right_score_label.set_text(f"{self.right_score:02d}")
            self.speed_label.set_text(f"{self.ball_speed:.1f}")
            self.rally_label.set_text(str(self.rally_count))
            self.mode_label.set_text("ИИ" if self.vs_ai else "2P")
    
    def update_ball_position(self):
        if self.ball_dx == 0 and self.ball_dy == 0:
            return
        
        x, y = self.ball.get_position()
        new_x = x + self.ball_dx
        new_y = y + self.ball_dy
        
        if new_y <= WALL_SIZE:
            new_y = WALL_SIZE
            self.ball_dy = abs(self.ball_dy) * 0.95
        elif new_y >= SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE:
            new_y = SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE
            self.ball_dy = -abs(self.ball_dy) * 0.95
        
        self.check_paddle_collisions(x, y)
        
        if new_x <= 0:
            self.score_point("right")
            return
        if new_x >= SCREEN_WIDTH - BALL_SIZE:
            self.score_point("left")
            return
        
        self.ball.update_position(new_x, new_y)
        
        if random.random() < 0.01:
            self.ball_dy += random.uniform(-0.2, 0.2)
            self.normalize_speed()
    
    def check_paddle_collisions(self, bx, by):
        ball_center_y = by + BALL_SIZE//2
        
        left_x, left_y = self.left_paddle.get_position()
        if self.ball_dx < 0 and bx < left_x + PADDLE_WIDTH and bx + BALL_SIZE > left_x and by < left_y + PADDLE_HEIGHT and by + BALL_SIZE > left_y:
            hit_pos = max(-1, min(1, (ball_center_y - (left_y + PADDLE_HEIGHT//2)) / (PADDLE_HEIGHT//2)))
            angle = hit_pos * 75
            self.ball_speed = min(self.ball_speed + SPEED_BOOST, BALL_MAX_SPEED)
            self.ball_dx = abs(self.ball_speed * math.cos(math.radians(angle)))
            self.ball_dy = self.ball_speed * math.sin(math.radians(angle))
            self.last_hit = "left"
            self.rally_count += 1
        
        right_x, right_y = self.right_paddle.get_position()
        if self.ball_dx > 0 and bx < right_x + PADDLE_WIDTH and bx + BALL_SIZE > right_x and by < right_y + PADDLE_HEIGHT and by + BALL_SIZE > right_y:
            hit_pos = max(-1, min(1, (ball_center_y - (right_y + PADDLE_HEIGHT//2)) / (PADDLE_HEIGHT//2)))
            angle = hit_pos * 75
            self.ball_speed = min(self.ball_speed + SPEED_BOOST, BALL_MAX_SPEED)
            self.ball_dx = -abs(self.ball_speed * math.cos(math.radians(angle)))
            self.ball_dy = self.ball_speed * math.sin(math.radians(angle))
            self.last_hit = "right"
            self.rally_count += 1
    
    def normalize_speed(self):
        current_speed = math.sqrt(self.ball_dx**2 + self.ball_dy**2)
        if current_speed > 0:
            factor = self.ball_speed / current_speed
            self.ball_dx *= factor
            self.ball_dy *= factor
    
    def serve_ball(self):
        if not self.game_active or self.paused:
            return
        
        self.ball.update_position(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2)
        self.ball_speed = BALL_SPEED
        self.rally_count = 0
        self.last_hit = None
        
        base_angle = random.uniform(-20, 20) if self.server == "left" else random.uniform(160, 200)
        self.ball_dx = self.ball_speed * math.cos(math.radians(base_angle))
        self.ball_dy = self.ball_speed * math.sin(math.radians(base_angle))
        
        self.serving = False
        self.status_label.set_text("ИГРА")
    
    def score_point(self, side):
        self.ball_dx = 0
        self.ball_dy = 0
        self.serving = True
        self.ball_speed = BALL_SPEED
        self.rally_count = 0
        self.last_hit = None
        
        if side == "left":
            self.left_score += 1
            self.server = "right"
        else:
            self.right_score += 1
            self.server = "left"
        
        if self.left_score >= WIN_SCORE or self.right_score >= WIN_SCORE:
            self.game_active = False
            self.status_label.set_text("GAME OVER")
        else:
            self.status_label.set_text("ПОДАЧА")
    
    def update_ai(self):
        if not self.vs_ai or self.paused or self.serving:
            return
        
        ball_x, ball_y = self.ball.get_position()
        paddle_x, paddle_y = self.right_paddle.get_position()
        
        if self.ball_dx > 0:
            time_to_reach = (paddle_x - ball_x) / self.ball_dx
            predicted_y = ball_y + self.ball_dy * time_to_reach
            
            while predicted_y < WALL_SIZE or predicted_y > SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE:
                if predicted_y < WALL_SIZE:
                    predicted_y = WALL_SIZE + (WALL_SIZE - predicted_y)
                else:
                    predicted_y = (SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE) - (predicted_y - (SCREEN_HEIGHT - BALL_SIZE - WALL_SIZE))
            
            target_y = max(WALL_SIZE, min(predicted_y - PADDLE_HEIGHT//2, SCREEN_HEIGHT - PADDLE_HEIGHT - WALL_SIZE))
            move = (target_y - paddle_y) * AI_DIFFICULTY
            move = max(-PADDLE_SPEED * 0.5, min(PADDLE_SPEED * 0.5, move))
            self.right_paddle.update_position(paddle_x, paddle_y + move)
    
    def toggle_pause(self):
        if self.game_active:
            self.paused = not self.paused
            self.status_label.set_text("ПАУЗА" if self.paused else "ИГРА")
    
    def toggle_mode(self):
        self.vs_ai = not self.vs_ai
    
    def reset_score(self):
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
        self.ball.update_position(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2)
        self.status_label.set_text("ГОТОВ")
    
    def update(self):
        if not self.game_active or self.paused:
            return
        
        left_x, left_y = self.left_paddle.get_position()
        
        if self.input_manager.is_key_down('w'):
            self.left_paddle.update_position(left_x, max(WALL_SIZE, left_y - PADDLE_SPEED))
        if self.input_manager.is_key_down('s'):
            self.left_paddle.update_position(left_x, min(SCREEN_HEIGHT - PADDLE_HEIGHT - WALL_SIZE, left_y + PADDLE_SPEED))
        
        if not self.vs_ai:
            right_x, right_y = self.right_paddle.get_position()
            if self.input_manager.is_key_down('Up'):
                self.right_paddle.update_position(right_x, max(WALL_SIZE, right_y - PADDLE_SPEED))
            if self.input_manager.is_key_down('Down'):
                self.right_paddle.update_position(right_x, min(SCREEN_HEIGHT - PADDLE_HEIGHT - WALL_SIZE, right_y + PADDLE_SPEED))
        else:
            self.update_ai()
        
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