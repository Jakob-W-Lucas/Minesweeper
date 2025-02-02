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

# Colors:
c_white = pygame.Color(213, 224, 216)       # White
c_grey  = pygame.Color(139, 143, 140)       # Grey
c_black = pygame.Color(24, 14, 26)          # Black

# All the current cells in the grid
cells = []

class Cell(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((cell_lw, cell_lw))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.mine = False
        self.surrounding_mines = 0
        
    def clicked(self):
        self.image.fill(c_black)
    
    def reveal_cell(self):
        pass

# Draws the minesweeper grid
def draw_grid():
    # Draw each line in the grid
    for i in range(grid_size + 1):
        # Size encompassing 1 cell 
        square = i * (cell_lw + line_size)
        
        # Each horizontal and vertical line in the grid
        pygame.draw.line(screen, c_grey, (0, square), (SCREEN_WIDTH, square), line_size)
        pygame.draw.line(screen, c_grey, (square, 0), (square, SCREEN_HEIGHT), line_size)

def create_cells():
    # Create each sprite in the grid
    for i in range(grid_size):
        
        row = pygame.sprite.Group()
        
        y = cell_lw * (i + 0.5) + line_size * (i + 1)
        
        for j in range(grid_size):
            
            x = cell_lw * (j + 0.5) + line_size * (j + 1)
            # Create the cell and add it to the row
            cell = Cell(c_white, x, y)
            row.add(cell)
            
        cells.append(row)

# Returns the cell based on coords from the screen
def get_cell(x: int, y: int) -> tuple[int, int]:
    
    # Calculate which cell has been clicked
    cell_x = x // (cell_lw + line_size)
    cell_y = y // (cell_lw + line_size)
    
    return [cell_x, cell_y]

run = True
# Game loop
while run:
    
    if len(cells) == 0:
        create_cells()
        
    # Create the screen and get the key presses
    screen.fill(c_black)
    key = pygame.key.get_pressed()
    
    draw_grid()
    
    for row in cells:
        # Update each cell in the grid
        row.update()
        # Draw each cell sprite in the grid
        row.draw(screen)
            
    # Exit
    if key[pygame.K_ESCAPE]:
       run = False
       
    # Quit game
    for event in pygame.event.get():
        # Call which cell was clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            r, c = get_cell(pos[0], pos[1])
            cells[c].sprites()[r].clicked()
      
        if event.type == pygame.QUIT:
            run = False
    
    # Update the game display
    pygame.display.update()

pygame.quit()
    