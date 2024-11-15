from components.character.character_stat import StatDefinition
from components.world.store import get_store, EntityType
from enum import Enum

from data.logs.logger import logger


class EventType(Enum):
    COMBAT = 1
    COLLECT = 2
    TRAINING = 3


class Event:
    id_counter = 0

    def __init__(self) -> None:
        self.id = Event.id_counter
        Event.id_counter += 1
        pass

    def execute(self):
        pass

    def get_id(self):
        return self.id


class CombatEvent(Event):
    # faction = character class name
    def __init__(self, tile_id) -> None:
        super().__init__()
        self.character_faction_ids = {}
        self.tile_id = tile_id
        tile = get_store().get(EntityType.TILE, self.tile_id)
        tile.set_tile_combat_status(is_combat=True, combat_event_id=self.id)

        logger.debug(f"New combat happen: {self.get_id()}:{self.character_faction_ids}")

    def add_character_id(self, faction, character_id):
        if faction not in self.character_faction_ids:
            self.character_faction_ids[faction] = [character_id]
        else:
            self.character_faction_ids[faction].append(character_id)

    def remove_character_id(self, faction, character_id):
        if faction in self.character_faction_ids:
            self.character_faction_ids[faction].remove(character_id)
            if len(self.character_faction_ids[faction]) == 0:
                self.character_faction_ids.pop(faction)

                # Exit combat for all characters has no hostile faction in combat
                all_factions = list(
                    self.character_faction_ids.keys()
                )  # clone list to avoid 'dictionary changed size during iteration'
                for faction in all_factions:
                    character_of_faction = get_store().get(
                        EntityType.CHARACTER, self.character_faction_ids[faction][0]
                    )
                    if not any(
                        hostile_faction in all_factions
                        for hostile_faction in character_of_faction.get_hostile_factions()
                    ):
                        self.exit_combat_faction(faction)

    def get_character_ids_with_faction(self, faction):
        if faction in self.character_faction_ids:
            return self.character_faction_ids[faction]
        return []

    def get_factions(self):
        return list(self.character_faction_ids.keys())

    def exit_combat_faction(self, faction):
        characters = [
            get_store().get(EntityType.CHARACTER, cid)
            for cid in self.character_faction_ids[faction]
        ]

        self.character_faction_ids.pop(faction)

        if len(self.character_faction_ids.keys()) == 0:
            store = get_store()
            store.remove(EntityType.EVENT, self.id)
            tile = store.get(EntityType.TILE, self.tile_id)
            tile.set_tile_combat_status(is_combat=False)

        for character in characters:
            character.exit_combat()

    def kill_character(self, character, killed_character):
        logger.debug(f"{character.get_info()} killed {killed_character.get_info()}")

        store = get_store()

        # TODO: better level up handling
        is_level_up = character.level.add_exp(
            killed_character.level.class_level.get_next_level_required_exp(
                killed_character.level.current_level
            )
        )
        if is_level_up:
            character.level_up()

        # TODO: Clean killed character and end combat for ally characters should be handled by another component
        # Remove dead character corpse
        target_faction = killed_character.get_faction()
        killed_character_id = killed_character.get_info().id
        killed_character.set_status("dead")
        tile_id = killed_character.tile_id
        tile = store.get(EntityType.TILE, tile_id)
        tile.remove_character_id(killed_character_id)

        self.remove_character_id(target_faction, killed_character_id)

        # if len(self.get_character_ids_with_faction(target_faction)) == 0:
        #     self.exit_combat_faction(character.get_faction())
        #     return True

        # return False

    def get_hostile_power(self, faction):
        store = get_store()
        other_factions = [f for f in self.character_faction_ids.keys() if f != faction]
        sum_power = 0
        # Calculate total power of factions, that hostile with the target faction
        for other_faction in other_factions:
            character_of_faction = store.get(
                EntityType.CHARACTER, self.character_faction_ids[other_faction][0]
            )
            # TODO: create faction class that can get hostile faction directly
            if character_of_faction.is_hostile_with(faction):
                sum_power += self.get_total_power_by_faction(other_faction)
        return sum_power

    def get_total_power_by_faction(self, faction):
        store = get_store()
        sum_power = 0
        for cid in self.character_faction_ids[faction]:
            power = store.get(
                EntityType.CHARACTER,
                cid,
            ).get_power()
            sum_power += power
        return sum_power

    def to_dict(self):
        return {
            "id": self.id,
            "type": "event",
            "event_type": "combat",
            "data": {
                faction: self.character_faction_ids[faction]
                for faction in self.character_faction_ids.keys()
            },
        }

    # @staticmethod
    # def execute(first_character, second_character):
    #     logger.debug(
    #         f"Combat between {first_character.get_info()} and {second_character.get_info()}"
    #     )
    #     while first_character.is_alive() and second_character.is_alive():
    #         first_character.character_stats.update_stat(
    #             StatDefinition.HEALTH,
    #             -second_character.character_stats.get_stat(StatDefinition.POWER).value,
    #         )
    #         second_character.character_stats.update_stat(
    #             StatDefinition.HEALTH,
    #             -first_character.character_stats.get_stat(StatDefinition.POWER).value,
    #         )
    #     dead_character = (
    #         first_character if not first_character.is_alive() else second_character
    #     )
    #     alive_character = (
    #         first_character if first_character.is_alive() else second_character
    #     )
    #     is_level_up = alive_character.level.add_exp(
    #         dead_character.level.class_level.get_next_level_required_exp(
    #             dead_character.level.current_level
    #         )
    #     )
    #     if is_level_up:
    #         alive_character.level_up()
    #     logger.debug(f"{alive_character.get_info()} won")

    #     store = get_store()
    #     # store.remove(EntityType.CHARACTER, dead_character.get_info().id)
    #     dead_character.set_status("dead")
    #     tile_id = dead_character.tile_id
    #     tile = store.get(EntityType.TILE, tile_id)
    #     tile.remove_character_id(dead_character.get_info().id)


class CollectEvent(Event):
    def __init__(self) -> None:
        super().__init__()


class TrainingEvent(Event):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def execute(character):
        max_health = character.character_stats.get_stat(StatDefinition.MAX_HEALTH).value
        character.character_stats.update_stat(
            StatDefinition.CURRENT_HEALTH, int(max_health / 10)
        )
        is_level_up = character.level.add_exp(100)
        if is_level_up:
            character.level_up()


class RestingEvent(Event):
    def __init__(self) -> None:
        super().__init__()
