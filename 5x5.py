"""
File: 5x5_game.py
Author: Apostolos Klimentzos
Course: CEN 4020
Assignment: 5x5 Grid Game
Description:
    Implements a 5x5 grid-based number placement game with
    move validation, scoring, and save/load functionality.
Date: 2026-01-19
"""


import json
import os
from pathlib import Path

def clear_console():
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':
        # For Windows
        _ = os.system('cls')
    else:
        # For Linux and other POSIX systems
        _ = os.system('clear')

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

class Interface:
    """Class used to interface with user and print the grid"""

    def __init__(self):  
        """Initialize the Logic and IO object for the interface object"""
        self.logic = Logic()
        self.IO = IO(self.logic)

    def grid(self): 
        """Genrate the grid to be printed on screen"""
        for x in range(5):
            for y in range(5):
                print('┌---┐', end='')
            print('')
            for y in range(5):
                if int(self.logic.get_grid_number(x,y)) == 0:
                     print('|   |', end='')
                else:
                    if int(self.logic.get_grid_number(x,y)) < 10:
                        print(f'| {self.logic.get_grid_number(x,y)} |', end='')
                    else:
                        print(f'| {self.logic.get_grid_number(x,y)}|', end='')
            print('')
            for y in range(5):
                print('└---┘', end='')
            print('')
            
    def get_user_input(self):
        """Receive and validate the user input"""
        while True:
            print(f'Score: {self.logic.get_score()}')
            print("save: Saves current game, quit: Closes games")
            user_in = input(f'Give your next input in this format "row(space)column" (Current Number: {self.logic.get_cur_num()}): ')
            user_in = user_in.split()

            #Quit condition
            if 'quit' in user_in:
                return('exit')
            
            #Save condition
            if 'save' in user_in:
                self.IO.save_game(self.logic.matrix, self.logic.cur_num, self.logic.score, self.logic.last_coords)
                print("Game saved")
                return('exit')

            #Input needs to include 2 numbers
            if len(user_in) != 2:
                print('You need to input 2 numbers')
                continue

            #Check if row and column inputs are in range
            if int(user_in[0]) > 5 or int(user_in[0]) < 0:
                print("Row number needs to be between 1 and 5")
                continue
            
            if int(user_in[1]) > 5 or int(user_in[1]) < 0:
                print("Column number needs to be between 1 and 5")
                continue

            return(user_in)

    def run_game(self):
        """Main game loop and initialization"""
        #Initialize the IO file
        self.IO.file_initalize()
        #Generate grid
        self.grid()

        #Main game loop
        while True:
            user_input = self.get_user_input()
            if user_input == 'exit':
                print('Exiting Game')
                input("")
                break

            #Make the move based on user input
            self.logic.make_move(user_input)
            #Check if logic returned a fail condition
            check = self.logic.get_check()
            if check == "Fail":
                input("")
                break
            
            #Check if last number was placed
            if self.logic.get_cur_num() == 26:
                clear_console()
                self.grid()
                print("Game finished")
                print(f"Final Score: {self.logic.get_score()}")
                break

            clear_console()
            self.grid()

class IO:
    """IO object for managing save file"""
    def __init__(self, logic):
        """Genrate base filepath and import logic object"""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.base_dir, "data.json")
        self.logic = logic
        self.data = {}

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

def run():
    """Initialize interface object and run game"""
    game = Interface()
    game.run_game()


run()
