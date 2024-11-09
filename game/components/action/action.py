import random

from components.world.store import get_store, EntityType
from components.common.point import Point
from components.action.event import Event, CombatEvent, TrainingEvent, EventType
from components.character.character_stat import StatDefinition
from components.common.path_finding import get_move_to_target
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

    def random_move(self, character):
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
        if not self.check_valid_step(character.pos + next_move):
            return self.random_move(character)
        return next_move

    def get_next_move(self, character):
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
                    if character.is_hostile_with(other_character):
                        return get_move_to_target(character.pos, other_character.pos)

        # Not found any enemy, random movement
        return self.random_move(character)

    def do_action(self, character, **kwargs):

        store = get_store()

        next_move = self.get_next_move(character)

        previous_tile_id = store.get(EntityType.GRID, 0).get_tile(character.pos)
        previous_tile = store.get(EntityType.TILE, previous_tile_id)
        previous_tile.remove_character_id(character.get_info().id)

        character.pos += next_move
        new_tile_id = store.get(EntityType.GRID, 0).get_tile(character.pos)
        new_tile = store.get(EntityType.TILE, new_tile_id)
        new_tile.add_character_id(character.get_info().id)
        character.tile_id = new_tile.id

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
        # store = get_store()
        # target_character_ids = kwargs.get("target_character_ids")
        # # TODO: smarter target selection
        # target_character_id = random.choice(target_character_ids)
        # target_character = store.get(EntityType.CHARACTER, target_character_id)
        # target_character.character_stats.update_stat(
        #     StatDefinition.HEALTH,
        #     -character.character_stats.get_stat(StatDefinition.POWER).value,
        # )
        # logger.debug(f"{character.get_info()} hit {target_character.get_info()}")
        # if not target_character.is_alive():
        #     logger.debug(f"{character.get_info()} killed {target_character.get_info()}")
        #     is_level_up = character.level.add_exp(
        #         target_character.level.class_level.get_next_level_required_exp(
        #             target_character.level.current_level
        #         )
        #     )
        #     if is_level_up:
        #         character.level_up()

        #     # Remove dead character corpse
        #     target_character.set_status("dead")
        #     tile_id = target_character.tile_id
        #     tile = store.get(EntityType.TILE, tile_id)
        #     tile.remove_character_id(target_character.get_info().id)

        #     target_character_ids.remove(target_character_id)

        #     if len(target_character_ids) == 0:
        #         character.exit_combat()
        #         return True

        # return False

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

            combat_event.remove_character_id(target_faction, target_character_id)

            if len(combat_event.get_character_ids_with_faction(target_faction)) == 0:
                combat_event.exit_combat_faction(character.get_faction())
                return True

        return False


class Escape(Action):
    action_name = "Escape"

    def do_action(self, character, **kwargs):
        return False
