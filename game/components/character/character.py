# from components.global_object.world_notification import (
#     get_world_notification_manager,
#     WorldNotificationType,
# )
from components.common.point import Point
from components.common.game_object import GameObject
from components.action.event import Event, CombatEvent, TrainingEvent, EventType
from components.action.strategy.base_strategy import BaseStrategy
from components.action.action import ActionResult
from components.world.tile import Tile
from components.character.character_info import CharacterInfo
from components.character.character_action_management import CharacterActionManagement
from components.character.character_action import (
    CharacterAction,
    BasicCharacterAction,
    CombatCharacterAction,
    CharacterActionModifyReason,
    FindItemCharacterAction,
)
from components.character.character_strategy import (
    CharacterStrategy,
    CharacterStrategyType,
)
from components.character.character_stat import CharacterStat, StatDefinition
from components.attribute.attribute import AttributeProficiencyResult
from components.attribute.character_attribute import CharacterAttribute
from components.character.character_status import CharacterStatus
from components.character.status import LightInjury, HeavyInjury
from components.character.character_class import CharacterClass
from components.character.character_level import CharacterLevel
from components.character.character_vision import CharacterVision
from components.character.character_power import CharacterPower
from components.character.memory.character_memory import CharacterMemory
from components.character.character_behavior import FightingBehavior
from components.character.character_goal import CharacterGoal

from components.character.character_inventory import CharacterInventory, OnAddItemAction
from components.character.character_equipment import CharacterEquipment

from components.world.store import get_store, EntityType

from components.utils.visualization_converter import convert_to_progress_string

from data.logs.logger import logger


class Character(GameObject):
    def __init__(
        self,
        pos: Point,
        img: str,
        character_info: CharacterInfo,
        # character_stats: CharacterStat,
        character_attributes: CharacterAttribute,
        character_class: CharacterClass,
        level: int,
    ):
        super().__init__(pos, img)
        self.pos = pos
        self.img = img
        self.action_percentage = 0
        self.character_info = character_info
        self.character_strategy = CharacterStrategy()
        # self.character_stats = character_stats
        self.character_attributes = character_attributes
        self.character_stats = CharacterStat(character_attr=character_attributes)
        self.character_status = CharacterStatus()
        self.character_class = character_class
        self.character_vision = CharacterVision(5)
        self.level = CharacterLevel(character_class.class_level, level)
        self.character_memory = CharacterMemory()
        self.character_goal = CharacterGoal()
        self.character_action_management = CharacterActionManagement(
            self.character_goal
        )
        self.behaviors = {}

        self.character_inventory = CharacterInventory()
        self.character_equipment = CharacterEquipment()

        self.is_dead = False

        store = get_store()
        self.tile_id = store.get(EntityType.GRID, 0).tiles[pos.x][pos.y]
        tile = store.get(EntityType.TILE, self.tile_id)
        tile.add_character_id(character_info.id)

        self.is_just_changed_location = True

        logger.debug(f"{self.get_info()} has {self.get_power()} power")

    def get_location(self):
        return self.pos

    def get_info(self):
        return self.character_info

    def get_id(self):
        return self.character_info.id

    def get_character_stat(self):
        return self.character_stats

    def get_character_attributes(self):
        return self.character_attributes

    def get_final_stat(self):
        return self.get_character_stat().get_final_stat(self)

    def get_vision(self):
        return self.character_vision

    def get_visible_tiles(self):
        return self.character_vision.get_visible_tiles(self.get_pos())

    def get_faction(self):
        return self.character_class.__class__.__name__

    def get_hostile_factions(self):
        return self.character_class.get_hostile_factions()

    def get_power(self):
        return CharacterPower.get_power(self.get_final_stat())

    def get_max_power(self):
        return CharacterPower.get_max_power(self.get_final_stat())

    def get_detailed_power(self):
        return CharacterPower.get_detailed_character_power(self)

    def get_memory(self):
        return self.character_memory

    def get_level(self):
        return self.level

    def get_current_level(self):
        return self.level.get_current_level()

    def get_restricted_tile_types(self):
        return self.character_class.get_restricted_tile_types()

    def get_strategy(self, strategy_type: CharacterStrategyType):
        return self.character_strategy.get(strategy_type)

    def get_character_status(self):
        return self.character_status

    def get_character_equipment(self):
        return self.character_equipment

    def get_recently_added_inventory_item_names(self):
        return self.character_inventory.get_recently_added_item_names()

    def clear_recently_added_inventory_item_names(self):
        return self.character_inventory.clear_recently_added_item_names()

    def update_action_percentage(self, action_percentage: float):
        self.action_percentage = action_percentage

    def add_item(self, item):
        on_add_item_action = self.character_inventory.add_item(item)
        if on_add_item_action is OnAddItemAction.CAN_EQUIP_ITEM:
            (
                before_power,
                after_power,
            ) = CharacterPower.get_character_before_and_after_equip_equipment(
                self, item
            )
            if after_power > before_power:
                logger.debug(
                    f"The new collected equipment {item.get_name()} is stronger than current, apply it"
                )
                self.equip(item)
        elif on_add_item_action is OnAddItemAction.CAN_CONSUME_ITEM:
            pass

    def equip(self, equipment):
        equipment_name = equipment.get_name()
        if not self.get_character_inventory().get_item(equipment_name):
            raise Exception(
                f"Equipment {equipment_name} is not found in the character {self.get_info()} inventory"
            )
        self.get_character_inventory().remove_item(equipment_name)
        self.get_character_equipment().equip(equipment)
        logger.debug(f"Character equipped {equipment.get_name()}")
        # get_world_notification_manager().publish(
        #     WorldNotificationType.CHARACTER.CHANGE_INFO, self.get_id()
        # )

    def get_character_inventory(self):
        return self.character_inventory

    def add_strategy(
        self, strategy_type: CharacterStrategyType, strategy: BaseStrategy
    ):
        self.character_strategy.add(strategy_type, strategy)

    def add_goal(self, priority: int, goal):
        self.character_goal.add(priority, goal)
        self.character_action_management.on_new_goal_added(self)

    def has_goal(self):
        return self.character_goal.has_goal()

    def get_current_goal(self):
        return self.character_goal.get_current_goal()

    def check_done_current_goal(self):
        is_done = self.character_goal.check_done_current_goal(self)
        if is_done:
            self.character_action_management.on_goal_completed(self)

    def is_alive(self):
        return (
            not self.is_dead
            and self.character_stats.get_stat(StatDefinition.CURRENT_HEALTH).value > 0
        )

    def is_mob(self):
        return self.character_class.is_mob()

    def get_character_class_name(self):
        return self.character_class.__class__.__name__

    # TODO: Better management state
    def set_state(self, state):
        if state == "dead":
            self.is_dead = True

    def set_vision_range(self, vision_range: int):
        self.character_vision.set_range(vision_range)

    def get_character_action(self):
        return self.character_action_management.get_character_action()

    def set_character_action(self, character_action):
        self.character_action_management.set(character_action, self)

    def is_hostile_with(self, character: "Character"):
        hostile_factions = self.character_class.get_hostile_factions()
        if isinstance(character, Character):
            return character.character_class.__class__.__name__ in hostile_factions
        if isinstance(character, str):
            return character in hostile_factions
        raise NotImplemented

    # Same faction can fight each other if need
    def is_ally_with(self, character: "Character"):
        ally_factions = self.character_class.get_ally_factions()
        if isinstance(character, Character):
            return character.character_class.__class__.__name__ in ally_factions
        if isinstance(character, str):
            return character in ally_factions
        raise NotImplemented

    def level_up(self):
        logger.debug(
            f"{self.get_info()} level up, before attributes: {self.get_character_attributes()}"
        )
        self.get_character_attributes().modify_caps(
            self.character_class.get_attributes_cap_gain()
        )
        logger.debug(
            f"{self.get_info()} leveled up, after attributes: {self.get_character_attributes()}"
        )

    def gain_proficiency(self, attr_name: str, value: int):
        attr = self.get_character_attributes().get_base_attr(attr_name)
        attr_prof_result: AttributeProficiencyResult = attr.increase_proficiency(value)
        if attr_prof_result is AttributeProficiencyResult.IS_LEVELED_UP:
            new_stat_gained = attr.clone()
            new_stat_gained.set_value(1)
            self.get_character_stat().update_stat_with_new_attribute_gained(
                new_stat_gained
            )
            logger.debug(f"The attribute {attr_name} is leveled up {attr.get_info()}")
        if attr_prof_result is AttributeProficiencyResult.IS_CAPPED:
            logger.debug(
                f"The attribute {attr_name} is reaching its cap {attr.get_cap()}"
            )
            # TODO: is_increased let character know it already maxed out or not
            # later we can change goal when maxed out proficiency
            pass

    def gain_experience(self, exp_value: int):
        is_level_up = self.level.add_exp(exp_value)
        if is_level_up:
            self.level_up()

    def enter_combat(self, combat_event_id):
        self.set_character_action(
            CombatCharacterAction(
                **{
                    "combat_event_id": combat_event_id,
                    FightingBehavior.name: self.get_behavior(FightingBehavior.name),
                }
            )
        )

    def exit_combat(self):
        # TODO: critical health should depend on characteristic
        # TODO: refactor for a module that manage the status applying
        health_ratio = self.get_final_stat().get_health_ratio()
        if health_ratio < 0.25:
            logger.debug(
                f"{self.get_info()} suffered from HeavyInjury after exit combat"
            )
            self.character_status.add_status(HeavyInjury(5))
        elif health_ratio < 0.5:
            logger.debug(
                f"{self.get_info()} suffered from LightInjury after exit combat"
            )
            self.character_status.add_status(LightInjury(5))
        self.set_character_action(BasicCharacterAction())
        self.set_redraw_status(True)

    def get_last_action_results(self):
        return self.get_character_action().get_last_action_results()

    def add_last_action_result(self, action_result: ActionResult):
        self.get_character_action().add_last_action_result(action_result)

    def is_just_act(self, action_result: ActionResult):
        last_action_results = self.get_character_action().get_last_action_results()
        if last_action_results:
            return action_result in last_action_results
        return None

    def is_just_moved(self):
        return self.is_just_act(ActionResult.MOVED_INTO_NEW_TILE)

    def do_action(self):
        is_just_changed_location = self.get_character_action().do_action(self)

        if self.is_just_changed_location == False:
            self.is_just_changed_location = is_just_changed_location

        # Decrease all statuses' duration by one
        self.character_status.change_duration(-1)

        # Check goal is done yet
        if self.character_goal.has_goal():
            self.check_done_current_goal()

    def on_moving_into_new_tile(self, new_tile: Tile):
        store = get_store()
        # Enter a tile that holding a combat event
        if new_tile.is_combat_happen():
            combat_event_id = new_tile.get_event(EventType.COMBAT)
            combat_event: CombatEvent = store.get(EntityType.EVENT, combat_event_id)
            all_factions = combat_event.get_factions()
            for hostile_faction in self.get_hostile_factions():
                if hostile_faction in all_factions:
                    combat_event.add_hostile_faction(
                        self.get_faction(), hostile_faction
                    )
                    combat_event.add_character_id(
                        self.get_faction(), self.get_info().id
                    )
                    self.enter_combat(combat_event_id)
                    return False, [ActionResult.JOIN_COMBAT]

        # Enter a tile with other characters standing on it, may cause a combat event happen
        all_characters = [
            store.get(EntityType.CHARACTER, cid)
            for cid in new_tile.get_character_ids()
            if cid != self.get_info().id
        ]
        hostile_faction_to_characters = {}
        for hostile_faction in self.get_hostile_factions():
            hostile_faction_to_characters[hostile_faction] = []
            for other_character in all_characters:
                if other_character.get_faction() == hostile_faction:
                    hostile_faction_to_characters[hostile_faction].append(
                        other_character
                    )
        for hostile_faction in self.get_hostile_factions():
            if len(hostile_faction_to_characters[hostile_faction]) > 0:
                new_combat_event: CombatEvent = CombatEvent(new_tile.get_id())
                new_combat_event_id = new_combat_event.id
                character_faction = self.get_faction()

                new_combat_event.add_hostile_faction(character_faction, hostile_faction)

                for enemy_character in hostile_faction_to_characters[hostile_faction]:
                    new_combat_event.add_character_id(
                        hostile_faction, enemy_character.get_info().id
                    )
                    enemy_character.enter_combat(new_combat_event_id)

                new_combat_event.add_character_id(character_faction, self.get_info().id)
                self.enter_combat(new_combat_event_id)

                store.add(EntityType.EVENT, new_combat_event_id, new_combat_event)

                return False, [ActionResult.START_COMBAT]

        # Enter a collectable_items tile, and current goal is collect items, match the target items
        # => Change to FindItemCharacterAction
        # Checking current goal
        if self.has_goal():
            current_goal = self.get_current_goal()
            # FindingItemGoal
            if current_goal.is_finding_item():
                collectable_item_list = list(new_tile.get_collectable_items().keys())
                if (
                    new_tile.is_collectable()
                    and current_goal.is_collectable_items_match(collectable_item_list)
                ):
                    # Add more target items if satisfy the goal and can be collected in the tile
                    for collectable_item in collectable_item_list:
                        if current_goal.is_item_satisfy_goal(collectable_item):
                            current_goal.add_item_to_goal(collectable_item)
                    self.set_character_action(
                        FindItemCharacterAction(**{"max_attempt": 5})
                    )
                elif (
                    self.get_character_action().get_name()
                    == FindItemCharacterAction.get_name()
                ):
                    # TODO: Think about the better approach to end the FindItemCharacterAction action
                    self.set_character_action(BasicCharacterAction())

        return True, []

    def on_character_attribute_changed(self):
        # self.get_character_stat().apply_character_attributes(
        #     self.get_character_attributes()
        # )
        pass

    def reset_to_basic_character_action(self):
        self.set_character_action(BasicCharacterAction())

    def should_redraw(self):
        return self.is_just_changed_location

    def set_redraw_status(self, status):
        self.is_just_changed_location = status

    def add_status(self, status):
        self.character_status.add_status(status)

    def get_behaviors(self):
        return self.behaviors

    def get_behavior(self, key):
        if key in self.behaviors:
            return self.behaviors[key]
        return None

    def add_behavior(self, key, behavior):
        logger.debug(
            f"{self.get_info()} added behavior '{key}':'{behavior.__class__.__name__}'"
        )
        self.behaviors[key] = behavior

    def get_character_action_type(self):
        return self.get_character_action().__class__.__name__

    def get_action_percentage_visualization(self):
        progress_string = convert_to_progress_string(
            percentage=(1 - self.action_percentage), block_length=20
        )
        return progress_string

    def get_exp_visualization(self):
        return self.get_level().get_exp_visualization()

    def get_character_detailed_info_string(self):
        # TODO: Some like equipments and buffs should be displayed as icon instead of raw text
        return (
            f"Action: {self.get_action_percentage_visualization()} | "
            f"{self.get_info()} LVL {self.get_current_level()} {self.get_exp_visualization()} | "
            f"Power: {self.get_power()} ({self.get_max_power()}) | "
            f"HP: {self.get_character_stat().get_health_visualization()} {self.get_character_stat().get_stat_value(StatDefinition.MAX_HEALTH)} | "
            f"{self.get_character_attributes()} | "
            f"Goal: {self.get_current_goal().get_name() if self.character_goal.has_goal() else ''} | "
            f"{self.get_character_equipment()} | "
            f"Status: {self.get_character_status()}"
        )

    def to_dict(self):
        return {
            "id": self.get_info().id,
            "type": "character",
            "info": str(self.get_info()),
            "faction": self.get_faction(),
            "is_alive": self.is_alive(),
            "stats": {
                "current_health": self.character_stats.get_stat(
                    StatDefinition.CURRENT_HEALTH
                ).value,
                "max_health": self.character_stats.get_stat(
                    StatDefinition.MAX_HEALTH
                ).value,
                "power": self.character_stats.get_stat(StatDefinition.POWER).value,
                "speed": self.character_stats.get_stat(StatDefinition.SPEED).value,
            },
            "level": {
                "current_level": self.level.current_level,
                "current_exp": self.level.current_exp,
                "next_level_exp": self.level.next_level_required_exp,
            },
            "tile_id": self.tile_id,
            "character_action": self.get_character_action_type(),
        }
