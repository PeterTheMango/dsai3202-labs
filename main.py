"""
Main entry point for the maze runner game.
"""

import argparse
import sys
from src.game import run_game
from src.explorer import Explorer
from src.enhanced import Explorer as EnhancedExplorer
from src.diagonal_enhanced import Explorer as DiagonalEnhancedExplorer


def main():
    parser = argparse.ArgumentParser(description="Maze Runner Game")
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
    parser.add_argument("--num_explorers", type=int, default=None,
                        help="Number of parallel explorers (use parallel_main.py instead)")
    parser.add_argument("--distributed", action="store_true",
                        help="Use Celery and RabbitMQ for distributed execution (use parallel_main.py instead)")
    
    args = parser.parse_args()
    
    # Check for parallelization flags
    if args.num_explorers is not None or args.distributed:
        print("Error: Parallel and distributed execution features are not available in main.py")
        print("Please use parallel_main.py instead with the following command:")
        cmd = "python parallel_main.py"
        if args.type:
            cmd += f" --type {args.type}"
        if args.width:
            cmd += f" --width {args.width}"
        if args.height:
            cmd += f" --height {args.height}"
        if args.auto:
            cmd += " --auto"
        if args.visualize:
            cmd += " --visualize"
        if args.enhanced:
            cmd += f" --enhanced {args.enhanced}"
        if args.num_explorers:
            cmd += f" --num_explorers {args.num_explorers}"
        if args.distributed:
            cmd += " --distributed"
        print(f"\n{cmd}")
        sys.exit(1)
    
    if args.auto:
        # Create maze and run automated exploration
        from src.maze import create_maze
        maze = create_maze(args.width, args.height, args.type)
        
        if args.enhanced == "enhanced":
            explorer = EnhancedExplorer(maze, visualize=args.visualize)
        elif args.enhanced == "diagonal":
            explorer = DiagonalEnhancedExplorer(maze, visualize=args.visualize)
        else:
            explorer = Explorer(maze, visualize=args.visualize)
        
        time_taken, moves = explorer.solve()
        print(f"Maze solved in {time_taken:.2f} seconds")
        print(f"Number of moves: {len(moves)}")
        if args.type == "static":
            print("Note: Width and height arguments were ignored for the static maze")
        
    else:
        # Run the interactive game
        run_game(maze_type=args.type, width=args.width, height=args.height)


if __name__ == "__main__":
    main()