import random

from components.world.store import get_store, EntityType
from components.common.point import Point
from components.action.event import Event, CombatEvent, TrainingEvent, EventType
from components.character.character_stat import StatDefinition
from components.common.path_finding import get_move_to_target
from components.character.memory.memory import MemoryCharacter, PowerEst
from data.logs.logger import logger


class Action:
    action_name = "Action"

    @classmethod
    def do_action(cls, character):
        pass

    @classmethod
    def execute(cls, character, **kwargs):
        logger.debug(f"{character.get_info()} do {Action.action_name}")
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
                        character, other_character, perception_accuracy=90
                    )
                    character.get_memory().add(EntityType.CHARACTER, cid, memory)


class Move(Action):
    action_name = "Move"

    @staticmethod
    def check_valid_step(new_pos: Point):
        store = get_store()
        tile_id = store.get(EntityType.GRID, 0).get_tile(new_pos)
        tile = store.get(EntityType.TILE, tile_id)
        if tile.is_obstacle():
            return False
        return tile

    @staticmethod
    def random_move(character):
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
        if not Move.check_valid_step(character.pos + next_move):
            return Move.random_move(character)
        return next_move

    @staticmethod
    def get_next_move(character, is_random_move=False):
        if not is_random_move:
            characters_in_memory = character.get_memory().get_all(EntityType.CHARACTER)
            for memory_character in characters_in_memory:
                if character.is_hostile_with(
                    memory_character.get_faction()
                ) and memory_character.get_power_est() in [
                    PowerEst.MUCH_WEAKER,
                    PowerEst.WEAKER,
                ]:
                    logger.debug(
                        f"{character.get_info()}:{character.get_power()} is chasing {memory_character.get_power_est()}"
                    )
                    return get_move_to_target(
                        character.pos, memory_character.get_location()
                    )
                # TODO: Run if the enemy is much stronger
                # TODO: Add characteristic

        # Not found any enemy or is_random_move, random movement
        return Move.random_move(character)

    @classmethod
    def do_action(cls, character, **kwargs):

        store = get_store()

        if kwargs.get("random_move"):
            next_move = Move.get_next_move(character, is_random_move=True)
        else:
            next_move = Move.get_next_move(character, is_random_move=False)

        previous_tile_id = store.get(EntityType.GRID, 0).get_tile(character.pos)
        previous_tile = store.get(EntityType.TILE, previous_tile_id)
        previous_tile.remove_character_id(character.get_info().id)

        character.pos += next_move
        new_tile_id = store.get(EntityType.GRID, 0).get_tile(character.pos)
        new_tile = store.get(EntityType.TILE, new_tile_id)
        new_tile.add_character_id(character.get_info().id)
        character.tile_id = new_tile.id

        # Enter a tile that holding a combat event
        if new_tile.is_combat_happen():
            combat_event_id = new_tile.get_event(EventType.COMBAT)
            combat_event: CombatEvent = store.get(EntityType.EVENT, combat_event_id)
            all_factions = combat_event.get_factions()
            for hostile_faction in character.get_hostile_factions():
                if hostile_faction in all_factions:
                    combat_event.add_character_id(
                        character.get_faction(), character.get_info().id
                    )
                    character.enter_combat(combat_event_id, hostile_faction)
                    return False

        # Enter a tile with other characters standing on it, may cause a combat event happen
        all_characters = [
            store.get(EntityType.CHARACTER, cid)
            for cid in new_tile.get_character_ids()
            if cid != character.get_info().id
        ]
        hostile_faction_to_characters = {}
        for hostile_faction in character.get_hostile_factions():
            hostile_faction_to_characters[hostile_faction] = []
            for other_character in all_characters:
                if other_character.get_faction() == hostile_faction:
                    hostile_faction_to_characters[hostile_faction].append(
                        other_character
                    )
        for hostile_faction in character.get_hostile_factions():
            if len(hostile_faction_to_characters[hostile_faction]) > 0:
                new_combat_event: CombatEvent = CombatEvent(new_tile_id)
                new_combat_event_id = new_combat_event.id
                for enemy_character in hostile_faction_to_characters[hostile_faction]:
                    new_combat_event.add_character_id(
                        hostile_faction, enemy_character.get_info().id
                    )
                    enemy_character.enter_combat(
                        new_combat_event_id, character.get_faction()
                    )

                new_combat_event.add_character_id(
                    character.get_faction(), character.get_info().id
                )
                character.enter_combat(new_combat_event_id, hostile_faction)

                store.add(EntityType.EVENT, new_combat_event_id, new_combat_event)

                return False

        # for other_character in other_characters:
        #     if character.is_hostile_with(other_character):
        #         # CombatEvent().execute(character, other_character)
        #         character.enter_combat([other_character.get_info().id])
        #         other_character.enter_combat([character.get_info().id])
        #         # Create a combat event to manage all the characters from Human/Demon
        #         # Dead characters remove from the event -> update all targets -> won't kill the already dead characters
        #         return True

        return True


class Interact(Action):
    action_name = "Interact"

    @classmethod
    def do_action(cls, character, **kwargs):
        return False


class Standby(Action):
    action_name = "Standby"

    @classmethod
    def do_action(cls, character, **kwargs):
        TrainingEvent().execute(character)
        return False


class Fight(Action):
    action_name = "Fight"

    @classmethod
    def do_action(cls, character, **kwargs):
        store = get_store()
        target_faction = kwargs.get("target_faction")
        combat_event_id = kwargs.get("combat_event_id")
        combat_event: CombatEvent = store.get(EntityType.EVENT, combat_event_id)
        target_character_ids = combat_event.get_character_ids_with_faction(
            target_faction
        )
        # TODO: smarter target selection
        target_character_id = random.choice(target_character_ids)
        target_character = store.get(EntityType.CHARACTER, target_character_id)
        target_character.character_stats.update_stat(
            StatDefinition.CURRENT_HEALTH,
            -character.character_stats.get_stat(StatDefinition.POWER).value,
        )
        logger.debug(f"{character.get_info()} hit {target_character.get_info()}")
        if not target_character.is_alive():
            combat_event.kill_character(character, target_character)
            # is_end_combat = combat_event.kill_character(character, target_character)
            # return is_end_combat

        return False


class Escape(Action):
    action_name = "Escape"

    @classmethod
    def do_action(cls, character, **kwargs):
        store = get_store()

        combat_event_id = kwargs.get("combat_event_id")
        combat_event: CombatEvent = store.get(EntityType.EVENT, combat_event_id)

        total_hostile_power = combat_event.get_hostile_power(character.get_faction())
        character_power = character.get_power()
        escape_chance = 0.3
        if total_hostile_power > 3 * character_power:
            escape_chance = 0.05
        elif total_hostile_power < character_power:
            escape_chance = 0.9

        if random.random() < escape_chance:
            logger.debug(f"{character.get_info()} escape successfully")
            character_id = character.get_info().id
            combat_event.remove_character_id(character.get_faction(), character_id)

            character.exit_combat()

            # TODO: Random move (should trigger the Move class function => convert Move into classmethod?)
            Move.do_action(character, **{"random_move": True})

            return True

        logger.debug(f"{character.get_info()} escape failed")
        return False
