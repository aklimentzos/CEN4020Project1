from level_1.level_1_logic import Level1State
from level_1.level_1_logic import Level1Controller
from level_2.level_2_logic import Level2State
from level_2.level_2_ui import Level2UI
from ui_elements import InputBox
from ui_elements import Button
from ui_elements import TextBox
from ui_elements import Grid
import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import json


class Level1UI:
    def __init__(self, gamestate):
        self.board_width = 900
        self.board_height = 700
        self.font = pygame.font.Font(None, 32)
        self.inputbox_username = InputBox(600, 50, 210, 40, self.font, placeholder="Enter name...")
        self.button_save = Button(600, 100, 100, 40, "Save", self.font)
        self.button_undo = Button(710, 100, 100, 40, "Undo", self.font)
        self.button_clear = Button(600, 150, 210, 40, "Clear Board", self.font)
        self.button_continue = Button(300, 650, 210, 40, "Next Level", self.font, visible=False)
        self.button_load = Button(600, 200, 210, 40, "Load Game", self.font)
        self.textbox_error = TextBox(100, 600, "", self.font, visible= False)
        self.status_box = TextBox(150, 20, f"Score: {gamestate.score}       Cur Num: {gamestate.cur_num}", self.font)
        self.gamestate = gamestate
        self.game_cont = Level1Controller(self.gamestate)
        self.grid_main = Grid(5, 90, 50, 50, self.game_cont.get_matrix(), self.font)
        self.username_locked = False
        self.final_username = ""   
    
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
        pygame.init()
        pygame.mixer.init()
        
        screen = pygame.display.set_mode((self.board_width, self.board_height))
        pygame.display.set_caption("Level 1")

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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
                        self.textbox_error.set_visible(False)
                        pygame.mixer.Sound.play(pygame.mixer.Sound(str(self.game_cont.base_dir / "assets" / "successful_move_sound.mp3"))).set_volume(0.5)
                    # Handling invalid move with error message and sound.
                    else:
                        self.textbox_error.set_text(self.game_cont.get_fail())
                        self.textbox_error.set_visible(True)
                        pygame.mixer.Sound.play(pygame.mixer.Sound(str(self.game_cont.base_dir / "assets" / "invalid_move_sound.mp3"))).set_volume(0.5)
                
                self.inputbox_username.handle_event(event)

                # Event handler for saving a game.
                if self.button_save.handle_event(event) == 'clicked':
                    if self.inputbox_username.value == "":
                        self.textbox_error.set_text("Please enter a username before saving.")
                        self.textbox_error.set_visible(True)
                    else:
                        self.game_cont.save_game(str(self.game_cont.base_dir / "saves" / f"{self.inputbox_username.value}_level1_save.json"))
                
                # Event handler for undoing a move.
                if self.button_undo.handle_event(event) == 'clicked':
                    self.game_cont.undo()

                # Event handler for clearing the board.
                if self.button_clear.handle_event(event) == 'clicked':
                    self.game_cont.clear_board()

                # Event handler for loading a game.
                if self.button_load.handle_event(event) == 'clicked':
                    path = self.open_file_dialog(str(self.game_cont.base_dir / "saves"))

                    if path:
                        with open(str(path)) as f:
                            meta = json.load(f)

                        level = meta.get("level")
                        print(f"Loaded save file for level {level}")

                        # Handling loading game from level 1 to level 2 and vice versa with appropriate UI updates.
                        if level == 1:
                            self.game_cont.load_game(path)
                            self.grid_main.set_matrix(self.game_cont.get_matrix())
                            self.textbox_error.set_visible(False)
                            self.status_box.set_text( f"Score: {self.gamestate.score}       Cur Num: {self.gamestate.cur_num}")
                            pygame.display.flip()
                        elif level == 2:
                            return ("switch_to_level2", path)

                # Event handler for when the game is completed.
                if self.gamestate.cur_num >= 26:
                    if self.inputbox_username.value == "":
                        self.textbox_error.set_text("Please enter a username before next level.")
                        self.textbox_error.set_visible(True)
                    else:
                        self.game_cont.save_completed_game(self.inputbox_username.value, self.gamestate.score, self.gamestate.matrix)
                        self.textbox_error.set_text("Congratulations! You've completed Level 1!")
                        self.textbox_error.set_visible(True)
                        self.button_continue.set_visible(True) 

                    # Event handler for if the user wishes to continue to the next level after completing the game.
                    if self.button_continue.handle_event(event) == 'clicked':
                        level2_state = Level2State(self.gamestate)
                        level2_ui = Level2UI(level2_state)
                        level2_ui.display()
                        return

            self.status_box.set_text( f"Score: {self.gamestate.score}       Cur Num: {self.gamestate.cur_num}")

            screen.fill((245, 245, 245))
            self.button_save.draw(screen)
            self.button_undo.draw(screen)
            self.button_clear.draw(screen)
            self.button_continue.draw(screen)
            self.button_load.draw(screen)
            self.inputbox_username.draw(screen)
            self.textbox_error.draw(screen)
            self.status_box.draw(screen)
            self.grid_main.draw(screen)
            pygame.display.flip()
            clock.tick(60)