from components.character.character_stat import StatDefinition
from components.world.store import get_store, EntityType

from data.logs.logger import logger


class Event:
    def __init__(self) -> None:
        pass

    def execute(self):
        pass


class CombatEvent(Event):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def execute(first_character, second_character):
        logger.debug(
            f"Combat between {first_character.get_info()} and {second_character.get_info()}"
        )
        while first_character.is_alive() and second_character.is_alive():
            first_character.character_stats.update_stat(
                StatDefinition.HEALTH,
                -second_character.character_stats.get_stat(StatDefinition.POWER).value,
            )
            second_character.character_stats.update_stat(
                StatDefinition.HEALTH,
                -first_character.character_stats.get_stat(StatDefinition.POWER).value,
            )
        dead_character = (
            first_character if not first_character.is_alive() else second_character
        )
        alive_character = (
            first_character if first_character.is_alive() else second_character
        )
        is_level_up = alive_character.level.add_exp(
            dead_character.level.class_level.get_next_level_required_exp(
                dead_character.level.current_level
            )
        )
        if is_level_up:
            alive_character.level_up()
        logger.debug(f"{alive_character.get_info()} won")

        store = get_store()
        # store.remove(EntityType.CHARACTER, dead_character.get_info().id)
        dead_character.set_status("dead")
        tile_id = dead_character.tile_id
        tile = store.get(EntityType.TILE, tile_id)
        tile.remove_character_id(dead_character.get_info().id)


class CollectEvent(Event):
    pass


class TrainingEvent(Event):
    @staticmethod
    def execute(character):
        is_level_up = character.level.add_exp(100)
        if is_level_up:
            character.level_up()


class RestingEvent(Event):
    pass
