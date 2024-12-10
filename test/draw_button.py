import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Icon Button with Modal Description")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)

# Load Icon (ensure you have an image file named 'icon.png' in the same directory)
icon_image = pygame.image.load("test/button.png")
icon_image = pygame.transform.scale(icon_image, (50, 50))  # Resize icon

pygame.draw.rect(
    icon_image,
    BLACK,
    icon_image.get_rect(),
    1,
)

# Button settings
button_rect = icon_image.get_rect(topleft=(175, 125))
is_hovered = False
description_text = "Lock character"

# Font
font = pygame.font.Font(None, 24)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if button_rect.collidepoint(event.pos):
                    print("Button clicked!")

    # Check if mouse is hovering over the button
    is_hovered = button_rect.collidepoint(pygame.mouse.get_pos())

    # Draw button (icon)
    screen.blit(icon_image, button_rect.topleft)

    # Draw modal-like box for description if hovered
    if is_hovered:
        # Calculate the modal's position and size
        text_surface = font.render(description_text, True, BLACK)
        text_width, text_height = text_surface.get_size()
        padding = 10
        modal_width = text_width + padding * 2
        modal_height = text_height + padding * 2
        modal_x = button_rect.right + 10  # 10 pixels to the right of the button
        modal_y = button_rect.bottom + 10  # 10 pixels below the button

        # Draw the modal background
        modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
        pygame.draw.rect(screen, GRAY, modal_rect)
        pygame.draw.rect(screen, BLACK, modal_rect, 2)  # Border

        # Render and draw the text inside the modal
        text_x = modal_x + padding
        text_y = modal_y + padding
        screen.blit(text_surface, (text_x, text_y))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
