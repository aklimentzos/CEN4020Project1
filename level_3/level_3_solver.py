import random
class Level3Solver:
    def __init__(self, grid):
        self.SIZE = 7
        self.grid = grid
        self.MOVES = [
            (0, 1, False), (0, -1, False), (1, 0, False), (-1, 0, False),
            (1, 1, True), (1, -1, True), (-1, 1, True), (-1, -1, True)
        ]
        self.FULL_SIZE = 7 
        self.INNER_START = 1
        self.INNER_END = 5
        self.TOTAL_INNER_CELLS = 25

    def get_degree(self, x, y):
        count = 0
        for dx, dy, is_diag in self.MOVES:
            nx, ny = x + dx, y + dy
            # Only count neighbors within the 5x5 inner grid that are empty
            if self.INNER_START <= nx <= self.INNER_END and self.INNER_START <= ny <= self.INNER_END:
                if self.grid[nx][ny] == 0:
                    count += 1
        return count

    def solve(self, x, y, step_count):
        # Base Case: All 25 inner cells are filled
        if step_count == self.TOTAL_INNER_CELLS:
            return True

        # Get valid candidates within the inner 5x5
        candidates = []
        for dx, dy, is_diag in self.MOVES:
            nx, ny = x + dx, y + dy
            if self.INNER_START <= nx <= self.INNER_END and self.INNER_START <= ny <= self.INNER_END:
                if self.grid[nx][ny] == 0:
                    degree = self.get_degree(nx, ny)
                    if(self.check_outer_ring(nx,ny, step_count+1)):
                        candidates.append((nx, ny, degree))

        # Warnsdorff's Heuristic: Sort by degree ascending (fewest options first)

        candidates.sort(key=lambda c: c[2])

        for nx, ny, deg in candidates:
            self.grid[nx][ny] = step_count + 1
            
            if self.solve(nx, ny, step_count + 1):
                return True
                
            # Backtrack
            self.grid[nx][ny] = 0
            
        return False

    def check_outer_ring(self, x, y, num):  
        if(self.grid[0][y] == num or self.grid[6][y] == num or self.grid[x][0] == num or self.grid[x][6] == num):
            return True
        if x == y:  # Main diagonal
            if(self.grid[0][0] == num or self.grid[6][6] == num):
                return True
        if x + y == 6:  # Anti-diagonal
            if(self.grid[0][6] == num or self.grid[6][0] == num):
                return True
        return False
