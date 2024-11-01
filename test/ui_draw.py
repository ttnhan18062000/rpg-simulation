import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Scrollable Health Status Window")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)

# Font
font = pygame.font.SysFont(None, 24)

# Sample character data (name, current health, max health)
characters = [
    {"name": f"Character {i}", "current_health": 70 + i * 5, "max_health": 100 + i * 10}
    for i in range(20)  # Many characters to demonstrate scrolling
]

# Window dimensions
window_width, window_height = 200, 150
window_x, window_y = 50, 50

# Cross button dimensions
cross_box_size = 20
cross_box_rect = pygame.Rect(
    window_x + window_width - cross_box_size - 5,
    window_y + 5,
    cross_box_size,
    cross_box_size,
)

# Scroll settings
max_visible_characters = 5  # Max number of characters to show at once
scroll_offset = 0  # Current scroll position


# Draw health bar
def draw_health_bar(x, y, current, max_health, bar_width=150, bar_height=20):
    health_ratio = current / max_health
    pygame.draw.rect(
        screen, RED, (x, y, bar_width, bar_height)
    )  # Background (empty bar)
    pygame.draw.rect(
        screen, GREEN, (x, y, bar_width * health_ratio, bar_height)
    )  # Filled (current health)


# Main loop
running = True
show_window = True

while running:
    screen.fill(BLACK)  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if cross_box_rect.collidepoint(event.pos):
                show_window = False  # Close the window if "X" is clicked
        elif event.type == pygame.MOUSEWHEEL:
            # Scroll up
            if event.y > 0 and scroll_offset > 0:
                scroll_offset -= 1
            # Scroll down
            elif (
                event.y < 0 and scroll_offset < len(characters) - max_visible_characters
            ):
                scroll_offset += 1

    # Draw health status window
    if show_window:
        # Window background
        pygame.draw.rect(
            screen, WHITE, (window_x, window_y, window_width, window_height)
        )

        # Border
        pygame.draw.rect(
            screen, CYAN, (window_x, window_y, window_width, window_height), 2
        )

        # "X" Close box
        pygame.draw.rect(screen, RED, cross_box_rect)
        pygame.draw.line(
            screen,
            WHITE,
            (cross_box_rect.left + 4, cross_box_rect.top + 4),
            (cross_box_rect.right - 4, cross_box_rect.bottom - 4),
            2,
        )
        pygame.draw.line(
            screen,
            WHITE,
            (cross_box_rect.left + 4, cross_box_rect.bottom - 4),
            (cross_box_rect.right - 4, cross_box_rect.top + 4),
            2,
        )

        # Display visible characters with scroll offset
        for idx in range(max_visible_characters):
            char_idx = idx + scroll_offset
            if char_idx >= len(characters):
                break

            char = characters[char_idx]
            # Name text
            name_text = font.render(char["name"], True, BLACK)
            screen.blit(name_text, (window_x + 10, window_y + 10 + idx * 40))

            # Health bar
            draw_health_bar(
                window_x + 10,
                window_y + 30 + idx * 40,
                char["current_health"],
                char["max_health"],
            )

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
