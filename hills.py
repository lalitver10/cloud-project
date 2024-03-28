import random
import copy

# Define parameters
NUM_FOG_DEVICES = 8
MAX_ITER = 1000
NUM_RESOURCES = 100

# Define resource capacities for each fog device
resource_capacities = [
    {'memory': 1024, 'bandwidth': 100, 'CPU_utilization': 1},
    {'memory': 2048, 'bandwidth': 150, 'CPU_utilization': 1},
    {'memory': 1536, 'bandwidth': 120, 'CPU_utilization': 1},
    {'memory': 512, 'bandwidth': 80, 'CPU_utilization': 1},
    {'memory': 1024, 'bandwidth': 100, 'CPU_utilization': 1}
]

# Processing time for each resource on each fog device (example data)
processing_times = [[random.randint(1, 10) for _ in range(NUM_RESOURCES)] for _ in range(NUM_FOG_DEVICES)]

# Generate a random initial solution
def generate_random_solution():
    solution = {}
    for resource in range(NUM_RESOURCES):
        fog_device = random.randint(0, NUM_FOG_DEVICES - 1)
        solution[resource] = fog_device
    return solution

# Calculate the makespan of a solution
def calculate_makespan(solution):
    fog_completion_times = [0] * NUM_FOG_DEVICES
    for resource, fog_device in solution.items():
        fog_completion_times[fog_device] += processing_times[fog_device][resource]
    return max(fog_completion_times)

# Generate a neighbor solution by moving one resource
def generate_neighbor(solution):
    neighbor = copy.deepcopy(solution)
    resource_to_change = random.choice(list(neighbor.keys()))
    new_fog_device = random.randint(0, NUM_FOG_DEVICES - 1)
    neighbor[resource_to_change] = new_fog_device
    return neighbor

# Hill Climbing algorithm
def hill_climbing():
    current_solution = generate_random_solution()
    current_cost = calculate_makespan(current_solution)
    for _ in range(MAX_ITER):
        neighbor = generate_neighbor(current_solution)
        neighbor_cost = calculate_makespan(neighbor)
        if neighbor_cost < current_cost:
            current_solution = neighbor
            current_cost = neighbor_cost
    return current_solution, current_cost

# Example usage
best_solution, best_makespan = hill_climbing()
print("Best solution:", best_solution)
print("Makespan:", best_makespan)
