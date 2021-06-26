# Self Driving Car
To gain a little bit of experience with machine learning concepts, I wanted to build a small python program that could train a neural network to drive a car on a 2D plane with a genetic algorithm. I wanted to avoid using libraries as much as possible and write the machine learning portion on my own.

# Description
This project uses pygame to simulate 40 cars driving in a top-down view on a driving course. Each car is given 7 distance sensors that measure the distance (in pixels) to the nearest wall. In generation 0, each of the 40 cars are given neural network with randomly generated weights. At the end of each generation, the best performers have their neural networks "bred" and passed to the next generation.

The networks take the distances from the 7 sensors as inputs and output 2 values: throttle and steer. Throttle simply controls the acceleration of the car, while steer is used to determine which direction the car should turn and how quickly. Note that only the current "lead" car is shown on the screen in each generation.

# Neural Network
I didn't spend much time optimizing the neural network structure, but I opted for two hidden layers and use the RELU activation function for all neurons (except for the output neurons, which use sigmoid to crunch the value into the range (0, 1)).

Numpy was used to compute the outputs for each layer of the neural network to take advantage of its fast matrix operations (although I spent very little effort optimizing the performance of the program). While the cars are training, the structure of the best car's neural network can be seen on the right side of the screen. See the video below for more details.

# Video
[![YouTube Video](https://img.youtube.com/vi/KPhiy4DYCsc/0.jpg)](https://youtu.be/KPhiy4DYCsc)
