from gamelib.core.model.components.image_for_base_gameObj import Component

class AnimationComponent(Component):
    def __init__(self, frames, frame_duration=100):
        self.frames = frames  # список изображений
        self.frame_duration = frame_duration  # мс
        self.current_frame = 0
        self.playing = False
        self.loop = True
        
    def play(self, loop=True):
        self.playing = True
        self.loop = loop
        self._animate()
    
    def _animate(self):
        if not self.playing:
            return
        # Смена кадра
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        # Обновление изображения
        if self.obj and hasattr(self.obj, 'update_image'):
            self.obj.update_image(self.frames[self.current_frame])
        # Планирование следующего кадра
        if self.playing and (self.loop or self.current_frame < len(self.frames)-1):
            self.obj.canvas.after(self.frame_duration, self._animate)