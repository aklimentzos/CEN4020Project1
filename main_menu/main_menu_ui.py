import pygame
import sys
import os
from ui_elements import Button
from ui_elements import TextBox
import tkinter as tk
from tkinter import filedialog
import json
from pathlib import Path

class MainMenu:
    def __init__(self, authenticated_user=""):
        self.authenticated_user = authenticated_user
        self.board_width = 900
        self.board_height = 700
        self.font = pygame.font.Font(None, 32)
        self.textbox_menu = TextBox(340, 50, "Project 1", pygame.font.Font(None, 72))
        self.textbox_welcome = TextBox(360, 115, f"Welcome, {authenticated_user}!", self.font, visible=bool(authenticated_user))
        self.button_newgame = Button(235, 200, 420, 80, "New Game", self.font)
        self.button_loadgame = Button(235, 300, 420, 80, "Load Game", self.font)
        self.button_highscores = Button(235, 400, 420, 80, "High Scores", self.font)
        self.button_exit = Button(235, 500, 420, 80, "Exit", self.font)

    def open_file_dialog(self, start_dir="."):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            initialdir=start_dir,
            title="Select saved game",
            filetypes=[("JSON save files", self.authenticated_user + "_*.json"), ("All files", "*.*")]
        )

        root.destroy()
        return file_path

    def display(self):
        pygame.init()

        screen = pygame.display.set_mode((self.board_width, self.board_height))
        pygame.display.set_caption("Main Menu")

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.button_newgame.handle_event(event) == 'clicked':
                    return "new_game"
                
                if self.button_loadgame.handle_event(event) == 'clicked':
                    base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
                    path = self.open_file_dialog(base_dir / "saves")
                    
                    if path:
                        with open(str(path)) as f:
                            meta = json.load(f)

                    # verifying a path was selected
                    if path is not None and path != "":
                        level = meta.get("level")

                        if level == 1:
                            return "switch_to_level_1", path
                        elif level == 2:
                            return "switch_to_level_2", path
                        elif level == 3:
                            return "switch_to_level_3", path
                    
                if self.button_highscores.handle_event(event) == 'clicked':
                    return "high_scores"

                if self.button_exit.handle_event(event) == 'clicked':
                    pygame.quit()
                    sys.exit()
    
            screen.fill((245, 245, 245))
            self.textbox_menu.draw(screen)
            self.textbox_welcome.draw(screen)
            self.button_newgame.draw(screen)
            self.button_loadgame.draw(screen)
            self.button_highscores.draw(screen)
            self.button_exit.draw(screen)
            pygame.display.flip()
            clock.tick(60)