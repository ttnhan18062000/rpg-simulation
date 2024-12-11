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

        # Clear screen if display has changed
        if is_display_changed:
            self.main_surface.fill((0, 0, 0))

        # Pre-fetch grid and settings
        grid = store.get(EntityType.GRID, 0)
        cell_size = display_setting.cell_size
        main_screen_width, main_screen_height = display_setting.main_screen_size
        offset_x, offset_y = offset

        # Determine visible tiles and memory for focusing character
        visible_tile_ids, visible_points, memory_tile_ids = self.get_visibility_info(
            focusing_character
        )

        # Draw tiles
        self.draw_tiles(
            grid,
            cell_size,
            main_screen_width,
            main_screen_height,
            offset_x,
            offset_y,
            is_display_changed,
            visible_tile_ids,
            memory_tile_ids,
            focusing_character,
        )

        # Draw characters
        self.draw_characters(
            store,
            cell_size,
            offset_x,
            offset_y,
            main_screen_width,
            main_screen_height,
            is_display_changed,
            font,
            focusing_character,
            visible_points,
        )

        # Render the main surface onto the target surface
        surface.blit(self.main_surface, (0, 0))

    def get_visibility_info(self, focusing_character):
        if not focusing_character:
            return [], [], []

        visible_tile_ids = [
            tile.get_id() for tile in focusing_character.get_visible_tile_objects()
        ]
        visible_points = focusing_character.get_visible_tiles()
        memory_tile_ids = [
            memory_tile.get_tile().get_id()
            for memory_tile in focusing_character.get_memory().get_all(
                EntityType.TILE, focusing_character.get_location()
            )
        ]
        return visible_tile_ids, visible_points, memory_tile_ids

    def draw_tiles(
        self,
        grid,
        cell_size,
        screen_width,
        screen_height,
        offset_x,
        offset_y,
        is_display_changed,
        visible_tile_ids,
        memory_tile_ids,
        focusing_character,
    ):
        store = get_store()
        start_x = offset_x // cell_size * cell_size
        start_y = offset_y // cell_size * cell_size

        for x in range(start_x, start_x + screen_width + cell_size, cell_size):
            for y in range(start_y, start_y + screen_height + cell_size, cell_size):
                cell_x, cell_y = x // cell_size, y // cell_size

                if not (0 <= cell_x < grid.width and 0 <= cell_y < grid.height):
                    continue

                tile = store.get(EntityType.TILE, grid.tiles[cell_x][cell_y])
                if not is_display_changed and not tile.should_redraw():
                    continue

                is_visible = (
                    not focusing_character
                    or tile.get_id() in visible_tile_ids
                    or Point(cell_x, cell_y) == focusing_character.get_pos()
                    or tile.get_id() in memory_tile_ids
                )

                if is_visible:
                    self.render_tile(
                        tile,
                        x,
                        y,
                        cell_size,
                        offset_x,
                        offset_y,
                        focusing_character and tile.get_id() not in visible_tile_ids,
                    )

    def render_tile(self, tile, x, y, cell_size, offset_x, offset_y, is_memory_tile):
        cell_image = tile.get_image()
        if tile.is_combat_happen():
            cell_image = pygame.image.load("data/sprites/combat.png")
        else:
            tile.reset_redraw_status()

        cell_image = pygame.transform.scale(cell_image, (cell_size, cell_size))
        self.main_surface.blit(cell_image, (x - offset_x, y - offset_y))

        if is_memory_tile:
            dark_filter = pygame.Surface(cell_image.get_size())
            dark_filter.fill((0, 0, 0))
            dark_filter.set_alpha(200)
            self.main_surface.blit(dark_filter, (x - offset_x, y - offset_y))

    def draw_characters(
        self,
        store,
        cell_size,
        offset_x,
        offset_y,
        screen_width,
        screen_height,
        is_display_changed,
        font,
        focusing_character,
        visible_points,
    ):
        all_characters = store.get_all(EntityType.CHARACTER)
        drawn_positions = set()

        for character in all_characters:
            char_pos = character.get_pos()
            if (
                focusing_character
                and char_pos not in visible_points
                and char_pos != focusing_character.get_pos()
            ):
                continue

            x, y = char_pos.x * cell_size, char_pos.y * cell_size
            if (x, y) in drawn_positions or not (
                offset_x <= x < offset_x + screen_width
                and offset_y <= y < offset_y + screen_height
            ):
                continue

            if not character.is_alive() or (
                not is_display_changed and not character.should_redraw()
            ):
                continue

            drawn_positions.add((x, y))
            character_icon = pygame.transform.scale(
                character.img, (cell_size, cell_size)
            )
            self.main_surface.blit(character_icon, (x - offset_x, y - offset_y))

            # Render additional details
            level_text = font.render(
                str(character.get_level().get_current_level()), True, (0, 255, 0)
            )
            self.main_surface.blit(
                level_text, (x - offset_x + (cell_size - 10), y - offset_y)
            )

            tile = get_tile_object(char_pos)
            char_count = len(tile.character_ids)
            count_text = font.render(str(char_count), True, (255, 0, 0))
            self.main_surface.blit(count_text, (x - offset_x, y - offset_y))
