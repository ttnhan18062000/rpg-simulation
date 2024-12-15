# from components.global_object.world_notification import (
#     get_world_notification_manager,
#     WorldNotificationType,
# )
from components.common.point import Point
from components.common.game_object import GameObject
from components.action.event import Event, CombatEvent, TrainingEvent, EventType
from components.action.strategy.base_strategy import BaseStrategy
from components.action.action import ActionResult
from components.action.goal.goal import RecoveryGoal
from components.action.goal.archetype_goal import UnlockArchetypeGoal, LearningSkillGoal
from components.action.goal.basic_development_goal import AttributeTrainingGoal
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
from components.attribute.attribute import AttributeProficiencyResult, Attribute
from components.attribute.character_attribute import CharacterAttribute
from components.character.character_status import CharacterStatus
from components.character.status import LightInjury, HeavyInjury
from components.race.race import Race
from components.archetype.character_archetype import CharacterArchetype
from components.archetype.archetype import Mob, Player, Archetype
from components.character.character_level import CharacterLevel
from components.character.character_vision import CharacterVision
from components.character.character_power import CharacterPower
from components.memory.character_memory import CharacterMemory
from components.character.character_behavior import FightingBehavior
from components.action.goal.character_goal import CharacterGoal

from components.knowledge.character_knowledge import CharacterKnowledge
from components.knowledge.knowledge import Knowledge, KnowledgeType

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
        race: Race,
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
        self.race = race
        self.character_archetype = CharacterArchetype()
        self.character_vision = CharacterVision(5)
        self.level = CharacterLevel(race.class_level, level)
        self.character_memory = CharacterMemory()

        self.character_goal = CharacterGoal()

        self.character_knowledge = CharacterKnowledge()

        self.character_action_management = CharacterActionManagement(
            self.character_goal
        )
        self.character_action_management.set(BasicCharacterAction(), self)
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

    # -------------------- INFORMATION, RACE, STATE ----------------------------------------------------------

    def get_location(self):
        return self.pos

    def get_info(self):
        return self.character_info

    def get_id(self):
        return self.character_info.id

    def get_race(self):
        return self.race.__class__.__name__

    def get_hostile_races(self):
        return self.race.get_hostile_races()

    def get_restricted_tile_types(self):
        return self.race.get_restricted_tile_types()

    def get_character_knowledge(self):
        return self.character_knowledge

    def is_alive(self):
        return (
            not self.is_dead
            and self.character_stats.get_stat(StatDefinition.CURRENT_HEALTH).value > 0
        )

    # TODO: Better management state
    def set_state(self, state):
        if state == "dead":
            self.is_dead = True

    def is_hostile_with(self, character: "Character"):
        hostile_races = self.race.get_hostile_races()
        if isinstance(character, Character):
            return character.get_race() in hostile_races
        if isinstance(character, str):
            return character in hostile_races
        raise NotImplemented

    # Same faction can fight each other if need
    def is_ally_with(self, character: "Character"):
        friendly_races = self.race.get_friendly_races()
        if isinstance(character, Character):
            return character.get_race() in friendly_races
        if isinstance(character, str):
            return character in friendly_races
        raise NotImplemented

    # -------------------- COMPONENTS ----------------------------------------------------------

    def get_character_stat(self):
        return self.character_stats

    def get_character_attributes(self):
        return self.character_attributes

    def get_level(self):
        return self.level

    def get_memory(self):
        return self.character_memory

    def get_character_status(self):
        return self.character_status

    def get_character_equipment(self):
        return self.character_equipment

    def get_character_inventory(self):
        return self.character_inventory

    # -------------------- VISION & LOCATION ----------------------------------------------------------

    def get_vision(self):
        return self.character_vision

    def get_visible_tiles(self):
        return self.character_vision.get_visible_tiles(self.get_pos())

    def get_visible_tile_objects(self):
        return self.character_vision.get_visible_tile_objects(self.get_pos())

    def set_vision_range(self, vision_range: int):
        self.character_vision.set_range(vision_range)

    # -------------------- STATS & ATTRIBUTES ----------------------------------------------------------

    def get_final_stat(self):
        return self.get_character_stat().get_final_stat(self)

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
            # => Already did in resolve_block_if_have in goal
            pass

    def on_character_attribute_changed(self):
        # self.get_character_stat().apply_character_attributes(
        #     self.get_character_attributes()
        # )
        pass

    # -------------------- LEVEL ----------------------------------------------------------

    def get_current_level(self):
        return self.level.get_current_level()

    def level_up(self):
        logger.debug(
            f"{self.get_info()} level up, before attributes: {self.get_character_attributes()}"
        )
        self.get_character_attributes().modify_caps(self.race.get_attributes_cap_gain())
        logger.debug(
            f"{self.get_info()} leveled up, after attributes: {self.get_character_attributes()}"
        )

    def gain_experience(self, exp_value: int):
        is_level_up = self.level.add_exp(exp_value)
        if is_level_up:
            self.level_up()

    # -------------------- POWER ----------------------------------------------------------

    def get_power(self):
        return CharacterPower.get_power(self.get_final_stat())

    def get_max_power(self):
        return CharacterPower.get_max_power(self.get_final_stat())

    def get_detailed_power(self):
        return CharacterPower.get_detailed_character_power(self)

    # -------------------- ACTION ----------------------------------------------------------

    def update_action_percentage(self, action_percentage: float):
        self.action_percentage = action_percentage

    def get_character_action(self):
        return self.character_action_management.get_character_action()

    def set_character_action(self, character_action):
        self.character_action_management.set(character_action, self)

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
            # TODO: Later add more complexity or consider about refactoring
            # TODO: NOT APPLY to mobs
            self.add_goal(
                1,
                RecoveryGoal(
                    **{
                        RecoveryGoal.target_debuff_classes_key: [
                            HeavyInjury.get_status_class()
                        ],
                        RecoveryGoal.target_health_ratio_key: 0.95,
                    }
                ),
            )
        elif health_ratio < 0.5:
            logger.debug(
                f"{self.get_info()} suffered from LightInjury after exit combat"
            )
            self.character_status.add_status(LightInjury(5))
            self.add_goal(
                1,
                RecoveryGoal(
                    **{
                        RecoveryGoal.target_debuff_classes_key: [
                            LightInjury.get_status_class()
                        ],
                        RecoveryGoal.target_health_ratio_key: 0.95,
                    }
                ),
            )
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

        # Decrease all statuses' duration by one, only for status that can be expired overtime
        self.character_status.change_duration(-1)

        # Check goal is done yet
        if self.character_goal.has_goal():
            self.check_done_current_goal()
            self.resolve_goal_block_if_have()

    def on_moving_into_new_tile(self, new_tile: Tile):
        store = get_store()
        # Enter a tile that holding a combat event
        if new_tile.is_combat_happen():
            combat_event_id = new_tile.get_event(EventType.COMBAT)
            combat_event: CombatEvent = store.get(EntityType.EVENT, combat_event_id)
            all_factions = combat_event.get_factions()
            for hostile_faction in self.get_hostile_races():
                if hostile_faction in all_factions:
                    combat_event.add_hostile_faction(self.get_race(), hostile_faction)
                    combat_event.add_character_id(self.get_race(), self.get_info().id)
                    self.enter_combat(combat_event_id)
                    return False, [ActionResult.JOIN_COMBAT]

        # Enter a tile with other characters standing on it, may cause a combat event happen
        all_characters = [
            store.get(EntityType.CHARACTER, cid)
            for cid in new_tile.get_character_ids()
            if cid != self.get_info().id
        ]
        hostile_faction_to_characters = {}
        for hostile_faction in self.get_hostile_races():
            hostile_faction_to_characters[hostile_faction] = []
            for other_character in all_characters:
                if other_character.get_race() == hostile_faction:
                    hostile_faction_to_characters[hostile_faction].append(
                        other_character
                    )
        for hostile_faction in self.get_hostile_races():
            if len(hostile_faction_to_characters[hostile_faction]) > 0:
                new_combat_event: CombatEvent = CombatEvent(new_tile.get_id())
                new_combat_event_id = new_combat_event.id
                character_faction = self.get_race()

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

    def reset_to_basic_character_action(self):
        self.set_character_action(BasicCharacterAction())

    def get_character_action_type(self):
        return self.get_character_action().__class__.__name__

    # -------------------- MEMORY ----------------------------------------------------------

    # -------------------- STRATEGY ----------------------------------------------------------

    def get_strategy(self, strategy_type: CharacterStrategyType):
        return self.character_strategy.get(strategy_type)

    def add_strategy(
        self, strategy_type: CharacterStrategyType, strategy: BaseStrategy
    ):
        self.character_strategy.add(strategy_type, strategy)

    # -------------------- BEHAVIOR ----------------------------------------------------------

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

    # -------------------- GOAL ----------------------------------------------------------

    def add_goal(self, priority: int, goal):
        priority = self.character_goal.add(priority, goal)
        if priority <= 1:
            self.character_action_management.on_new_goal_added(self)
        return priority

    def has_goal(self):
        return self.character_goal.has_goal()

    def get_current_goal(self):
        return self.character_goal.get_current_goal()

    def clear_current_goal(self):
        self.character_goal.clear_current_goal()

    def check_done_current_goal(self):
        is_done = self.character_goal.check_done_current_goal(self)
        if is_done:
            self.character_action_management.on_goal_completed(self)

    def resolve_goal_block_if_have(self):
        is_blocked = self.character_goal.check_block_current_goal(self)
        if is_blocked:
            # TODO: RETHINK IF THE LOGIC IS WRONG
            # get current goal -> clear it -> resolve to readd the goal and then required goals
            # The expected priority required goals first, then the blocked goal
            current_goal = self.get_current_goal()

            self.clear_current_goal()

            current_goal.resolve_block(self)

    # -------------------- INVENTORY & EQUIPMENT ----------------------------------------------------------

    def get_recently_added_inventory_item_names(self):
        return self.character_inventory.get_recently_added_item_names()

    def clear_recently_added_inventory_item_names(self):
        return self.character_inventory.clear_recently_added_item_names()

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

    # -------------------- ARCHETYPE & RACE ----------------------------------------------------------

    def is_mob(self):
        return self.character_archetype.is_archetype(Mob)

    def get_race(self):
        return self.race.__class__.__name__

    def get_archetypes(self):
        return self.character_archetype.get_archetypes()

    def get_archetype_names(self):
        return self.character_archetype.get_archetype_names()

    def has_archetype(self, archetype):
        return self.character_archetype.has_archetype(archetype)

    def is_able_to_unlock_archetype(self, archetype):
        return self.character_archetype.is_able_to_unlock_archetype(self, archetype)

    def add_archetype(self, archetype: Archetype):
        is_able_to_unlock, requires = self.is_able_to_unlock_archetype(archetype)
        if is_able_to_unlock:
            self.character_archetype.add_archetype(archetype)
            # TODO: Learn skills by decisions/strategies/goals
            # TODO: Think about which skills to learn first, priority, ignore, etc.
            learnable_skills = archetype.get_learnable_skills()
            for skill in learnable_skills:
                self.add_goal(
                    1, LearningSkillGoal(**{LearningSkillGoal.target_skills_key: skill})
                )
        else:
            # TODO: Add goals or decisions to complete the conditions

            # TODO: Re-add the archetype as goal first, to later push by other smaller goals
            self.add_goal(
                1,
                UnlockArchetypeGoal(
                    **{UnlockArchetypeGoal.target_archetype_key: archetype}
                ),
            )

            reason_string = [f"{key.name}: {value}" for key, value in requires.items()]
            logger.debug(
                f"{self.get_info()} cannot unlock Archetype {archetype.get_name()}, requiments has not met: {reason_string}"
            )
            required_attrs = requires.get(Archetype.UnlockType.REQUIRE_ATTRIBUTES, None)
            if required_attrs:
                for attr in required_attrs:
                    self.add_goal(
                        1,
                        AttributeTrainingGoal(
                            **{AttributeTrainingGoal.target_attribute_key: attr}
                        ),
                    )

    def add_skill(self, skill):
        self.character_archetype.add_skill(skill)

    def get_all_skills(self):
        return self.character_archetype.get_all_skills()

    def get_skill(self, skill):
        return self.character_archetype.get_skill(skill)

    def has_skill(self, skill):
        return self.character_archetype.has_skill(skill)

    def gain_mastery_proficiency(self, skill, mastery_point: int):
        return self.character_archetype.gain_mastery_proficiency(skill, mastery_point)

    # -------------------- DRAWING & DISPLAY ----------------------------------------------------------

    def should_redraw(self):
        return self.is_just_changed_location

    def set_redraw_status(self, status):
        self.is_just_changed_location = status

    def add_status(self, status):
        self.character_status.add_status(status)

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
            f"Archetypes: {self.character_archetype} | "
            f"Skills: {self.character_archetype.get_skill_names_string()} | "
            f"Power: {self.get_power()} ({self.get_max_power()}) | "
            f"HP    : {self.get_character_stat().get_health_visualization()} {self.get_character_stat().get_stat_value(StatDefinition.CURRENT_HEALTH)}/{self.get_character_stat().get_stat_value(StatDefinition.MAX_HEALTH)} | "
            f"Energy: {self.get_character_stat().get_energy_visualization()} {self.get_character_stat().get_stat_value(StatDefinition.CURRENT_ENERGY)}/{self.get_character_stat().get_stat_value(StatDefinition.MAX_ENERGY)} | "
            f"{self.get_character_attributes()} | "
            f"Goal: {self.get_current_goal().get_name() if self.character_goal.has_goal() else ''} | "
            f"{self.get_character_equipment()} | "
            f"Status: {self.get_character_status()}"
        )

    # TODO: Need update
    def to_dict(self):
        return {
            "id": self.get_info().id,
            "type": "character",
            "info": str(self.get_info()),
            "faction": self.get_race(),
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
