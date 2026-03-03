import random

class Level3Solver:
    def __init__(self, grid):
        self.SIZE = 7
        self.grid = grid
        self.MOVES = [
            (0, 1, False), (0, -1, False), (1, 0, False), (-1, 0, False),
            (1, 1, True), (1, -1, True), (-1, 1, True), (-1, -1, True)
        ]
        self.INNER_START = 1
        self.INNER_END = 5
        self.TOTAL_INNER_CELLS = 25

    #Check how many empty neighbors a cell has
    def get_degree(self, x, y):
        count = 0
        for dx, dy, is_diag in self.MOVES:
            nx, ny = x + dx, y + dy
            if self.INNER_START <= nx <= self.INNER_END and self.INNER_START <= ny <= self.INNER_END:
                if self.grid[nx][ny] == 0:
                    count += 1
        return count

    # Solve using backtracking with heuristics
    def solve(self, x, y, step_count):
        # Base Case: All inner cells filled
        if step_count == self.TOTAL_INNER_CELLS:
            return True

        next_val = step_count + 1
        candidates = []
        # Generate candidates based on valid moves
        for dx, dy, is_diag in self.MOVES:
            nx, ny = x + dx, y + dy
            if self.INNER_START <= nx <= self.INNER_END and self.INNER_START <= ny <= self.INNER_END:
                if self.grid[nx][ny] == 0:
                    if self.is_move_valid(nx, ny, next_val):
                        deg = self.get_degree(nx, ny)
                        candidates.append((nx, ny, deg))
        # Sort candidates by degree (ascending) to implement a heuristic that tries less constrained cells first
        candidates.sort(key=lambda c: c[2])
        # Try candidates in sorted order
        for nx, ny, deg in candidates:
            self.grid[nx][ny] = next_val
            if self.solve(nx, ny, next_val):
                return True
            self.grid[nx][ny] = 0 
            
        return False
    
    # Check if placing 'num' at (x, y) is valid based on the nums in the outer ring
    def is_move_valid(self, x, y, num):

        for i in [0, 6]:
            if (self.grid[i][y] == num or self.grid[x][i] == num):
                return True
        
        if x == y and (self.grid[0][0] == num or self.grid[6][6] == num):
            return True
            
        if x + y == 6 and (self.grid[0][6] == num or self.grid[6][0] == num):
            return True
 
        return not self.clue_exists_in_ring(num)

    # Check if the clue number exists in the outer ring
    def clue_exists_in_ring(self, num):
        for i in range(self.SIZE):
            if self.grid[0][i] == num or self.grid[6][i] == num or \
               self.grid[i][0] == num or self.grid[i][6] == num:
                return True
        return False

    # Find the best solution starting from the current grid state
    def find_best_solution(self):
        start_x, start_y, max_val = -1, -1, 0
        for r in range(self.INNER_START, self.INNER_END + 1):
            for c in range(self.INNER_START, self.INNER_END + 1):
                if self.grid[r][c] > max_val:
                    max_val = self.grid[r][c]
                    start_x, start_y = r, c

        if start_x == -1: return None, None

        # Store the original max value to compare against later
        original_max = max_val
        if self.solve(start_x, start_y, max_val):
            mask = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
            for r in range(self.INNER_START, self.INNER_END + 1):
                for c in range(self.INNER_START, self.INNER_END + 1):
                    if self.grid[r][c] > original_max:
                        mask[r][c] = True
            return self.grid, mask
        return None, None