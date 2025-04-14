"""
Maze Explorer module that implements automated maze solving using A* search algorithm with diagonal movement and backtracking support.
"""

import time
import pygame
import heapq
from typing import Tuple, List, Optional, Deque
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)
        self.moves = []
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        self.move_history = deque(maxlen=3)
        self.backtracking = False
        self.backtrack_path = []
        self.backtrack_count = 0
        self.last_junction = None
        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - Automated Solving")
            self.clock = pygame.time.Clock()

    def count_available_choices(self, pos: Tuple[int, int]) -> int:
        """Count available non-wall neighbor positions including diagonals."""
        x, y = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        choices = 0
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0):
                choices += 1
        return choices

    def draw_state(self):
        self.screen.fill(WHITE)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE,
                                      CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.maze.start_pos[0] * CELL_SIZE,
                          self.maze.start_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.maze.end_pos[0] * CELL_SIZE,
                          self.maze.end_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLUE,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        self.clock.tick(30)

    def print_statistics(self, time_taken: float):
        print("\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("==================================\n")

    def find_backtrack_path(self) -> List[Tuple[int, int]]:
        if self.last_junction and self.last_junction in self.moves:
            junction_index = self.moves.index(self.last_junction)
            path = self.moves[junction_index:]
            return path[::-1]
        path = []
        visited = set()
        for i in range(len(self.moves) - 1, -1, -1):
            pos = self.moves[i]
            if pos in visited:
                continue
            visited.add(pos)
            path.append(pos)
            if self.count_available_choices(pos) > 1:
                return path[::-1]
        return path[::-1]

    def backtrack(self) -> bool:
        if not self.backtrack_path:
            self.backtrack_path = self.find_backtrack_path()
        if self.backtrack_path:
            next_pos = self.backtrack_path.pop(0)
            self.x, self.y = next_pos
            self.backtrack_count += 1
            if self.visualize:
                self.draw_state()
            return True
        return False

    def astar(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
            dx = abs(a[0] - b[0])
            dy = abs(a[1] - b[1])
            return max(dx, dy) + (1.4142 - 1) * min(dx, dy)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]

        open_set = []
        heapq.heappush(open_set, (heuristic(start, goal), start))
        came_from = {}
        g_score = {start: 0}
        closed_set = set()

        while open_set:
            current_priority, current = heapq.heappop(open_set)

            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            closed_set.add(current)

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if not (0 <= neighbor[0] < self.maze.width and 
                        0 <= neighbor[1] < self.maze.height):
                    continue
                if self.maze.grid[neighbor[1]][neighbor[0]] != 0:
                    continue
                if neighbor in closed_set:
                    continue

                move_cost = 1.4142 if dx != 0 and dy != 0 else 1.0
                tentative_g_score = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

                    if self.count_available_choices(neighbor) > 2:
                        self.last_junction = neighbor
        return None

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        self.start_time = time.time()
        path = self.astar((self.x, self.y), self.maze.end_pos)

        if path:
            for pos in path[1:]:
                self.x, self.y = pos
                self.moves.append(pos)
                self.move_history.append(pos)
                if self.count_available_choices(pos) > 2:
                    self.last_junction = pos
                if self.visualize:
                    self.draw_state()
                    pygame.time.delay(100)
        else:
            print("A* search failed to find a path. Attempting backtracking from last junction.")
            while (self.x, self.y) != self.maze.end_pos:
                if not self.backtrack():
                    print("No viable backtracking path found. Maze cannot be solved.")
                    break

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time

        if self.visualize:
            pygame.time.wait(2000)
            pygame.quit()

        self.print_statistics(time_taken)
        return time_taken, self.moves