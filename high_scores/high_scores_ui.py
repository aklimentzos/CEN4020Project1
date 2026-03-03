import pygame
import sys
import os
import json
from pathlib import Path
from ui_elements import Button
from ui_elements import TextBox

class HighScoresUI:
    def __init__(self):
        self.board_width = 900
        self.board_height = 700
        self.font = pygame.font.Font(None, 32)
        self.textbox_title = TextBox(310, 50, "High Scores", pygame.font.Font(None, 72))
        self.button_back = Button(335, 600, 210, 40, "Back to Main Menu", self.font)

        self.col_rank = 80
        self.col_username = 150
        self.col_level = 350
        self.col_score = 450
        self.col_date = 550
        self.start_y = 150
        self.row_spacing = 40
        self.score_textboxes = []
        self.load_and_build_list()

    def load_high_scores(self):
        directory = "completed_games"
        scores = []

        if not os.path.exists(directory):
            return []

        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)

                with open(filepath, "r") as f:
                    data = json.load(f)

                    scores.append({
                        "username": data["username"],
                        "level": data["level"],
                        "score": data["score"],
                        "date": data["date"]
                    })

        # obtaining top 10 scores sorted by score in descending order
        scores.sort(key=lambda x: x["score"], reverse=True)

        return scores[:10]
    
    def load_and_build_list(self):
        scores = self.load_high_scores()
        self.score_textboxes.clear()

        # headers to organize columns for high scores
        headers = [
            ("Rank", self.col_rank),
            ("Username", self.col_username),
            ("Level", self.col_level),
            ("Score", self.col_score),
            ("Date", self.col_date),
        ]

        # creating textboxes for headers
        for text, x in headers:
            tb = TextBox(
                x=x,
                y=self.start_y,
                text=text,
                font=self.font,
                active=True
            )
            self.score_textboxes.append(tb)

        # obtaining high score data and creating textboxes for each entry
        for i, entry in enumerate(scores):
            y = self.start_y + (i + 1) * self.row_spacing

            row_data = [
                (str(i + 1), self.col_rank),
                (entry["username"], self.col_username),
                (str(entry["level"]), self.col_level),
                (str(entry["score"]), self.col_score),
                (entry["date"], self.col_date),
            ]

            for text, x in row_data:
                tb = TextBox(
                    x=x,
                    y=y,
                    text=text,
                    font=self.font
                )
                self.score_textboxes.append(tb)

    def display(self):
        pygame.init()

        screen = pygame.display.set_mode((self.board_width, self.board_height))
        pygame.display.set_caption("High Scores")

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.button_back.handle_event(event) == 'clicked':
                    return "back_to_menu"

            screen.fill((240, 240, 240))
            self.textbox_title.draw(screen)
            self.button_back.draw(screen)

            for tb in self.score_textboxes:
                tb.draw(screen)

            pygame.display.flip()
            clock.tick(60)