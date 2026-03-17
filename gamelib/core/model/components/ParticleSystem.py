from gamelib.core.model.components.image_for_base_gameObj import Component

class Particle:
    def __init__(self, x, y, velocity, lifetime, color):
        self.x = x
        self.y = y
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.age = 0
        self.color = color
        self.active = True

class ParticleSystem(Component):
    def __init__(self, emission_rate=10):
        super().__init__()
        self.particles = []
        self.emission_rate = emission_rate
        self.emitting = False
        self.particle_texture = None
        
    def emit_burst(self, count, position, velocity_range):
        for _ in range(count):
            # Создание частиц с случайными параметрами
            pass
    
    def update(self):
        # Обновление позиций частиц
        # Удаление мертвых частиц
        # Отрисовка
        pass