import random
import copy

# Define parameters
NUM_FOG_DEVICES = 10
MAX_ITER = 1000
NUM_RESOURCES = 100
# Define resource capacities for each fog device
resource_capacities = [
    {'memory': 1024, 'bandwidth': 100, 'CPU_utilization': 1},
    {'memory': 2048, 'bandwidth': 150, 'CPU_utilization': 1},
    {'memory': 1536, 'bandwidth': 120, 'CPU_utilization': 1},
    {'memory': 512, 'bandwidth': 80, 'CPU_utilization': 1},
    {'memory': 1024, 'bandwidth': 100, 'CPU_utilization': 1},
    {'memory': 1024, 'bandwidth': 100, 'CPU_utilization': 1},
    {'memory': 2048, 'bandwidth': 150, 'CPU_utilization': 1},
    {'memory': 1536, 'bandwidth': 120, 'CPU_utilization': 1},
    {'memory': 512, 'bandwidth': 80, 'CPU_utilization': 1},
    {'memory': 1024, 'bandwidth': 100, 'CPU_utilization': 1}
]

# Processing time for each resource on each fog device 

processing_times = [[random.randint(1, 10) for _ in range(NUM_RESOURCES)] for _ in range(NUM_FOG_DEVICES)]

# Define objective function (to be minimized)
def objective_function(solution):
    makespan = calculate_makespan(solution)
    return makespan

# Calculate makespan for a solution
def calculate_makespan(solution):
    fog_completion_times = [0] * NUM_FOG_DEVICES
    for resource, fog_device in solution.items():
        fog_completion_times[fog_device] += processing_times[fog_device][resource]
    return max(fog_completion_times)

# Initialize population of solutions (random assignment of resources to fog devices)
def initialize_population():
    population = []
    for _ in range(NUM_FOG_DEVICES):
        solution = generate_valid_solution()
        population.append(solution)
    return population

# Generate a valid solution respecting resource constraints
def generate_valid_solution():
    solution = {}
    for resource in range(NUM_RESOURCES):
        fog_device = random.randint(0, NUM_FOG_DEVICES - 1)
        if check_resource_constraints(solution, fog_device, resource):
            solution[resource] = fog_device
    return solution

# Check if assigning a resource to a fog device violates resource constraints
def check_resource_constraints(solution, fog_device, resource):
    if fog_device in solution.values():
        memory_usage = sum(processing_times[fog_device][r] for r, f in solution.items() if f == fog_device)
        memory_usage += processing_times[fog_device][resource]
        if memory_usage > resource_capacities[fog_device]['memory']:
            return False
    return True

# Employed bees phase
def employed_bees_phase(population):
    new_population = []
    for solution in population:
        for _ in range(NUM_RESOURCES):  # Each employed bee tries to improve the solution by one resource
            new_solution = copy.deepcopy(solution)
            resource_to_change = random.choice(list(new_solution.keys()))
            new_fog_device = random.randint(0, NUM_FOG_DEVICES - 1)
            if check_resource_constraints(new_solution, new_fog_device, resource_to_change):
                new_solution[resource_to_change] = new_fog_device
            if objective_function(new_solution) < objective_function(solution):
                solution = new_solution
        new_population.append(solution)
    return new_population

# Onlooker bees phase
def onlooker_bees_phase(population):
    fitness_values = [1 / (objective_function(solution) + 1) for solution in population]
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]
    new_population = []
    for _ in range(NUM_FOG_DEVICES):
        selected_index = roulette_wheel_selection(probabilities)
        new_population.append(population[selected_index])
    return new_population

def roulette_wheel_selection(probabilities):
    r = random.uniform(0, 1)
    c = probabilities[0]
    i = 0
    while c < r:
        i += 1
        c += probabilities[i]
    return i

# Scout bees phase (abandon solutions that haven't improved)
def scout_bees_phase(population):
    new_population = []
    for solution in population:
        if random.random() < 0.1:  # Probability of abandonment (adjust as needed)
            new_population.append(generate_valid_solution())
        else:
            new_population.append(solution)
    return new_population

# Main function for HBOA
def honey_bee_optimization():
    population = initialize_population()
    for iteration in range(MAX_ITER):
        population = employed_bees_phase(population)
        population = onlooker_bees_phase(population)
        population = scout_bees_phase(population)
    # Select the best solution
    best_solution = min(population, key=objective_function)
    return best_solution

# Generate dummy input for requests
def generate_dummy_requests():
    requests = []
    for i in range(100):
        arrival_time = random.randint(0, 200)
        data_size = random.randint(50, 200)
        deadline = random.randint(200, 400)
        CPU_utilization = round(random.uniform(0.5, 0.9), 2)
        bandwidth = random.randint(10, 20)
        memory = random.choice([256, 512, 768, 1024, 1536])
        requests.append({'arrival_time': arrival_time, 'data_size': data_size, 'deadline': deadline, 'resources': {'CPU_utilization': CPU_utilization, 'bandwidth': bandwidth, 'memory': memory}})
    return requests

# Example usage
print("Generating dummy input for 5 requests...")
requests = generate_dummy_requests()
print("\nRunning optimization algorithm...\n")
best_solution = honey_bee_optimization()
print("\nBest solution:", best_solution)
print("Makespan:", calculate_makespan(best_solution))
