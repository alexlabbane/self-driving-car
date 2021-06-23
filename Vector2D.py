from math import sqrt, asin, degrees, sin, cos
import numpy as np

class Vector2D:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return str(round(self.x, 2)) + ", " + str(round(self.y, 2))

    def __add__(self, o):
        return Vector2D(self.x + o.x, self.y + o.y)
    
    def copy(self):
        return Vector2D(self.x, self.y)

    def scale(self, scale):
        self.x *= scale
        self.y *= scale

        return self

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def cross_magnitude(self, o):
        return self.x * o.y - self.y * o.x

    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2)
    
    def normalized(self):
        magnitude = self.magnitude()

        if abs(magnitude) < 1e-6:
            return Vector2D(0, 0)

        return Vector2D(self.x / magnitude, self.y / magnitude)

    def dist_squared(self, o):
        return (self.x - o.x)**2 + (self.y - o.y)**2

    def dist(self, o):
        return sqrt(self.dist_squared(o))

    # Rotate counter-clockwise by deg
    def rotated(self, deg):
        rad = np.deg2rad(deg)

        cosine = cos(rad)
        sine = sin(rad)

        new_vector = Vector2D(
            self.x * cosine - self.y * sine,
            self.x * sine + self.y * cosine
        )

        return new_vector

    def angle(self, v):

        u = self

        if(u.magnitude() * v.magnitude() < 1e-2):
            return 0
        return degrees(np.arctan2(-self.y, self.x))