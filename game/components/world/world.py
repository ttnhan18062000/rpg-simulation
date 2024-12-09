import pygame
from queue import PriorityQueue
import time

from components.display.drawer import Drawer
from components.world.grid import Grid
from components.world.store import get_store, EntityType
from components.configuration.display_setting import DisplaySetting
from components.common.point import Point
from components.character.character import Character
from components.character.character_stat import StatDefinition
from components.utils.tile_utils import get_tile_object
from components.character.character_class import Human, Demon

from data.logs.logger import logger


class World:
    def __init__(self, grid_data, generators) -> None:
        get_store().add(EntityType.GRID, 0, Grid(grid_data))

        self.character_action_values = {}
        self.generators = generators
        self.char_speed_multiplier = 1
        self.tracking_info_characters = {}
        self.tracking_info_character_factions = [Human.get_name(), Demon.get_name()]

    def set_char_speed_multiplier(self, char_speed_multiplier):
        self.char_speed_multiplier = char_speed_multiplier

    def is_moveable_tile(self, pos: Point):
        return self.grid.is_moveable_tile(pos)

    def draw_world(
        self,
        surface: pygame.Surface,
        font,
        display_setting: DisplaySetting,
        offset,
        is_display_changed: bool,
    ):
        store = get_store()
        if is_display_changed:
            # Clear screen
            surface.fill((0, 0, 0))

        # Draw grid cells
        cell_size = display_setting.cell_size
        grid = store.get(EntityType.GRID, 0)
        # Draw only screen tiles
        offset_x, offset_y = offset
        cell_size = display_setting.cell_size
        main_screen_width, main_screen_height = display_setting.main_screen_size
        start_x = offset_x // cell_size * cell_size
        start_y = offset_y // cell_size * cell_size
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
                        cell_image = tile.get_image()
                        if tile.is_combat_happen():
                            cell_image = pygame.image.load("data/sprites/combat.png")
                        else:
                            tile.reset_redraw_status()
                        cell_image = pygame.transform.scale(
                            cell_image, (cell_size, cell_size)
                        )
                        # Draw cell image at position
                        surface.blit(cell_image, (x - offset_x, y - offset_y))

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
                    surface.blit(character_icon, (x - offset_x, y - offset_y))

                    # Write character level
                    text_surface = font.render(
                        str(character.get_level().get_current_level()),
                        True,
                        (0, 255, 0),
                    )
                    surface.blit(
                        text_surface, (x - offset_x + (cell_size - 10), y - offset_y)
                    )

                    # Write number of character on the tile
                    tile = get_tile_object(character.pos)
                    n_of_chars = len(tile.character_ids)
                    text_surface = font.render(str(n_of_chars), True, (255, 0, 0))
                    surface.blit(text_surface, (x - offset_x, y - offset_y))

                    character.set_redraw_status(False)

    def draw_character_info_in_box(self, character_surface, text, font, color, margin):
        width, height = character_surface.get_size()
        character_info_surface = pygame.Surface(
            (
                width - margin * 2,
                height - margin * 2,
            )
        )
        character_info_surface.fill((222, 222, 222))
        Drawer.render_text_box(character_info_surface, text, font, color)
        character_surface.blit(character_info_surface, (margin, margin))

    def update_tracking_characters_with_tile_pos(self, tile_pos):
        store = get_store()
        tile = get_tile_object(tile_pos)
        tile_character_ids = tile.get_character_ids()
        tile_cid_to_characters = {
            cid: store.get(EntityType.CHARACTER, cid) for cid in tile_character_ids
        }
        self.tracking_info_characters.update(tile_cid_to_characters)

    # TODO: The bar need rollable when there are too many tracking characters
    def draw_info_left_bar(
        self,
        surface: pygame.Surface,
        font,
        display_setting: DisplaySetting,
    ):
        new_tracking_info_characters = {
            cid: character
            for cid, character in self.tracking_info_characters.items()
            if character.is_alive()
        }
        self.tracking_info_characters = new_tracking_info_characters
        if self.tracking_info_characters:
            store = get_store()

            info_surface = pygame.Surface(
                (
                    display_setting.left_screen_size[0],
                    display_setting.left_screen_size[1],
                )
            )
            info_surface.fill((111, 111, 111))
            # Define the border width
            border_width = 5
            # Draw a black border on the surface
            border_color = (0, 0, 0)  # Black
            pygame.draw.rect(
                info_surface, border_color, info_surface.get_rect(), border_width
            )

            current_offset = 0
            character_surface_height = 320
            character_box_margin = 10
            between_box_margin = 0
            for cid, character in self.tracking_info_characters.items():
                character_surface = pygame.Surface(
                    (
                        display_setting.left_screen_size[0],
                        character_surface_height,
                    )
                )
                character_surface.fill((222, 222, 222))
                pygame.draw.rect(
                    character_surface,
                    border_color,
                    character_surface.get_rect(),
                    border_width,
                )
                text_color = (0, 0, 0)
                character_detailed_info_string = (
                    character.get_character_detailed_info_string()
                )

                self.draw_character_info_in_box(
                    character_surface,
                    character_detailed_info_string,
                    font,
                    text_color,
                    character_box_margin,
                )

                info_surface.blit(character_surface, (0, current_offset))
                current_offset += character_surface_height + between_box_margin

            surface.blit(info_surface, (640, 0))

    def update(self):
        store = get_store()

        for generator in self.generators:
            if not generator.is_stop():
                is_new_character_spawn = generator.update()
                if is_new_character_spawn:
                    recently_added_character = store.get_recently_added(
                        EntityType.CHARACTER
                    )
                    if (
                        recently_added_character.get_faction()
                        in self.tracking_info_character_factions
                    ):
                        self.tracking_info_characters[
                            recently_added_character.get_id()
                        ] = recently_added_character

        all_characters = store.get_all(EntityType.CHARACTER)
        for character in all_characters:
            cid = character.get_info().id
            if character.is_alive() == False:
                if cid in self.character_action_values:
                    self.character_action_values.pop(cid)
            else:
                seconds_per_action = (
                    100 / self.char_speed_multiplier
                ) / character.get_final_stat().get_stat(StatDefinition.SPEED).value
                if cid not in self.character_action_values:
                    self.character_action_values[cid] = seconds_per_action + time.time()
                if self.character_action_values[cid] < time.time():
                    character.do_action()
                    self.character_action_values[cid] = seconds_per_action + time.time()

                action_percentage = (
                    self.character_action_values[cid] - time.time()
                ) / seconds_per_action
                character.update_action_percentage(action_percentage)
