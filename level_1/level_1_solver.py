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
        self.max_diagonal_score = -1
        self.found_count = 0

    def get_degree(self, x, y):
        count = 0
        for dx, dy, _ in self.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.SIZE and 0 <= ny < self.SIZE and self.grid[nx][ny] == 0:
                count += 1
        return count

    def solve(self, x, y, step_count, current_score):
        if step_count == self.SIZE * self.SIZE:
            self.found_count += 1
            if current_score > self.max_diagonal_score:
                self.max_diagonal_score = current_score
                self.best_grid = [row[:] for row in self.grid]
            return current_score >= 13  # stop early if good enough

        candidates = []
        for dx, dy, is_diag in self.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.SIZE and 0 <= ny < self.SIZE and self.grid[nx][ny] == 0:
                candidates.append((nx, ny, is_diag, self.get_degree(nx, ny)))

        candidates.sort(key=lambda c: (c[3], -int(c[2])))

        for nx, ny, is_diag, _deg in candidates:
            self.grid[nx][ny] = step_count + 1
            if self.solve(nx, ny, step_count + 1, current_score + (1 if is_diag else 0)):
                return True
            self.grid[nx][ny] = 0

        return False

    def get_best_solution(self, score):
        # reset per-run state
        self.best_grid = None
        self.max_diagonal_score = -1
        self.found_count = 0

        # snapshot right before solving
        before = [row[:] for row in self.grid]

        # find max number + its position
        max_num = 0
        start_pos = None
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                v = self.grid[r][c]
                if v > max_num:
                    max_num = v
                    start_pos = (r, c)

        if not start_pos:
            return None, None  # nothing to continue from

        # continue from current max_num position
        self.solve(start_pos[0], start_pos[1], max_num, score)

        if not self.best_grid:
            return None, None

        # mask only what solver filled this run
        solved_mask = [[0]*self.SIZE for _ in range(self.SIZE)]
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if before[r][c] == 0 and self.best_grid[r][c] != 0:
                    solved_mask[r][c] = 1

        return self.best_grid, solved_mask