from Population import Population
import numpy
from NeuralNetwork import Layer, NeuralNetwork
from math import inf
from Map import Map
import pygame
import pygame.time
from Car import Car
from Vector2D import Vector2D
from time import sleep
from SelfDrivingCar import SelfDrivingCar, Sensor
import os, sys
from pygame.locals import *
import numpy as np

# For pyinstaller exports (ignore)
def resource_path(relative_path):
    return relative_path

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

flags = DOUBLEBUF
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH + 600, HEIGHT))
pygame.font.init()
CAR_SURFACE = pygame.surface.Surface((WIDTH + 600, HEIGHT), pygame.SRCALPHA, 32)
CAR_SURFACE = CAR_SURFACE.convert_alpha()
OBSTACLE_SURFACE = pygame.surface.Surface((WIDTH, HEIGHT))
TEST_SURFACE = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)

WHITE = (255, 255, 255)
EMPTY = pygame.Color(0,0,0,0)

FPS = 15
CAR_IMAGE = pygame.image.load(resource_path('./assets/box.png')).convert()

MAP = Map(resource_path(input("Enter map name: ")), 64, 36, 1280, 720)
MAP.read()

CLOCK = pygame.time.Clock()

# Main pygame loop
def main():
    global CAR_IMAGE
    run = True
    population = Population(MAP, 40)

    OBSTACLE_SURFACE.fill(WHITE)
    MAP.draw(OBSTACLE_SURFACE)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        CAR_SURFACE.fill(EMPTY)

        population.draw(CAR_SURFACE, CAR_IMAGE)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_k]:
            population = population.generate_next_generation()

        population.apply_nn_throttle()
        population.compute_movement(FPS)
        population = population.score(MAP)
        
        WIN.blit(OBSTACLE_SURFACE, (0, 0)) 
        WIN.blit(CAR_SURFACE, (0, 0))

        pygame.display.flip()
    pygame.quit()

def compute_steer(keys_pressed) -> float:
    if keys_pressed[pygame.K_a]:
        return 0.25
    elif keys_pressed[pygame.K_d]:
        return 0.75
    
    return 0.5

def compute_throttle(keys_pressed) -> float:
    if keys_pressed[pygame.K_w]:
        return 1
    
    return 0

if __name__ == "__main__":
    main()