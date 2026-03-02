from level_1.level_1_logic import Level1State, Level1Controller
from level_2.level_2_logic import Level2State, Level2Controller
from level_3.level_3_logic import Level3State, Level3Controller

import pygame
import sys

from level_1.level_1_ui import Level1UI
from level_2.level_2_ui import Level2UI
from level_3.level_3_ui import Level3UI


def main():
    pygame.init()

    current_level = 1

    level1_state = Level1State()
    level2_state = None
    level3_state = None

    while True:
        # Pick which UI to run
        if current_level == 1:
            ui = Level1UI(level1_state)

        elif current_level == 2:
            if level2_state is None:
                level2_state = Level2State(level1_state)
            ui = Level2UI(level2_state)

        else:  # current_level == 3
            if level3_state is None:
                # Level 3 should be built from the current level2_state
                if level2_state is None:
                    level2_state = Level2State(level1_state)
                level3_state = Level3State(level2_state)
            ui = Level3UI(level3_state)

        result = ui.display()

        if result == "quit":
            break

        # Handle switching between levels via UI return tuples
        if isinstance(result, tuple):
            cmd, payload = result

            if cmd == "switch_to_level2":
                path = payload
                level2_state = Level2State(level1_state)
                level2_controller = Level2Controller(level2_state)
                level2_controller.load_game(path)

                # If we’re switching back to level 2, drop level 3 state so it rebuilds cleanly later
                level3_state = None
                current_level = 2

            elif cmd == "switch_to_level3":
                path = payload

                # Need a valid level2_state as the base for level3
                if level2_state is None:
                    level2_state = Level2State(level1_state)

                # Build level3 from level2 then load the save
                level3_state = Level3State(level2_state)
                level3_controller = Level3Controller(level3_state)
                level3_controller.load_game(path)

                current_level = 3

            elif cmd == "switch_to_level1":
                path = payload
                level1_state = Level1State()
                level1_controller = Level1Controller(level1_state)
                level1_controller.load_game(path)

                # Reset downstream states because they depend on level1
                level2_state = None
                level3_state = None
                current_level = 1


if __name__ == "__main__":
    main()