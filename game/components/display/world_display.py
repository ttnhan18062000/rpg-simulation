import pygame
import time

from components.common.point import Point
from components.display.drawer import Drawer
from components.configuration.display_setting import DisplaySetting
from components.world.store import get_store, EntityType
from components.utils.tile_utils import get_tile_object

from data.logs.logger import logger


class WorldDisplay:
    def __init__(self, display_setting):
        self.init_surface(display_setting)

    def init_surface(self, display_setting):
        main_screen_width, main_screen_height = display_setting.main_screen_size
        self.main_surface = pygame.Surface(
            (
                main_screen_width,
                main_screen_height,
            )
        )
        self.main_surface_pos = (0, 0)

    def get_main_surface(self):
        return self.main_surface

    def get_main_surface_pos(self):
        return self.main_surface_pos

    def draw(
        self,
        surface: pygame.Surface,
        font,
        display_setting: DisplaySetting,
        offset,
        is_display_changed: bool,
        focusing_character,
    ):
        store = get_store()
        if is_display_changed:
            # Clear screen
            self.main_surface.fill((0, 0, 0))

        # Draw grid cells
        cell_size = display_setting.cell_size
        grid = store.get(EntityType.GRID, 0)

        cell_size = display_setting.cell_size
        main_screen_width, main_screen_height = display_setting.main_screen_size

        # Draw only screen tiles
        offset_x, offset_y = offset

        start_x = offset_x // cell_size * cell_size
        start_y = offset_y // cell_size * cell_size

        # If focusing a character, apply their vision
        visible_tile_ids = []
        memory_tile_ids = []
        if focusing_character:
            visible_tile_ids = [
                tile.get_id() for tile in focusing_character.get_visible_tiles()
            ]
            memory_tile_ids = [
                memory_tile.get_tile().get_id()
                for memory_tile in focusing_character.get_memory().get_all(
                    EntityType.TILE, focusing_character.get_location()
                )
            ]

        for x in range(start_x, start_x + main_screen_width + cell_size, cell_size):
            for y in range(
                start_y, start_y + main_screen_height + cell_size, cell_size
            ):
                cell_x = x // cell_size
                cell_y = y // cell_size
                if (
                    0 <= cell_x < display_setting.max_x_cell
                    and 0 <= cell_y < display_setting.max_y_cell
                ):
                    tile = store.get(EntityType.TILE, grid.tiles[cell_x][cell_y])
                    if is_display_changed or tile.should_redraw():
                        # TODO: Need refactoring
                        if not focusing_character:
                            cell_image = tile.get_image()
                            if tile.is_combat_happen():
                                cell_image = pygame.image.load(
                                    "data/sprites/combat.png"
                                )
                            else:
                                tile.reset_redraw_status()
                            cell_image = pygame.transform.scale(
                                cell_image, (cell_size, cell_size)
                            )
                            # Draw cell image at position
                            self.main_surface.blit(
                                cell_image, (x - offset_x, y - offset_y)
                            )
                        else:
                            # TODO: need refactoring, current a MESS
                            if (
                                tile.get_id() in visible_tile_ids
                                or Point(cell_x, cell_y) == focusing_character.get_pos()
                                or tile.get_id() in memory_tile_ids
                            ):
                                cell_image = tile.get_image()
                                if tile.is_combat_happen():
                                    cell_image = pygame.image.load(
                                        "data/sprites/combat.png"
                                    )
                                else:
                                    tile.reset_redraw_status()
                                cell_image = pygame.transform.scale(
                                    cell_image, (cell_size, cell_size)
                                )
                                # Draw cell image at position
                                self.main_surface.blit(
                                    cell_image, (x - offset_x, y - offset_y)
                                )

                                if (
                                    tile.get_id() not in visible_tile_ids
                                    and Point(cell_x, cell_y)
                                    != focusing_character.get_pos()
                                ):
                                    # Create the dark filter
                                    dark_filter = pygame.Surface(
                                        (
                                            cell_image.get_width(),
                                            cell_image.get_height(),
                                        )
                                    )
                                    dark_filter.fill((0, 0, 0))  # Black color
                                    dark_filter.set_alpha(
                                        128
                                    )  # Set transparency (0-255)

        # Draw character icons on top of cells
        all_characters = store.get_all(EntityType.CHARACTER)
        drawn_characters = {}
        for character in all_characters:
            character = store.get(EntityType.CHARACTER, character.get_info().id)
            x = character.pos.x * cell_size
            y = character.pos.y * cell_size
            if (
                start_x <= x <= start_x + main_screen_width + cell_size
                and start_y <= y <= start_y + main_screen_height + cell_size
            ) and ((x, y) not in drawn_characters):
                if character.is_alive() and (
                    is_display_changed or character.should_redraw()
                ):
                    drawn_characters[(x, y)] = 1
                    # Blit character icon on top of the tile
                    character_icon = pygame.transform.scale(
                        character.img, (cell_size, cell_size)
                    )
                    self.main_surface.blit(character_icon, (x - offset_x, y - offset_y))

                    # Write character level
                    text_surface = font.render(
                        str(character.get_level().get_current_level()),
                        True,
                        (0, 255, 0),
                    )
                    self.main_surface.blit(
                        text_surface, (x - offset_x + (cell_size - 10), y - offset_y)
                    )

                    # Write number of character on the tile
                    tile = get_tile_object(character.pos)
                    n_of_chars = len(tile.character_ids)
                    text_surface = font.render(str(n_of_chars), True, (255, 0, 0))
                    self.main_surface.blit(text_surface, (x - offset_x, y - offset_y))

                    character.set_redraw_status(False)
        surface.blit(self.main_surface, (0, 0))
