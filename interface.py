import os
from io_handler import IO
from logic import Logic

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

def clear_console():
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':
        # For Windows
        _ = os.system('cls')
    else:
        # For Linux and other POSIX systems
        _ = os.system('clear')
