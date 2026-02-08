from level_1.level_1_logic import Level1State
from level_2.level_2_logic import Level2State
from level_1.level_1_logic import Level1Controller
from level_2.level_2_logic import Level2Controller
import pygame
import sys
from level_1.level_1_ui import Level1UI
from level_2.level_2_ui import Level2UI

def main():
    pygame.init()

    current_level = 1
    level1_state = Level1State()
    level2_state = None

    while True:
        if current_level == 1:
            ui = Level1UI(level1_state)
        else:
            if level2_state is None:
                level2_state = Level2State(level1_state)
            ui = Level2UI(level2_state)

        result = ui.display()

        if result == "quit":
            break

        # Logic for loading game from level 1 state to level 2 state and vice versa.
        if isinstance(result, tuple):
            cmd, payload = result

            if cmd == "switch_to_level2":
                path = payload
                level2_state = Level2State(level1_state)
                level2_controller = Level2Controller(level2_state)
                level2_controller.load_game(path)
                current_level = 2

            if cmd == "switch_to_level1":
                path = payload
                level1_state = Level1State()
                level1_controller = Level1Controller(level1_state)
                level1_controller.load_game(path)
                current_level = 1

if __name__ == "__main__":
    main()