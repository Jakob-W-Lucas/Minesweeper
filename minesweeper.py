"""
A simple minesweeper game

Author: Jakob Lucas
"""

import pygame # type: ignore
import math
import random

pygame.init()

# Size of the grid
grid_size = [18, 15]
# Percentage of mines in the grid
mine_density = 0.14
# Size of each cell
cell_size = 8
# Scale size for each game pixel
pixel_size = 10
# Length and width for each cell
cell_lw = cell_size * pixel_size
# Size of lines separating cells
line_size = 2 

# Screen size and creation
SCREEN_WIDTH = (grid_size[0] * cell_lw) + (grid_size[0] + 1) * line_size
SCREEN_HEIGHT = (grid_size[1] * cell_lw) + (grid_size[1] + 1) * line_size

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
s_FLAG = get_image(sprite_sheet_image, 1, 1, 8, 8, pixel_size, BLACK)
s_MINE = get_image(sprite_sheet_image, 2, 1, 8, 8, pixel_size, BLACK)

# All the current cells in the grid
cells = []

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, location: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = s_CELL
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.column, self.row = location
        
        self.is_mine = False
        self.surrounding_mines = 0
        
        self.mined = False
        
    def left_clicked(self):
        
        self.mined = True
         
        if not self.is_mine and self.surrounding_mines == 0:
            
            self.image = pygame.Surface((cell_lw, cell_lw))
            self.image.fill(CRT_BLACK)
        elif self.is_mine:
            self.image = s_MINE
            # Game over
        else:
            self.image = get_image(sprite_sheet_image, self.surrounding_mines - 1, 0, 8, 8, pixel_size, BLACK)
            print(f"surrounding mines: {self.surrounding_mines}")
    
    def right_clicked(self):
        
        if self.mined == True:
            return
        
        self.image = s_FLAG

# Draws the minesweeper grid
def draw_grid():
    
    # Size encompassing 1 cell 
    square = cell_lw + line_size
    
    # Draw each line in the grid
    for i in range(grid_size[0] + 1):
        # Each vertical line in the grid
        pygame.draw.line(screen, CRT_GREY, (square * i, 0), (square * i, SCREEN_HEIGHT), line_size)
    
    for i in range(grid_size[1] + 1):
        # Each horizontal line in the grid
        pygame.draw.line(screen, CRT_GREY, (0, square * i), (SCREEN_WIDTH, square * i), line_size)

def increment_surrounding_cells(c: int, r: int):
    # Increase the surrounding mines for each cell
    for column in range(-1, 2):
        for row in range(-1, 2):
            if c + column < 0 or r + row < 0 or\
                c + column > grid_size[1] - 1 or r + row > grid_size[0] - 1:
                continue
            cells[c + column].sprites()[r + row].surrounding_mines += 1
            
            print(f"Cell incrementing: {c}, {r}. Incrementing {c + column}, {r + row}")

mine_count = math.floor(mine_density * grid_size[0] * grid_size[1])

def get_randomized_cells() -> tuple[Cell]:
    random_cells = []
    for i in range(grid_size[1]):
        for j in range(grid_size[0]):
            random_cells.append(cells[i].sprites()[j])
    random.shuffle(random_cells)
    
    return random_cells

def generate_grid():
    # Spawn mines and update cells
    random_cells = get_randomized_cells()
    current_mine_count = mine_count
    
    while current_mine_count > 0:
        cell = random_cells.pop()
        
        cell.is_mine = True
        increment_surrounding_cells(cell.column, cell.row)
        
        current_mine_count -= 1
        

def initialise_cells():
    # Create each sprite in the grid
    for i in range(grid_size[1]):
        
        row = pygame.sprite.Group()
        
        y = cell_lw * (i + 0.5) + line_size * (i + 1)
        
        for j in range(grid_size[0]):
            
            x = cell_lw * (j + 0.5) + line_size * (j + 1)
            # Create the cell and add it to the row
            cell = Cell(x, y, (i, j))
            row.add(cell)
            
        cells.append(row)
    
    generate_grid()

# Returns the cell based on coords from the screen
def get_cell(x: int, y: int) -> tuple[int, int]:
    
    # Calculate which cell has been clicked
    cell_x = x // (cell_lw + line_size)
    cell_y = y // (cell_lw + line_size)
    
    return [cell_x, cell_y]

# Mouse buttons
m_LEFT = 1
m_RIGHT = 3

run = True
# Game loop
while run:
    
    if len(cells) == 0:
        initialise_cells()
        
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
            
            if r > grid_size[0] - 1 or c > grid_size[1] - 1 or\
                r < 0 or c < 0:
                continue
            
            cell = cells[c].sprites()[r]
            
            if event.button == m_LEFT:
                cell.left_clicked()
            elif event.button == m_RIGHT:
                cell.right_clicked()
      
        if event.type == pygame.QUIT:
            run = False
    
    # Update the game display
    pygame.display.update()

pygame.quit()
    