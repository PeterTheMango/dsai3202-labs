# Maze Explorer Game

A simple maze exploration game built with Pygame where you can either manually navigate through a maze or watch an automated solver find its way to the exit.

### 1. Project Setup

1. Create and activate a Conda environment:

```bash
# Create a new conda environment with Python 3.12
conda create -n maze-runner python=3.12

# Activate the conda environment
conda activate maze-runner
```

2. Install Jupyter and the required dependencies:

```bash
# Install Jupyter
pip install jupyter

# Install project dependencies
pip install -r requirements.txt
```

## Running the Maze Runner Game

### 🧩 Basic (Default Random Maze)

```bash
python main.py
```

---

### 🎮 Manual Mode (Interactive Player-Controlled)

Use arrow keys to navigate through the maze manually.

```bash
# Random maze
python main.py

# Static maze
python main.py --type static

# Custom maze size
python main.py --type random --width 40 --height 40
```

---

### 🤖 Auto Mode (Automated Maze Solver)

The explorer solves the maze and prints performance statistics.

```bash
# Auto exploration (random maze)
python main.py --auto

# Auto exploration (static maze)
python main.py --type static --auto

# Auto exploration with visualization
python main.py --auto --visualize

# Enhanced algorithm with diagonal movement
python main.py --auto --enhanced diagonal

# Enhanced with visualization and larger maze
python main.py --auto --visualize --enhanced enhanced --width 40 --height 40
```

---

### ☁️ Distributed Mode (Celery + RabbitMQ)

Use parallel execution with multiple explorers. Run with `parallel_main.py`.

```bash
# Run in parallel using multiprocessing (4 explorers)
python parallel_main.py --auto --num_explorers 4

# Run in distributed mode using Celery workers (RabbitMQ required)
python parallel_main.py --auto --distributed --num_explorers 4
```

Available arguments:

`--type`: Choose between `"random"` (default) or `"static"` maze generation  
`--width`: Set maze width (default: 30). Ignored if maze type is static.  
`--height`: Set maze height (default: 30). Ignored if maze type is static.  
`--auto`: Enable automated maze exploration (non-interactive)  
`--visualize`: Show real-time visualization of the automated exploration (only works in single-explorer mode)  
`--enhanced`: Select exploration algorithm mode:

- `"normal"`: Basic algorithm
- `"enhanced"`: A\* algorithm with Improved backtracking
- `"diagonal"`: Enhanced A\* algorithm with diagonal movement

`--num_explorers`: Set number of parallel explorers (use `parallel_main.py` instead)  
`--distributed`: Use Celery and RabbitMQ for distributed execution (use `parallel_main.py` instead)

## Maze Types

### Random Maze (Default)

- Generated using depth-first search algorithm
- Different layout each time you run the program
- Customizable dimensions
- Default type if no type is specified

### Static Maze

- Predefined maze pattern
- Fixed dimensions (50x50)
- Same layout every time
- Width and height arguments are ignored

## How to Play

### Manual Mode

1. Controls:

- Use the arrow keys to move the player (<span style="color:blue">blue circle</span>)
- Start at the <span style="color:green">green square</span>
- Reach the <span style="color:red">red square</span> to win
- Avoid the <span style="color:black">black walls</span>

### Automated Mode

- The explorer uses the right-hand rule algorithm to solve the maze
- Automatically finds the path from start to finish
- Displays detailed statistics at the end:
  - Total time taken
  - Total moves made
  - Number of backtrack operations
  - Average moves per second
- Works with both random and static mazes
- Optional real-time visualization:
  - Shows the explorer's position in <span style="color:blue">blue</span>
  - Updates at 30 frames per second
  - Pauses for 2 seconds at the end to show the final state

## Student Questions

### Question 1 (10 points)

#### Algorithm Overview

The explorer uses the right-hand rule algorithm following the steps:

1. Try to turn right
2. If right is blocked, try forward
3. If forward is blocked, try left
4. If all else fails, turns around and repeat

#### Loop Detection and Handling

There is always a possibility that the explorer could get stuck when looking for a solution. The algorithm uses the following steps to mitigate it:

1. **Loop Detection**:

   - Maintains a history of the last 3 moves
   - Detects when it's stuck in a loop by checking if the last 3 positions are the same
   - Uses a `move_history` deque with a maximum length of 3 to track recent positions

2. **Backtracking Strategy**:
   - When a loop is detected, the explorer initiates a backtracking operation
   - Backtracks to the last position where multiple path choices were available
   - Uses a `backtrack_path` to store the path back to a decision point
   - Counts the number of backtrack operations performed

#### Backtracking Implementation

The backtracking system works as follows:

1. When stuck, the explorer:

   - Finds a path back to a position with multiple choices.
   - Counts available choices at each position.
   - Returns to the most recent position with multiple path options
   - Maintains a record of backtrack operations

2. The backtracking path is determined by:
   - Starting from the current position
   - Moving backwards through the move history
   - Looking for positions with multiple available choices
   - Creating a path back to the most recent decision point

#### Statistics and Performance Metrics

At the end of exploration, the system provides detailed statistics:

1. **Time Metrics**:

   - Total time taken to solve the maze
   - Average moves per second

2. **Move Statistics**:

   - Total number of moves made
   - Number of backtrack operations performed

---

### Question 2 (30 points)

### 🎯 Objective

Modify the maze explorer to run **multiple agents in parallel** to discover the **fastest or shortest solution path** using either:

- **Multiprocessing**
- **Distributed execution with Celery + RabbitMQ**

### ⚙️ Implementation Overview

The program is modularly designed in `parallel_main.py` to support **two modes of parallelism**, controlled by a command-line flag:

- `--distributed`: Enables distributed execution via Celery
- `--num_explorers`: Specifies the number of parallel explorer instances

The solution satisfies all task requirements: parallel execution, task distribution, and result comparison.

### 🧪 Mode Switching via Arguments

The execution mode is controlled through CLI flags:

| Flag              | Function                                           |
| ----------------- | -------------------------------------------------- |
| `--distributed`   | Enables distributed mode using Celery and RabbitMQ |
| `--num_explorers` | Sets the number of parallel explorers (default: 4) |

#### 🖥️ Multiprocessing Mode (Default)

If `--distributed` is **not** specified, the system uses `multiprocessing.Pool`:

```python
with Pool(processes=args.num_explorers) as pool:
    results = pool.map(run_explorer, [explorer_args] * args.num_explorers)
```

Each explorer runs in its own process and returns:

- Time taken
- Path followed
- Number of steps

### ☁️ Distributed Mode (Celery + RabbitMQ)

If `--distributed` is passed:

```python
result = run_explorer_task.delay(explorer_args)
```

This submits tasks to Celery workers. Each worker solves a maze independently and returns the result.

Tasks are registered via:

```python
@app.task(name='maze_runner.tasks.run_explorer_task', queue='maze_exploration')
```

All results are collected using:

```python
result.get()
```

### 📊 Result Comparison Logic

After all explorers finish, their results are compared:

```python
for i, (time_taken, moves, num_moves) in enumerate(results):
    if time_taken < best_time:
        best_time = time_taken
        best_explorer = i + 1
    if num_moves < best_moves:
        best_moves = num_moves
        best_explorer = i + 1
```

This identifies:

- The explorer that solved the maze **fastest**
- The one with the **least number of moves**

And prints:

```
=== Best Performance ===
Best explorer: 2
Best time: 11.63 seconds
Best moves: 84
```

---

### Question 3 (10 points)

### 🧪 Experiment Setup

To analyze the performance of different maze explorers, we ran **4 explorers simultaneously** on a **static maze** using parallel execution. Each explorer was tasked with solving the same maze, starting from the same entry point and aiming to reach the same goal.

### 📊 Collected Metrics

The following statistics were recorded:

```
Explorer 1:
Time taken: 0.00 seconds
Number of moves: 127

Explorer 2:
Time taken: 0.00 seconds
Number of moves: 127

Explorer 3:
Time taken: 0.00 seconds
Number of moves: 127

Explorer 4:
Time taken: 0.00 seconds
Number of moves: 127

=== Best Performance ===
Best explorer: 2
Best time: 0.00 seconds
Best moves: 127
```

### 🧠 Analysis & Observations

- **Identical Move Counts**: All explorers completed the maze in exactly 127 moves. This is expected because the **static maze** has a fixed structure, and each explorer is initialized with the **same starting and ending points**. As a result, the **pathfinding algorithm behaves deterministically**, producing the same path each time.

- **Identical Time Taken**: The reported execution time for all explorers is `0.00 seconds`, which implies that the solving process was **extremely fast and below measurable threshold** in Python's time resolution. This is likely due to the simplicity of the static maze or the efficiency of the A\* algorithm.

- **Best Explorer Is Arbitrary**: Although "Explorer 2" is marked as the best based on time and move count, the selection is arbitrary because all explorers performed identically. The designation is simply a byproduct of how ties are handled in the result comparison logic.

- **Why the Results Are Identical**: In static maze mode:

  - Maze generation is **non-random**
  - The path is always the same
  - Explorers face no variation in obstacle layout, allowing for **perfect reproducibility**

- **Timing Variation**: In general, **execution time may vary slightly** between explorers due to:

  - **Operating system process scheduling**
  - **Parallel processing overhead**
  - **Memory/cache contention**

  However, in this run, the variance was not large enough to affect measurement.

### ✅ Conclusion

When running multiple explorers on a **static maze**, the performance metrics are **identical** due to the deterministic nature of the task. This demonstrates consistency and reliability of the algorithm across multiple executions. Any slight differences in execution time that might arise in other environments would be attributed to system-level concurrency and resource allocation rather than algorithm performance.

---

### Question 4 (20 points)

Based on your analysis from Question 3, propose and implement enhancements to the maze explorer to overcome its limitations. Your solution should:

1. Identify and explain the main limitations of the current explorer:

- This takes a long amount of time as it is continuously roaming the search space until it finds the goal which the time it takes to complete as well as the moves required grow exponentially as the size of the maze increases.
- Finding a path for backtracking does linear movement where it keeps trying to find a node until it finds a node with multiple options. It also does not keep track of nodes that lead to dead ends
- Though we are keeping track of what nodes we have visited, they are not used in the decision of the next move the player will do.

2. Propose specific improvements to the exploration algorithm:

- Implementation of a path finding algorithm rather than just right-hand turn algorithm can vastly improve the path finding of the program and reduce the number of moves needed to reach the goal.
- Keeping track of nodes that lead to dead ends/loops.
- Keep track of the last recorded junction to stop linear backtracking to have less backtracking and faster processing times.

3. Implement at least two of the proposed improvements:

## Maze Explorer Details

This document explains the design and implementation decisions behind the Maze Explorer module, including the exploration algorithm, loop detection, backtracking strategy, and post-exploration statistics.

### Chnaged Algorithm Used by the Explorer

The explorer uses the **A\*** search algorithm to find a path through the maze. Key details include:

- **Heuristic Function**:  
  The A\* algorithm employs the Manhattan distance as its heuristic function. This choice is well-suited for grid-based mazes where movement is restricted to four directions (up, down, left, right).

- **Priority Queue**:  
  The open set is managed with a priority queue (using Python's `heapq`). This ensures that the node with the lowest estimated total cost (the sum of the cost so far and the heuristic estimate) is processed first.

- **Path Reconstruction**:  
  When the goal is reached, the algorithm reconstructs the path by backtracking through a dictionary (`came_from`) that maps each explored node to its parent.

- **Junction Recording**:  
  During the search, nodes with more than two open adjacent cells (junctions) are recorded. This information is used later in the backtracking phase if the explorer gets stuck.

### Updated Backtracking Strategy

If the A\* search or the current exploration strategy fails to provide a complete solution, the explorer employs a backtracking strategy to recover:

- **Last Junction Identification**:  
  The algorithm remembers the last recorded junction—the node from which multiple paths were available. This node represents a potential decision point where an alternative route might lead to a solution.

- **Path Reconstruction for Backtracking**:  
  The method `find_backtrack_path()` analyzes the move history to generate a reversed path from the current node back to the last junction. This backtracking path is then used to reposition the explorer to a point with unexplored alternatives.

- **Incremental Backtracking Steps**:  
  The `backtrack()` method moves the explorer one step along the calculated backtracking path. The counter for backtrack operations is incremented each time a backtracking move is performed.

### Question 5 (20 points)

#### ✅ Enhanced Explorer Performance Comparison

##### 📊 Performance Metrics (Static Maze)

| Explorer Type           | Time Taken (s) | Moves Made | Backtracks | Avg Moves/sec |
| ----------------------- | -------------- | ---------- | ---------- | ------------- |
| Normal (Right-hand)     | 0.00           | 1279       | 0          | 899,482.70    |
| Enhanced (A\*)          | 0.00           | 127        | 0          | 72,720.36     |
| Diagonal (Enhanced A\*) | 0.01           | 98         | 0          | 18,391.13     |

---

##### 🧠 Analysis of Results

- **Normal (Right-hand rule)**:

  - Follows the **right-hand rule**, which explores all reachable paths by hugging the right side of the wall.
  - Solves the maze using **1279 moves**, significantly more than necessary.
  - Although it completed the task quickly in wall time, the path is **inefficient and non-optimal**.

- **Enhanced Explorer**:

  - Uses a **heuristic-driven approach** (A\*).
  - Solves the same maze in **127 moves**, achieving near-optimal efficiency.
  - Results are consistent, as the static maze ensures deterministic execution.

- **Diagonal Enhanced Explorer**:
  - Extends the A\* algorithm by allowing **8-direction movement**, including diagonals.
  - Solves the maze in just **98 moves**, the shortest of all.
  - Slightly higher execution time (`0.01s`) is negligible but reflects **extra branching** in diagonal exploration.

---

##### ⚖️ Trade-offs & Limitations

###### ✅ Benefits of Enhanced and Diagonal A\*:

- **Path efficiency**: Far fewer moves than the right-hand rule.
- **Algorithmic accuracy**: Guarantees optimal or near-optimal paths in static mazes.
- **Consistency**: All explorers produce the same results every time in static mode.

###### ⚠️ Trade-offs:

- **Right-hand rule (normal)**: Simple to implement but **highly inefficient** in large or open mazes.
- **Enhanced A\***: Adds complexity, requires **heuristic function** and **more memory** (for g-scores, open/closed sets).
- **Diagonal movement**: May not be realistic in real-world robotics or constrained grid applications; also slightly increases computational overhead.

---

#### 📌 Conclusion

The comparison shows that the **right-hand rule (normal)** is a brute-force, exploration-heavy strategy that sacrifices efficiency. In contrast, the **enhanced A\*** algorithm provides a substantial performance boost by using informed search. Adding diagonal capabilities further optimizes the path but introduces minor complexity. For static mazes with known configurations, **enhanced or diagonal-enhanced exploration** is clearly superior.

### Final points 6 (10 points)

1. Solve the static maze in 150 moves or less to get 10 points.
2. Solve the static maze in 135 moves or less to get 15 points.
3. Solve the static maze in 130 moves or less to get 100% in your assignment.

### Bonus points

1. Fastest solver to get top 10% routes (number of moves)
2. Finding a solution with no backtrack operations
3. Least number of moves.
