# gamelib/core/model/audio/audio_system.py
import os
import sys
import threading
import time
import tempfile
from pydub import AudioSegment
from gamelib.core.model.events.events_system import global_bus

# Определяем платформу
IS_WINDOWS = sys.platform == 'win32'
if IS_WINDOWS:
    import winsound

class AudioSystem:
    """Главная система звуков с использованием pydub и winsound (Windows)"""
    
    def __init__(self):
        self.sounds = {}
        self.music_thread = None
        self.music_playing = False
        self.music = None
        self.sound_volume = 1.0
        self.music_volume = 0.7
        self.muted = False
        self.temp_files = []
        self.has_ffmpeg = self._check_ffmpeg()
        
        if not IS_WINDOWS:
            print("⚠️ Звуковая система работает только на Windows")
        
        if not self.has_ffmpeg:
            print("\n⚠️ ffmpeg не найден! MP3 файлы не будут работать.")
            print("   Установите ffmpeg: https://ffmpeg.org/download.html")
            print("   Для теста используйте WAV файлы\n")
    
    def _check_ffmpeg(self):
        """Проверяет наличие ffmpeg"""
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         check=True)
            return True
        except:
            return False
    
    def _adjust_volume(self, audio, volume):
        """Изменяет громкость"""
        if volume >= 1.0:
            return audio
        db_change = 20 * (volume - 1.0)
        return audio.apply_gain(db_change)
    
    def _save_temp_wav(self, audio):
        """Сохраняет во временный WAV"""
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp.close()
        audio.export(temp.name, format='wav')
        self.temp_files.append(temp.name)
        return temp.name
    
    def load_sound(self, name, file_path):
        """Загрузить звук (MP3, WAV, OGG и т.д.)"""
        try:
            if not os.path.exists(file_path):
                print(f"⚠️ Файл не найден: {file_path}")
                return False
            
            # Проверяем формат
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.mp3' and not self.has_ffmpeg:
                print(f"⚠️ MP3 файл требует ffmpeg: {os.path.basename(file_path)}")
                return False
            
            # Загружаем аудио
            audio = AudioSegment.from_file(file_path)
            wav_path = self._save_temp_wav(audio)
            
            self.sounds[name] = {
                'file': wav_path,
                'original': file_path,
                'duration': len(audio) / 1000.0,
                'audio': audio
            }
            print(f"✓ Звук загружен: {name} (длит: {self.sounds[name]['duration']:.2f} сек)")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка загрузки {name}: {e}")
            return False
    
    def play_sound(self, name, volume=None):
        """Воспроизвести звук"""
        if self.muted or not IS_WINDOWS:
            return
        if name not in self.sounds:
            print(f"⚠️ Звук не найден: {name}")
            return
        
        sound = self.sounds[name]
        vol = volume if volume is not None else self.sound_volume
        
        thread = threading.Thread(target=self._play_sound_thread, args=(sound, vol, name))
        thread.daemon = True
        thread.start()
        
        global_bus.emit(self, 'sound_played', {'name': name, 'volume': vol})
    
    def _play_sound_thread(self, sound, volume, name):
        """Воспроизведение в потоке"""
        try:
            if volume < 1.0:
                adj_audio = self._adjust_volume(sound['audio'], volume)
                temp_file = self._save_temp_wav(adj_audio)
                winsound.PlaySound(temp_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
                time.sleep(sound['duration'] + 0.1)
                try:
                    os.unlink(temp_file)
                    if temp_file in self.temp_files:
                        self.temp_files.remove(temp_file)
                except:
                    pass
            else:
                winsound.PlaySound(sound['file'], winsound.SND_FILENAME | winsound.SND_ASYNC)
                time.sleep(sound['duration'] + 0.1)
        except Exception as e:
            print(f"✗ Ошибка воспроизведения {name}: {e}")
    
    def play_music(self, file_path, loop=True, volume=None):
        """Воспроизвести музыку (MP3, WAV)"""
        if self.muted or not IS_WINDOWS:
            return
        
        try:
            if not os.path.exists(file_path):
                print(f"⚠️ Файл не найден: {file_path}")
                return
            
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.mp3' and not self.has_ffmpeg:
                print(f"⚠️ MP3 музыка требует ffmpeg")
                return
            
            self.stop_music()
            
            # Загружаем и конвертируем
            audio = AudioSegment.from_file(file_path)
            vol = volume if volume is not None else self.music_volume
            if vol < 1.0:
                audio = self._adjust_volume(audio, vol)
            
            wav_path = self._save_temp_wav(audio)
            
            self.music = {
                'file': wav_path,
                'original': file_path,
                'loop': loop,
                'duration': len(audio) / 1000.0,
                'audio': audio
            }
            self.music_playing = True
            self.music_thread = threading.Thread(target=self._music_loop)
            self.music_thread.daemon = True
            self.music_thread.start()
            
            global_bus.emit(self, 'music_started', {'file': file_path})
            print(f"♪ Музыка: {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"✗ Ошибка: {e}")
    
    def _music_loop(self):
        """Цикл воспроизведения музыки"""
        if not self.music:
            return
        
        music = self.music
        while self.music_playing:
            try:
                winsound.PlaySound(music['file'], winsound.SND_FILENAME | winsound.SND_ASYNC)
                time.sleep(music['duration'] + 0.1)
                if not music['loop']:
                    break
            except Exception as e:
                print(f"✗ Ошибка: {e}")
                break
        
        self.music_playing = False
    
    def stop_music(self):
        """Остановить музыку"""
        self.music_playing = False
        if self.music_thread:
            self.music_thread = None
        winsound.PlaySound(None, winsound.SND_PURGE)
        global_bus.emit(self, 'music_stopped', {})
    
    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))
        print(f"🔊 Звуки: {self.sound_volume:.0%}")
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        print(f"🎵 Музыка: {self.music_volume:.0%}")
        if self.music_playing and self.music:
            was_playing = True
            self.stop_music()
            if was_playing:
                self.play_music(self.music['original'], loop=self.music['loop'], volume=self.music_volume)
    
    def mute(self):
        self.muted = True
        self.stop_music()
        global_bus.emit(self, 'audio_muted', {})
        print("🔇 Звук выключен")
    
    def unmute(self):
        self.muted = False
        global_bus.emit(self, 'audio_unmuted', {})
        print("🔊 Звук включен")
    
    def toggle_mute(self):
        if self.muted:
            self.unmute()
        else:
            self.mute()
    
    def cleanup(self):
        for f in self.temp_files:
            try:
                if os.path.exists(f):
                    os.unlink(f)
            except:
                pass
        self.temp_files = []
    
    def __del__(self):
        self.cleanup()

global_audio = AudioSystem()