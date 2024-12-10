import pygame
import time
import math

from components.common.point import Point
from components.configuration.display_setting import DisplaySetting

from data.logs.logger import logger


class ControlEventHandler:
    def __init__(self):
        self.dragging = False
        self.holding_timestamp = None
        self.dragging_time_threshold = 0.2  # seconds
        self.dragging_distance_threshold = 5  # pixels
        self.drag_start_pos = (0, 0)
        self.offset_x = 0
        self.offset_y = 0
        self.selected_tile_pos = None

    # TODO: Move to the other module
    def calculate_distance(self, start_pos, end_pos):
        x1, y1 = start_pos
        x2, y2 = end_pos
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def get_clicked_child_surface(self, mouse_pos, surface_dict, surface_pos_dict):
        if not surface_dict or not surface_pos_dict:
            return None
        for surface_id, surface in surface_dict.items():
            # Get the rectangle for the child surface
            child_rect = surface.get_rect(topleft=surface_pos_dict[surface_id])

            # Check if the mouse click is within the child surface's rectangle
            if child_rect.collidepoint(mouse_pos):
                print(f"11111111111111111 {surface_id}")
                return surface_id
        return None

    # TODO: Refactor to Point instance instead of x, y
    def handle(
        self,
        event: pygame.event.Event,
        display_setting: DisplaySetting,
        surface_dict,
        surface_pos_dict,
    ):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                # Start dragging
                self.dragging = True
                self.holding_timestamp = time.time()
                self.drag_start_pos = event.pos
                return True
            elif event.button == 1:  # Left mouse button (for cell click, no drag)
                self.get_clicked_child_surface(
                    event.pos, surface_dict, surface_pos_dict
                )
                mouse_x, mouse_y = event.pos
                self.selected_tile_pos = Point(
                    (self.offset_x + mouse_x) // display_setting.cell_size,
                    (self.offset_y + mouse_y) // display_setting.cell_size,
                )
                logger.debug(f"Clicked at TILE {self.selected_tile_pos}")
                return False
            elif event.button == 4:  # Scroll up for zoom in
                new_cell_size = min(
                    display_setting.cell_size + 5, display_setting.max_cell_size
                )

                # Calculate how much to adjust the offset to maintain zoom at the same center
                mouse_x, mouse_y = event.pos
                self.offset_x = int(
                    (self.offset_x + mouse_x)
                    * new_cell_size
                    / display_setting.cell_size
                    - mouse_x
                )
                self.offset_y = int(
                    (self.offset_y + mouse_y)
                    * new_cell_size
                    / display_setting.cell_size
                    - mouse_y
                )

                display_setting.cell_size = new_cell_size
                display_setting.map_size_x = new_cell_size * display_setting.max_x_cell
                display_setting.map_size_y = new_cell_size * display_setting.max_y_cell
                return True
            elif event.button == 5:  # Scroll down for zoom out
                new_cell_size = max(
                    display_setting.cell_size - 5, display_setting.min_cell_size
                )

                # Calculate how much to adjust the offset to maintain zoom at the same center
                mouse_x, mouse_y = event.pos
                self.offset_x = int(
                    (self.offset_x + mouse_x)
                    * new_cell_size
                    / display_setting.cell_size
                    - mouse_x
                )
                self.offset_y = int(
                    (self.offset_y + mouse_y)
                    * new_cell_size
                    / display_setting.cell_size
                    - mouse_y
                )

                display_setting.cell_size = new_cell_size
                display_setting.map_size_x = new_cell_size * display_setting.max_x_cell
                display_setting.map_size_y = new_cell_size * display_setting.max_y_cell
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Stop dragging
                self.dragging = False
                delta_distance = self.calculate_distance(self.drag_start_pos, event.pos)
                delta_time = (
                    0
                    if not self.holding_timestamp
                    else time.time() - self.holding_timestamp
                )
                if (delta_time > self.dragging_time_threshold) or (
                    delta_distance > self.dragging_distance_threshold
                ):
                    # Actual dragging
                    return True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:  # If dragging, update offsets
                mouse_x, mouse_y = event.pos
                dx = mouse_x - self.drag_start_pos[0]
                dy = mouse_y - self.drag_start_pos[1]
                self.offset_x = max(
                    0,
                    min(
                        display_setting.map_size_x
                        - display_setting.main_screen_size[0],
                        self.offset_x - dx,
                    ),
                )
                self.offset_y = max(
                    0,
                    min(
                        display_setting.map_size_y
                        - display_setting.main_screen_size[1],
                        self.offset_y - dy,
                    ),
                )
                self.drag_start_pos = event.pos  # Update the drag start point
                return True
