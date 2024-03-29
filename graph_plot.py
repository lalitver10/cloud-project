import matplotlib.pyplot as plt

# Data for three algorithms
algorithms = ['BES', 'HBO', 'Hills']
num_fog_devices = [1,2,5,10]  # Number of fog devices
makespan = {
    'BES': [540,244, 102,55],  # Makespan 
    'HBO': [557, 264, 111,63],  # Makespan
    'Hills': [534,274,124,83]  # Makespan 
}

# Create bar graph
bar_width = 0.25
index = range(len(num_fog_devices))

for i, algo in enumerate(algorithms):
    plt.bar([x + i * bar_width for x in index], makespan[algo], bar_width, label=algo)

plt.xlabel('Number of Fog Devices')
plt.ylabel('Makespan')
plt.title('Comparison of Algorithms with Varying Number of Fog Devices')
plt.xticks([i + bar_width for i in index], num_fog_devices)
plt.legend()
plt.tight_layout()

# Show plot
plt.show()
