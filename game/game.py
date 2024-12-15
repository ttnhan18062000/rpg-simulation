import pygame
import sys
import json
import time
import argparse

sys.path.append("..")
sys.path.append(".")

from components.configuration.display_setting import DisplaySetting
from components.world.world import World
from components.display.character_info_display import CharacterInfoDisplay
from components.display.world_display import WorldDisplay
from components.character.character import Character
from components.character.character_info import CharacterInfo
from components.character.character_stat import CharacterStat
from components.world.store import get_store, EntityType
from components.control.monitoring import Monitoring
from components.common.point import Point
from components.control.control_event_handler import ControlEventHandler
from components.world.map_generator import generate_voronoi_map
from components.world.character_generator import (
    HumanGenerator,
    DemonGenerator,
    RuinMobGenerator,
    ForsetMobGenerator,
)
from components.world.map_loader import MapLoader
from components.utils.random_utils import random_once


class Game:

    # TODO: Cleaner creating Game/World, currently a mess
    def __init__(self, char_speed_multiplier=None) -> None:
        self.max_x_cell = 7
        self.max_y_cell = 7
        self.world = None
        self.initialize_world()
        if char_speed_multiplier:
            self.world.set_char_speed_multiplier(char_speed_multiplier)
        self.display_setting = DisplaySetting(self.max_x_cell, self.max_y_cell)
        self.control_event_handler = ControlEventHandler()
        self.is_display_changed = True
        self.surface = None
        self.store = get_store()
        self.initialize_game()
        self.running = True
        self.monitor = Monitoring()

        self.world_display = WorldDisplay(self.display_setting)
        self.character_info_display = CharacterInfoDisplay(self.display_setting)

        # TODO: Later optimization and refactoring
        self.max_refresh_per_second = 120
        self.last_refresh = time.perf_counter()

    def initialize_game(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.display_setting.window_size)
        self.font = pygame.font.Font(None, 20)
        self.info_font = pygame.font.Font(None, 25)

    def initialize_generators(self, grid_data):
        demon_spawn = False
        human_spawn = False
        generators = []
        for x in range(len(grid_data)):
            for y in range(len(grid_data[0])):
                # TODO: Avoid hard-coded tile value
                if grid_data[x][y] == 8 and not demon_spawn:
                    generators.append(DemonGenerator(1, 1, Point(x, y)))
                    demon_spawn = True
                elif grid_data[x][y] == 3 and not human_spawn:
                    generators.append(HumanGenerator(1, 1, Point(x, y)))
                    human_spawn = True
                elif grid_data[x][y] == 11 and random_once(0.25):
                    generators.append(RuinMobGenerator(1, 1, Point(x, y)))
                elif grid_data[x][y] == 5 and random_once(0.25):
                    generators.append(ForsetMobGenerator(1, 1, Point(x, y)))
        return generators

    def initialize_world(self):
        # grid_data = generate_voronoi_map(self.max_x_cell, self.max_y_cell) # Random generated map
        grid_data = MapLoader.load_map("data/world/map2.txt")  # Load defined map
        self.max_x_cell = len(grid_data[0])
        self.max_y_cell = len(grid_data)
        generators = self.initialize_generators(grid_data)
        # generators = [] # TODO: Temporary not spawn any characters to test regions
        self.world = World(grid_data, generators)

    def get_all_surfaces(self):
        surfaces = {}
        surfaces.update({"world_surface": self.world_display.get_main_surface()})
        surfaces.update(self.character_info_display.get_character_info_surfaces())
        return surfaces

    def get_all_surfaces_pos_absolute(self):
        surfaces_pos = {}
        surfaces_pos.update(
            {"world_surface": self.world_display.get_main_surface_pos()}
        )
        surfaces_pos.update(
            self.character_info_display.get_character_info_surfaces_pos_absolute()
        )
        return surfaces_pos

    def draw(self):
        self.world_display.draw(
            self.surface,
            self.font,
            self.display_setting,
            (
                self.control_event_handler.get_offset_x(),
                self.control_event_handler.get_offset_y(),
            ),
            self.is_display_changed,
            self.world.get_focusing_character(),
        )

        self.character_info_display.draw(
            self.surface,
            self.info_font,
            self.display_setting,
            self.world.get_tracking_info_characters(),
        )

        self.is_display_changed = False

    def update_information_based_on_event(self):
        selected_tile_pos = self.control_event_handler.get_selected_tile_pos()
        if selected_tile_pos:
            self.world.update_tracking_characters_with_tile_pos(selected_tile_pos)

        selected_character_info_id = (
            self.control_event_handler.get_selected_character_info_id()
        )
        self.character_info_display.set_focusing_character_info_id(
            selected_character_info_id
        )

        # Allow to set selected_character_info_id to None, to exist the focusing mode
        self.world.update_focusing_character_id(selected_character_info_id)

    # TODO: Need refactoring, currently a mess
    def update_display_information(self):
        is_changed = self.world.update_tracking_characters_status()
        if is_changed:
            self.character_info_display.refresh_character_info_surfaces()

        self.world.update_focusing_character_status()

        if self.world.is_just_select_focusing_character():
            self.is_display_changed = True
        # If is in focusing specific character mode
        # set the offset to keep character in the center
        selected_character = self.world.get_focusing_character()
        if selected_character and (
            self.world.is_just_select_focusing_character()
            or selected_character.is_just_moved()
        ):
            self.world.set_already_focused_on_character()
            cell_size = self.display_setting.cell_size
            main_screen_width, main_screen_height = (
                self.display_setting.main_screen_size
            )
            character_pos = selected_character.get_pos()
            offset_x = int(character_pos.x * cell_size - main_screen_width / 2)
            offset_y = int(character_pos.y * cell_size - main_screen_height / 2)
            self.control_event_handler.update_offset(offset_x, offset_y)
            self.is_display_changed = True

    def update(self):
        self.monitor.check()
        self.world.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    is_display_changed = self.control_event_handler.handle(
                        event,
                        self.display_setting,
                        self.get_all_surfaces(),
                        self.get_all_surfaces_pos_absolute(),
                    )
                    if (
                        is_display_changed and self.is_display_changed == False
                    ) or self.is_display_changed:
                        self.is_display_changed = True
                    else:
                        self.is_display_changed = False

            if self.last_refresh <= time.perf_counter():
                self.last_refresh = (
                    time.perf_counter() + 1 / self.max_refresh_per_second
                )
                self.update_information_based_on_event()
                self.update_display_information()

            self.update()

            self.draw()

            # Update display
            # pygame.display.flip()
            pygame.display.update()

        # Quit Pygame
        pygame.quit()


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="Description of your script's functionality."
    )

    # Add arguments
    parser.add_argument(
        "--char-speed", type=float, help="Character speed multiplier", required=False
    )

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    char_speed_multiplier = args.char_speed

    game = Game(char_speed_multiplier=char_speed_multiplier)
    game.run()


if __name__ == "__main__":
    main()
