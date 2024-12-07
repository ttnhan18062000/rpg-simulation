import pygame
import sys
import json
import argparse

sys.path.append("..")
sys.path.append(".")

from components.configuration.display_setting import DisplaySetting
from components.world.world import World
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

    def initialize_game(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.display_setting.window_size)
        self.font = pygame.font.Font(None, 20)
        self.info_font = pygame.font.Font(None, 30)

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

    def draw(self):
        self.world.draw_world(
            self.surface,
            self.font,
            self.display_setting,
            (
                self.control_event_handler.offset_x,
                self.control_event_handler.offset_y,
            ),
            self.is_display_changed,
        )
        if self.control_event_handler.selected_tile_pos:
            self.world.update_tracking_characters_with_tile_pos(
                self.control_event_handler.selected_tile_pos
            )
        self.world.draw_info_left_bar(
            self.surface,
            self.info_font,
            self.display_setting,
        )

        self.is_display_changed = False

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
                        event, self.display_setting
                    )
                    if (
                        is_display_changed and self.is_display_changed == False
                    ) or self.is_display_changed:
                        self.is_display_changed = True
                    else:
                        self.is_display_changed = False

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
