import random

# Define classes for resources and requests
class CloudResource:
    def _init_(self, cpu_rate, bandwidth, memory):
        self.cpu_rate = cpu_rate
        self.bandwidth = bandwidth
        self.memory = memory

class FogResource:
    def _init_(self, name, cpu_rate, bandwidth, memory):
        self.name = name
        self.cpu_rate = cpu_rate
        self.bandwidth = bandwidth
        self.memory = memory

    def _str_(self):
        return f"FogResource(name={self.name}, cpu_rate={self.cpu_rate}, bandwidth={self.bandwidth}, memory={self.memory})"

class ServiceRequest:
    def _init_(self, arrival_time, data_size, cpu_requirements, memory_requirements, bandwidth_requirements):
        self.arrival_time = arrival_time
        self.data_size = data_size
        self.deadline = arrival_time + 50
        self.cpu_requirements = cpu_requirements
        self.memory_requirements = memory_requirements
        self.bandwidth_requirements = bandwidth_requirements

    def _str_(self):
        return f"ServiceRequest(arrival_time={self.arrival_time}, data_size={self.data_size}, deadline={self.deadline}, cpu_requirements={self.cpu_requirements}, memory_requirements={self.memory_requirements}, bandwidth_requirements={self.bandwidth_requirements})"

# Define DRAM algorithm
# def dram(service_requests, fog_nodes, cloud_node):
#     for request in service_requests:
#         if request.arrival_time < request.deadline:
#             fog_node = select_fog_node(fog_nodes, request)
#             if fog_node is not None:
#                 execute_request(fog_node, request)
#             else:
#                 execute_request(cloud_node, request)

def dram(service_requests, fog_nodes, cloud_node):
    start_time = min(request.arrival_time for request in service_requests)
    end_time = start_time  # Initialize end time as start time
    
    total_energy_consumption = 0
    
    for request in service_requests:
        if request.arrival_time < request.deadline:
            fog_node = select_fog_node(fog_nodes, request)
            if fog_node is not None:
                execute_request(fog_node, request)
                end_time = max(end_time, request.arrival_time)  # Update end time
                total_energy_consumption += calculate_energy_consumption(fog_node, request)
            else:
                execute_request(cloud_node, request)
                end_time = max(end_time, request.arrival_time)  # Update end time
                total_energy_consumption += calculate_energy_consumption(cloud_node, request)

    makespan = end_time - start_time
    
    return makespan, total_energy_consumption


def calculate_energy_consumption(node, request):
    # Assuming energy consumption formula based on CPU, memory, and bandwidth usage
    # This is a simplified example, actual formulas may vary
    fog_energy = node.cpu_rate * request.cpu_requirements + node.memory * request.memory_requirements + node.bandwidth * request.bandwidth_requirements
    return fog_energy


def select_fog_node(fog_nodes, request):
    for fog_node in fog_nodes:
        if fog_node.cpu_rate >= request.cpu_requirements and fog_node.memory >= request.memory_requirements and fog_node.bandwidth >= request.bandwidth_requirements:
            return fog_node
    return None

def execute_request(node, request):
    print(f"Executing request {request} on {node}.")

# Configuration values
cloud_node = CloudResource(cpu_rate=44000, bandwidth=10000, memory=40000)
fog_nodes = [
    FogResource(name="FogNode1", cpu_rate=22000, bandwidth=8000, memory=8000),
    FogResource(name="FogNode2", cpu_rate=22000, bandwidth=8000, memory=8000)
]

# Simulate service requests
service_requests = [
    ServiceRequest(arrival_time=random.randint(0, 10), 
                   data_size=random.randint(10, 500), 
                   cpu_requirements=random.randint(10, 2000), 
                   memory_requirements=random.randint(10, 1600), 
                   bandwidth_requirements=random.randint(10, 1600))
    for _ in range(10)  # Reduced number of requests for readability
]

# Execute DRAM algorithm
# dram(service_requests, fog_nodes, cloud_node)
# Usage
makespan, energy_consumption = dram(service_requests, fog_nodes, cloud_node)
print(f"Makespan: {makespan} ms")
print(f"Total Energy Consumption: {energy_consumption} J")