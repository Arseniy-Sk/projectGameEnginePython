# gamelib/core/model/audio/audio_system.py
import os
import sys
import threading
import time
import tempfile
import subprocess
import winsound
from pydub import AudioSegment
from gamelib.core.model.events.events_system import global_bus


class AudioSystem:
    """Главная система звуков"""
    
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
    
    def _check_ffmpeg(self):
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         check=True)
            return True
        except:
            return False
    
    def _adjust_volume(self, audio, volume):
        if volume >= 1.0:
            return audio
        db_change = 20 * (volume - 1.0)
        return audio.apply_gain(db_change)
    
    def _save_temp_wav(self, audio):
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp.close()
        audio.export(temp.name, format='wav')
        self.temp_files.append(temp.name)
        return temp.name
    
    def load_sound(self, name, file_path):
        try:
            if not os.path.exists(file_path):
                return False
            
            audio = AudioSegment.from_file(file_path)
            wav_path = self._save_temp_wav(audio)
            
            self.sounds[name] = {
                'file': wav_path,
                'original': file_path,
                'duration': len(audio) / 1000.0,
                'audio': audio
            }
            return True
        except Exception as e:
            print(f"Ошибка загрузки {name}: {e}")
            return False
    
    def play_sound(self, name, volume=None):
        if self.muted or name not in self.sounds:
            return
        
        sound = self.sounds[name]
        vol = volume if volume is not None else self.sound_volume
        
        thread = threading.Thread(target=self._play_sound_thread, args=(sound, vol, name))
        thread.daemon = True
        thread.start()
        
        global_bus.emit(self, 'sound_played', {'name': name, 'volume': vol})
    
    def _play_sound_thread(self, sound, volume, name):
        try:
            if volume < 1.0:
                adj_audio = self._adjust_volume(sound['audio'], volume)
                temp_file = self._save_temp_wav(adj_audio)
                winsound.PlaySound(temp_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
                time.sleep(sound['duration'] + 0.1)
                os.unlink(temp_file)
                if temp_file in self.temp_files:
                    self.temp_files.remove(temp_file)
            else:
                winsound.PlaySound(sound['file'], winsound.SND_FILENAME | winsound.SND_ASYNC)
                time.sleep(sound['duration'] + 0.1)
        except Exception as e:
            print(f"Ошибка воспроизведения {name}: {e}")
    
    def play_music(self, file_path, loop=True, volume=None):
        if self.muted:
            return
        
        try:
            self.stop_music()
            
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
        except Exception as e:
            print(f"Ошибка воспроизведения музыки: {e}")
    
    def _music_loop(self):
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
                print(f"Ошибка: {e}")
                break
        
        self.music_playing = False
    
    def stop_music(self):
        self.music_playing = False
        self.music_thread = None
        winsound.PlaySound(None, winsound.SND_PURGE)
        global_bus.emit(self, 'music_stopped', {})
    
    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music_playing and self.music:
            was_playing = True
            self.stop_music()
            if was_playing:
                self.play_music(self.music['original'], loop=self.music['loop'], volume=self.music_volume)
    
    def mute(self):
        self.muted = True
        self.stop_music()
        global_bus.emit(self, 'audio_muted', {})
    
    def unmute(self):
        self.muted = False
        global_bus.emit(self, 'audio_unmuted', {})
    
    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            self.stop_music()
            global_bus.emit(self, 'audio_muted', {})
        else:
            global_bus.emit(self, 'audio_unmuted', {})
    
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