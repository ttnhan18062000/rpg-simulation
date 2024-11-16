import pygame
import sys
import json

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
from components.world.character_generator import HumanGenerator, DemonGenerator
from data.world.grid_data import grid1


class Game:
    def __init__(self) -> None:
        self.max_n_cell = 7
        self.display_setting = DisplaySetting(self.max_n_cell)
        self.control_event_handler = ControlEventHandler()
        self.is_display_changed = True
        self.surface = None
        self.world = None
        self.store = get_store()
        self.initialize_game()
        self.initialize_world()
        self.running = True
        self.monitor = Monitoring()

    def initialize_game(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.display_setting.window_size)
        self.font = pygame.font.Font(None, 20)

    def initialize_generators(self, grid_data):
        generators = []
        for x in range(len(grid_data)):
            for y in range(len(grid_data[0])):
                # TODO: Avoid hard-coded tile value
                if grid_data[x][y] == 3:
                    generators.append(DemonGenerator(1, 3, Point(x, y)))
                if grid_data[x][y] == 4:
                    generators.append(HumanGenerator(1, 3, Point(x, y)))
        return generators

    def initialize_world(self):
        grid_data = generate_voronoi_map(self.max_n_cell, self.max_n_cell)
        print(grid_data)
        generators = self.initialize_generators(grid_data)
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


game = Game()
game.run()
