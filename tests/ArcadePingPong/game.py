"""Pong - main, точка входа"""
import sys
import os
import math
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gamelib import *
from gamelib.core.model.gui.gui_factory import Label, Button, Panel
from pong_config import *
from pong_core import Paddle, Ball, AIController, GameState


class PongGame(Game):
    def __init__(self):
        super().__init__("PONG", SCREEN_WIDTH + GUI_WIDTH, SCREEN_HEIGHT, '#000000')
        self.scene = None
        self.input = None
        self.p1 = None
        self.p2 = None
        self.ball = None
        self.state = GameState()
        self.gui_labels = {}
    
    def setup(self):
        self.scene = Scene(self.window)
        self.scene.canvas.configure(bg=C_BG)
        
        # Игровое поле
        self._create_field()
        
        # Объекты
        self.p1 = Paddle(self.scene.canvas, 40, SCREEN_HEIGHT//2 - PADDLE_H//2, C_P1, self.scene, gameObject)
        self.p2 = Paddle(self.scene.canvas, SCREEN_WIDTH - 40 - PADDLE_W, SCREEN_HEIGHT//2 - PADDLE_H//2, C_P2, self.scene, gameObject)
        self.ball = Ball(self.scene.canvas, self.scene, gameObject, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # GUI
        self._build_gui()
        
        # Ввод
        self.input = InputManager(self.window.root)
        
        # Запуск цикла
        self.window.root.after(16, self.loop)
    
    def _create_field(self):
        gameObject.Rectangle(self.scene.canvas, 0, 0, SCREEN_WIDTH, WALL, C_WALL, self.scene)
        gameObject.Rectangle(self.scene.canvas, 0, SCREEN_HEIGHT-WALL, SCREEN_WIDTH, WALL, C_WALL, self.scene)
        for y in range(WALL+10, SCREEN_HEIGHT-WALL-10, 25):
            gameObject.Rectangle(self.scene.canvas, SCREEN_WIDTH//2-3, y, 6, 12, C_WALL, self.scene)
    
    def _build_gui(self):
        panel = Panel(self.window.root, bg=C_GUI)
        panel.place(x=SCREEN_WIDTH + 10, y=10)
        
        Label(panel.widget, text="PONG", font=("Courier", 18, "bold"), color=C_TEXT, bg=C_GUI).pack(pady=10)
        
        sp = Panel(panel.widget, bg=C_PANEL)
        sp.pack(pady=5, padx=10, fill="x")
        Label(sp.widget, text="СЧЁТ", font=("Courier", 10), color='#00aa88', bg=C_PANEL).pack()
        
        row = Panel(sp.widget, bg=C_PANEL)
        row.pack(pady=5)
        self.gui_labels['l_score'] = Label(row.widget, text="0", font=("Courier", 24, "bold"), color=C_TEXT, bg=C_PANEL)
        self.gui_labels['l_score'].pack(side="left", padx=15)
        Label(row.widget, text=":", font=("Courier", 20, "bold"), color='#fff', bg=C_PANEL).pack(side="left")
        self.gui_labels['r_score'] = Label(row.widget, text="0", font=("Courier", 24, "bold"), color=C_TEXT, bg=C_PANEL)
        self.gui_labels['r_score'].pack(side="left", padx=15)
        
        bs = {"font": ("Courier", 10, "bold"), "bg": "#2a2a3e"}
        Button(panel.widget, text="ПОДАЧА", command=self.serve, color=C_TEXT, **bs).pack(pady=3, padx=10, fill="x")
        Button(panel.widget, text="ПАУЗА", command=self.toggle_pause, color='#ffff00', **bs).pack(pady=3, padx=10, fill="x")
        Button(panel.widget, text="СБРОС", command=self.reset_game, color='#ff8866', **bs).pack(pady=3, padx=10, fill="x")
        Button(panel.widget, text="ИИ/2P", command=self.toggle_mode, color='#88aaff', **bs).pack(pady=3, padx=10, fill="x")
        
        self.gui_labels['status'] = Label(panel.widget, text="ГОТОВ", font=("Courier", 12, "bold"), color='#ffff00', bg=C_GUI)
        self.gui_labels['status'].pack(pady=10)
        
        Label(panel.widget, text="W/S — левый\n↑/↓ — правый\nSPACE — подача", font=("Courier", 8), color='#888', bg=C_GUI).pack(pady=5)
    
    def loop(self):
        if not self.state.paused and self.state.running and not self.state.serving:
            self._update_ball()
        
        self._handle_input()
        self._update_gui()
        self.window.root.after(16, self.loop)
    
    def _update_ball(self):
        self.ball.update(WALL)
        bx, by = self.ball.pos()
        
        # Столкновения
        p1x, p1y = self.p1.pos()
        if (self.ball.dx < 0 and
            bx < p1x + PADDLE_W and bx + BALL_SIZE > p1x and
            by < p1y + PADDLE_H and by + BALL_SIZE > p1y):
            self.ball.hit_paddle(self.p1, 'left', SPEED_UP, BALL_MAX)
            self.state.rally += 1
        
        p2x, p2y = self.p2.pos()
        if (self.ball.dx > 0 and
            bx < p2x + PADDLE_W and bx + BALL_SIZE > p2x and
            by < p2y + PADDLE_H and by + BALL_SIZE > p2y):
            self.ball.hit_paddle(self.p2, 'right', SPEED_UP, BALL_MAX)
            self.state.rally += 1
        
        # Гол
        if bx <= 0:
            self._score('p2')
        elif bx >= SCREEN_WIDTH:
            self._score('p1')
        
        # ИИ
        if self.state.vs_ai:
            AIController.update(self.p2, self.ball, AI_SPEED, WALL, SCREEN_HEIGHT, PADDLE_SPEED)
    
    def _handle_input(self):
        if self.input.is_key_down('w'):
            self.p1.move(-PADDLE_SPEED, WALL, SCREEN_HEIGHT)
        if self.input.is_key_down('s'):
            self.p1.move(PADDLE_SPEED, WALL, SCREEN_HEIGHT)
        
        if not self.state.vs_ai:
            if self.input.is_key_down('Up'):
                self.p2.move(-PADDLE_SPEED, WALL, SCREEN_HEIGHT)
            if self.input.is_key_down('Down'):
                self.p2.move(PADDLE_SPEED, WALL, SCREEN_HEIGHT)
        
        if self.input.is_key_down('space') and self.state.serving:
            self.serve()
        if self.input.is_key_down('p'):
            self.toggle_pause()
            self.window.root.after(200, lambda: None)
        if self.input.is_key_down('r'):
            self.reset_game()
            self.window.root.after(200, lambda: None)
        if self.input.is_key_down('a'):
            self.toggle_mode()
            self.window.root.after(200, lambda: None)
        if self.input.is_key_down('Escape'):
            self.window.root.quit()
    
    def serve(self):
        if not self.state.running or self.state.paused:
            return
        self.ball.serve(self.state.server)
        self.state.serving = False
        self.state.rally = 0
    
    def _score(self, who):
        if who == 'p1':
            self.p1.score += 1
            self.state.server = 'right'
        else:
            self.p2.score += 1
            self.state.server = 'left'
        
        self.state.serving = True
        self.ball.obj.update_position(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2)
        self.ball.dx = 0
        self.ball.dy = 0
        
        if self.p1.score >= WIN_SCORE or self.p2.score >= WIN_SCORE:
            self.state.running = False
            self.state.winner = 'ЛЕВЫЙ' if self.p1.score >= WIN_SCORE else 'ПРАВЫЙ'
    
    def _update_gui(self):
        self.gui_labels['l_score'].set_text(str(self.p1.score))
        self.gui_labels['r_score'].set_text(str(self.p2.score))
        
        if not self.state.running:
            status = f"ПОБЕДА: {self.state.winner}"
        elif self.state.paused:
            status = "ПАУЗА"
        elif self.state.serving:
            status = "ПОДАЧА"
        else:
            status = "ИГРА"
        self.gui_labels['status'].set_text(status)
    
    def toggle_pause(self):
        self.state.paused = not self.state.paused
    
    def toggle_mode(self):
        self.state.vs_ai = not self.state.vs_ai
    
    def reset_game(self):
        self.p1.score = 0
        self.p2.score = 0
        self.p1.reset(40, SCREEN_HEIGHT//2 - PADDLE_H//2)
        self.p2.reset(SCREEN_WIDTH - 40 - PADDLE_W, SCREEN_HEIGHT//2 - PADDLE_H//2)
        self.ball.obj.update_position(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2)
        self.ball.dx = 0
        self.ball.dy = 0
        self.state.reset()
    
    def update(self):
        pass


def main():
    game = PongGame()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()

if __name__ == "__main__":
    main()