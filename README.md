Project 1 (Sprint 2) – Multi-level Number Placement Game System

ABSTRACT
This document presents the Multi-level Number Placement Game System, a GUI-based puzzle game developed for CEN 4020.
The system supports multi-level gameplay, sound feedback, undo functionality, and persistent game logging.

1. INTRODUCTION
   The Multi-level Number Placement Game System expands an initial prototype that has been previously iterated (Sprint 1) into a fully interactive graphical application
   following agile development practices. Sprint 2 focuses on more gameplay features/additions, more UI and authentication features, and source code reorganization.

2. SYSTEM OVERVIEW
   The game allows players to place sequential numbers into a 5x5 grid and an expanded Level 2 and Level 3 board with an outer ring.
   The system enforces level specific placement rules and provides real-time feedback.

3. FUNCTIONAL REQUIREMENTS

- Level 3 expansion
- Level 2 and Level 3 reward implementation
- Per-level time limit with associated scoring (i.e., remove points when out of time, add points when completed before time limit)
- Auto-solving for each level
- Player authentication
- User-friendly main menu to start a new game, load a new game, or view high scores.
- Implementation of a High Scores menu that uses previously unused completed game data. 

4. NON-FUNCTIONAL REQUIREMENTS

- User-friendly interface
- Responsive system behavior
- Data and authentication persistence
- File structure and object definition organization

5. SYSTEM REQUIREMENTS
   Operating System: Windows
   Languages: Python
   Tools: VS Code, PyGame

6. FILE STRUCTURE

Proj1/

   ├── main.py

   ├── main.spec

   ├── sprint2_checklist.xlsx

   ├── players_db.json

   ├── Sprint2Demonstration.mp4

   ├── ui_elements.py

   └── README.md

 level_1/

   ├── level_1_logic.py

   ├── level_1_solver.py

   └──level_1_ui.py

 level_2/

   ├── level_2_logic.py

   ├── level_2_solver.py

   └──level_2_ui.py

 level_3/

   ├── level_3_logic.py

   ├── level_3_solver.py

   └──level_3_ui.py

 authentication/

   ├── auth_ui.py

   └── database_manager.py

 high_scores/

   └── high_scores_ui.py

main_menu/

   └── main_menu_ui.py

 assets/

   ├── invalid_move_sound.mp3

   └──successful_move_sound.mp3

 completed_games/

   ├── t_level2_completed.json

   ├── te_level2_completed.json

   ├── tes_level2_completed.json

   ├── test_level1_completed.json

   ├── test_level2_completed.json

   └── test_level3_completed.json

 saves/

   ├── test_level1_save.json

   ├── test_level2_save.json

   └── test_level3_save.json

8. EXECUTION INSTRUCTIONS
   Run the executable file or compile and run source code using the appropriate language commands (ex. python main.py [when in Proj1 directory]). Running the executable works alone outside of the Proj1
   directory but will not have access to any saved or completed games and will also not have access to "test" users found in the "players_db.json" database file.

   LOGGING IN - If you wish to login with one of our two test users, the following is their usernames and passwords:
      Username : test   Password: test
      Username : test2  Password: test2

9. LIMITATIONS
   Current version supports only three gameplay levels with trivial scoring. Loading games requires the user to select the saved game file itself instead of using a UI for more seamless loading.

10. FUTURE ENHANCEMENTS

- Additional levels
- User-friendly game loading
- Upgraded/Enhanced User Interface
- Multiple pre-existing or custom user interface themes

10. TEAM INFORMATION
    Course: CEN 4020 – Software Engineering
    Group: 11

Members:

- Jacob Moran
- Aleksandre Papunashvili
- Apostolos Klimentzos
- Subriti Pradhan