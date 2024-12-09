import pygame


def render_text_box(surface, text, font, color, rect):
    """
    Render text within a specified rectangle, wrapping lines automatically.

    Args:
        surface: The Pygame surface to render the text onto.
        text: The string of text to render.
        font: The Pygame font object to use.
        color: The color of the text.
        rect: The rectangle (x, y, width, height) defining the text area.
    """
    x, y, width, height = rect
    words = text.split(" ")
    space_width, space_height = font.size(" ")
    line_spacing = space_height + 2

    lines = []
    current_line = []
    current_width = 0

    # Create lines of text that fit within the width
    for word in words:
        word_width, word_height = font.size(word)
        if current_width + word_width <= width:
            current_line.append(word)
            current_width += word_width + space_width
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width + space_width

    # Add the last line
    if current_line:
        lines.append(" ".join(current_line))

    # Render each line within the height limit
    for line in lines:
        if y + space_height > rect[1] + height:
            break  # Stop rendering if we exceed the height of the box
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y))
        y += line_spacing


# Example usage
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Text Wrapping Example")
font = pygame.font.Font(None, 30)  # Default font, size 30
clock = pygame.time.Clock()

text = (
    "This is a long paragraph of text that will be wrapped within the given box "
    "area. Pygame does not support automatic text wrapping out of the box, so we "
    "need to implement it ourselves."
)
color = (255, 255, 255)  # White
background_color = (0, 0, 0)  # Black
text_box = (50, 50, 200, 200)  # x, y, width, height

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    render_text_box(screen, text, font, color, text_box)
    pygame.draw.rect(screen, (255, 0, 0), text_box, 2)  # Draw the text box border
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
