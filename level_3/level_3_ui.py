from level_3.level_3_solver import Level3Solver
from level_3.level_3_logic import Level3Controller
from ui_elements import InputBox, Button, TextBox, Grid
import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import json


class Level3UI:
    def __init__(self, level3_state, authenticated_user=""):
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
        self.button_exit = Button(490, 750, 210, 40, "Exit", self.font, visible=False)
        self.button_solve = Button(750, 250, 210, 40, "Solve from Here", self.font)
        self.textbox_error = TextBox(100, 700, "", self.font, visible=False)

        self.status_box = TextBox(
            240, 20,
            f"Score: {level3_state.score}       Cur Num: {level3_state.cur_num}",
            self.font
        )

        self.gamestate = level3_state
        self.game_cont = Level3Controller(self.gamestate)

        self.grid_main = Grid(7, 90, 50, 50, self.game_cont.get_matrix(), self.font)

        # Timer setup
        self.timer_limit = 60
        self.start_ticks = pygame.time.get_ticks()
        self.current_time_left = self.timer_limit
        self.timer_box = TextBox(600, 20, f"Time: {self.current_time_left}", self.font)

        #Solver setup
        self.solver = Level3Solver(self.game_cont.get_matrix())
        self.solve_mask = None
        self.solved = False

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
        pygame.display.set_caption("Level 3")
        clock = pygame.time.Clock()

        #Flag to ensure we only add the time bonus once when the game is completed
        bonus_added = False

        while True:
            #Flag to check if the game is finished
            is_finished = self.gamestate.cur_num >= 26
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

                #Block that only runs if the game isn't finished yet
                if not is_finished:
                    coords = self.grid_main.handle_event(event)
                    if coords:
                        # Require username before moves
                        if not self.username_locked:
                            if self.inputbox_username.value == "":
                                self.textbox_error.set_text("Please enter a username before making a move.")
                                self.textbox_error.set_visible(True)
                                continue
                            else:
                                self.final_username = self.inputbox_username.value
                                self.username_locked = True
                                self.textbox_error.set_visible(False)

                        # Try move
                        if self.game_cont.make_move(coords):
                            self.grid_main.set_matrix(self.game_cont.get_matrix())
                            self.textbox_error.set_visible(False)

                            pygame.mixer.Sound.play(
                                pygame.mixer.Sound(str(self.game_cont.base_dir / "assets" / "successful_move_sound.mp3"))
                            ).set_volume(0.5)
                        else:
                            self.textbox_error.set_text(self.game_cont.get_fail())
                            self.textbox_error.set_visible(True)
                            pygame.mixer.Sound.play(
                                pygame.mixer.Sound(str(self.game_cont.base_dir / "assets" / "invalid_move_sound.mp3"))
                            ).set_volume(0.5)

                    # Solve button event
                    if self.button_solve.handle_event(event) == 'clicked':
                        if not is_finished:
                            # We find a solution starting from the highest number currently on the board
                            full_solution, mask = self.solver.find_best_solution()
                            
                            if full_solution:
                                self.solve_mask = mask
                                self.gamestate.matrix = full_solution  
                                self.gamestate.cur_num = 26            
                                self.solved = True                     
                                self.grid_main.set_matrix(full_solution)
                                self.textbox_error.set_text("Puzzle solved from your current position!")
                                self.textbox_error.set_visible(True)
                                self.button_newgame.set_visible(True)
                                self.button_exit.set_visible(True)
                            else:
                                self.textbox_error.set_text("No valid solution found from this state.")
                                self.textbox_error.set_visible(True)

                    # Undo
                    if self.button_undo.handle_event(event) == 'clicked':
                        self.game_cont.undo()
                        self.grid_main.set_matrix(self.game_cont.get_matrix())

                    # Clear
                    if self.button_clear.handle_event(event) == 'clicked':
                        self.game_cont.clear_board()
                        self.grid_main.set_matrix(self.game_cont.get_matrix())

                # Load
                if self.button_load.handle_event(event) == 'clicked':
                    path = self.open_file_dialog(self.game_cont.base_dir / "saves")
                    if path:
                        with open(str(path), encoding="utf-8") as f:
                            meta = json.load(f)

                        level = meta.get("level")

                        if level == 3:
                            self.game_cont.load_game(path)
                            self.grid_main.set_matrix(self.game_cont.get_matrix())
                            self.textbox_error.set_visible(False)
                            self.status_box.set_text(f"Score: {self.gamestate.score}       Cur Num: {self.gamestate.cur_num}")
                            pygame.display.flip()
                        elif level == 2:
                            return ("switch_to_level2", path)
                        elif level == 1:
                            return ("switch_to_level1", path)
                # Save
                if self.button_save.handle_event(event) == 'clicked':
                    if self.inputbox_username.value == "":
                        self.textbox_error.set_text("Please enter a username before saving.")
                        self.textbox_error.set_visible(True)
                    else:
                        self.game_cont.save_game(
                            str(self.game_cont.base_dir / "saves" / f"{self.inputbox_username.value}_level3_save.json")
                        )

                # Completed Level 3
                if is_finished and not self.solved:
                    if not bonus_added:
                        # Add remaining time to score
                        self.gamestate.score += self.current_time_left
                        bonus_added = True

                    if self.inputbox_username.value == "":
                        self.textbox_error.set_text("Please enter a username before finishing.")
                        self.textbox_error.set_visible(True)
                    else:
                        self.game_cont.save_completed_game(
                            self.inputbox_username.value,
                            self.gamestate.score,
                            self.gamestate.matrix
                        )
                        self.textbox_error.set_text("Congratulations! You've completed Level 3! Play again?")
                        self.textbox_error.set_visible(True)
                        self.button_newgame.set_visible(True)
                        self.button_exit.set_visible(True)

                if self.button_newgame.handle_event(event) == 'clicked':
                    return ("switch_to_level1", None)

                if self.button_exit.handle_event(event) == 'clicked':
                    pygame.quit()
                    sys.exit()

                self.inputbox_username.handle_event(event)
            self.status_box.set_text(f"Score: {self.gamestate.score}       Cur Num: {self.gamestate.cur_num}")

            screen.fill((245, 245, 245))
            self.button_save.draw(screen)
            self.button_undo.draw(screen)
            self.button_clear.draw(screen)
            self.button_newgame.draw(screen)
            self.timer_box.draw(screen)
            self.button_exit.draw(screen)
            self.button_load.draw(screen)
            self.inputbox_username.draw(screen)
            self.textbox_error.draw(screen)
            self.status_box.draw(screen)
            self.button_solve.draw(screen)
            self.grid_main.draw(screen, mask=getattr(self, 'solve_mask', None))

            pygame.display.flip()
            clock.tick(60)