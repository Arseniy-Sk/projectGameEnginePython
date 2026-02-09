import math

class Vector2():
    def __init__(self, x=0, y=0):
        """Инициализация вектора. По умолчанию нулевой вектор."""
        self.x = x
        self.y = y
    
    @classmethod
    def from_angle(cls, magnitude, angle_degrees):
        """Создает вектор из величины и угла (в градусах)"""
        angle_radians = math.radians(angle_degrees)
        x = magnitude * math.cos(angle_radians)
        y = magnitude * math.sin(angle_radians)
        return cls(x, y)
    
    @classmethod
    def from_points(cls, start_x, start_y, end_x, end_y):
        """Создает вектор из двух точек"""
        return cls(end_x - start_x, end_y - start_y)
    
    def magnitude(self):
        """Возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalized(self):
        """Возвращает нормализованный вектор (длиной 1)"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
    
    def angle(self):
        """Возвращает угол вектора в градусах (от 0 до 360)"""
        angle_rad = math.atan2(self.y, self.x)
        angle_deg = math.degrees(angle_rad)
        
        # Приводим угол к диапазону 0-360 градусов
        if angle_deg < 0:
            angle_deg += 360
        return angle_deg
    
    def scale(self, scalar):
        """Умножает вектор на скаляр"""
        return Vector2(self.x * scalar, self.y * scalar)
    
    def add(self, other):
        """Складывает два вектора"""
        return Vector2(self.x + other.x, self.y + other.y)
    
    def dot(self, other):
        """Скалярное произведение двух векторов"""
        return self.x * other.x + self.y * other.y
    
    def __str__(self):
        return f"Vector2({self.x:.2f}, {self.y:.2f})"
    
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
