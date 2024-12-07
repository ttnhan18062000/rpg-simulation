class Drawer:
    @staticmethod
    def render_text_box(surface, text, font, color):
        """
        Render text within a specified rectangle, wrapping lines automatically.

        Args:
            surface: The Pygame surface to render the text onto.
            text: The string of text to render.
            font: The Pygame font object to use.
            color: The color of the text.
            rect: The rectangle (x, y, width, height) defining the text area.
        """
        rect = surface.get_rect()
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
            if current_width + word_width <= width and "|" not in word:
                current_line.append(word)
                current_width += word_width + space_width
            else:
                if "|" in word:
                    word = word.replace("|", "")
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width + space_width

        # Add the last line
        if current_line:
            lines.append(" ".join(current_line))

        # Render each line within the height limit
        for line in lines:
            line = line.strip()
            if y + space_height > rect[1] + height:
                break  # Stop rendering if we exceed the height of the box
            line_surface = font.render(line, True, color)
            surface.blit(line_surface, (x, y))
            y += line_spacing
