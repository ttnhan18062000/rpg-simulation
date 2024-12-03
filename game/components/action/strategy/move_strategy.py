import random

from components.action.strategy.base_strategy import BaseStrategy
from components.common.point import Point
from components.common.path_finding import (
    get_move_from_target,
    check_valid_step,
)
from components.world.store import get_store, EntityType
from components.action.event import Event, CombatEvent, TrainingEvent, EventType
from components.character.memory.memory import MemoryCharacter, MemoryEvent, PowerEst
from components.utils.tile_utils import get_tile_object
from components.action.goal import FindingItemGoal

from data.logs.logger import logger
from data.game_settings import ACTION


class MoveStrategy(BaseStrategy):
    def __init__(self):
        pass

    @classmethod
    def get_next_move(cls, character):
        pass


class RandomMove:
    @staticmethod
    def get_next_move(character, retry=0):
        if retry == 50:
            # TODO: very small chance for a bug, character stay a same spot althrough they can move
            return None
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
        if not check_valid_step(character, character.pos + next_move):
            return RandomMove.get_next_move(character, retry=retry + 1)
        return next_move


class ThinkingMove(MoveStrategy):
    @classmethod
    def get_next_move(cls, character):
        # TODO: Prioritize between goals or decisions
        # Currently finding items first
        if character.has_goal():
            current_goal = character.get_current_goal()
            if current_goal.is_finding_item():
                logger.debug(
                    f"{character.get_info()} has the FindingItem goal, looking for the tile contains the item"
                )
                # TODO: Better strategy for reaching the collectable tiles
                # Currently, When there is no collectable tiles in the memory, Human -> go left, Demon -> go right
                tiles_in_memory = character.get_memory().get_all_sorted_distant(
                    EntityType.TILE, character.get_location()
                )
                for memory_tile in tiles_in_memory:
                    tile = memory_tile.get_tile()
                    if (
                        tile.is_collectable()
                        and current_goal.is_collectable_items_match(
                            tile.get_collectable_items()
                        )
                    ):
                        logger.debug(
                            f"{character.get_info()} has the memory about the {tile.get_name()} contain the item, moving into it"
                        )
                        return get_move_from_target(
                            character,
                            character.pos,
                            memory_tile.get_location(),
                            is_chasing=True,
                        )

        # Join nearby combat of own faction if favorable
        events_in_memory = character.get_memory().get_all_sorted_distant(
            EntityType.EVENT, character.get_location()
        )
        for memory_event in events_in_memory:
            if memory_event.get_event_type() is EventType.COMBAT:
                if memory_event.get_power_est() in [
                    PowerEst.MUCH_WEAKER,
                    PowerEst.WEAKER,
                ]:
                    logger.debug(
                        f"{character.get_info()}:{character.get_power()} is joining combat {memory_event.get_id()}:{memory_event.get_location()}:{memory_event.get_power_est()}"
                    )
                    return get_move_from_target(
                        character,
                        character.pos,
                        memory_event.get_location(),
                        is_chasing=True,
                    )

        # Chase or escape nearby enemies
        characters_in_memory = character.get_memory().get_all_sorted_distant(
            EntityType.CHARACTER, character.get_location()
        )
        for memory_character in characters_in_memory:
            if character.is_hostile_with(memory_character.get_faction()):
                # TODO: Path finding movement, avoid obstacle
                # TODO: smarter escape
                # TODO: Add characteristic for complex movement
                # if memory_character.get_power_est() in [
                #     PowerEst.MUCH_STRONGER,
                # ]:
                #     logger.debug(
                #         f"{character.get_info()}:{character.get_power()} is escaping from {memory_character.get_power_est()}"
                #     )
                #     return get_move_from_target(
                #         character,
                #         character.pos,
                #         memory_character.get_location(),
                #         is_chasing=False,
                #     )
                if memory_character.get_power_est() in [
                    PowerEst.MUCH_WEAKER,
                    PowerEst.WEAKER,
                ]:
                    logger.debug(
                        f"{character.get_info()}:{character.get_power()} is chasing {memory_character.get_power_est()}"
                    )
                    return get_move_from_target(
                        character,
                        character.pos,
                        memory_character.get_location(),
                        is_chasing=True,
                    )

        # Not found any enemy, random movement
        return RandomMove.get_next_move(character)


class AgressiveMobMove(MoveStrategy):
    @classmethod
    def get_next_move(cls, character):
        # Join nearby combat of own faction if favorable
        events_in_memory = character.get_memory().get_all_sorted_distant(
            EntityType.EVENT, character.get_location()
        )
        for memory_event in events_in_memory:
            if memory_event.get_event_type() is EventType.COMBAT:
                # if memory_event.get_power_est() in [
                #     PowerEst.MUCH_WEAKER,
                #     PowerEst.WEAKER,
                # ]:
                logger.debug(
                    f"{character.get_info()}:{character.get_power()} is joining combat {memory_event.get_id()}:{memory_event.get_location()}:{memory_event.get_power_est()}"
                )
                return get_move_from_target(
                    character,
                    character.pos,
                    memory_event.get_location(),
                    is_chasing=True,
                )

        # Chase or escape nearby enemies
        characters_in_memory = character.get_memory().get_all_sorted_distant(
            EntityType.CHARACTER, character.get_location()
        )
        for memory_character in characters_in_memory:
            if character.is_hostile_with(memory_character.get_faction()):
                # if memory_character.get_power_est() in [
                #     PowerEst.MUCH_WEAKER,
                #     PowerEst.WEAKER,
                # ]:
                logger.debug(
                    f"{character.get_info()}:{character.get_power()} is chasing {memory_character.get_power_est()}"
                )
                return get_move_from_target(
                    character,
                    character.pos,
                    memory_character.get_location(),
                    is_chasing=True,
                )

        # Not found any enemy, random movement
        return RandomMove.get_next_move(character)


# TODO: Add more characteristics(?)
class PassiveMobMove(MoveStrategy):
    @classmethod
    def get_next_move(cls, character):
        characters_in_memory = character.get_memory().get_all_sorted_distant(
            EntityType.CHARACTER, character.get_location()
        )
        for memory_character in characters_in_memory:
            if not character.is_ally_with(memory_character.get_faction()):
                if memory_character.get_power_est() in [
                    PowerEst.STRONGER,
                    PowerEst.MUCH_STRONGER,
                ]:
                    logger.debug(
                        f"{character.get_info()}:{character.get_power()} is escaping from {memory_character.get_power_est()}"
                    )
                    return get_move_from_target(
                        character,
                        character.pos,
                        memory_character.get_location(),
                        is_chasing=False,
                    )
        return RandomMove.get_next_move(character)
