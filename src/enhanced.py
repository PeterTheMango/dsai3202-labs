"""
Maze Explorer module that implements automated maze solving using A* search algorithm with backtracking support.
"""

import time
import pygame
import heapq  # For A* search priority queue
from typing import Tuple, List, Optional, Deque
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)  # Start facing right (retained but unused in the A* algorithm)
        self.moves = []
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        self.move_history = deque(maxlen=3)  # Keep track of last 3 moves for loop detection
        self.backtracking = False
        self.backtrack_path = []
        self.backtrack_count = 0  # Count number of backtrack operations
        self.last_junction = None  # Record the last junction (node with multiple paths)
        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - Automated Solving")
            self.clock = pygame.time.Clock()

    def turn_right(self):
        """Turn 90 degrees to the right."""
        x, y = self.direction
        self.direction = (-y, x)

    def turn_left(self):
        """Turn 90 degrees to the left."""
        x, y = self.direction
        self.direction = (y, -x)

    def can_move_forward(self) -> bool:
        """Check if we can move forward in the current direction."""
        dx, dy = self.direction
        new_x, new_y = self.x + dx, self.y + dy
        return (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0)

    def move_forward(self):
        """Move forward in the current direction."""
        dx, dy = self.direction
        self.x += dx
        self.y += dy
        current_move = (self.x, self.y)
        self.moves.append(current_move)
        self.move_history.append(current_move)
        if self.visualize:
            self.draw_state()

    def is_stuck(self) -> bool:
        """Check if the explorer is stuck in a loop."""
        if len(self.move_history) < 3:
            return False
        # Check if the last 3 moves are the same
        return (self.move_history[0] == self.move_history[1] == self.move_history[2])

    def backtrack(self) -> bool:
        """
        Backtrack to the last junction recorded (node with multiple choices).
        
        This method uses the backtrack path computed by find_backtrack_path and moves one step
        along that path. It increments the backtracking counter for statistics.
        """
        if not self.backtrack_path:
            # If no backtrack path exists, try to compute one based on the last junction.
            self.backtrack_path = self.find_backtrack_path()
        
        if self.backtrack_path:
            # Move to the next position along the backtracking path.
            next_pos = self.backtrack_path.pop(0)
            self.x, self.y = next_pos
            self.backtrack_count += 1
            if self.visualize:
                self.draw_state()
            return True
        return False

    def find_backtrack_path(self) -> List[Tuple[int, int]]:
        """
        Find a path back to the last recorded junction (node with multiple choices).
        
        The modified approach here first checks if there is a recorded junction from which
        alternative paths may exist. If so, it returns the portion of the visited moves that 
        leads back to that junction.
        """
        if self.last_junction and self.last_junction in self.moves:
            junction_index = self.moves.index(self.last_junction)
            # Build backtrack path from current position back to the junction.
            path = self.moves[junction_index:]
            return path[::-1]  # Reverse the path for backtracking
        # Fallback: traverse the moves history in reverse looking for a junction.
        path = []
        visited = set()
        for i in range(len(self.moves) - 1, -1, -1):
            pos = self.moves[i]
            if pos in visited:
                continue
            visited.add(pos)
            path.append(pos)
            # A position with more than one exit is considered a junction.
            if self.count_available_choices(pos) > 1:
                return path[::-1]
        return path[::-1]

    def count_available_choices(self, pos: Tuple[int, int]) -> int:
        """Count the number of available moves from a given position."""
        x, y = pos
        choices = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0):
                choices += 1
        return choices

    def draw_state(self):
        """Draw the current state of the maze and explorer."""
        self.screen.fill(WHITE)
        
        # Draw the maze walls.
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE,
                                      CELL_SIZE, CELL_SIZE))
        
        # Draw start and end points.
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.maze.start_pos[0] * CELL_SIZE,
                          self.maze.start_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.maze.end_pos[0] * CELL_SIZE,
                          self.maze.end_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        
        # Draw the explorer.
        pygame.draw.rect(self.screen, BLUE,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
        self.clock.tick(30)  # Control visualization frame rate

    def print_statistics(self, time_taken: float):
        """Print detailed statistics about the maze exploration."""
        print("\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("==================================\n")

    def astar(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        A* search algorithm implementation to find the shortest path from start to goal.
        
        Changes include:
          - Using a priority queue (heapq) for the open set.
          - Maintaining a closed_set to prevent revisiting nodes.
          - Using Manhattan distance as the heuristic.
          - Recording junction nodes (nodes with >2 free neighboring cells) in last_junction.
        """
        # Heuristic: Manhattan distance.
        def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        open_set = []
        heapq.heappush(open_set, (heuristic(start, goal), start))
        came_from = {}
        g_score = {start: 0}
        closed_set = set()
        
        while open_set:
            current_priority, current = heapq.heappop(open_set)
            
            # Goal check: if we reached the goal, reconstruct the path.
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]  # Reverse the path to go from start to goal.
            
            closed_set.add(current)
            
            # Explore neighbors (up, down, left, right).
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Check that neighbor is within bounds and is not a wall.
                if not (0 <= neighbor[0] < self.maze.width and 
                        0 <= neighbor[1] < self.maze.height):
                    continue
                if self.maze.grid[neighbor[1]][neighbor[0]] != 0:
                    continue
                if neighbor in closed_set:
                    continue
                
                tentative_g_score = g_score[current] + 1  # The cost to move from one cell to another is 1.
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
                    
                    # Record junction nodes (if more than 2 available adjacent free cells).
                    if self.count_available_choices(neighbor) > 2:
                        self.last_junction = neighbor
                        
        # If no path is found, return None.
        return None

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Solve the maze using the A* search algorithm.
        
        Changes and additions made:
          - Replaced the right-hand turn algorithm with A* search.
          - Within A*, visited nodes are tracked (closed_set) to prevent redundant searches.
          - Junction nodes (with multiple possible moves) are recorded for backtracking.
          - If A* fails to find a complete path, the algorithm will attempt backtracking from the last recorded junction.
        """
        self.start_time = time.time()
        
        # Attempt to find a complete path using the A* search algorithm.
        path = self.astar((self.x, self.y), self.maze.end_pos)
        
        if path:
            # Simulate movement along the computed A* path (skip the start position).
            for pos in path[1:]:
                self.x, self.y = pos
                self.moves.append(pos)
                self.move_history.append(pos)
                
                # Update the last junction if this cell offers multiple choices.
                if self.count_available_choices(pos) > 2:
                    self.last_junction = pos
                
                if self.visualize:
                    self.draw_state()
                    # Optional delay for visualization.
                    pygame.time.delay(100)
        else:
            # If A* fails, attempt backtracking from the last recorded junction.
            print("A* search failed to find a path. Attempting backtracking from last junction.")
            while (self.x, self.y) != self.maze.end_pos:
                if not self.backtrack():
                    print("No viable backtracking path found. Maze cannot be solved.")
                    break
        
        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        
        if self.visualize:
            # Show the final state briefly and then clean up.
            pygame.time.wait(2000)
            pygame.quit()
        
        # Print detailed statistics about the maze solving process.
        self.print_statistics(time_taken)
            
        return time_taken, self.moves