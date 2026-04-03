# gamelib/core/model/audio/audio_component.py
from gamelib.core.model.audio.audio_system import global_audio
from gamelib.core.model.components.image_for_base_gameObj import Component
from gamelib.core.model.events.events_system import global_bus

class AudioSource(Component):
    """Компонент для воспроизведения звуков от игрового объекта"""
    
    def __init__(self):
        super().__init__()
        self.sounds = {}
        self.auto_play_on_collision = None
    
    def set_game_object(self, obj):
        super().set_game_object(obj)
    
    def add_sound(self, name, file_path):
        sound_key = f"{id(self.obj)}_{name}"
        if global_audio.load_sound(sound_key, file_path):
            self.sounds[name] = sound_key
            return True
        return False
    
    def play(self, sound_name, volume=None):
        if sound_name in self.sounds:
            global_audio.play_sound(self.sounds[sound_name], volume)
        else:
            print(f"⚠️ Звук {sound_name} не найден")
    
    def set_collision_sound(self, sound_name):
        self.auto_play_on_collision = sound_name
    
    def on_collision(self, other):
        if self.auto_play_on_collision:
            self.play(self.auto_play_on_collision)
            global_bus.emit(self.obj, 'collision_sound_played', 
                           {'sound': self.auto_play_on_collision, 'other': other})

class AudioListener(Component):
    """Компонент для прослушивания событий"""
    
    def __init__(self):
        super().__init__()
        self.event_sounds = {}
    
    def set_game_object(self, obj):
        super().set_game_object(obj)
        global_bus.subscribe(obj, None, self.on_event)
    
    def on_event(self, event):
        if event.type in self.event_sounds:
            global_audio.play_sound(self.event_sounds[event.type])
    
    def bind_event(self, event_type, sound_name):
        self.event_sounds[event_type] = sound_name
    
    def unbind_event(self, event_type):
        if event_type in self.event_sounds:
            del self.event_sounds[event_type]