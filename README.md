# Distributed Virus Spread Simulation Lab

## Overview
This lab demonstrates the implementation of a distributed virus spread simulation using MPI (Message Passing Interface) for parallel computing. The simulation models how a virus spreads through a population while taking into account vaccination rates and infection probabilities.

## Key Concepts

### 1. MPI (Message Passing Interface)
- Used for distributed computing across multiple machines
- Implements a master-worker pattern where rank 0 acts as the coordinator
- Demonstrates inter-process communication using `comm.send()` and `comm.recv()`

### 2. Virus Spread Simulation
- Models a population of individuals in three states:
  - 0: Uninfected
  - 1: Infected
  - 2: Vaccinated
- Implements virus spread mechanics:
  - Random initial infection (10% of population)
  - Neighbor-based infection spread
  - Configurable spread probability (30%)
  - Random vaccination rate (10-50%)

### 3. Distributed Computing Features
- Population is distributed across multiple processes
- Each process handles a portion of the population
- Data aggregation at rank 0 for global state updates
- Synchronized simulation steps across all processes

## Implementation Details

### Population Management
- Population size: 100 individuals
- Initial infection rate: 10% of unvaccinated population
- Virus spread chance: 30% per contact
- Vaccination rate: Random between 10-50%

### Simulation Process
1. MPI environment initialization
2. Population initialization with random vaccinations
3. Initial infection seeding
4. Iterative virus spread simulation (10 time steps)
5. Inter-process communication for state updates
6. Final infection rate calculation

### Communication Pattern
- Worker processes (rank > 0) send their population state to rank 0
- Rank 0 aggregates data and broadcasts updated state
- Ensures consistent global state across all processes

## Running the Simulation
The simulation can be run using MPI:
```bash
mpirun -np <number_of_processes> python main.py
```

## Learning Outcomes
1. Understanding distributed computing concepts
2. Implementing MPI-based parallel processing
3. Modeling complex systems (virus spread) in a distributed environment
4. Managing state synchronization across multiple processes
5. Working with probability-based simulations
6. Implementing master-worker patterns in distributed systems

## Technical Requirements
- Python with mpi4py package
- MPI implementation (e.g., OpenMPI)
- Multiple machines for distributed execution (configured in machines.txt)