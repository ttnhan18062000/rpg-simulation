import random
import numpy
from enum import Enum
import copy

from components.common.damage_formula import get_final_damage_output
from components.world.store import get_store, EntityType
from components.common.point import Point
from components.action.event import Event, CombatEvent, TrainingEvent, EventType
from components.character.character_stat import StatDefinition
from components.common.path_finding import (
    get_move_from_target,
    check_valid_step,
)
from components.character.memory.memory import (
    MemoryCharacter,
    MemoryEvent,
    PowerEst,
    MemoryTile,
)
from components.character.memory.character_memory import CharacterMemoryType
from components.utils.tile_utils import get_tile_object
from components.character.character_strategy import CharacterStrategyType
from components.attribute.attribute import Vitality, Endurance, Strength, Agility
from data.logs.logger import logger
from data.game_settings import ACTION


class ActionResult(Enum):
    START_COMBAT = 1
    JOIN_COMBAT = 2
    SUCCESS_ESCAPE_COMBAT = 3
    FAIL_ESCAPE_COMBAT = 4
    SUCCESS_FIND_ITEM = 5
    FAIL_FIND_ITEM = 6
    TRAINED = 7
    HIT_ENEMY = 8


class Action:
    action_name = "Action"

    @classmethod
    def do_action(cls, character, **kwargs):
        pass

    @classmethod
    def execute(cls, character, **kwargs):
        if not character.is_mob():
            # TODO: The total power should be total value of three powers, this for validation
            (
                base_stat_power,
                equipment_power,
                status_power,
            ) = character.get_detailed_power()
            total_power = character.get_power()
            logger.debug(
                f"{character.get_info()} do {cls.action_name}. Stat: base='{base_stat_power}' equipment='{equipment_power}' status='{status_power}' total='{total_power}'"
            )
        cls.inspect_around(character)
        return cls.do_action(character, **kwargs)

    @classmethod
    def inspect_around(cls, character):
        # TODO: instead of reset memory every action, better delete only old memories, or wrong memories
        # like doesn't see the remembered character at the location (they already escaped)

        character.get_memory().reset()
        store = get_store()
        visible_points = character.get_vision().get_visible_tiles(character.pos)
        for point in visible_points:
            tile_id = store.get(EntityType.GRID, 0).get_tile(point)
            tile = store.get(EntityType.TILE, tile_id)

            # Remember the tile permanently
            # TODO: Beware of too much data copied, when character remember/store the whole map
            # TODO: we should remember the tile status at the moment (use copy) instead of something like store the tile_id.
            # To make case like character A remember the item then the item is taken by another character B, A doesn't know until he check the tile again
            memory_tile = MemoryTile(tile_id, point, copy.deepcopy(tile))
            character.get_memory().add(
                EntityType.TILE, tile_id, memory_tile, CharacterMemoryType.PERMANENT
            )

            # Examine combat event on visible tiles
            if tile.is_combat_happen():
                combat_id = tile.get_event(EventType.COMBAT)
                combat = store.get(EntityType.EVENT, combat_id)
                if character.get_faction() in combat.get_factions():
                    memory = MemoryEvent(combat_id, point, event_type=EventType.COMBAT)
                    memory.remember_power(character, combat, perception_accuracy=90)
                    character.get_memory().add(
                        EntityType.EVENT,
                        combat_id,
                        memory,
                        CharacterMemoryType.TEMPORARY,
                    )

            # Examine character powers on visible tiles
            character_ids_on_tile = store.get(
                EntityType.TILE, tile_id
            ).get_character_ids()
            if len(character_ids_on_tile) > 0:
                for cid in character_ids_on_tile:
                    other_character = store.get(EntityType.CHARACTER, cid)
                    memory = MemoryCharacter(
                        cid, other_character.pos, other_character.get_faction()
                    )
                    memory.remember_power(
                        character,
                        other_character,
                        perception_accuracy=ACTION.BASE_POWER_PERCEPTION_ACCURACY,
                    )
                    character.get_memory().add(
                        EntityType.CHARACTER, cid, memory, CharacterMemoryType.TEMPORARY
                    )

        # Increase proficiency
        # TODO: Increase something like Sensitive, currently not implemented


class Move(Action):
    action_name = "Move"

    @classmethod
    def do_action(cls, character, **kwargs):
        store = get_store()

        next_move = character.get_strategy(CharacterStrategyType.Move).get_next_move(
            character
        )

        previous_tile = get_tile_object(character.pos)
        previous_tile.remove_character_id(character.get_info().id)

        # Perform move, move into tile and trigger following logics
        character.pos += next_move
        new_tile = get_tile_object(character.pos)
        new_tile.character_move_in(character)
        character.tile_id = new_tile.id

        # Increase proficiency
        character.gain_proficiency(Agility.get_name(), 10)

        return character.on_moving_into_new_tile(new_tile)


class Search(Action):
    action_name = "Search"

    @classmethod
    def do_action(cls, character, **kwargs):
        # Increase proficiency
        # TODO: increase something like dexterity, currently not implemented yet

        success_chance = 0.25  # TODO: this should based on character's attribute
        if random.random() < success_chance:
            current_tile = get_tile_object(character.pos)
            collectable_items = current_tile.get_collectable_items()
            received_item = numpy.random.choice(
                list(collectable_items.keys()),
                p=list(collectable_items.values()),
            )
            character.add_item(received_item)
            logger.debug(f"{character.get_info()} collected {received_item.get_name()}")
            return True, ActionResult.SUCCESS_FIND_ITEM

        logger.debug(f"{character.get_info()} Search failed")
        return False, ActionResult.FAIL_FIND_ITEM


class Interact(Action):
    action_name = "Interact"

    @classmethod
    def do_action(cls, character, **kwargs):
        # Increase proficiency
        # TODO: increase something like charisma, currently not implemented yet
        return False


class Train(Action):
    action_name = "Train"

    @classmethod
    def do_action(cls, character, **kwargs):
        TrainingEvent().execute(character)
        character.gain_proficiency(Vitality.get_name(), 20)
        character.gain_proficiency(Strength.get_name(), 10)
        character.gain_proficiency(Endurance.get_name(), 5)
        character.gain_proficiency(Agility.get_name(), 5)
        return False, ActionResult.TRAINED


class Standby(Action):
    action_name = "Standby"

    @classmethod
    def do_action(cls, character, **kwargs):
        return False, None


class Fight(Action):
    action_name = "Fight"

    @classmethod
    def do_action(cls, character, **kwargs):
        store = get_store()
        combat_event_id = kwargs.get("combat_event_id")
        combat_event: CombatEvent = store.get(EntityType.EVENT, combat_event_id)
        charcter_faction = character.get_faction()
        # TODO: Proritize factions or specific targets
        target_character_ids = combat_event.get_target_character_ids_of_faction(
            charcter_faction
        )
        # TODO: smarter target selection
        target_character_id = random.choice(target_character_ids)
        target_character = store.get(EntityType.CHARACTER, target_character_id)
        target_character.character_stats.update_stat(
            StatDefinition.CURRENT_HEALTH,
            -character.character_stats.get_stat(StatDefinition.POWER).value,
        )
        character_power = character.character_stats.get_stat_value(StatDefinition.POWER)
        target_character_defense = target_character.character_stats.get_stat_value(
            StatDefinition.DEFENSE
        )
        damage_dealt = get_final_damage_output(
            source_power=character_power,
            target_defense=target_character_defense,
        )
        target_character_remaining_health = target_character.character_stats.get_stat(
            StatDefinition.CURRENT_HEALTH
        ).value

        # Increase proficiency
        character.gain_proficiency(Strength.get_name(), 20)
        target_character.gain_proficiency(Endurance.get_name(), 20)

        logger.debug(
            f"{character.get_info()}:POWER{character_power} hit {target_character.get_info()}:DEFENSE{target_character_defense} for {damage_dealt} damage, left {target_character_remaining_health} HP"
        )
        if not target_character.is_alive():
            combat_event.kill_character(character, target_character)
            # is_end_combat = combat_event.kill_character(character, target_character)
            # return is_end_combat

        # There is a twist, if the combat is over, the combat_event will reset the redraw status (True)
        # but if we return True here, it will be replaced and not drawing the character
        return character.should_redraw(), ActionResult.HIT_ENEMY


class Escape(Action):
    action_name = "Escape"

    @classmethod
    def do_action(cls, character, **kwargs):
        store = get_store()

        combat_event_id = kwargs.get("combat_event_id")
        combat_event: CombatEvent = store.get(EntityType.EVENT, combat_event_id)

        total_hostile_power = combat_event.get_hostile_power(character.get_faction())
        character_power = character.get_power()
        escape_chance = ACTION.BASE_ESCAPE_CHANCE
        if total_hostile_power > ACTION.LOW_ESCAPE_POWER_THRESHOLD * character_power:
            escape_chance = ACTION.LOW_ESCAPE_CHANCE
        elif total_hostile_power < ACTION.HIGH_ESCAPE_POWER_THRESHOLD * character_power:
            escape_chance = ACTION.HIGH_ESCAPE_CHANCE

        # Increase proficiency
        character.gain_proficiency(Agility.get_name(), 20)

        if random.random() < escape_chance:
            logger.debug(f"{character.get_info()} escape successfully")
            character_id = character.get_info().id
            combat_event.remove_character_id(character.get_faction(), character_id)

            character.exit_combat()

            Move.do_action(
                character, **{"action_result": ActionResult.SUCCESS_ESCAPE_COMBAT}
            )

            return True, ActionResult.SUCCESS_ESCAPE_COMBAT

        logger.debug(f"{character.get_info()} escape failed")
        return False, ActionResult.FAIL_ESCAPE_COMBAT
