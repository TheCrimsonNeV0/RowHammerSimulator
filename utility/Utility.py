import Configurations


def generate_list_of_lists(i):
    if i < 2:
        raise ValueError("i must be greater than or equal to 2.")
    if i % 2 != 0:
        i -= 1
    result = []
    for x in range(1, i, 2):
        result.append([x, x + 2])
    return result

# Gradient ascent algorithm
def gradient_ascent(p, adaptation_rate=Configurations.ARAR_ADAPTATION_RATE):
    if p <= Configurations.ARAR_PROBABILITY_END:
        gradient_value = gradient_function_arar(p)  # Compute the gradient at the current value of p
        p += adaptation_rate * gradient_value  # Update p by moving in the direction of the gradient
        return p
    return Configurations.ARAR_PROBABILITY_END


# Mathematical utility functions for ARAR gradient ascent
def function_arar(p):
    return -(p - 1) ** 2


def gradient_function_arar(p):
    return -2 * (p - 1)