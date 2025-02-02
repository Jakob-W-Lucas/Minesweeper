"""
A simple minesweeper game

Author: Jakob Lucas
"""

import pygame # type: ignore
import math
import random

pygame.init()

grid_size = 15
cell_size = 6
pixel_size = 10

# Screen size and creation
SCREEN_WIDTH = 15 * cell_size * pixel_size
SCREEN_HEIGHT = SCREEN_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True

# Game loop
while run:
    
    # Create the screen and get the key presses
    screen.fill((24, 14, 26))
    key = pygame.key.get_pressed()
    
    # Exit
    if key[pygame.K_ESCAPE]:
       run = False
       
    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Update the game display
    pygame.display.update()

pygame.quit()
    