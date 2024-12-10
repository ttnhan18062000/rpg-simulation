import pygame
import time

from components.display.drawer import Drawer
from components.configuration.display_setting import DisplaySetting

from data.logs.logger import logger


class CharacterInfoDisplay:
    def __init__(self, display_setting):
        # self.should_redraw = True
        # TODO: Replace other timestamp with time.time with time.perf_counter
        self.last_draw_timestamp = time.perf_counter()
        self.character_info_surfaces = {}
        self.character_info_surfaces_pos = {}
        self.init_main_surface(display_setting)
        self.text_color = (0, 0, 0)
        self.main_surface_pos = (640, 0)

    def init_main_surface(self, display_setting):
        self.main_surface = pygame.Surface(
            (
                display_setting.left_screen_size[0],
                display_setting.left_screen_size[1],
            )
        )

    def get_main_surface(self):
        return self.main_surface

    def get_character_info_surfaces(self):
        return self.character_info_surfaces

    def get_character_info_surfaces_pos_absolute(self):
        self.character_info_surfaces_pos_abs = {}
        for cid, pos in self.character_info_surfaces_pos.items():
            pos_abs = (
                pos[0] + self.main_surface_pos[0],
                pos[1] + self.main_surface_pos[1],
            )
            self.character_info_surfaces_pos_abs[cid] = pos_abs
        return self.character_info_surfaces_pos_abs

    # def set_should_redraw(self, should_redraw: bool):
    #     self.should_redraw = should_redraw

    def draw_character_info_in_box(self, character_surface, text, font, color, margin):
        width, height = character_surface.get_size()
        character_info_surfaces = pygame.Surface(
            (
                width - margin * 2,
                height - margin * 2,
            )
        )
        character_info_surfaces.fill((222, 222, 222))
        Drawer.render_text_box(character_info_surfaces, text, font, color)
        character_surface.blit(character_info_surfaces, (margin, margin))

    # TODO: The bar need rollable when there are too many tracking characters
    def draw(
        self,
        surface: pygame.Surface,
        font,
        display_setting: DisplaySetting,
        tracking_info_characters,
    ):
        if (
            tracking_info_characters
            and time.perf_counter() - self.last_draw_timestamp
            > 1 / display_setting.max_draw_per_second
        ):
            self.last_draw_timestamp = time.perf_counter()
            self.main_surface.fill((111, 111, 111))
            # Define the border width
            border_width = 5
            # Draw a black border on the surface
            border_color = (0, 0, 0)  # Black
            pygame.draw.rect(
                self.main_surface,
                border_color,
                self.main_surface.get_rect(),
                border_width,
            )

            current_offset = 0
            character_surface_height = 320
            character_box_margin = 10
            between_box_margin = 0
            for cid, character in tracking_info_characters.items():
                if cid not in self.character_info_surfaces:
                    self.character_info_surfaces[cid] = pygame.Surface(
                        (
                            display_setting.left_screen_size[0],
                            character_surface_height,
                        )
                    )
                    self.character_info_surfaces[cid].fill((222, 222, 222))
                    pygame.draw.rect(
                        self.character_info_surfaces[cid],
                        border_color,
                        self.character_info_surfaces[cid].get_rect(),
                        border_width,
                    )
                    self.character_info_surfaces_pos[cid] = (0, current_offset)

                character_detailed_info_string = (
                    character.get_character_detailed_info_string()
                )

                self.draw_character_info_in_box(
                    self.character_info_surfaces[cid],
                    character_detailed_info_string,
                    font,
                    self.text_color,
                    character_box_margin,
                )

                self.main_surface.blit(
                    self.character_info_surfaces[cid], (0, current_offset)
                )
                current_offset += character_surface_height + between_box_margin

            surface.blit(self.main_surface, self.main_surface_pos)

        # self.set_should_redraw(False)
