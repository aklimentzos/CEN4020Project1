Project 1 – 5x5 Number Placement Game System

ABSTRACT
This document presents the 5x5 Number Placement Game System, a GUI-based puzzle game developed for CEN 4020.
The system supports multi-level gameplay, sound feedback, undo functionality, and persistent game logging.

1. INTRODUCTION
   The 5x5 Number Placement Game System expands an initial prototype into a
   fully interactive graphical application following agile development practices.

   The system now includes three progressive gameplay levels, each introducing new rules
   and challenges while maintaining consistent scoring and usability features.
   
2. SYSTEM OVERVIEW
   The game allows players to place sequential numbers into a 5x5 grid and expanded boards across multiple levels:
      Level 1: Core 5x5 number placement gameplay
      Level 2: Expanded 7x7 board with an outer ring and directional placement rules
      Level 3: Final challenge level using outer-ring constraints and adjacency-based placement rules
   The system enforces placement rules, provides real-time feedback, and automatically progresses players to the 
   next level upon completion.

   Scores accumulate across all levels, allowing players to track overall performance throughout the full game experience.
3. FUNCTIONAL REQUIREMENTS

   -Graphical board interaction
   -Automatic next-number generation
   -Sound feedback for valid and invalid actions
   -Undo and reset features
   -Game completion logging
   -Multi-level gameplay progression (Levels 1 to 3)
   -Persistent save and load functionality across levels
   -Cumulative scoring system:
      +1 point for each successful number placement
      -1 point for each undo or rollback action
      Score carries across all levels

4. NON-FUNCTIONAL REQUIREMENTS

- User-friendly interface
- Responsive system behavior
- Data persistence
-Consistent gameplay experience across levels

5. SYSTEM REQUIREMENTS
   Operating System: Windows
   Languages: Python
   Tools: VS Code, PyGame
6. FILE STRUCTURE

Proj1/

   ├── main.py

   ├── main.spec

   ├── sprint1_checklist.xlsx

   ├── Sprint1Demonstration.mp4

   ├── ui_elements.py

   └── ReadMe.txt

   _internal/
      
      └── Various files for executable to run (PyInstaller provided)

   level_1/

      ├── level_1_logic.py

      └──level_1_ui.py
   level_2/

      ├── level_2_logic.py

      └──level_2_ui.py
   level_3/

      ├── level_3_logic.py

      └──level_3_ui.py
   assets/
      ├── invalid_move_sound.mp3

      └──successful_move_sound.mp3
   completed_games/
      ├── test_level1_completed.json

      └──test_level2_completed.json
   saves/
      ├── test_level1_save.json

      └──test_level2_save.json

8. EXECUTION INSTRUCTIONS
   Run the executable file or compile and run source code using the appropriate language commands (ex. python main.py [when in Proj1 directory]).

9. LIMITATIONS
   Current version supports two gameplay levels with basic scoring.

10. FUTURE ENHANCEMENTS

- Leaderboard integration
- Time-based scoring
- Enhanced user interface themes

11. TEAM INFORMATION
    Course: CEN 4020 – Software Engineering
    Group: 11

Members:

- Jacob Moran
- Aleksandre Papunashvili
- Apostolos Klimentzos
- Subriti Pradhan