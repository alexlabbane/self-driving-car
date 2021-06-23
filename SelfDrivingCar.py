from math import inf
from NeuralNetwork import NeuralNetwork
from Map import Map
from Vector2D import Vector2D
from Car import Car

class Sensor:
    
    def __init__(self, pos_x: float, pos_y: float, angle: float, map: Map, color):
        self.pos = Vector2D(pos_x, pos_y)
        self.angle = angle
        self.map = map
        self.color = color

    def get_reading(self, x=None, y=None, dir: Vector2D = None, SURFACE=None):
        if x != None:
            self.pos.x = x
        if y != None:
            self.pos.y = y

        return self.map.cast_collision_ray(self.pos, dir.rotated(self.angle), SURFACE, self.color) - 16

class SelfDrivingCar:

    def __init__(self, x, y, map, mass: float = 1, max_ticks: int = 1000):
        self.map = map

        self.sensors = [
            Sensor(x, y, 0, map, [255,0,0]),
            Sensor(x, y, 30, map, [0,255,0]),
            Sensor(x, y, -30, map, [0,0,255]),
            Sensor(x, y, 45, map, [128, 128, 0]),
            Sensor(x, y, -45, map, [0, 128, 128]),
            Sensor(x, y, 75, map, [128, 0, 128]),
            Sensor(x, y, -75, map, [50, 100, 150]),
        ]

        self.neural_net = NeuralNetwork(7, 2, [4, 5])
        self.car = Car(x, y, mass)
        self.alive = True
        self.max_fitness = 0
        self.fitness = 0
        self.ticks = 0
        self.max_ticks = max_ticks

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def cross(self, partner):
        child_car = SelfDrivingCar(160, 100, self.map)
        child_car.neural_net = self.neural_net.cross(partner.neural_net)

        return child_car

    def score(self, MAP):
        if not self.alive:
            return

        score = min([
            MAP.score[int(self.car.position.y - 16)][int(self.car.position.x - 16)],
            MAP.score[int(self.car.position.y + 16)][int(self.car.position.x - 16)],
            MAP.score[int(self.car.position.y - 16)][int(self.car.position.x + 16)],
            MAP.score[int(self.car.position.y + 16)][int(self.car.position.x + 16)]
        ])

        if score == -inf:
            self.alive = False
            return

        self.ticks += 1

        if score > self.max_fitness:
            self.max_fitness = score
            self.ticks = 0

        if self.ticks >= self.max_ticks:
            self.alive = False
            return

        # Fitness is last score before it died
        self.fitness = score



    def normal_force_magnitude(self) -> float:
        return self.car.normal_force_magnitude()

    def frictional_force_magnitude(self) -> float:
        return self.car.frictional_force_magnitude()

    def frictional_acceleration_magnitude(self) -> float:
        return self.car.frictional_acceleration_magnitude()

    def frictional_acceleration(self) -> Vector2D:
        return self.car.frictional_acceleration()

    def apply_nn_throttle(self, simulate=False, SURFACE=None):
        if not self.alive:
            return 0, 0

        sensor_readings = [sensor.get_reading(self.car.position.x, self.car.position.y, self.car.get_facing(), SURFACE) for sensor in self.sensors]
        bigget_dist = max(sensor_readings)
        for i in range(len(sensor_readings)):
            sensor_readings[i] = sensor_readings[i] / bigget_dist

        nn_in = sensor_readings

        throttle, steer = self.neural_net.think(nn_in) # Between 0 and 1

        if not simulate:
            self.apply_throttle(throttle)
            self.steer(steer)

        return throttle, steer

    def apply_throttle(self, throttle: float):
        if not self.alive:
            return

        self.car.apply_throttle(throttle)

    def steer(self, amount, FPS=15):
        if not self.alive:
            return
        
        self.car.steer(amount, FPS)

    def accelerate(self, FPS):
        if not self.alive:
            return

        self.car.accelerate(FPS)

    def move(self, FPS):
        if not self.alive:
            return

        self.car.move(FPS)

    def compute_movement(self, FPS):
        if not self.alive:
            return

        self.car.compute_movement(FPS)

    def draw(self, WINDOW, CAR_IMAGE):
        if not self.alive:
            return
            
        self.car.draw(WINDOW, CAR_IMAGE)

    def rot_center(self, image, angle, x, y):
        return self.car.rot_center(image, angle, x, y)

    def get_sensor_readings(self, SURFACE=None):
        if not self.alive:
            return

        dists = []

        for sensor in self.sensors:
            sensor.pos = self.car.position
            dists.append(sensor.get_reading(SURFACE))
        
        return dists