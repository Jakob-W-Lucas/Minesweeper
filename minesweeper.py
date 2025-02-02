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
line_size = 2 
cell_lw = cell_size * pixel_size

# Screen size and creation
SCREEN_WIDTH = (15 * cell_lw) + (grid_size + 1) * line_size
SCREEN_HEIGHT = SCREEN_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Cell():
    def __init__(self):
        self.mine = False
        self.surrounding_mines = 0
    
    def reveal_cell(self):
        pass

# Draws the minesweeper grid
def draw_grid():
    for i in range(grid_size + 1):
        pygame.draw.line(screen, pygame.Color(213, 224, 216), (0, i * (cell_lw + line_size)), (SCREEN_WIDTH, i * (cell_lw + line_size)), line_size)
        pygame.draw.line(screen, pygame.Color(213, 224, 216), (i * (cell_lw + line_size), 0), (i * (cell_lw + line_size), SCREEN_HEIGHT), line_size)

# Returns the cell based on coords from the screen
def get_cell(x: int, y: int) -> tuple[int, int]:
    
    cell_x = x // (cell_lw + line_size)
    cell_y = y // (cell_lw + line_size)
    
    return [cell_x, cell_y]

cells = []

def create_cells():
    for _ in range(grid_size):
        row = []
        for _ in range(grid_size):
            row.append(Cell())
        cells.append(row)

run = True
# Game loop
while run:
    
    if len(cells) == 0:
        create_cells()
        
    # Create the screen and get the key presses
    screen.fill((24, 14, 26))
    key = pygame.key.get_pressed()
    
    draw_grid()
    
    # Exit
    if key[pygame.K_ESCAPE]:
       run = False
       
    # Quit game
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(get_cell(pos[0], pos[1]))
      
        if event.type == pygame.QUIT:
            run = False
    
    # Update the game display
    pygame.display.update()

pygame.quit()
    