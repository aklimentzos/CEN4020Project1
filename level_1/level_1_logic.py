from pathlib import Path
import json
import os
import datetime
from pathlib import Path

class Level1State:
    """Class running the logic for the game"""
    def __init__(self):
        #Matrix used to keep track of the grid
        self.matrix = [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]
        
        #Stack used to for "undo"
        self.move_stack = []
        
        #Keep track of the current number to be placed and the score
        self.cur_num = 1
        self.score = 0

        #Used to exit the game for any specific reason
        self.check = "Pass"
        self.fail_reason = ""

        #Saves the coords the last number was placed on. Used for invalid move calculations
        self.last_coords = [-1 , -1]
        

class Level1Controller:
    def __init__(self, state : Level1State):
        self.state = state
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
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

    

    def make_move(self, user_input):
        """Makes the move for the user"""
        grid_coords = user_input
        if(self.state.last_coords[0] == -1):
            self.state.move_stack.append((grid_coords[0], grid_coords[1], 0))
            self.update_matrix(grid_coords)
            return True
        else:
            #Check if new coords are only one block away from last number placed
            print(f"last coords: {self.state.last_coords}")
            print(f"cur coords: {grid_coords}")
            print(f"difference1: {abs(grid_coords[0] - self.state.last_coords[0])}, difference2: {abs(grid_coords[1] - self.state.last_coords[1])}")
            if(abs(grid_coords[0] - self.state.last_coords[0]) <= 1 and abs(grid_coords[1] - self.state.last_coords[1]) <= 1):
                #Check if number was already placed there
                if(self.state.matrix[grid_coords[0]][grid_coords[1]] == 0):
                    self.state.move_stack.append([grid_coords[0], grid_coords[1], 0])
                    self.update_score(grid_coords)
                    self.update_matrix(grid_coords)
                    return True
                else:
                    self.state.fail_reason = "Invalid Move, cell occupied"
                    return False
            else:
                self.state.fail_reason = "Invalid Move, new number must be next to the previous one"
                return False

    def update_score(self, new_coords):
        """Update the score if the user made a diagonal move"""
        if(abs(new_coords[0] - self.state.last_coords[0]) == 1 and abs(new_coords[1] - self.state.last_coords[1]) == 1):       
            self.state.score = self.state.score + 1
            self.state.move_stack[-1][2] = 1

    def get_score(self):
        """Return current score"""
        return self.state.score
    

    def undo(self):
        if(self.state.cur_num == 1):
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
        dump = {"level": 1, 
                "matrix": self.state.matrix, 
                "cur_num": self.state.cur_num, 
                "core":self.state.score, 
                "last_coords": self.state.last_coords, 
                "move_stack": self.state.move_stack}
        with open(path, "w") as f:
            json.dump(dump ,f)

    def save_completed_game(self, username, score, matrix):
        """Saves completed game to high score list"""
        #Load existing high score data
        if Path(self.completed_path).is_file():
            with open(self.completed_path, 'r') as f:
                self.completed_data = json.load(f)
        else:
            self.completed_data = {}

        #Create high score list if it does not exist
        if "high_scores" not in self.completed_data:
            self.completed_data["high_scores"] = []

        #Append new high score
        self.completed_data["high_scores"].append({"username": username, "score": score, "matrix": matrix, "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
        
        #Save updated high score list
        with open(self.completed_path, "w") as f:
            json.dump(self.completed_data ,f)

