"""
Celery tasks for the maze runner game.
"""

from celery import Celery
from kombu import Queue
from typing import List, Tuple, Dict
from src.explorer import Explorer
from src.enhanced import Explorer as EnhancedExplorer
from src.maze import create_maze

app = Celery('maze_runner', 
             broker="pyamqp://guest@10.102.0.149//", 
             backend='rpc://')
app.conf.task_queues = [
    Queue('maze_exploration', routing_key='maze.exploration')
]

def run_explorer(args: Dict) -> Tuple[float, List[Tuple[int, int]], int]:
    """Run a single maze explorer instance."""
    maze = create_maze(args['width'], args['height'], args['type'])
    
    if args['enhanced']:
        explorer = EnhancedExplorer(maze, visualize=False)
    else:
        explorer = Explorer(maze, visualize=False)
    
    time_taken, moves = explorer.solve()
    return time_taken, moves, len(moves)

@app.task(name='maze_runner.tasks.run_explorer_task', 
          queue='maze_exploration')
def run_explorer_task(args: Dict) -> Tuple[float, List[Tuple[int, int]], int]:
    return run_explorer(args) 