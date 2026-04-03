# gamelib/core/model/vectors/verctor2.py
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
    
    # Магические методы для арифметических операций
    def __add__(self, other):
        """Сложение векторов: v1 + v2"""
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        else:
            return NotImplemented
    
    def __radd__(self, other):
        """Правое сложение: other + v1"""
        return self.__add__(other)
    
    def __sub__(self, other):
        """Вычитание векторов: v1 - v2"""
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)
        else:
            return NotImplemented
    
    def __rsub__(self, other):
        """Правое вычитание: other - v1"""
        if isinstance(other, (int, float)):
            return Vector2(other - self.x, other - self.y)
        return NotImplemented
    
    def __mul__(self, other):
        """Умножение на скаляр: v1 * scalar"""
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        elif isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return NotImplemented
    
    def __rmul__(self, other):
        """Правое умножение: scalar * v1"""
        return self.__mul__(other)
    
    def __truediv__(self, other):
        """Деление на скаляр: v1 / scalar"""
        if isinstance(other, (int, float)) and other != 0:
            return Vector2(self.x / other, self.y / other)
        else:
            return NotImplemented
    
    def __neg__(self):
        """Унарный минус: -v1"""
        return Vector2(-self.x, -self.y)
    
    def __eq__(self, other):
        """Сравнение на равенство: v1 == v2"""
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False
    
    def __ne__(self, other):
        """Сравнение на неравенство: v1 != v2"""
        return not self.__eq__(other)
    
    def __iter__(self):
        """Итератор для распаковки"""
        yield self.x
        yield self.y
    
    def __getitem__(self, index):
        """Доступ по индексу: v[0], v[1]"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector2 index out of range")
    
    def __setitem__(self, index, value):
        """Установка значения по индексу: v[0] = 5"""
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Vector2 index out of range")
    
    def __str__(self):
        return f"Vector2({self.x:.2f}, {self.y:.2f})"
    
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"