import random

class Level1Solver:
    def __init__(self, grid):
        self.SIZE = 5
        self.grid = grid
        self.MOVES = [
            (0, 1, False), (0, -1, False), (1, 0, False), (-1, 0, False),
            (1, 1, True), (1, -1, True), (-1, 1, True), (-1, -1, True)
        ]
        self.best_grid = None
        self.original_grid = [row[:] for row in grid]
        self.max_diagonal_score = -1
        self.found_count = 0    

    #Check how many empty neighbors a cell has
    def get_degree(self, x, y):
        count = 0
        for dx, dy, move in self.MOVES:
            nx = x + dx 
            ny = y + dy
            if 0 <= nx < self.SIZE and 0 <= ny < self.SIZE and self.grid[nx][ny] == 0:
                count += 1
        return count

    def solve(self, x, y, step_count, current_score):   
        # Base Case: All cells filled
        if step_count == self.SIZE * self.SIZE:
            self.found_count += 1
            if current_score > self.max_diagonal_score:
                self.max_diagonal_score = current_score
                self.best_grid = [row[:] for row in self.grid]
            
            # Stop after finding a solution with score 13 or higher
            if current_score >= 13:
                return True
            return False

        # Get and sort candidates
        candidates = []
        for dx, dy, is_diag in self.MOVES:
            nx = x + dx 
            ny = y + dy
            if 0 <= nx < self.SIZE and 0 <= ny < self.SIZE and self.grid[nx][ny] == 0:
                degree = self.get_degree(nx, ny)
                candidates.append((nx, ny, is_diag, degree))

        #Sort by degree (ascending) and then by diagonal move (descending)
        candidates.sort(key=lambda c: (c[3], -int(c[2])))

        for nx, ny, is_diag, candidate in candidates:
            self.grid[nx][ny] = step_count + 1
            # If solve returns True stop recursing
            if self.solve(nx, ny, step_count + 1, current_score + (1 if is_diag else 0)):
                return True
            self.grid[nx][ny] = 0 # Backtrack
            
        return False
    
    def get_best_solution(self,score):
        # Find the current max number and its position
        max_num = 0
        start_pos = None
        
        # Identify the starting point for the solver
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                val = self.grid[r][c]
                if val > 0:
                    if val > max_num:
                        max_num = val
                        start_pos = (r, c)
        
        if not start_pos:
            return None 

        #Call the solver with the current max number and score
        self.solve(start_pos[0], start_pos[1], max_num, score)
        
        if self.best_grid:
            # Create the mask for coloring
            solved_mask = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
            for r in range(self.SIZE):
                for c in range(self.SIZE):
                    # Only mark cells that were originally empty and are now filled in the best solution
                    if self.original_grid[r][c] == 0 and self.best_grid[r][c] != 0:
                        solved_mask[r][c] = 1
            return self.best_grid, solved_mask
                    
        return None, None
