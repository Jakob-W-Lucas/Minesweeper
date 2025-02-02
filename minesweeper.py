"""
A simple minesweeper game

Author: Jakob Lucas
"""

import pygame # type: ignore
import math
import random

pygame.init()

# Size of the grid (length * width)
grid_size = 15
# Size of each cell
cell_size = 8
# Scale size for each game pixel
pixel_size = 10
# Length and width for each cell
cell_lw = cell_size * pixel_size
# Size of lines separating cells
line_size = 2 

# Screen size and creation
SCREEN_WIDTH = (15 * cell_lw) + (grid_size + 1) * line_size
SCREEN_HEIGHT = SCREEN_WIDTH

# Colors:
CRT_WHITE = (213, 224, 216)       # White
CRT_GREY  = (139, 143, 140)       # Grey
CRT_BLACK = (24, 14, 26)          # CRT Black
BLACK = (0, 0, 0)

# Display the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Minesweeper')

# Load the sprite sheet
sprite_sheet_image = pygame.image.load('minesweeper_sprites.png').convert_alpha()

# Get the individual images from the sprite sheet
def get_image(sheet, frame_x, frame_y, width, height, scale, color):
    
    # Create a base square to place sprite image on top of
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame_x * width), (frame_y * height), width, height))
    
    # Transform the image
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    
    return image

# Images:
s_CELL = get_image(sprite_sheet_image, 0, 1, 8, 8, pixel_size, BLACK)
s_MINE = get_image(sprite_sheet_image, 1, 1, 8, 8, pixel_size, BLACK)

# All the current cells in the grid
cells = []

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = s_CELL
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.mine = False
        self.surrounding_mines = 0
        
    def clicked(self):
        
        if self.mine and self.surrounding_mines == 0:
            self.image = pygame.Surface((cell_lw, cell_lw))
            self.image.fill(CRT_BLACK)
        elif self.mine:
            self.image = s_MINE
        else:
            self.image = get_image(sprite_sheet_image, self.surrounding_mines - 1, 0, 8, 8, pixel_size, BLACK)
    
    def reveal_cell(self):
        pass

# Draws the minesweeper grid
def draw_grid():
    # Draw each line in the grid
    for i in range(grid_size + 1):
        # Size encompassing 1 cell 
        square = i * (cell_lw + line_size)
        
        # Each horizontal and vertical line in the grid
        pygame.draw.line(screen, CRT_GREY, (0, square), (SCREEN_WIDTH, square), line_size)
        pygame.draw.line(screen, CRT_GREY, (square, 0), (square, SCREEN_HEIGHT), line_size)

def create_cells():
    # Create each sprite in the grid
    for i in range(grid_size):
        
        row = pygame.sprite.Group()
        
        y = cell_lw * (i + 0.5) + line_size * (i + 1)
        
        for j in range(grid_size):
            
            x = cell_lw * (j + 0.5) + line_size * (j + 1)
            # Create the cell and add it to the row
            cell = Cell(x, y)
            cell.surrounding_mines = random.randint(0, 8)
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
        
    # Create the screen background
    screen.fill(CRT_BLACK)
    
    # Display Grid
    draw_grid()
    
    for row in cells:
        # Update each cell in the grid
        row.update()
        # Draw each cell sprite in the grid
        row.draw(screen)
    
    # Get key presses
    key = pygame.key.get_pressed()
    
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
    