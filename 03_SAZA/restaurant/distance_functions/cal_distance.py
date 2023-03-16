import math

def get_distance(current, destination): 
    return math.dist(current, destination)

def check_1km(distance):
    if (distance > 0.01):
        return False
    else:
        return True

