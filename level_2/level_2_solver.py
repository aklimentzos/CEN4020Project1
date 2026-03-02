class Level2Solver:
    def __init__(self, matrix):

        self.matrix = matrix

    def solve(self,number_to_place):
        # Base Case: All numbers from 2 to 25 are placed
        if number_to_place > 25:
            return True 

        # Find the coordinates (r, c) of 'number_to_place' in the 5x5 matrix
        r, c = self.find_position_in_inner_board(number_to_place)
        
        # Get all possible target cells in the outer ring
        possible_cells = self.get_valid_outer_ring_cells(r, c)

        for cell in possible_cells:
            if self.matrix[cell[0]][cell[1]] == 0:
                self.matrix[cell[0]][cell[1]] = number_to_place  # Make a move
                
                if self.solve(number_to_place + 1): # Recursively try to place the next number
                    return True
                
                self.matrix[cell[0]][cell[1]] = 0 # Backtrack
                
        return False # Hit a dead end

    def find_position_in_inner_board(self, number):
        for i in range(1, 6):
            for j in range(1, 6):
                if self.matrix[i][j] == number:
                    if number  == 5:
                        print(f"Found {number} at position: ({i}, {j})") 
                    return (i, j)     
        return None

    def get_valid_outer_ring_cells(self,r, c):
        valid_cells = []
        
        # Check same row and column in the outer ring
        
        valid_cells.append((0, c))  # Top row
        valid_cells.append((6, c))  # Bottom row
        valid_cells.append((r, 0))  # Left column
        valid_cells.append((r, 6))  # Right column
        
        # Check corners based on diagonal rules
        if r == c:  # Main diagonal
            valid_cells.append((0, 0))
            valid_cells.append((6, 6))
        if r + c == 6:  # Anti-diagonal
            valid_cells.append((0, 6))
            valid_cells.append((6, 0))
        
        return valid_cells
    
    def find_best_solution(self):
        # Start the recursive backtracking solver with the first number to place (2)
        if self.solve(2):
            return self.matrix
        else:
            return None


