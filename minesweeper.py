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
# Remaining mines in the grid
total_mines = math.floor(mine_density * grid_size[0] * grid_size[1])

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

# Load the sprite sheets
sprite_sheet_image = pygame.image.load('minesweeper_sprites.png').convert_alpha()
game_over_image = pygame.image.load('game_over_sprite.png').convert_alpha()
restart_image = pygame.image.load('restart_sprite.png').convert_alpha()
win_image = pygame.image.load('win_sprite.png').convert_alpha()

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
s_CELL = get_image(sprite_sheet_image, 10, 0, 8, 8, pixel_size, BLACK)
s_FLAG = get_image(sprite_sheet_image, 11, 0, 8, 8, pixel_size, BLACK)
s_MINE = get_image(sprite_sheet_image, 12, 0, 8, 8, pixel_size, BLACK)
s_GAMEOVER = get_image(game_over_image, 0, 0, 31, 19, pixel_size, BLACK)
s_RESTART = get_image(restart_image, 0, 0, 19, 19, pixel_size, BLACK)
s_WIN = get_image(win_image, 0, 0, 32, 19, pixel_size, BLACK)

# Positions of images
go_h = game_over_image.get_height() * pixel_size
go_w = game_over_image.get_width() * pixel_size

win_h = win_image.get_height() * pixel_size
win_w = win_image.get_width() * pixel_size

rs_h = restart_image.get_height() * pixel_size
rs_w = restart_image.get_width() * pixel_size

# Draw image in the centre of the screen
game_over_image_pos = [(SCREEN_WIDTH - go_w - rs_w) // 2, (SCREEN_HEIGHT - go_h) // 2]
win_image_pos = [(SCREEN_WIDTH - win_w - rs_w) // 2, (SCREEN_HEIGHT - win_h) // 2]
restart_image_pos = [(SCREEN_WIDTH - rs_w + go_w) // 2, (SCREEN_HEIGHT - rs_h) // 2]

# Cell class
class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, location: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = s_CELL
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # location of the cell on the grid
        self.location = location
        
        self.is_mine = False
        self.surrounding_mines = 0
        
        # If the cell has been mined or flagged
        self.mined = False
        self.flagged = False
        
        # Get a random flower for the cell to become if it is a mine
        self.rand_flower = get_image(sprite_sheet_image, random.randint(13, 15), 0, 8, 8, pixel_size, BLACK)
    
    # Mine the cell
    def mine_cell(self, win: bool = False):
        
        self.mined = True
         
        # Clear cell
        if not self.is_mine and self.surrounding_mines == 0:
            self.image = pygame.Surface((cell_lw, cell_lw))
            self.image.fill(CRT_BLACK)
        # Win condition
        elif self.is_mine and win:
            # Turn the mine into a random flower
            self.image = self.rand_flower
        # Mine cell
        elif self.is_mine:
            self.image = s_MINE
        # Number cell
        else:
            # Get the appropriate number from the image
            self.image = get_image(sprite_sheet_image, self.surrounding_mines - 1, 0, 8, 8, pixel_size, BLACK)
    
    # Flag a cell
    def flag_cell(self):
        
        if self.mined:
            return
        
        # Switch between a flag and a cell
        if self.flagged:
            self.image = s_CELL
        else:
            self.image = s_FLAG
        
        self.flagged = not self.flagged
        
class Game():
    
    # Create a new game
    def __init__(self):
        # Create the cells array
        self.cells = []
        self.initialise_cells()
        
        self.game_over = False
        
        # Calculate the total cells to mine to win the game
        self.total_cells_to_mine = grid_size[0] * grid_size[1] - total_mines
        
    def initialise_cells(self):
        
        # Reset cells
        self.cells.clear()
        
        # Create each cell sprite in the grid
        for i in range(grid_size[1]):
            
            row = pygame.sprite.Group()
            y = cell_lw * (i + 0.5) + line_size * (i + 1)
            
            for j in range(grid_size[0]):
                
                x = cell_lw * (j + 0.5) + line_size * (j + 1)
                # Create the cell and add it to the row
                cell = Cell(x, y, (i, j))
                row.add(cell)
                
            self.cells.append(row)

    # Mine a cell and determine the outcome
    def mine_cells(self, mouse_pos: tuple):
        
        cell = self.get_cell(mouse_pos)
        
        if not cell:
            return
        
        if cell.mined:
            return
        
        cell.mine_cell()
        
        if cell.is_mine:
            self.game_over = True
            return
        
        # All surrounding clear cells are also cleared
        if cell.surrounding_mines == 0:
            self.total_cells_to_mine -= self.clear_cells(cell.location)
            
        self.total_cells_to_mine -= 1
    
    def flag_cells(self, mouse_pos: tuple):
        
        cell = self.get_cell(mouse_pos)
        
        if not cell:
            return
            
        cell.flag_cell()
    
    # Return the cells with a distance of 1 cell in every direction
    def get_surrounding_cells(self, centre: tuple) -> tuple[Cell]:
        
        c_centre, r_centre = centre
        
        surrounding_cells = []
        
        for column in range(-1, 2):
            for row in range(-1, 2):
                if c_centre + column < 0 or r_centre + row < 0 or\
                    c_centre + column > grid_size[1] - 1 or r_centre + row > grid_size[0] - 1:
                    continue
                
                surrounding_cells.append(self.cells[c_centre + column].sprites()[r_centre + row])
                
        return surrounding_cells

    # Increase the surrounding mines for each cell
    def increment_surrounding_cells(self, location: tuple):
        
        s_cells = self.get_surrounding_cells(location)
        for cell in s_cells:
            cell.surrounding_mines += 1

    # Get random positions on the grid for each mine
    def get_randomized_cells(self, first_cell_location: tuple) -> tuple[Cell]:
        
        # Get the cells surrounding the first click
        first_cells = self.get_surrounding_cells(first_cell_location)
        
        random_cells = []
        for i in range(grid_size[1]):
            for j in range(grid_size[0]):
                random_cells.append(self.cells[i].sprites()[j])
        
        # Remove the first cells from the list to ensure no mines
        random_cells = [x for x in random_cells if x not in first_cells]
        random.shuffle(random_cells)
        
        return random_cells

    # Place each mine in the grid and update the cells
    def generate_grid(self, first_click: tuple):
        
        # Spawn mines and update cells
        first_cell_location = self.get_cell(first_click).location
        random_cells = self.get_randomized_cells(first_cell_location)
        current_mine_count = total_mines
        
        # Get random positions until each mine has been placed
        while current_mine_count > 0:
            cell = random_cells.pop()
            
            cell.is_mine = True
            self.increment_surrounding_cells(cell.location)
            
            current_mine_count -= 1

    # Returns the cell based on coords from the screen
    def get_cell(self, pos: tuple) -> Cell:
        
        # Calculate which cell has been clicked
        x, y = pos
        
        row = x // (cell_lw + line_size)
        column = y // (cell_lw + line_size)
        
        # Return nothing if coords are outside bounds
        if row >= grid_size[0] or column >= grid_size[1] or\
            row < 0 or column < 0:
            return None
        
        return self.cells[column].sprites()[row]

    # Clears the surrounding empty cells (recursive)
    def clear_cells(self, location: tuple) -> int:
        
        # Get each surrounding cell
        s_cells = self.get_surrounding_cells(location)
        cleared = 0
        
        # Clear each surrounding cell
        for cell in s_cells:
            if cell.mined or cell.is_mine:
                continue
            
            cell.mine_cell()
            cleared += 1
            
            # Continue to clear empty cells
            if cell.surrounding_mines == 0:
                # Recursive call
                cleared += self.clear_cells(cell.location)
        
        # Returns the total amount of cleared cells
        return cleared

    # Reset the game state
    def restart(self) -> bool:
        self.initialise_cells()
        self.game_over = False
        self.total_cells_to_mine = grid_size[0] * grid_size[1] - total_mines
        
    def clear_all(self, win: bool = False) -> None:
        for column in self.cells:
            for cell in column.sprites():
                cell.mine_cell(win)
    

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

# Mouse buttons
m_LEFT = 1
m_RIGHT = 3

# Game state
run = True
game = None

# Game loop
while run:
        
    # Create the screen background
    screen.fill(CRT_BLACK)
    
    # Create the game
    if game == None:
        game = Game()
    
    # Display Grid
    draw_grid()
    
    # Update the cells
    for row in game.cells:
        # Draw each cell sprite in the grid
        row.draw(screen)
    
    # Display the game over and restart screen
    if game.game_over:
        screen.blit(s_GAMEOVER, (game_over_image_pos[0], game_over_image_pos[1]))
        screen.blit(s_RESTART, (restart_image_pos[0], restart_image_pos[1]))
        
        game.clear_all(False)
        
    
    # Display the win and restart screen
    if game.total_cells_to_mine == 0:
        screen.blit(s_WIN, (win_image_pos[0], win_image_pos[1]))
        screen.blit(s_RESTART, (restart_image_pos[0], restart_image_pos[1]))
        
        game.clear_all(True)
    
    # Get key presses
    key = pygame.key.get_pressed()
    
    # Exit
    if key[pygame.K_ESCAPE]:
       run = False
       
    # Quit game
    for event in pygame.event.get():
        # Call which cell was clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Mouse position
            pos = pygame.mouse.get_pos()
            
            if game.total_cells_to_mine == grid_size[0] * grid_size[1] - total_mines:
                game.generate_grid(pos)
            
            # Check if mouse click is within restart button bounds
            if game.game_over or game.total_cells_to_mine == 0:
                if pos[0] >= restart_image_pos[0] and pos[0] <= restart_image_pos[0] + rs_w and\
                    pos[1] >= restart_image_pos[1] and pos[1] <= restart_image_pos[1] + rs_h:
                        # Reset cells
                        game.restart()
                continue
            
            # Left click to mine cells
            if event.button == m_LEFT:
                game.mine_cells(pos)
            
            # Right click to flag cells
            elif event.button == m_RIGHT:
                game.flag_cells(pos)

        # Quit the game
        if event.type == pygame.QUIT:
            run = False
    
    # Update the game display
    pygame.display.update()

pygame.quit()
    