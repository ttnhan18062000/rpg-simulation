import pygame
from queue import PriorityQueue
import time

from components.world.grid import Grid
from components.world.store import get_store, EntityType
from components.configuration.display_setting import DisplaySetting
from components.common.point import Point
from components.character.character import Character
from components.character.character_stat import StatDefinition
from components.utils.tile_utils import get_tile_object


class World:
    def __init__(self, grid_data, generators) -> None:
        get_store().add(EntityType.GRID, 0, Grid(grid_data))

        self.character_action_values = {}
        self.generators = generators

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
        window_width, window_height = display_setting.window_size
        start_x = offset_x // cell_size * cell_size
        start_y = offset_y // cell_size * cell_size
        for x in range(start_x, start_x + window_width + cell_size, cell_size):
            for y in range(start_y, start_y + window_height + cell_size, cell_size):
                cell_x = x // cell_size
                cell_y = y // cell_size
                if (
                    0 <= cell_x < display_setting.max_x_cell
                    and 0 <= cell_y < display_setting.max_y_cell
                ):
                    tile = store.get(EntityType.TILE, grid.tiles[cell_x][cell_y])
                    if is_display_changed or tile.should_redraw():
                        cell_image = tile.image
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
                start_x <= x <= start_x + window_width + cell_size
                and start_y <= y <= start_y + window_height + cell_size
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

    def update(self):
        for generator in self.generators:
            if not generator.is_stop():
                generator.update()

        all_characters = get_store().get_all(EntityType.CHARACTER)
        for character in all_characters:
            cid = character.get_info().id
            if character.is_alive() == False:
                if cid in self.character_action_values:
                    self.character_action_values.pop(cid)
            else:
                if cid not in self.character_action_values:
                    self.character_action_values[cid] = (
                        100
                        / character.get_status_applied_character_stat()
                        .get_stat(StatDefinition.SPEED)
                        .value
                        + time.time()
                    )
                if self.character_action_values[cid] < time.time():
                    character.do_action()
                    self.character_action_values[cid] = (
                        100
                        / character.get_status_applied_character_stat()
                        .get_stat(StatDefinition.SPEED)
                        .value
                        + time.time()
                    )
