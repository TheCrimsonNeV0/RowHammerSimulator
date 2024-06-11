import numpy as np

# Define the function f(p) = -(p - 1)^2
def f(p):
    return -(p - 1)**2

# Define the gradient of the function, which is the derivative
def gradient_f(p):
    return -2 * (p - 1)

# Gradient ascent algorithm
def gradient_ascent(starting_p, learning_rate, iterations):
    p = starting_p
    for i in range(iterations):
        grad = gradient_f(p)      # Compute the gradient at the current value of p
        p += learning_rate * grad # Update p by moving in the direction of the gradient
        print(f"Iteration {i+1}: p = {p}, f(p) = {f(p)}")
    return p

# Parameters for the gradient ascent
starting_p = 0.001
learning_rate = 0.1
iterations = 100

# Run the gradient ascent algorithm
optimal_p = gradient_ascent(starting_p, learning_rate, iterations)
print(f"Optimal p: {optimal_p}")
