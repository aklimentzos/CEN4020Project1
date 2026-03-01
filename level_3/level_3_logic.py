from level_2.level_2_logic import Level2State
from pathlib import Path
import json
import os
import datetime


class Level3State:
    """Class running the logic for Level 3 of the game"""

    def __init__(self, level2_state: Level2State):
        # 7x7 grid
        self.matrix = [[0 for _ in range(7)] for _ in range(7)]

        # Bring over ring numbers, wipe inner except '1'
        self._import_outer_and_reset_inner(level2_state)

        # Stack used for "undo": each entry = [row, col, scored_flag]
        self.move_stack = []

        # Next number to place and cumulative score
        self.cur_num = 2
        self.score = level2_state.score

        # Used to exit the game / display messages
        self.check = "Pass"
        self.fail_reason = ""

        # Track last placed number coords (starts at the location of 1 if present)
        self.last_coords = self._find_one_coords()  # [r,c] or [-1,-1]

    def _import_outer_and_reset_inner(self, level2_state: Level2State):
        """
        Copies the entire 7x7 from level2_state, then wipes inner 5x5 (1..5, 1..5)
        to 0 except keeping whatever cell contains 1.
        """
        # Copy everything first (keeps ring as-is)
        for r in range(7):
            for c in range(7):
                self.matrix[r][c] = level2_state.matrix[r][c]

        # Wipe inner except 1
        for r in range(1, 6):
            for c in range(1, 6):
                if self.matrix[r][c] != 1:
                    self.matrix[r][c] = 0

    def _find_one_coords(self):
        """Finds the position of the number 1 in the inner board; if not found returns [-1,-1]."""
        for r in range(1, 6):
            for c in range(1, 6):
                if self.matrix[r][c] == 1:
                    return [r, c]
        return [-1, -1]


class Level3Controller:
    def __init__(self, state: Level3State):
        self.state = state
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
        self.err_msg = ""

    def get_grid_number(self, x, y):
        return self.state.matrix[x][y]

    def get_cur_num(self):
        return int(self.state.cur_num)

    def get_matrix(self):
        return self.state.matrix

    def get_fail(self):
        return self.state.fail_reason

    def get_score(self):
        return self.state.score

    # ---------------------------
    # Level 3 rule helpers
    # ---------------------------

    def _is_inner_cell(self, r, c):
        return 1 <= r <= 5 and 1 <= c <= 5

    def _is_adjacent_to_last(self, r, c):
        """
        must be adjacent to the previous number.
        We treat adjacency as 8-neighborhood.
        """
        lr, lc = self.state.last_coords
        if lr == -1 or lc == -1:
            # No known last position (means 1 wasn't found). In that case, can't validate adjacency.
            return False
        dr = abs(r - lr)
        dc = abs(c - lc)
        return (dr <= 1 and dc <= 1) and not (dr == 0 and dc == 0)

    def _is_diagonal_from_last(self, r, c):
        """
        score +1 if diagonally adjacent to the previous.
        """
        lr, lc = self.state.last_coords
        if lr == -1 or lc == -1:
            return False
        return abs(r - lr) == 1 and abs(c - lc) == 1

    def _ring_endpoints_contain_cur_num(self, r, c):
        """
        placement cell must be intersection of a row and column
        with the current number printed in either end of the row or column.
        Interpreted as: cur_num is at (r,0) or (r,6) or (0,c) or (6,c).
        """
        n = self.state.cur_num
        return (
            self.state.matrix[r][0] == n or
            self.state.matrix[r][6] == n or
            self.state.matrix[0][c] == n or
            self.state.matrix[6][c] == n
        )

    def _cur_num_is_on_corner(self):
        """
        number is printed on a yellow ring corner cell.
        Corners: (0,0), (0,6), (6,0), (6,6)
        """
        n = self.state.cur_num
        corners = [(0, 0), (0, 6), (6, 0), (6, 6)]
        return any(self.state.matrix[r][c] == n for r, c in corners)

    def _is_on_long_diagonal(self, r, c):
        """
        if cur_num is in a corner, placement must be on one of the two longest diagonals.
        For 7x7 diagonals: r==c or r+c==6
        """
        return (r == c) or (r + c == 6)

    # ---------------------------
    # Core logic
    # ---------------------------

    def is_valid_move(self, coords):
        """
        Level 3 validity checks
        - must place in inner cells
        - must be adjacent to previous number
        - must satisfy ring endpoint intersection rule
        - if cur_num is in a ring corner, must be on long diagonal
        """
        r, c = coords

        # only inner cells
        if not self._is_inner_cell(r, c):
            self.state.fail_reason = "Invalid Move, must place inside the 5x5 inner board"
            return False

        # must be empty
        if self.state.matrix[r][c] != 0:
            self.state.fail_reason = "Invalid Move, cell occupied"
            return False

        # adjacent to previous
        if not self._is_adjacent_to_last(r, c):
            self.state.fail_reason = "Invalid Move, must be adjacent to previous number"
            return False

        
        # row/col endpoints must include cur_num
        if not self._ring_endpoints_contain_cur_num(r, c) and not self._cur_num_is_on_corner():
            self.state.fail_reason = "Invalid Move, row/column endpoints don't match current number"
            return False
        
        # if cur_num printed in a corner, must place on long diagonal
        if self._cur_num_is_on_corner() and not self._is_on_long_diagonal(r, c):
            self.state.fail_reason = "Invalid Move, corner-number must be placed on a main diagonal"
            return False

        self.state.fail_reason = ""
        return True

    def update_matrix(self, coords):
        r, c = coords
        self.state.matrix[r][c] = self.state.cur_num
        self.state.last_coords = [r, c]
        self.state.cur_num += 1

    def update_score(self, placed_coords):
        """
        +1 if placed diagonally from previous.
        """
        r, c = placed_coords
        scored = 1 if self._is_diagonal_from_last(r, c) else 0
        if scored:
            self.state.score += 1
        # record scored flag into last move stack entry
        self.state.move_stack[-1][2] = scored

    def make_move(self, user_input):
        coords = [int(user_input[0]), int(user_input[1])]

        # Save old last_coords so scoring can compare against the previous number
        prev_last = self.state.last_coords.copy()

        if not self.is_valid_move(coords):
            return False

        # push move with placeholder scored flag
        self.state.move_stack.append([coords[0], coords[1], 0])

        # scoring based on prev_last
        self.state.last_coords = prev_last
        self.update_score(coords)

        # now place number and advance cur_num + last_coords
        self.update_matrix(coords)
        return True

    def undo(self):
        """
        rollback from most recent.
        Restores:
        - cell to 0
        - cur_num decremented
        - score decremented only if that move scored
        - last_coords becomes previous move position, or the position of 1 if no moves left
        """
        if self.state.cur_num == 2:
            return False  # nothing placed yet in level 3

        last_move = self.state.move_stack.pop()
        r, c, scored_flag = last_move

        # remove the placed number
        self.state.matrix[r][c] = 0

        # revert score if that move scored
        if scored_flag == 1:
            self.state.score -= 1

        # revert cur_num
        self.state.cur_num -= 1

        # restore last_coords
        if self.state.move_stack:
            pr, pc, _ = self.state.move_stack[-1]
            self.state.last_coords = [pr, pc]
        else:
            # back to '1' position
            self.state.last_coords = self.state._find_one_coords()

        return True

    def clear_board(self):
        while self.undo():
            pass

    # ---------------------------
    # Save / Load (same style as Level 2)
    # ---------------------------

    def load_game(self, path):
        required_keys = {"level", "matrix", "cur_num", "score", "last_coords", "move_stack"}
        p = Path(str(path))

        if not p.is_file() or p.suffix.lower() != ".json":
            self.err_msg = "Not a valid save file."
            return None

        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            self.err_msg = "Save file is not valid JSON."
            return None

        if not isinstance(data, dict) or not required_keys.issubset(data.keys()):
            self.err_msg = "Save file does not match expected schema."
            return None

        save_level = data["level"]
        self.state.matrix = data["matrix"]
        self.state.cur_num = data["cur_num"]
        self.state.score = data["score"]
        self.state.last_coords = data["last_coords"]
        self.state.move_stack = data["move_stack"]
        return save_level

    def save_game(self, path):
        dump = {
            "level": 3,
            "matrix": self.state.matrix,
            "cur_num": self.state.cur_num,
            "score": self.state.score,
            "last_coords": self.state.last_coords,
            "move_stack": self.state.move_stack,
        }
        with open(str(path), "w", encoding="utf-8") as f:
            json.dump(dump, f)

    def save_completed_game(self, username, score, matrix):
        save_complete_path = self.base_dir / "completed_games" / f"{username}_level3_completed.json"
        completed_data = {
            "username": username,
            "level": 3,
            "score": score,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "matrix": matrix,
        }
        with open(str(save_complete_path), "w", encoding="utf-8") as f:
            json.dump(completed_data, f)