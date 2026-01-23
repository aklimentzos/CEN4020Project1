

class Logic:
    """Class running the logic for the game"""
    def __init__(self):
        #Matrix used to keep track of the grid
        self.matrix = [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]
        
        #Keep track of the current number to be placed and the score
        self.cur_num = 1
        self.score = 0

        #Used to exit the game for any specific reason
        self.check = "Pass"
        self.fail_reason = ""

        #Saves the coords the last number was placed on. Used for invalid move calculations
        self.last_coords = [-1 , -1]


    def get_grid_number(self, x, y):
        """Returns number given a grid coordinate"""
        return self.matrix[x][y]

    def get_cur_num(self):
        """Returns the next number to be placed"""
        return int(self.cur_num)

    def update_matrix(self, coords):
        """Updates the matrix with the new number"""
        self.last_coords = coords
        self.matrix[int(coords[0])][int(coords[1])] = self.cur_num
        self.cur_num = self.cur_num + 1

    def make_move(self, user_input):
        """Makes the move for the user"""
        grid_coords = user_input
        #Normalize input to be used for list indexing
        grid_coords[0] = int(grid_coords[0]) -1
        grid_coords[1] = int(grid_coords[1]) -1
        self.check_valid_move(grid_coords)

    def check_valid_move(self, new_coords):
        """Check if move is valid"""
        #Check if this is first move. Can be placed anywhere on grid
        if(self.last_coords[0] == -1):
            self.update_matrix(new_coords)
        else:
            #Check if new coords are only one block away from last number placed
            if(abs(new_coords[0] - self.last_coords[0]) == 1 or abs(new_coords[1] - self.last_coords[1]) == 1):
                #Check if number was already placed there
                if(self.matrix[new_coords[0]][new_coords[1]] == 0):
                    self.update_score(new_coords)
                    self.update_matrix(new_coords)
                else:
                    self.check = "Fail"
                    self.fail_reason = "Invalid Move"
            else:
                self.check = "Fail"
                self.fail_reason = "Invalid Move"
        
    def get_check(self):
        """Return the fail condition and the reason why"""
        if(self.check == "Fail"):
            print(self.fail_reason)
        return self.check

    def update_score(self, new_coords):
        """Update the score if the user made a diagonal move"""
        if(abs(new_coords[0] - self.last_coords[0]) == 1 and abs(new_coords[1] - self.last_coords[1]) == 1):       
            self.score = self.score + 1

    def get_score(self):
        """Return current score"""
        return self.score