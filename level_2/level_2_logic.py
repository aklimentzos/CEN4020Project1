from level_1.level_1_logic import Level1State
from pathlib import Path
import json
import os
import datetime
from pathlib import Path

class Level2State:
    """Class running the logic for the game"""
    def __init__(self, level1_state : Level1State):
        #Matrix used to keep track of the grid
        self.matrix = [[0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]]
        
        #Updating matrix with level 1 data
        self._import_inner_matrix(level1_state)

        #Stack used to for "undo"
        self.move_stack = []
        
        #Keep track of the current number to be placed and the score
        self.cur_num = 2
        self.score = level1_state.score

        #Used to exit the game for any specific reason
        self.check = "Pass"
        self.fail_reason = ""

        #Saves the coords the last number was placed on. Used for invalid move calculations
        self.last_coords = [-1 , -1]

    def _import_inner_matrix(self, level1_state : Level1State):
        for i in range(5):
            for j in range(5):
                self.matrix[i+1][j+1] = level1_state.matrix[i][j]

class Level2Controller:
    def __init__(self, state : Level2State):
        self.state = state
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
        self.err_msg = ""

    def get_grid_number(self, x, y):
        """Returns number given a grid coordinate"""
        return self.state.matrix[x][y]
    
    def get_cur_num(self):
        """Returns the next number to be placed"""
        return int(self.state.cur_num)
    
    def get_matrix(self):
        """returns the current board"""
        return self.state.matrix
    
    def get_fail(self):
        "returns reason why move failed"
        return self.state.fail_reason
    
    def update_matrix(self, coords):
        """Updates the matrix with the new number"""
        self.state.last_coords = coords
        self.state.matrix[int(coords[0])][int(coords[1])] = self.state.cur_num
        self.state.cur_num = self.state.cur_num + 1

    def is_valid_move(self, coords):
        """Checks if the move is valid according to level 2 rules"""
        row, column = coords

        # Verifying if the move is on the border
        if row not in (0, 6) and column not in (0, 6):
            return False
        
        # Finding the valid positions for the current number
        valid_row = -1
        valid_col = -1

        for i in range(5):
            for j in range(5):
                if self.state.matrix[i+1][j+1] == self.state.cur_num:
                    valid_row = i+1
                    valid_col = j+1
                    break

        inner_row = valid_row - 1
        inner_col = valid_col - 1

        # Checking if the move is in the same row or column as the valid positions
        if (row == valid_row or column == valid_col):
            return True

        allowed_corners = []

        # Allowing corner moves if on the main diagonal
        if inner_row == inner_col:
            allowed_corners.extend([(0,0), (6,6)])

        # Allowing corner moves if on the anti diagonal
        if inner_row + inner_col == 4:
            allowed_corners.extend([(0,6), (6,0)])

        # Checking if move is in allowed corners
        if allowed_corners:
            return (row, column) in allowed_corners

        return False

    def make_move(self, user_input):
        """Makes the move for the user"""
        grid_coords = user_input

        # Check if cell is already occupied
        if self.state.matrix[int(grid_coords[0])][int(grid_coords[1])] != 0:
            self.state.fail_reason = "Invalid Move, cell occupied"
            return False
        # Verifies if the move is valid according to level 2 rules
        elif not self.is_valid_move(grid_coords):
            self.state.fail_reason = "Invalid Move, not a valid move"
            return False
        # Playing the move and updating move stack
        else:
            self.state.move_stack.append([grid_coords[0], grid_coords[1], 0])
            self.update_matrix(grid_coords)
            self.update_score()
        return True

    def update_score(self):
        """Updates the score"""
        # No scoring method specified for level 2, so just incrementing by 1 for each valid move
        self.state.score = self.state.score + 1
        self.state.move_stack[-1][2] = 1

    def get_score(self):
        """Returns the current score"""
        return self.state.score
    
    def undo(self):
        """Undoes the last move"""
        if(self.state.cur_num == 2):
            return False
        else:
            if(self.state.move_stack[-1][2] == 1):
                self.state.score = self.state.score - 1
            self.state.matrix[self.state.last_coords[0]][self.state.last_coords[1]] = 0
            self.state.move_stack.pop()
            try:
                self.state.last_coords = [self.state.move_stack[-1][0], self.state.move_stack[-1][1]]
            except IndexError:
                self.state.last_coords = [-1,-1]
            self.state.cur_num = self.state.cur_num - 1

    def load_game(self, path):
        """Loads game from a save file. returns True if successfully loaded, False otherwise and saves error message"""
        required_keys = {"level", "matrix", "cur_num", "score", "last_coords", "move_stack"}
        p = Path(path)
        if not p.is_file() or p.suffix.lower() != ".json":
            self.err_msg = "Not a valid save file."
            return True
        
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            self.err_msg = "Save file is not valid JSON."
            return False
        
        if not isinstance(data, dict):
            self.err_msg = "Save file has invalid format."
            return False
        
        if not required_keys.issubset(data.keys()):
            self.err_msg = "Save file does not match expected schema."
            return False
        
        if data["level"] == 1:
            self.err_msg = "Wrong level save file"
            return False
        
        self.state.matrix = data["matrix"]
        self.state.cur_num = data["cur_num"]
        self.state.score = data["score"]
        self.state.last_coords = data["last_coords"]
        self.state.move_stack = data["move_stack"]
        return True

    def save_game(self, path):
        """Saves current game"""
        dump = {"level": 2, 
                "matrix": self.state.matrix, 
                "cur_num": self.state.cur_num, 
                "score":self.state.score, 
                "last_coords": self.state.last_coords, 
                "move_stack": self.state.move_stack}
        with open(path, "w") as f:
            json.dump(dump ,f)

    def save_completed_game(self, username, score, matrix):
        """Saves completed game to high score list"""
        save_complete_path = self.base_dir / "completed_games.json"
        # If completed_games.json exists, append to it
        if save_complete_path.is_file():
            with open(self.base_dir / "completed_games.json", "r") as f:
                completed_games = json.load(f)

            if isinstance(completed_games, dict):
                completed_games = [completed_games]

            completed_games.append({
                "username": username,
                "level": 1,
                "score": score,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "matrix": matrix
            })

            with open(self.base_dir / "completed_games.json", "w") as f:
                json.dump(completed_games, f)
        # If it does not exist, create it and add the first entry
        else:
            completed_data = {
                "username": username,
                "level": 1,
                "score": score,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "matrix": matrix
            }
            with open(self.base_dir / "completed_games.json", "w") as f:
                json.dump(completed_data, f)