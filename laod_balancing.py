import random
import math

class Whale:
    def __init__(self, id, resources):
        self.id = id
        self.resources = resources
        self.fitness = None

def initialize_whales(num_whales, max_resources):
    whales = []
    for i in range(num_whales):
        resources = {
            'CPU': random.uniform(0.5, max_resources['CPU']),
            'Bandwidth': random.uniform(1, max_resources['Bandwidth']),
            'Memory': random.uniform(1, max_resources['Memory'])
        }
        whales.append(Whale(i, resources))
    return whales

def calculate_fitness(whale, task):
    fitness = 0
    for resource_type, requirement in task['resources'].items():
        if resource_type in whale.resources and whale.resources[resource_type] >= requirement:
            fitness += 1
    return fitness

def update_position(whale, best_whale, a, A, C, l, p, max_resources):
    for resource_type, _ in whale.resources.items():
        if best_whale is not None:  # Ensure best_whale is defined
            dist_to_leader = abs(best_whale.resources[resource_type] - whale.resources[resource_type])
            whale.resources[resource_type] = best_whale.resources[resource_type] - A * dist_to_leader * math.exp(a * l) * math.cos(2 * math.pi * l)
        else:
            whale.resources[resource_type] = random.uniform(0, max_resources[resource_type])
    # Ensure the whale doesn't go beyond the search space
    for resource_type, value in whale.resources.items():
        whale.resources[resource_type] = max(0, min(value, max_resources[resource_type]))
def woa(whales, tasks, max_iterations):
    max_resources = {'CPU': 5, 'Bandwidth': 5, 'Memory': 10}  # Define max_resources within the woa function
    for whale in whales:
        whale.fitness = calculate_fitness(whale, tasks[0])  # Calculate initial fitness for each whale

    for t in range(max_iterations):
        best_whale = min(whales, key=lambda whale: whale.fitness)  # Update best whale for each iteration
        for whale in whales:
            a = 2 - t * (2 / max_iterations)  # Linearly decreases from 2 to 0
            A = 2 * random.random() - 1  # A in [-1, 1]
            C = 2 * random.random()  # C in [0, 2]
            l = random.uniform(-1, 1)
            p = random.random()
            update_position(whale, best_whale, a, A, C, l, p, max_resources)  # Pass max_resources to update_position
            whale.fitness = calculate_fitness(whale, tasks[0])  # Recalculate fitness

    best_whale = min(whales, key=lambda whale: whale.fitness)
    return best_whale

# Modify test cases accordingly
def test_basic_scenario():
    num_whales = 5
    max_iterations = 100

    whales = initialize_whales(num_whales)
    tasks = [
        {'resources': {'CPU': 2, 'Bandwidth': 3, 'Memory': 3}},
        {'resources': {'CPU': 1, 'Bandwidth': 2, 'Memory': 1}},
        {'resources': {'CPU': 3, 'Bandwidth': 4, 'Memory': 2}},
        {'resources': {'CPU': 1, 'Bandwidth': 1, 'Memory': 1}}
    ]

    best_whale = woa(whales, tasks, max_iterations)
    print("Best Whale:", best_whale.id)
def test_basic_scenario():
    num_whales = 5
    max_resources = {'CPU': 10, 'Bandwidth': 20, 'Memory': 20}
    max_iterations = 100

    whales = initialize_whales(num_whales, max_resources)  # Pass max_resources to initialize_whales
    tasks = [
        {'resources': {'CPU': 2, 'Bandwidth': 3, 'Memory': 3}},
        {'resources': {'CPU': 1, 'Bandwidth': 2, 'Memory': 1}},
        {'resources': {'CPU': 3, 'Bandwidth': 4, 'Memory': 2}},
        {'resources': {'CPU': 1, 'Bandwidth': 1, 'Memory': 1}}
    ]

    best_whale = woa(whales, tasks, max_iterations)
    print("Best Whale:", best_whale.id)

def test_edge_case_maximum_resources():
    num_whales = 5
    max_resources = {'CPU': 1000, 'Bandwidth': 1000, 'Memory': 1000}  # Maximum resources
    max_iterations = 100

    whales = initialize_whales(num_whales, max_resources)  # Pass max_resources to initialize_whales
    tasks = [
        {'resources': {'CPU': 10, 'Bandwidth': 20, 'Memory': 20}},
        {'resources': {'CPU': 5, 'Bandwidth': 10, 'Memory': 10}},
        {'resources': {'CPU': 15, 'Bandwidth': 30, 'Memory': 30}},
        {'resources': {'CPU': 3, 'Bandwidth': 6, 'Memory': 6}}
    ]

    best_whale = woa(whales, tasks, max_iterations)
    print("Best Whale:", best_whale.id)

# Add more test cases as needed...

if __name__ == "__main__":
    test_basic_scenario()
    test_edge_case_maximum_resources()
