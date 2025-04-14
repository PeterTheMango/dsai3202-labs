"""
Parallel version of the maze runner game that supports both multiprocessing and distributed execution.
"""

import argparse
from multiprocessing import Pool
from typing import List, Tuple, Dict
from src.game import run_game
from src.explorer import Explorer
from src.enhanced import Explorer as EnhancedExplorer
from src.diagonal_enhanced import Explorer as DiagonalEnhancedExplorer
from src.maze import create_maze

# Celery imports (only used if --distributed flag is set)
try:
    from celery import Celery
    from kombu import Queue
except ImportError:
    Celery = None
    Queue = None

# Celery app configuration (only used if --distributed flag is set)
if Celery is not None:
    app = Celery('maze_runner', broker="pyamqp://guest@10.102.0.149//", backend='rpc://')
    app.conf.task_queues = [
        Queue('maze_exploration', routing_key='maze.exploration')
    ]

def run_explorer(args: Dict) -> Tuple[float, List[Tuple[int, int]], int]:
    """Run a single maze explorer instance."""
    maze = create_maze(args['width'], args['height'], args['type'])
    
    if args['enhanced'] == "enhanced":
        explorer = EnhancedExplorer(maze, visualize=False)
    elif args['enhanced'] == "diagonal":
        explorer = DiagonalEnhancedExplorer(maze, visualize=False)
    else:
        explorer = Explorer(maze, visualize=False)
    
    time_taken, moves = explorer.solve()
    return time_taken, moves, len(moves)

# Define Celery task (only used if --distributed flag is set)
if Celery is not None:
    @app.task(name='maze_runner.tasks.run_explorer_task', queue='maze_exploration')
    def run_explorer_task(args: Dict) -> Tuple[float, List[Tuple[int, int]], int]:
        return run_explorer(args)

def run_parallel_explorers(args: argparse.Namespace) -> None:
    """Run multiple explorers in parallel using either multiprocessing or Celery."""
    # Prepare arguments for each explorer
    explorer_args = {
        'type': args.type,
        'width': args.width,
        'height': args.height,
        'enhanced': args.enhanced
    }
    
    if args.distributed:
        if Celery is None:
            raise ImportError("Celery and RabbitMQ are required for distributed execution. "
                            "Please install them using: pip install celery kombu")
        
        # Start Celery workers
        print("Starting distributed exploration with Celery...")
        results = []
        for _ in range(args.num_explorers):
            result = run_explorer_task.delay(explorer_args)
            results.append(result)
        
        # Wait for all results
        completed_results = []
        for result in results:
            completed_results.append(result.get())
        results = completed_results
            
    else:
        # Use multiprocessing
        print(f"Starting parallel exploration with {args.num_explorers} processes...")
        with Pool(processes=args.num_explorers) as pool:
            results = pool.map(run_explorer, [explorer_args] * args.num_explorers)
    
    # Analyze results
    best_time = float('inf')
    best_moves = float('inf')
    best_explorer = -1
    
    print("\n=== Exploration Results ===")
    for i, (time_taken, moves, num_moves) in enumerate(results):
        print(f"\nExplorer {i+1}:")
        print(f"Time taken: {time_taken:.2f} seconds")
        print(f"Number of moves: {num_moves}")
        
        if time_taken < best_time:
            best_time = time_taken
            best_explorer = i + 1
            
        if num_moves < best_moves:
            best_moves = num_moves
            best_explorer = i + 1
    
    print("\n=== Best Performance ===")
    print(f"Best explorer: {best_explorer}")
    print(f"Best time: {best_time:.2f} seconds")
    print(f"Best moves: {best_moves}")

def main():
    parser = argparse.ArgumentParser(description="Parallel Maze Runner Game")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate (random or static)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--auto", action="store_true",
                        help="Run automated maze exploration")
    parser.add_argument("--visualize", action="store_true",
                        help="Visualize the automated exploration in real-time")
    parser.add_argument("--enhanced", choices=["normal", "enhanced", "diagonal"], default="normal",
                        help="Use normal or enhanced exploration algorithm with or without diagonal movement")
    parser.add_argument("--num_explorers", type=int, default=4,
                        help="Number of parallel explorers (default: 4)")
    parser.add_argument("--distributed", action="store_true",
                        help="Use Celery and RabbitMQ for distributed execution")
    
    args = parser.parse_args()
    
    if args.auto:
        run_parallel_explorers(args)
    else:
        # Run the interactive game (single process)
        run_game(maze_type=args.type, width=args.width, height=args.height)

if __name__ == "__main__":
    main()
