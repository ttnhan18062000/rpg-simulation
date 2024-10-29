import random

from components.world.store import get_store, EntityType
from components.common.point import Point
from components.action.event import CombatEvent, TrainingEvent
from data.logs.logger import logger


class Action:
    action_name = "Action"

    def do_action(self, character):
        pass

    def execute(self, character):
        logger.debug(f"{character.get_info()} do {self.action_name}")
        self.do_action(character)


class Move(Action):
    action_name = "Move"

    def check_valid_step(self, new_pos: Point):
        store = get_store()
        tile_id = store.get(EntityType.GRID, 0).get_tile(new_pos)
        tile = store.get(EntityType.TILE, tile_id)
        if tile.is_obstacle():
            return False
        return tile

    def do_action(self, character):
        direction = random.randint(0, 3)
        next_move = Point(0, 0)
        if direction == 0:
            next_move = Point(0, -1)
        elif direction == 1:
            next_move = Point(0, 1)
        elif direction == 2:
            next_move = Point(-1, 0)
        elif direction == 3:
            next_move = Point(1, 0)

        if self.check_valid_step(character.pos + next_move):
            store = get_store()

            previous_tile_id = store.get(EntityType.GRID, 0).get_tile(character.pos)
            previous_tile = store.get(EntityType.TILE, previous_tile_id)
            previous_tile.remove_character_id(character.get_info().id)

            character.pos += next_move
            new_tile_id = store.get(EntityType.GRID, 0).get_tile(character.pos)
            new_tile = store.get(EntityType.TILE, new_tile_id)
            new_tile.add_character_id(character.get_info().id)
            character.tile_id = new_tile.id

            other_characters = [
                store.get(EntityType.CHARACTER, cid)
                for cid in new_tile.get_character_ids()
            ]
            for other_character in other_characters:
                if character.is_hostile_with(other_character):
                    CombatEvent().execute(character, other_character)
                    return

        else:
            self.do_action(character)


class Interact(Action):
    action_name = "Interact"

    def do_action(self, character):
        pass


class Standby(Action):
    action_name = "Standby"

    def do_action(self, character):
        TrainingEvent().execute(character)
