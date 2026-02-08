import pygame

class InputBox:
    def __init__(self, x, y, w, h, font, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.placeholder = placeholder

        self.text = ""
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return "submit"  # optional signal to caller
            else:
                # Basic character filter:
                # event.unicode is the typed character (respects shift, etc.)
                if event.unicode.isprintable():
                    self.text += event.unicode

        return None

    def update(self, dt_ms):
        # blink cursor when active
        if self.active:
            self.cursor_timer += dt_ms
            if self.cursor_timer >= 500:
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible
        else:
            self.cursor_visible = False
            self.cursor_timer = 0

    def draw(self, screen):
        # box
        border_color = (40, 40, 40) if self.active else (120, 120, 120)
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 2)

        # text (or placeholder)
        if self.text:
            display = self.text
        elif self.active:
            display = ""
        else:
            display = self.placeholder

        text_color = (20, 20, 20) if self.text else (140, 140, 140)

        surf = self.font.render(display, True, text_color)
        text_pos = (self.rect.x + 8, self.rect.y + (self.rect.h - surf.get_height()) // 2)
        screen.blit(surf, text_pos)

        # cursor
        if self.active and self.cursor_visible:
            cursor_x = text_pos[0] + surf.get_width() + 2
            cy1 = self.rect.y + 6
            cy2 = self.rect.y + self.rect.h - 6
            pygame.draw.line(screen, (20, 20, 20), (cursor_x, cy1), (cursor_x, cy2), 2)
    
    # obtains text input from textbox
    @property
    def value(self):
        return self.text
         
           
class Button:
    def __init__(self, x, y, w, h, text, font, callback=None, visible=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False
        self.enabled = True
        self.visible = visible

    def handle_event(self, event):
        if not self.enabled:
            return None

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return "clicked"

        return None

    def set_visible(self, is_visible: bool):
        self.visible = bool(is_visible)

    def draw(self, screen):
        if not self.visible:
            return
        
        if not self.enabled:
            bg = (180, 180, 180)
            fg = (120, 120, 120)
        else:
            bg = (170, 170, 170) if self.hovered else (200, 200, 200)
            fg = (20, 20, 20)

        pygame.draw.rect(screen, bg, self.rect, border_radius=6)
        pygame.draw.rect(screen, (50, 50, 50), self.rect, 2, border_radius=6)

        label = self.font.render(self.text, True, fg)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)
        
        
class TextBox:
    def __init__(self, x, y, text, font, active = True,
                 color_active=(20, 20, 20),
                 color_inactive=(140, 140, 140),
                 visible=True):
        self.x = x
        self.y = y
        self.text = str(text)
        self.font = font
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.active = True
        self.visible = visible

    def set_text(self, new_text):
        self.text = str(new_text)

    def set_active(self, is_active: bool):
        self.active = bool(is_active)

    def set_visible(self, is_visible: bool):
        self.visible = bool(is_visible)

    def draw(self, screen):
        if not self.visible:
            return

        color = self.color_active if self.active else self.color_inactive
        surf = self.font.render(self.text, True, color)
        screen.blit(surf, (self.x, self.y))
        
            
class Grid:
    def __init__(self, grid_size, cell_size, left, top, matrix, font = None,  line_width=2):
        """
        grid_size: N (grid is NxN)
        cell_size: pixel size of a cell
        left, top: pixel position of top-left corner of the grid
        """
        self.grid_size = int(grid_size)
        self.cell_size = int(cell_size)
        self.left = int(left)
        self.top = int(top)
        self.line_width = int(line_width)

        self.matrix = matrix
        self.font = font

    def set_font(self, font):
        """Font used to draw numbers."""
        self.font = font

    def set_matrix(self, matrix):
        """
        matrix: NxN list of ints.
        """
        if not isinstance(matrix, list) or len(matrix) != self.grid_size:
            raise ValueError("Matrix must be NxN and match grid_size.")
        for row in matrix:
            if not isinstance(row, list) or len(row) != self.grid_size:
                raise ValueError("Matrix must be NxN and match grid_size.")
            for cell in row:
                if not isinstance(cell, int):
                    raise ValueError("Matrix values must be integers.")
        self.matrix = matrix

    def board_px(self):
        return self.grid_size * self.cell_size

    def rect(self):
        """Returns the pygame.Rect covering the whole grid."""
        return pygame.Rect(self.left, self.top, self.board_px(), self.board_px())

    def draw(self, screen,
             bg_color=(245, 245, 245),
             line_color=(30, 30, 30),
             text_color=(20, 20, 20),
             draw_bg=False):
        """
        Draw the grid. If draw_bg=True, fills grid area background (not whole screen).
        """
        if draw_bg:
            pygame.draw.rect(screen, bg_color, self.rect())

        board_px = self.board_px()

        # Grid lines
        for c in range(self.grid_size + 1):
            x = self.left + c * self.cell_size
            pygame.draw.line(screen, line_color, (x, self.top), (x, self.top + board_px), self.line_width)

        for r in range(self.grid_size + 1):
            y = self.top + r * self.cell_size
            pygame.draw.line(screen, line_color, (self.left, y), (self.left + board_px, y), self.line_width)

        # Numbers
        if self.font is not None:
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    val = self.matrix[r][c]
                    if val != 0:
                        surf = self.font.render(str(val), True, text_color)
                        center_x = self.left + c * self.cell_size + self.cell_size // 2
                        center_y = self.top + r * self.cell_size + self.cell_size // 2
                        rect = surf.get_rect(center=(center_x, center_y))
                        screen.blit(surf, rect)

    def cell_from_pos(self, pos):
        """
        pos: (mx, my)
        Returns (row, col) if inside grid, else None.
        """
        mx, my = pos
        if not self.rect().collidepoint(mx, my):
            return None

        col = (mx - self.left) // self.cell_size
        row = (my - self.top) // self.cell_size

        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return int(row), int(col)
        return None

    def handle_event(self, event):
        """
        Convenience: call this from your event loop.
        Returns (row, col) on left click, else None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.cell_from_pos(event.pos)
        return None

