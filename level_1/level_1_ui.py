from level_1.level_1_logic import Level1State
from level_1.level_1_logic import Level1Controller
from ui_elements import InputBox
from ui_elements import Button
from ui_elements import TextBox
from ui_elements import Grid
import pygame
import sys


class Level1UI:
    def __init__(self):
        self.board_width = 900
        self.board_height = 700
        self.font = pygame.font.Font(None, 32)
        self.inputbox_username = InputBox(600, 50, 220, 40, self.font, placeholder="Enter name...")
        self.button_save = Button(600, 90, 100, 40, "Save", self.font)
        self.textbox_error = TextBox(100, 600, "", self.font, visible= False)
        self.gamestate = Level1State()
        self.game_cont = Level1Controller(self.gamestate)
        self.grid_main = Grid(5, 90, 50, 50, self.game_cont.get_matrix(), self.font)
        
        
        
    
    def display(self):
        pygame.init()

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
                    if self.game_cont.make_move(coords):
                        self.grid_main.set_matrix(self.game_cont.get_matrix())
                        self.textbox_error.set_visible(False)
                    else:
                        self.textbox_error.set_text(self.game_cont.get_fail())
                        self.textbox_error.set_visible(True)
                
                self.inputbox_username.handle_event(event)
                # if self.button_save.handle_event(event) == 'clicked':
                    
            
            screen.fill((245, 245, 245))
            self.button_save.draw(screen)
            self.inputbox_username.draw(screen)
            self.textbox_error.draw(screen)
            self.grid_main.draw(screen)
            pygame.display.flip()
            clock.tick(60)