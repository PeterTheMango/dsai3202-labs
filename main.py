from mpi4py import MPI
import random

# Step 1: Initialize the MPI Environment
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Step 2: Define Parameters
population_size = 100
spread_chance = 0.3  # Probability of virus spread
vaccination_rate = random.uniform(0.1, 0.5)  # Random vaccination rate between 0.1 and 0.5

# Step 3: Initialize the Population
population = [0] * population_size  # 0 = uninfected, 1 = infected, 2 = vaccinated

# Vaccinate individuals randomly based on vaccination_rate
for i in range(population_size):
    if random.random() < vaccination_rate:
        population[i] = 2  # Vaccinated individuals

# Infect a small percentage (10%) of individuals initially in rank 0
if rank == 0:
    infected_count = int(0.1 * population_size)
    infected_indices = random.sample([i for i in range(population_size) if population[i] == 0], infected_count)
    for idx in infected_indices:
        population[idx] = 1  # Infect

# Step 4: Implement Virus Spread Function
def spread_virus(population):
    new_population = population[:]
    for i in range(len(population)):
        if population[i] == 1:  # If infected
            # Try to infect neighbors (left and right)
            neighbors = []
            if i > 0:
                neighbors.append(i - 1)
            if i < len(population) - 1:
                neighbors.append(i + 1)
            for neighbor in neighbors:
                if population[neighbor] == 0:  # Uninfected and not vaccinated
                    if random.random() < spread_chance:
                        new_population[neighbor] = 1  # Infect
    return new_population

# Step 5: Simulate Virus Spread
time_steps = 10
for _ in range(time_steps):
    population = spread_virus(population)
    
    # Communicate data to rank 0 for aggregation
    if rank != 0:
        comm.send(population, dest=0)
        population = comm.recv(source=0)  # Receive updated combined data
    else:
        # Rank 0 collects and aggregates data
        total_population = population[:]
        for i in range(1, size):
            received_population = comm.recv(source=i)
            # Aggregate infections
            for j in range(population_size):
                if received_population[j] == 1:
                    total_population[j] = 1  # Update infection if any process has it
        # Send updated data back to other ranks
        for i in range(1, size):
            comm.send(total_population, dest=i)
        population = total_population

# Step 6: Calculate Infection Rate
infected_total = sum(1 for i in population if i == 1)
infection_rate = infected_total / population_size
print(f"Process {rank}: Vaccination Rate = {vaccination_rate:.2f}, Infection Rate = {infection_rate:.2f}")
