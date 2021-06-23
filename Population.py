import pygame
from Vector2D import Vector2D
from math import ceil, floor
from SelfDrivingCar import SelfDrivingCar
from random import randint

cnt = 0

class Population:

    def __init__(self, MAP, num_cars, cars=None, max_ticks=15000):
        self.map = MAP
        self.size = num_cars
        self.max_ticks = max_ticks
        self.ticks = 0
        self.best_car = None
        self.neural_network_surface = pygame.surface.Surface((600, 800))

        if cars != None:
            self.cars: list[SelfDrivingCar] = cars
        else:
            self.cars: list[SelfDrivingCar] = []

            for i in range(self.size):
                self.cars.append(SelfDrivingCar(160, 100, self.map))

    def draw(self, SURFACE, IMAGE):
        prev_best_car = self.best_car

        best_score = -1
        self.best_car = self.cars[0]
        for car in self.cars:
            if car.fitness > best_score and car.alive:
                best_score = car.fitness
                self.best_car = car

        self.best_car.draw(SURFACE, IMAGE)
        readings = ""
        for sensor in self.best_car.sensors:
            readings += str(round(sensor.get_reading(self.best_car.car.position.x, self.best_car.car.position.y, self.best_car.car.get_facing(), SURFACE), 2))
            readings += "  "
        font = pygame.font.SysFont('Comic Sans MS', 12)
        textsurface = font.render("Sensors: " + readings, False, (255,255,255))
        SURFACE.blit(textsurface, (800, 20))

        str_score = str(self.best_car.fitness)
        score_surface = font.render("Fitness: " + str_score, False, (255, 255, 255))
        SURFACE.blit(score_surface, (800, 40))

        throttle, steer = self.best_car.apply_nn_throttle(simulate=True)
        throttle_surface = font.render("Throttle: " + str(throttle), False, (255, 255, 255))
        SURFACE.blit(throttle_surface, (800, 60))

        steer_surface = font.render("Steer: " + str(steer), False, (255, 255, 255))
        SURFACE.blit(steer_surface, (800, 80))

        # If the best network has changed, redraw it
        if prev_best_car is not self.best_car:
            self.best_car.neural_net.draw_network(self.neural_network_surface)
        SURFACE.blit(self.neural_network_surface, (1280, 20))
    

    def apply_nn_throttle(self, SURFACE=None):
        for car in self.cars:
            car.apply_nn_throttle(SURFACE)
        
    def compute_movement(self, FPS):
        for car in self.cars:
            car.compute_movement(FPS)
    
    def score(self, MAP):
        self.ticks += 1

        if self.ticks >= self.max_ticks:
            return self.generate_next_generation()

        for car in self.cars:
            if car.alive:
                break
        else:
            return self.generate_next_generation()

        best_score = -1
        best_car = self.cars[0]
        for car in self.cars:
            car.score(MAP)

            if car.fitness > best_score:
                best_score = car.fitness
                best_car = car
                
        return self
        
    def generate_next_generation(self):
        global cnt

        self.cars.sort(reverse=True)

        print("POPULATION", cnt, "FITNESS")
        for car in self.cars:
            print(round(car.fitness, 3), end=', ')
        print()
        cnt += 1

        new_cars = []
        cars_left = self.size

        randomness_bucket = []
        counter = self.size * int(self.size / 5)
        sub = 4 * int(self.size / 5)
        for i in range(self.size):
            for j in range(floor(self.cars[i].fitness)):
                randomness_bucket.append(i)
            
            counter -= sub
            counter = max(0, counter)

        # Top 10% surive to next generation
        for i in range(ceil(0.1 * cars_left)):
            new_car = SelfDrivingCar(160, 100, self.cars[i].map)
            new_car.neural_net = self.cars[i].neural_net
            new_cars.append(new_car)

        cars_left = self.size - len(new_cars)

        # Next are bred (priority to higher fitness) with mutations
        for i in range(ceil(0.7 * cars_left)):
            idx1 = randint(0, len(randomness_bucket) - 1)
            idx2 = idx1
            while idx2 == idx1:
                idx2 = randint(0, len(randomness_bucket) - 1)

            new_cars.append(self.cars[randomness_bucket[idx1]].cross(self.cars[randomness_bucket[idx2]]))

        cars_left = self.size - len(new_cars)

        # Rest are randomly generated again
        for i in range(cars_left):
            new_cars.append(SelfDrivingCar(160, 100, self.map))

        return Population(self.map, self.size, new_cars)
