# DSAI3202 - Lab 06: Parallel Computing with MPI and Multiprocessing

## Overview
This lab demonstrates the implementation of parallel computing concepts using both MPI (Message Passing Interface) and Python's multiprocessing module. The lab focuses on creating a distributed system that performs parallel computation of square numbers across multiple processes.

## Key Concepts Covered

### 1. MPI (Message Passing Interface)
- Process Communication
- Rank-based Process Identification
- Data Gathering and Distribution
- Collective Communication Operations

### 2. Python Multiprocessing
- Process Pool Management
- Parallel Task Execution
- Worker Process Distribution
- Resource Management

### 3. Hybrid Parallel Computing
- Combining MPI and Multiprocessing
- Nested Parallelism
- Process Coordination
- Time-based Task Management

## Implementation Details

The lab implements a parallel computing system that:
1. Uses MPI to distribute work across multiple nodes
2. Utilizes Python's multiprocessing to parallelize tasks within each node
3. Computes square numbers in parallel with a time limit
4. Gathers and aggregates results from all processes

### Key Components:
- `square_wrapper`: Handles individual square computations
- `parallel_square_worker`: Manages parallel processing within each MPI rank
- `main`: Coordinates MPI processes and result aggregation

## How to Run

1. Ensure you have the required dependencies:
   ```bash
   pip install mpi4py numpy
   ```

2. Run the program using mpirun:
   ```bash
   mpirun -n <number_of_processes> python main.py
   ```

## Expected Output
The program will:
- Display progress from each rank
- Show the highest square computed
- Report the total number of squares computed
- Indicate when the time limit is reached

## Learning Outcomes
- Understanding distributed computing principles
- Implementing hybrid parallel processing
- Managing process communication and coordination
- Handling time-based task execution
- Working with both MPI and Python multiprocessing
