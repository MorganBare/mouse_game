
import sys

import pygame

from settings import Settings
from cat import Cat
from cheese import Cheese 
from mouse import Mouse

class MouseGame:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height 
        pygame.display.set_caption("Macka Mouse Game")

        self.cat = Cat(self)
        self.cheeses = pygame.sprite.Group() 
        self.mice = pygame.sprite.Group()

        self._create_pack()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.cat.update()
            self._update_cheese()
            self._update_screen()

    def _check_events(self):
        # Responds to keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = True
        if event.key == pygame.K_UP:
            self.cat.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.cat.moving_down = True
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_cheese_()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = False
        if event.key == pygame.K_UP:
            self.cat.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.cat.moving_down = False

    def _fire_cheese_(self):
        """Create a new cheese and add it to the cheese group"""
        if len(self.cheeses) < self.settings.cheese_allowed:
            new_cheese = Cheese(self)
            self.cheeses.add(new_cheese)

    def _create_pack(self):
        """Create a pack of mice"""
        #Create a mouse and find the number of mice in a row
        #Spacing between each mouse is equal to one mouse width
        mouse = Mouse(self)
        mouse_width, mouse_height = mouse.rect.size 
        available_space_x = self.settings.screen_width - (2* mouse_width)
        number_mice_x = available_space_x // (2 * mouse_width)

        # Determine the number of mice that can fit on the screen
        cat_height = self.cat.rect.height 
        available_space_y = (self.settings.screen_height - (3 * mouse_height) - cat_height)
        number_rows = available_space_y // (4 * mouse_height)

        # Create the full pack of mice
        for row_number in range(number_rows):
            for mouse_number in range(number_mice_x):
                self._create_mouse(mouse_number, row_number)

    def _create_mouse(self, mouse_number, row_number):
        """Create a mouse and put it in the row"""
        mouse = Mouse(self)
        mouse_width, mouse_height = mouse.rect.size 
        mouse.x = mouse_width + 2 * mouse_width * mouse_number
        mouse.rect.x = mouse.x
        mouse.rect.y = mouse.rect.height + 2 * mouse.rect.height * row_number 
        self.mice.add(mouse)

    def _update_cheese(self):
        """Update the position of the cheese and get rid of old cheese"""
        # Update cheese positions
        self.cheeses.update()

        # Get rid of old cheese
        for cheese in self.cheeses.copy():
            if cheese.rect.bottom <= 0:
                self.cheeses.remove(cheese)

    
    def _update_screen(self):
         # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.cat.blitme()
        for cheese in self.cheeses.sprites():
            cheese.blt_cheese()
        self.mice.draw(self.screen)
        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    mg = MouseGame()
    mg.run_game()