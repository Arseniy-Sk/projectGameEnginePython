import math


class Vector2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    @classmethod
    def from_angle(cls, magnitude, angle_degrees):
        angle_rad = math.radians(angle_degrees)
        return cls(magnitude * math.cos(angle_rad), magnitude * math.sin(angle_rad))
    
    @classmethod
    def from_points(cls, start_x, start_y, end_x, end_y):
        return cls(end_x - start_x, end_y - start_y)
    
    def magnitude(self):
        return math.hypot(self.x, self.y)
    
    def normalized(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
    
    def angle(self):
        angle = math.degrees(math.atan2(self.y, self.x))
        return angle if angle >= 0 else angle + 360
    
    def scale(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(other - self.x, other - self.y)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)) and other != 0:
            return Vector2(self.x / other, self.y / other)
        return NotImplemented
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __eq__(self, other):
        return isinstance(other, Vector2) and self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError("Vector2 index out of range")
    
    def __setitem__(self, index, value):
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