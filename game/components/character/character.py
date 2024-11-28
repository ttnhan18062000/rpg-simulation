from components.common.point import Point
from components.common.game_object import GameObject
from components.character.character_info import CharacterInfo
from components.character.character_action import (
    CharacterAction,
    BasicCharacterAction,
    CombatCharacterAction,
)
from components.character.character_strategy import (
    CharacterStrategy,
    CharacterStrategyType,
)
from components.action.strategy.base_strategy import BaseStrategy
from components.character.character_stat import CharacterStat, StatDefinition
from components.character.character_status import CharacterStatus
from components.character.status import LightInjury, HeavyInjury
from components.character.character_class import CharacterClass
from components.character.character_level import CharacterLevel
from components.character.character_vision import CharacterVision
from components.character.character_power import CharacterPower
from components.character.memory.character_memory import CharacterMemory
from components.character.character_behavior import FightingBehavior
from components.character.character_goal import CharacterGoal
from components.world.store import get_store, EntityType

from data.logs.logger import logger


class Character(GameObject):
    def __init__(
        self,
        pos: Point,
        img: str,
        character_info: CharacterInfo,
        character_stats: CharacterStat,
        character_class: CharacterClass,
        level: int,
    ):
        super().__init__(pos, img)
        self.pos = pos
        self.img = img
        self.character_info = character_info
        self.character_action = BasicCharacterAction()
        self.character_strategy = CharacterStrategy()
        self.character_stats = character_stats
        self.character_status = CharacterStatus()
        self.character_class = character_class
        self.character_vision = CharacterVision(5)
        self.level = CharacterLevel(character_class.class_level, level)
        self.character_memory = CharacterMemory()
        self.character_goal = CharacterGoal()
        self.behaviors = {}
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

    def get_character_stat(self):
        return self.character_stats

    def get_status_applied_character_stat(self):
        if self.character_status.is_empty():
            return self.get_character_stat()
        return self.character_stats.get_applied_statuses_character_stat(
            self.character_status
        )

    def get_vision(self):
        return self.character_vision

    def get_faction(self):
        return self.character_class.__class__.__name__

    def get_hostile_factions(self):
        return self.character_class.get_hostile_factions()

    def get_power(self):
        return CharacterPower.get_power(self.get_status_applied_character_stat())

    def get_memory(self):
        return self.character_memory

    def get_level(self):
        return self.level

    def get_restricted_tile_types(self):
        return self.character_class.get_restricted_tile_types()

    def get_strategy(self, strategy_type: CharacterStrategyType):
        return self.character_strategy.get(strategy_type)

    def add_strategy(
        self, strategy_type: CharacterStrategyType, strategy: BaseStrategy
    ):
        self.character_strategy.add(strategy_type, strategy)

    def add_goal(self, priority: int, goal):
        self.character_goal.add(priority, goal)

    def get_current_goal(self):
        return self.character_goal.get_current_goal()

    def complete_goal(self):
        self.character_goal.complete_goal()

    def is_alive(self):
        return (
            not self.is_dead
            and self.character_stats.get_stat(StatDefinition.CURRENT_HEALTH).value > 0
        )

    def set_status(self, status):
        if status == "dead":
            self.is_dead = True

    def set_vision_range(self, vision_range: int):
        self.character_vision.set_range(vision_range)

    def set_character_action(self, character_action: CharacterAction):
        self.character_action = character_action

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
        for stat_def, value in self.character_class.stats_gain.items():
            self.character_stats.update_stat(stat_def, value)
        logger.debug(f"f{self.get_info()} has leveled up: {self.get_power()}")

    def do_action(self):
        if self.is_just_changed_location == False:
            self.is_just_changed_location = self.character_action.do_action(self)

        # Decrease all statuses' duration by one
        self.character_status.change_duration(-1)

    def should_redraw(self):
        return self.is_just_changed_location

    def set_redraw_status(self, status):
        self.is_just_changed_location = status

    def add_status(self, status):
        self.character_status.add_status(status)

    def exit_combat(self):
        # TODO: critical health should depend on characteristic
        # TODO: refactor for a module that manage the status applying
        health_ratio = self.get_status_applied_character_stat().get_health_ratio()
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
        self.character_action = BasicCharacterAction()
        self.set_redraw_status(True)

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

    def enter_combat(self, combat_event_id, target_faction):
        self.character_action = CombatCharacterAction(
            **{
                "combat_event_id": combat_event_id,
                "target_faction": target_faction,
                FightingBehavior.name: self.get_behavior(FightingBehavior.name),
            }
        )

    def get_character_action_type(self):
        return self.character_action.__class__.__name__

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
