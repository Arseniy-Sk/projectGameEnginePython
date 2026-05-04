"""Бизнес-логика"""
import math
import random


class Paddle:
    """Ракетка"""
    def __init__(self, canvas, x, y, color, scene, game_object_factory):
        self.obj = game_object_factory.Rectangle(
            canvas, x=x, y=y,
            width=20, height=120,  # PADDLE_W, PADDLE_H
            color=color, scene=scene
        )
        self.score = 0
        self.paddle_w = 20
        self.paddle_h = 120
    
    def pos(self):
        return self.obj.get_position()
    
    def move(self, dy, wall_size=15, screen_height=600):
        x, y = self.pos()
        new_y = max(wall_size, min(screen_height - self.paddle_h - wall_size, y + dy))
        self.obj.update_position(x, new_y)
    
    def center_y(self):
        return self.pos()[1] + self.paddle_h // 2
    
    def reset(self, x, y):
        self.obj.update_position(x, y)


class Ball:
    """Мяч"""
    def __init__(self, canvas, scene, game_object_factory, screen_width=900, screen_height=600):
        self.obj = game_object_factory.Rectangle(
            canvas,
            x=screen_width//2 - 5,  # BALL_SIZE//2
            y=screen_height//2 - 5,
            width=10, height=10,  # BALL_SIZE
            color='#FFFFFF',
            scene=scene
        )
        self.dx = 0
        self.dy = 0
        self.speed = 4  # BALL_SPEED
        self.ball_size = 10
        self.sw = screen_width
        self.sh = screen_height
    
    def pos(self):
        return self.obj.get_position()
    
    def serve(self, direction='left'):
        self.obj.update_position(self.sw//2 - 5, self.sh//2 - 5)
        self.speed = 4
        angle = random.uniform(-20, 20)
        if direction == 'right':
            angle += 180
        rad = math.radians(angle)
        self.dx = self.speed * math.cos(rad)
        self.dy = self.speed * math.sin(rad)
    
    def update(self, wall_size=15):
        x, y = self.pos()
        new_x = x + self.dx
        new_y = y + self.dy
        
        if new_y <= wall_size:
            new_y = wall_size
            self.dy = abs(self.dy)
        elif new_y >= self.sh - self.ball_size - wall_size:
            new_y = self.sh - self.ball_size - wall_size
            self.dy = -abs(self.dy)
        
        self.obj.update_position(new_x, new_y)
        
        if random.random() < 0.01:
            self.dy += random.uniform(-0.2, 0.2)
            self._normalize()
    
    def hit_paddle(self, paddle, side='left', speed_up=0.2, max_speed=12):
        ball_y = self.pos()[1] + self.ball_size // 2
        hit_pos = (ball_y - paddle.center_y()) / (paddle.paddle_h // 2)
        hit_pos = max(-1, min(1, hit_pos))
        
        angle = hit_pos * 70
        self.speed = min(self.speed + speed_up, max_speed)
        
        direction = 1 if side == 'left' else -1
        self.dx = direction * abs(self.speed * math.cos(math.radians(angle)))
        self.dy = self.speed * math.sin(math.radians(angle))
    
    def _normalize(self):
        cur = math.hypot(self.dx, self.dy)
        if cur > 0:
            self.dx = self.dx / cur * self.speed
            self.dy = self.dy / cur * self.speed


class AIController:
    """Управление ИИ"""
    @staticmethod
    def update(paddle, ball, ai_speed=0.04, wall=15, screen_h=600, paddle_speed=10):
        if ball.dx <= 0:
            return
        
        bx, by = ball.pos()
        px, py = paddle.pos()
        
        if ball.dx > 0:
            time = (px - bx) / ball.dx
            pred_y = by + ball.dy * time
            
            while pred_y < wall or pred_y > screen_h - 10 - wall:
                if pred_y < wall:
                    pred_y = 2 * wall - pred_y
                else:
                    pred_y = 2 * (screen_h - 10 - wall) - pred_y
            
            target_y = pred_y - 60  # PADDLE_H // 2
            target_y = max(wall, min(screen_h - 120 - wall, target_y))
            
            dy = (target_y - py) * ai_speed
            paddle.move(max(-paddle_speed * 0.8, min(paddle_speed * 0.8, dy)))


class GameState:
    """Состояние игры"""
    def __init__(self):
        self.running = True
        self.paused = False
        self.serving = True
        self.server = 'left'
        self.vs_ai = True
        self.rally = 0
        self.winner = None
    
    def reset(self):
        self.running = True
        self.serving = True
        self.server = 'left'
        self.rally = 0
        self.paused = False
        self.winner = None