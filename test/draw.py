import pygame
import sys

sys.path.append("..")
sys.path.append(".")

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(
    (800, 600)
)  # Set screen size to fit your grid dimensions

# Define grid size and cell dimensions
grid_width, grid_height = 10, 10  # 10x10 grid
cell_size = 100  # Size of each cell in pixels
character_size = 100

# Load images for different cell types
ground_image = pygame.image.load("data/sprites/ground.png")
town_image = pygame.image.load("data/sprites/town.png")
# Scale images to fit cell size if needed
ground_image = pygame.transform.scale(ground_image, (cell_size, cell_size))
town_image = pygame.transform.scale(town_image, (cell_size, cell_size))

# Load character icon
character_icon = pygame.image.load("data/sprites/character3.png")
character_icon = pygame.transform.scale(
    character_icon, (character_size, character_size)
)

# Example 2D grid with different types (0=grass, 1=water, 2=dirt)
grid = [
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
]

# Map grid types to images
image_map = {
    0: ground_image,
    1: town_image,
}

# Character positions (a list of (row, col) tuples for each character)
character_positions = [(1, 1), (0, 4)]  # Add more positions as needed

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw grid cells
    for row in range(grid_height):
        for col in range(grid_width):
            cell_type = grid[row][col]
            cell_image = image_map[cell_type]
            # Calculate cell position
            x = col * cell_size
            y = row * cell_size
            # Draw cell image at position
            screen.blit(cell_image, (x, y))

    # Draw character icons on top of cells
    for position in character_positions:
        row, col = position
        x = col * cell_size
        y = row * cell_size
        # Blit character icon on top of the tile
        screen.blit(character_icon, (x, y))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
