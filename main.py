from level_1.level_1_logic import Level1State
from level_1.level_1_logic import Level1Controller
import pygame
import sys
from level_1.level_1_ui import Level1UI

def main():
    pygame.init()
    
    myui = Level1UI()
    myui.display()

if __name__ == "__main__":
    main()