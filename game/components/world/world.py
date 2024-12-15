import pygame
from queue import PriorityQueue
import time

# from components.global_object.world_notification import (
#     get_world_notification_manager,
#     WorldNotificationType,
# )
from components.display.drawer import Drawer
from components.display.character_info_display import CharacterInfoDisplay
from components.display.world_display import WorldDisplay
from components.world.grid import Grid
from components.world.store import get_store, EntityType
from components.configuration.display_setting import DisplaySetting
from components.common.point import Point
from components.character.character import Character
from components.character.character_stat import StatDefinition
from components.utils.tile_utils import get_tile_object
from components.race.race import Human, Demon

from data.logs.logger import logger


class World:
    def __init__(self, grid_data, generators) -> None:
        get_store().add(EntityType.GRID, 0, Grid(grid_data))

        self.character_action_values = {}
        self.generators = generators
        self.char_speed_multiplier = 1
        self.tracking_info_characters = {}
        self.tracking_info_character_factions = [Human.get_name(), Demon.get_name()]
        self.focusing_character_id = None
        self.just_select_focusing_character = None
        # self.subscribe_to_world_notification()

    # TODO: Can be optimized further
    # def on_character_changed(self, **kwargs):
    #     cid = kwargs.get("cid")
    #     if cid in self.tracking_info_characters:
    #         self.on_tracking_characters_info_changed()

    # def subscribe_to_world_notification(self):
    #     world_notification_manager = get_world_notification_manager()
    #     world_notification_manager.subscribe(
    #         WorldNotificationType.CHARACTER.CHANGE_INFO, self.on_character_changed
    #     )

    def get_tracking_info_characters(self):
        return self.tracking_info_characters

    def set_focus_on_character():
        pass

    def set_char_speed_multiplier(self, char_speed_multiplier):
        self.char_speed_multiplier = char_speed_multiplier

    def is_moveable_tile(self, pos: Point):
        return self.grid.is_moveable_tile(pos)

    def update_tracking_characters_with_tile_pos(self, tile_pos):
        store = get_store()
        tile = get_tile_object(tile_pos)
        tile_character_ids = tile.get_character_ids()
        tile_cid_to_characters = {
            cid: store.get(EntityType.CHARACTER, cid) for cid in tile_character_ids
        }
        self.tracking_info_characters.update(tile_cid_to_characters)

    # def on_tracking_characters_info_changed(self):
    #     self.character_info_display.set_should_redraw(True)

    def update_tracking_characters_status(self):
        is_changed = False
        new_tracking_info_characters = {
            cid: character
            for cid, character in self.tracking_info_characters.items()
            if character.is_alive()
        }
        if set(self.tracking_info_characters.keys()) != set(
            new_tracking_info_characters.keys()
        ):
            is_changed = True
        self.tracking_info_characters = new_tracking_info_characters
        return is_changed

    def update_focusing_character_status(self):
        if self.focusing_character_id:
            focusing_character = get_store().get(
                EntityType.CHARACTER, self.focusing_character_id
            )
            if not focusing_character.is_alive():
                self.focusing_character_id = None

    def update_focusing_character_id(self, character_id):
        if self.focusing_character_id != character_id:
            self.just_select_focusing_character = True
        self.focusing_character_id = character_id

    def get_focusing_character_id(self):
        return self.focusing_character_id

    def get_focusing_character(self):
        if self.focusing_character_id:
            return get_store().get(EntityType.CHARACTER, self.focusing_character_id)
        return None

    def is_just_select_focusing_character(self):
        return self.just_select_focusing_character

    def set_already_focused_on_character(self):
        self.just_select_focusing_character = False

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
                        recently_added_character.get_race()
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
