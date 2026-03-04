import copy

from level_3.level_3_logic import Level3State
from level_3.level_3_ui import Level3UI
from level_2.level_2_logic import Level2Controller
from ui_elements import InputBox
from ui_elements import Button
from ui_elements import TextBox
from ui_elements import Grid
import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import json

from level_2.level_2_solver import Level2Solver


class Level2UI:
    def __init__(self, level2_state, authenticated_user=""):
        self.board_width = 1000
        self.board_height = 800
        self.font = pygame.font.Font(None, 32)
        self.inputbox_username = InputBox(750, 50, 210, 40, self.font, placeholder="Enter name...", readonly=bool(authenticated_user))
        self.inputbox_username.text = authenticated_user
        self.username_locked = bool(authenticated_user)

        self.button_save = Button(750, 100, 100, 40, "Save", self.font)
        self.button_undo = Button(860, 100, 100, 40, "Undo", self.font)
        self.button_clear = Button(750, 150, 210, 40, "Clear Board", self.font)
        self.button_load = Button(750, 200, 210, 40, "Load Game", self.font)
        self.button_newgame = Button(270, 750, 210, 40, "New Game", self.font, visible=False)
        self.button_nextlevel = Button(490, 750, 210, 40, "Next Level", self.font, visible=False)
        self.textbox_error = TextBox(100, 700, "", self.font, visible= False)
        self.status_box = TextBox(240, 20, f"Score: {level2_state.score}       Cur Num: {level2_state.cur_num}", self.font)
        self.gamestate = level2_state
        self.game_cont = Level2Controller(self.gamestate)
        self.grid_main = Grid(7, 90, 50, 50, self.game_cont.get_matrix(), self.font)
        self.button_solve = Button(750, 250, 210, 40, "Solve from Here", self.font)

        # Timer setup
        self.timer_limit = 60
        self.start_ticks = pygame.time.get_ticks()
        self.current_time_left = self.timer_limit
        self.timer_box = TextBox(600, 20, f"Time: {self.current_time_left}", self.font)

        #Solver setup
        self.solver = Level2Solver(self.game_cont.get_matrix())
        self.solve_mask = None
        self.solved = False
    
    # Helper function to open file dialog for loading saves
    def open_file_dialog(self, start_dir="."):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            initialdir=start_dir,
            title="Select saved game",
            filetypes=[("JSON save files", "*.json"), ("All files", "*.*")]
        )

        root.destroy()
        return file_path

    def display(self):
        
        screen = pygame.display.set_mode((self.board_width, self.board_height))
        pygame.display.set_caption("Level 2")

        clock = pygame.time.Clock()

        # Flag to ensure we only add the time bonus once
        bonus_added = False

        while True:
            # Check if game is finished
            is_finished = self.gamestate.cur_num >= 26
            #Only run timer if game is not finished
            if not is_finished:
                seconds_passed = (pygame.time.get_ticks() - self.start_ticks) // 1000
                if seconds_passed >= 1:
                    self.start_ticks = pygame.time.get_ticks()
                    if self.current_time_left > 0:
                        self.current_time_left -= 1
                    else:
                        self.gamestate.score = max(0, self.gamestate.score - 1)
                    
                    self.timer_box.set_text(f"Time: {self.current_time_left}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()   
                #Block that runs if game is not finished
                if not is_finished:
                    coords = self.grid_main.handle_event(event)
                    if coords:
                        # requiring username before allowing any moves to be made.
                        if not self.username_locked:
                            if self.inputbox_username.value == "":
                                self.textbox_error.set_text("Please enter a username before making a move.")
                                self.textbox_error.set_visible(True)
                                continue
                            else:
                                self.final_username = self.inputbox_username.value
                                self.username_locked = True
                                self.textbox_error.set_visible(False)

                        # Updating game state for valid move and playing sound.
                        if self.game_cont.make_move(coords):
                            self.grid_main.set_matrix(self.game_cont.get_matrix())
                            pygame.mixer.Sound.play(pygame.mixer.Sound(str(self.game_cont.base_dir / "assets" / "successful_move_sound.mp3"))).set_volume(0.5)
                        # Handling invalid move with error message and sound.
                        else:
                            self.textbox_error.set_text(self.game_cont.get_fail())
                            self.textbox_error.set_visible(True)
                            pygame.mixer.Sound.play(pygame.mixer.Sound(str(self.game_cont.base_dir / "assets" / "invalid_move_sound.mp3"))).set_volume(0.5)

                    if self.button_solve.handle_event(event) == 'clicked':
                        self.solver.matrix = [row[:] for row in self.game_cont.get_matrix()]
                        # Solve from the current state
                        solution, mask = self.solver.find_best_solution()

                        if solution is not None:
                            # Update logic state
                            self.gamestate.matrix = solution
                            # Update grid
                            self.grid_main.set_matrix(solution)
                            # Apply coloring mask
                            self.solve_mask = mask  
                            # Finish level
                            self.gamestate.cur_num = 26 
                            self.button_newgame.set_visible(True)
                            
                        else:
                            self.textbox_error.set_text("No solution possible from this state.")
                            self.textbox_error.set_visible(True)


                    # Event handler for undoing a move.
                    if self.button_undo.handle_event(event) == 'clicked':
                        self.game_cont.undo()

                    # Event handler for clearing the board.
                    if self.button_clear.handle_event(event) == 'clicked':
                        self.game_cont.clear_board()
                
                # Event handler for when the game is completed
                if is_finished and not self.solved:
                    if not bonus_added:
                        # Add remaining time to score
                        self.gamestate.score += self.current_time_left
                        bonus_added = True
                        
                    if self.inputbox_username.value == "":
                        self.textbox_error.set_text("Please enter a username before next level.")
                        self.textbox_error.set_visible(True)
                    else:
                        self.game_cont.save_completed_game(self.inputbox_username.value, self.gamestate.score, self.gamestate.matrix)
                        self.textbox_error.set_text("Congratulations! You've completed Level 2! Would like to play again?")
                        self.textbox_error.set_visible(True)
                        self.button_newgame.set_visible(True)
                        self.button_nextlevel.set_visible(True)
                    
                if self.button_nextlevel.handle_event(event) == 'clicked':
                    return ("switch_to_level3", None)

                # Event handler for if the user wishes to play again after completing the game.
                if self.button_newgame.handle_event(event) == 'clicked':
                    return ("switch_to_level1", None) 

                    
                # Event handler for loading a game.
                if self.button_load.handle_event(event) == 'clicked':
                    path = self.open_file_dialog(self.game_cont.base_dir / "saves")

                    if path:
                        with open(str(path)) as f:
                            meta = json.load(f)

                        level = meta.get("level")

                        # Handling loading game from level 1 to level 2 and vice versa with appropriate UI updates.
                        if level == 2:
                            self.game_cont.load_game(path)
                            self.grid_main.set_matrix(self.game_cont.get_matrix())
                            self.textbox_error.set_visible(False)
                            self.status_box.set_text( f"Score: {self.gamestate.score}       Cur Num: {self.gamestate.cur_num}")
                            pygame.display.flip()
                        elif level == 1:
                            return ("switch_to_level1", path)
                        elif level == 3:
                            return ("switch_to_level3", path)
                        
                # Event handler for saving a game.
                if self.button_save.handle_event(event) == 'clicked':
                    if self.inputbox_username.value == "": 
                        self.textbox_error.set_text("Please enter a username before saving.")
                        self.textbox_error.set_visible(True)
                    else:
                        self.game_cont.save_game(str(self.game_cont.base_dir / "saves" / f"{self.inputbox_username.value}_level2_save.json"))

                self.inputbox_username.handle_event(event)

            self.status_box.set_text( f"Score: {self.gamestate.score}       Cur Num: {self.gamestate.cur_num}")

            screen.fill((245, 245, 245))
            self.button_save.draw(screen)
            self.button_undo.draw(screen)
            self.button_clear.draw(screen)
            self.button_newgame.draw(screen)
            self.button_nextlevel.draw(screen)
            self.timer_box.draw(screen)
            self.button_solve.draw(screen)
            self.button_load.draw(screen)
            self.inputbox_username.draw(screen)
            self.textbox_error.draw(screen)
            self.status_box.draw(screen)
            self.grid_main.draw(screen, mask=getattr(self, 'solve_mask', None))
            pygame.display.flip()
            clock.tick(60)