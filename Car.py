from Vector2D import Vector2D
import pygame

class Car:
    GRAVITATIONAL_ACCELERATION: float = 1  # Makes it easy to deal with
    COEFFICIENT_OF_FRICTION: float = 0.05  # Technically should depend on surface car is driving on
    TERMINAL_VELOCITY = 5

    def __init__(self, x: float, y: float, mass: float = 1):
        self.facing = Vector2D(1, 0)
        self.position: Vector2D = Vector2D(x, y)
        self.velocity: Vector2D = Vector2D()
        self.acceleration: Vector2D = Vector2D()
        self.mass: float = mass

    def normal_force_magnitude(self) -> float:
        return self.mass * Car.GRAVITATIONAL_ACCELERATION

    def get_facing(self) -> Vector2D:
        if self.velocity.magnitude() > 1e-2:
            self.facing = self.velocity.normalized()

        return self.facing

    def frictional_force_magnitude(self) -> float:
        return Car.COEFFICIENT_OF_FRICTION * self.normal_force_magnitude()

    def frictional_acceleration_magnitude(self) -> float:
        return self.frictional_force_magnitude() / self.mass

    def frictional_acceleration(self) -> Vector2D:
        normalized_velocity: Vector2D = self.velocity.normalized()
        frictional_acceleration_magnitude = self.frictional_acceleration_magnitude()

        return Vector2D(
            -1 * normalized_velocity.x * frictional_acceleration_magnitude, 
            -1 * normalized_velocity.y * frictional_acceleration_magnitude
        )

    def apply_throttle(self, throttle: float):
        ''' Apply forward acceleration based on throttle '''
        dir = self.get_facing()
        accel = dir.copy().scale(throttle / 15)

        if self.velocity.magnitude() < Car.TERMINAL_VELOCITY:
            self.velocity = self.velocity + accel

    def steer(self, amount, FPS=15):
        ''' Steer the car left or right
            amount = 1 means to steer hard left
            amount = 0 means to steer hard right'''

        # when amount = 0, rotate velocity 90 degrees clockwise
        # when amount = 1, rotate velocity 90 degrees counter-clockwise
        # divide by FPS so that turn is not instant
        rotation_angle = (-90 + 180 * amount) / FPS / FPS

        self.velocity = self.velocity.rotated(rotation_angle)

    def move(self, FPS=15):
        self.position.x += self.velocity.x / FPS
        self.position.y += self.velocity.y / FPS

    def compute_movement(self, FPS=15):
        self.move(FPS)

    def draw(self, WINDOW, CAR_IMAGE):
        x_axis = Vector2D(1, 0)
        angle = self.velocity.angle(x_axis)

        if True or self.velocity.magnitude() < 0.1:
            angle = 0
        
        rot_image, rect = self.rot_center(CAR_IMAGE, angle, self.position.x, self.position.y)

        WINDOW.blit(rot_image, rect)

    def rot_center(self, image, angle, x, y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect