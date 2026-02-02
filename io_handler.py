from pathlib import Path
import json
import os
import datetime

class IO:
    """IO object for managing save file"""
    def __init__(self, logic):
        """Genrate base filepath and import logic object"""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.base_dir, "data.json")
        self.completed_path = os.path.join(self.base_dir, "high_scores.json")
        self.logic = logic
        self.data = {}
        self.completed_data = {}

    def file_initalize(self):
        """Check if data file exists and if a save game exists"""
        if Path(self.file_path).is_file():
            #Open file and load data
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)

            #If the data file contains an old game ask the user if they want to load it
            if (self.data["new_game"]) == False:
               load = input("A save game exists, do you wish to load game?(Yes/No): ")
               
               #Load saved game
               if load == "Yes":
                    self.logic.matrix = self.data["d_matrix"]
                    self.logic.cur_num = self.data["d_cur_num"]
                    self.logic.score = self.data["d_score"]
                    self.logic.last_coords = self.data["d_last_coords"]
               else:
                   print("Starting new game")
        #Create new default data file if one does not exist
        else:
            dump = {"new_game": True, "d_matrix": [[0,0,0,0,0],
                                                    [0,0,0,0,0],
                                                    [0,0,0,0,0],
                                                    [0,0,0,0,0],
                                                    [0,0,0,0,0]], 
                                                    "d_cur_num": 1,
                                                    "d_score":0,
                                                    "d_last_coords":[-1,-1]}
            with open(self.file_path, "w") as f:
                json.dump(dump ,f)
        
    
    def save_game(self, matrix, cur_num, score,last_coords):
        """Saves current game"""
        dump = {"new_game": False, "d_matrix": matrix, "d_cur_num": cur_num, "d_score":score, "d_last_coords":last_coords}
        with open(self.file_path, "w") as f:
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