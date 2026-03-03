import pygame
import sys
from ui_elements import InputBox
from ui_elements import Button
from ui_elements import TextBox
from authentication.database_manager import DatabaseManager

class AuthUI:
    def __init__(self):
        pygame.init()
        self.width = 400
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Authentication")
        self.font = pygame.font.Font(None, 32)
        self.db = DatabaseManager()

        # UI Elements
        self.title = TextBox(100, 50, "Game Login", pygame.font.Font(None, 48))
        
        self.label_user = TextBox(50, 110, "Username:", self.font)
        self.input_user = InputBox(180, 105, 170, 35, self.font, placeholder="Username")
        
        self.label_pass = TextBox(50, 160, "Password:", self.font)
        self.input_pass = InputBox(180, 155, 170, 35, self.font, placeholder="Password", is_password=True)
        
        self.btn_login = Button(50, 230, 140, 40, "Login", self.font)
        self.btn_register = Button(210, 230, 140, 40, "Register", self.font)
        
        self.status_msg = TextBox(50, 300, "", self.font, visible=False)

    def display(self):
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60)
            self.screen.fill((240, 240, 240))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                self.input_user.handle_event(event)
                self.input_pass.handle_event(event)
                
                if self.btn_login.handle_event(event) == "clicked":
                    username = self.input_user.value
                    password = self.input_pass.value
                    if self.db.authenticate(username, password):
                        return username
                    else:
                        self.status_msg.set_text("Invalid credentials!")
                        self.status_msg.set_visible(True)
                        self.status_msg.color_active = (200, 0, 0)
                
                if self.btn_register.handle_event(event) == "clicked":
                    username = self.input_user.value
                    password = self.input_pass.value
                    if not username or not password:
                        self.status_msg.set_text("Fields cannot be empty!")
                        self.status_msg.set_visible(True)
                        self.status_msg.color_active = (200, 0, 0)
                    else:
                        success, message = self.db.register(username, password)
                        self.status_msg.set_text(message)
                        self.status_msg.set_visible(True)
                        if success:
                            self.status_msg.color_active = (0, 150, 0)
                        else:
                            self.status_msg.color_active = (200, 0, 0)

            # Update
            self.input_user.update(dt)
            self.input_pass.update(dt)
            
            # Draw
            self.title.draw(self.screen)
            self.label_user.draw(self.screen)
            self.input_user.draw(self.screen)
            self.label_pass.draw(self.screen)
            self.input_pass.draw(self.screen)
            self.btn_login.draw(self.screen)
            self.btn_register.draw(self.screen)
            self.status_msg.draw(self.screen)
            
            pygame.display.flip()