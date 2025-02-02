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
cell_lw = cell_size * pixel_size

# Screen size and creation
SCREEN_WIDTH = (15 * cell_size * pixel_size) + (grid_size + 1) * pixel_size
SCREEN_HEIGHT = SCREEN_WIDTH

print(f"Width {SCREEN_WIDTH}, height: {SCREEN_HEIGHT}")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True

def create_screen():
    
    for i in range(grid_size + 1):
        
        pygame.draw.line(screen, pygame.Color(213, 224, 216), (0, i * cell_lw), (SCREEN_WIDTH, i * cell_lw), pixel_size)
        pygame.draw.line(screen, pygame.Color(213, 224, 216), (i * cell_lw, 0), (i * cell_lw, SCREEN_HEIGHT), pixel_size)

# Game loop
while run:
    
    # Create the screen and get the key presses
    screen.fill((24, 14, 26))
    key = pygame.key.get_pressed()
    create_screen()
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
    