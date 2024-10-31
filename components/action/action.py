import random

from components.world.store import get_store, EntityType
from components.common.point import Point
from components.action.event import CombatEvent, TrainingEvent
from components.character.character_stat import StatDefinition
from data.logs.logger import logger


class Action:
    action_name = "Action"

    def do_action(self, character):
        pass

    def execute(self, character, **kwargs):
        logger.debug(f"{character.get_info()} do {self.action_name}")
        return self.do_action(character, **kwargs)


class Move(Action):
    action_name = "Move"

    def check_valid_step(self, new_pos: Point):
        store = get_store()
        tile_id = store.get(EntityType.GRID, 0).get_tile(new_pos)
        tile = store.get(EntityType.TILE, tile_id)
        if tile.is_obstacle():
            return False
        return tile

    def do_action(self, character, **kwargs):
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
                    # CombatEvent().execute(character, other_character)
                    character.enter_combat([other_character.get_info().id])
                    other_character.enter_combat([character.get_info().id])
                    # Create a combat event to manage all the characters from Human/Demon
                    # Dead characters remove from the event -> update all targets -> won't kill the already dead characters
                    return True

        else:
            self.do_action(character)

        return True


class Interact(Action):
    action_name = "Interact"

    def do_action(self, character, **kwargs):
        return False


class Standby(Action):
    action_name = "Standby"

    def do_action(self, character, **kwargs):
        TrainingEvent().execute(character)
        return False


class Fight(Action):
    action_name = "Fight"

    def do_action(self, character, **kwargs):
        store = get_store()
        target_character_ids = kwargs.get("target_character_ids")
        # TODO: smarter target selection
        target_character_id = random.choice(target_character_ids)
        target_character = store.get(EntityType.CHARACTER, target_character_id)
        target_character.character_stats.update_stat(
            StatDefinition.HEALTH,
            -character.character_stats.get_stat(StatDefinition.POWER).value,
        )
        logger.debug(f"{character.get_info()} hit {target_character.get_info()}")
        if not target_character.is_alive():
            logger.debug(f"{character.get_info()} killed {target_character.get_info()}")
            is_level_up = character.level.add_exp(
                target_character.level.class_level.get_next_level_required_exp(
                    target_character.level.current_level
                )
            )
            if is_level_up:
                character.level_up()

            # Remove dead character corpse
            target_character.set_status("dead")
            tile_id = target_character.tile_id
            tile = store.get(EntityType.TILE, tile_id)
            tile.remove_character_id(target_character.get_info().id)

            target_character_ids.remove(target_character_id)

            if len(target_character_ids) == 0:
                character.exit_combat()
                return True

        return False


class Escape(Action):
    action_name = "Escape"

    def do_action(self, character, **kwargs):
        return False
