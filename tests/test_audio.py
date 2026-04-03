# tests/test_audio_full.py
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamelib import *
from gamelib.core.model.audio.audio_system import global_audio
from gamelib.core.model.components.audio_component import AudioSource

class AudioFullTest(Game):
    def __init__(self):
        super().__init__("🎵 Audio System Test", 900, 650, "#1e1e2e")
        self.scene_switcher = SceneSwitcher()
        self.input_manager = None
        self.audio_source = None
        self.buttons = {}
        self.current_music = None
        
    def setup(self):
        # Создаём сцену
        self.scene = Scene(self.window)
        self.scene_switcher.show_scene(self.scene)
        
        # Объект для звуков
        self.sound_holder = gameObject.Rectangle(
            self.scene.canvas, x=0, y=0, width=1, height=1, 
            color="", scene=self.scene
        )
        self.audio_source = AudioSource()
        self.sound_holder.add_component(self.audio_source)
        
        # Создаём тестовые WAV звуки
        self.create_test_sounds()
        
        # Создаём UI
        self.create_gui()
        
        self.input_manager = InputManager(self.window.root)
        
        # Выводим информацию о ffmpeg
        self.show_ffmpeg_info()
    
    def create_test_sounds(self):
        """Создаёт тестовые WAV звуки"""
        self.sounds_dir = os.path.join(os.path.dirname(__file__), "test_sounds")
        os.makedirs(self.sounds_dir, exist_ok=True)
        
        # Создаём несколько звуков
        sounds = [
            ("beep", 880, 0.3, "Писк"),
            ("bounce", 440, 0.4, "Отскок"),
            ("alert", 1760, 0.2, "Сигнал")
        ]
        
        for name, freq, duration, desc in sounds:
            filename = os.path.join(self.sounds_dir, f"{name}.wav")
            if not os.path.exists(filename):
                self.create_wav(filename, freq, duration)
            self.audio_source.add_sound(name, filename)
            print(f"✓ Загружен: {name} - {desc}")
    
    def create_wav(self, filename, frequency, duration):
        """Создаёт WAV файл"""
        import wave
        import struct
        import math
        
        sample_rate = 44100
        num_samples = int(duration * sample_rate)
        
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            value = int(32767 * math.sin(2 * math.pi * frequency * t))
            samples.append(value)
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            data = b''.join(struct.pack('<h', s) for s in samples)
            wav.writeframes(data)
    
    def show_ffmpeg_info(self):
        """Показывает информацию о ffmpeg"""
        if global_audio.has_ffmpeg:
            self.info_label.config(text="✓ ffmpeg найден - MP3 поддерживается", fg="#88ff88")
        else:
            self.info_label.config(text="⚠️ ffmpeg не найден - только WAV файлы", fg="#ff8888")
    
    def create_gui(self):
        """Создаёт интерфейс управления"""
        # Основная панель
        control_frame = tk.Frame(self.window.root, bg="#2d2d3a", relief="raised", bd=3)
        control_frame.place(x=650, y=20, width=240, height=600)
        
        # Заголовок
        tk.Label(control_frame, text="🎵 АУДИО КОНТРОЛЛЕР", 
                font=("Courier", 12, "bold"),
                bg="#2d2d3a", fg="#00ffaa").pack(pady=10)
        
        # Разделитель
        tk.Frame(control_frame, height=2, bg="#4a4a5a").pack(fill="x", padx=10, pady=5)
        
        # Секция звуков
        tk.Label(control_frame, text="📢 ЗВУКОВЫЕ ЭФФЕКТЫ", 
                font=("Courier", 10, "bold"),
                bg="#2d2d3a", fg="#88aaff").pack(pady=5)
        
        sounds_frame = tk.Frame(control_frame, bg="#2d2d3a")
        sounds_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Кнопка загрузки своего звука
        def load_custom_sound():
            filetypes = [("Аудио файлы", "*.mp3 *.wav *.ogg"), ("Все файлы", "*.*")]
            filename = filedialog.askopenfilename(title="Выберите звук", filetypes=filetypes)
            if filename:
                name = os.path.splitext(os.path.basename(filename))[0]
                if self.audio_source.add_sound(name, filename):
                    btn = tk.Button(sounds_frame, text=f"🔊 {name}", 
                                  font=("Courier", 9, "bold"),
                                  bg="#3a3a4a", fg="#ffffff",
                                  command=lambda n=name: self.play_with_feedback(n))
                    btn.pack(fill="x", pady=2)
                    self.buttons[name] = btn
        
        load_btn = tk.Button(control_frame, text="📂 ЗАГРУЗИТЬ ЗВУК", 
                            command=load_custom_sound,
                            bg="#3a3a4a", fg="#00ffaa", font=("Courier", 10, "bold"))
        load_btn.pack(pady=5)
        
        # Кнопки для тестовых звуков
        test_sounds = [
            ("beep", "🔔 Писк"),
            ("bounce", "⚡ Отскок"),
            ("alert", "⚠️ Сигнал")
        ]
        
        for name, label in test_sounds:
            btn = tk.Button(sounds_frame, text=label, 
                          font=("Courier", 9, "bold"),
                          bg="#3a3a4a", fg="#ffffff",
                          command=lambda n=name: self.play_with_feedback(n))
            btn.pack(fill="x", pady=2)
            self.buttons[name] = btn
        
        # Разделитель
        tk.Frame(control_frame, height=2, bg="#4a4a5a").pack(fill="x", padx=10, pady=5)
        
        # Секция музыки
        tk.Label(control_frame, text="🎵 ФОНОВАЯ МУЗЫКА", 
                font=("Courier", 10, "bold"),
                bg="#2d2d3a", fg="#88aaff").pack(pady=5)
        
        music_frame = tk.Frame(control_frame, bg="#2d2d3a")
        music_frame.pack(fill="x", padx=10, pady=5)
        
        def load_music():
            filetypes = [("MP3/WAV", "*.mp3 *.wav"), ("Все файлы", "*.*")]
            filename = filedialog.askopenfilename(title="Выберите музыку", filetypes=filetypes)
            if filename:
                self.current_music = filename
                global_audio.play_music(filename, loop=True)
                self.music_status.config(text=f"▶ {os.path.basename(filename)}")
        
        load_music_btn = tk.Button(music_frame, text="🎵 ВЫБРАТЬ МУЗЫКУ", 
                                  command=load_music,
                                  bg="#3a3a4a", fg="#ffaa00", font=("Courier", 9, "bold"))
        load_music_btn.pack(fill="x", pady=2)
        
        self.music_status = tk.Label(music_frame, text="⏸ Музыка не выбрана", 
                                     bg="#2d2d3a", fg="#aaaaaa", font=("Courier", 8))
        self.music_status.pack(pady=2)
        
        stop_music_btn = tk.Button(music_frame, text="⏹️ ОСТАНОВИТЬ", 
                                  command=global_audio.stop_music,
                                  bg="#3a3a4a", fg="#ff8888", font=("Courier", 9, "bold"))
        stop_music_btn.pack(fill="x", pady=2)
        
        # Разделитель
        tk.Frame(control_frame, height=2, bg="#4a4a5a").pack(fill="x", padx=10, pady=5)
        
        # Секция управления громкостью
        tk.Label(control_frame, text="🎚️ ГРОМКОСТЬ", 
                font=("Courier", 10, "bold"),
                bg="#2d2d3a", fg="#88aaff").pack(pady=5)
        
        vol_frame = tk.Frame(control_frame, bg="#2d2d3a")
        vol_frame.pack(fill="x", padx=10, pady=5)
        
        # Звуки
        tk.Label(vol_frame, text="Звуки:", bg="#2d2d3a", fg="#ffffff").pack(anchor="w")
        sound_slider = tk.Scale(vol_frame, from_=0, to=100, orient="horizontal", 
                               length=200, bg="#2d2d3a", fg="white",
                               command=lambda v: global_audio.set_sound_volume(int(v)/100))
        sound_slider.set(100)
        sound_slider.pack()
        
        # Музыка
        tk.Label(vol_frame, text="Музыка:", bg="#2d2d3a", fg="#ffffff").pack(anchor="w", pady=(5,0))
        music_slider = tk.Scale(vol_frame, from_=0, to=100, orient="horizontal", 
                               length=200, bg="#2d2d3a", fg="white",
                               command=lambda v: global_audio.set_music_volume(int(v)/100))
        music_slider.set(70)
        music_slider.pack()
        
        # Кнопка mute
        self.mute_btn = tk.Button(control_frame, text="🔇 ВЫКЛЮЧИТЬ ЗВУК", 
                                 command=self.toggle_mute,
                                 bg="#4a3a3a", fg="#ff8888", font=("Courier", 10, "bold"))
        self.mute_btn.pack(pady=10)
        
        # Информационная метка
        self.info_label = tk.Label(control_frame, text="Готов к работе", 
                                  bg="#2d2d3a", fg="#88ff88", font=("Courier", 9))
        self.info_label.pack(pady=5)
        
        # Статус ffmpeg
        ffmpeg_status = "✓ MP3 поддержка" if global_audio.has_ffmpeg else "⚠️ Только WAV"
        ffmpeg_color = "#88ff88" if global_audio.has_ffmpeg else "#ff8888"
        tk.Label(control_frame, text=ffmpeg_status, 
                bg="#2d2d3a", fg=ffmpeg_color, font=("Courier", 8)).pack(pady=2)
    
    def play_with_feedback(self, name):
        """Воспроизводит звук с обратной связью"""
        self.audio_source.play(name)
        self.info_label.config(text=f"🔊 Играет: {name}")
        self.window.root.after(1000, lambda: self.info_label.config(text="Готов к работе"))
    
    def toggle_mute(self):
        """Переключить отключение звука"""
        global_audio.toggle_mute()
        if global_audio.muted:
            self.mute_btn.config(text="🔊 ВКЛЮЧИТЬ ЗВУК", bg="#4a6a4a", fg="#88ff88")
            self.info_label.config(text="🔇 Звук выключен")
        else:
            self.mute_btn.config(text="🔇 ВЫКЛЮЧИТЬ ЗВУК", bg="#4a3a3a", fg="#ff8888")
            self.info_label.config(text="🔊 Звук включен")
            self.window.root.after(1000, lambda: self.info_label.config(text="Готов к работе"))
    
    def update(self):
        """Обновление игры"""
        # Горячие клавиши
        if self.input_manager.is_key_down('1'):
            self.play_with_feedback("beep")
        elif self.input_manager.is_key_down('2'):
            self.play_with_feedback("bounce")
        elif self.input_manager.is_key_down('3'):
            self.play_with_feedback("alert")
        elif self.input_manager.is_key_down('m'):
            self.toggle_mute()
            self.window.root.after(200, lambda: None)
    
    def start(self):
        super().start()
        print("\n" + "="*60)
        print("🎵 АУДИО СИСТЕМА - ПОЛНЫЙ ТЕСТ")
        print("="*60)
        print("\nУПРАВЛЕНИЕ:")
        print("  [1] - Писк")
        print("  [2] - Отскок") 
        print("  [3] - Сигнал")
        print("  [M] - Выключить/включить звук")
        print("\nВозможности:")
        print("  • Загрузка MP3/WAV/OGG файлов")
        print("  • Фоновая музыка с зацикливанием")
        print("  • Регулировка громкости")
        print("  • Отключение звука")
        print("="*60 + "\n")

def main():
    game = AudioFullTest()
    engine = Engine(game)
    game.set_engine(engine)
    game.start()
    game.window.root.mainloop()

if __name__ == "__main__":
    main()