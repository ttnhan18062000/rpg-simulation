from enum import Enum

from components.character.character_action import (
    ActionType,
    CharacterActionModifyReason,
)
from components.action.action import ActionResult
from components.item.item import Rarity, ItemType
from components.item.equipment import DamagedAncientArmor, DamagedAncientSword

from data.logs.logger import logger


class Goal:
    # TODO: Allow multiple goals added, for the case of Archetype Unlocking
    unique = False

    def __init__(self) -> None:
        self.applied_to_character = False
        pass

    def is_complete(self, character):
        pass

    def is_block(self, character):
        return False

    def resolve_block(self, character):
        self.on_complete(character)
        lowest_priority = self.add_resolve_block_goals(character)
        character.add_goal(lowest_priority, self)

    def add_resolve_block_goals(self, character):
        pass

    def is_applied_to_character(self):
        return self.applied_to_character

    def set_applied_to_character(self):
        self.applied_to_character = True

    @classmethod
    def is_unique(cls):
        return cls.unique

    def can_apply_to(self, character):
        pass

    def apply_to_actions(self, character):
        pass

    def apply_to_character(self, character):
        pass

    def on_complete(self, character):
        character.get_character_action().reset_probabilities(
            CharacterActionModifyReason.APPLY_GOAL
        )

    @classmethod
    def is_finding_item(cls):
        return False

    @classmethod
    def get_name(cls):
        return cls.__name__

    def __str__(self):
        return "Goal"

    def update_with_goal(self, other_goal):
        pass


class TrainingGoal(Goal):
    target_level_key = "target_level"

    # TODO: need refactor to use the target_level_key
    # Keep training until reach a given level
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.target_level = kwargs.get("target_level")

    def is_complete(self, character):
        return character.get_level().get_current_level() >= self.target_level

    def on_complete(self, character):
        character.get_character_action().reset_probabilities(
            CharacterActionModifyReason.APPLY_GOAL
        )
        # character.add_goal(
        #     1, FightingGoal(**{"target_level": character.get_current_level() + 1})
        # )

    def can_apply_to(self, character):
        return character.get_character_action().has_action(ActionType.TRAIN)

    def apply_to_actions(self, character):
        character.get_character_action().modify_probabilities(
            ActionType.TRAIN, 80, "fixed", CharacterActionModifyReason.APPLY_GOAL
        )

    def __str__(self):
        return f"{self.get_name()} for Level {self.target_level}"


class FightingGoal(Goal):
    # Keep training until reach a given level
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.target_level = kwargs.get("target_level")

    def is_complete(self, character):
        return character.get_level().get_current_level() >= self.target_level

    def on_complete(self, character):
        character.get_character_action().reset_probabilities(
            CharacterActionModifyReason.APPLY_GOAL
        )
        # TODO: Just for testing, change later
        # Currently is if the character strong enough, they need to find better equipments
        if character.get_current_level() >= 3:
            character.add_goal(
                1,
                FindingItemGoal(
                    **{
                        "target_items": {},
                        "target_item_types": [ItemType.EQUIPMENT],
                        "target_rarity": Rarity.UNCOMMON,
                    }
                ),
            )
        else:
            character.add_goal(
                1, FightingGoal(**{"target_level": character.get_current_level() + 1})
            )

    def can_apply_to(self, character):
        return character.get_character_action().has_action(ActionType.MOVE)

    def apply_to_actions(self, character):
        character.get_character_action().modify_probabilities(
            ActionType.MOVE, 80, "fixed", CharacterActionModifyReason.APPLY_GOAL
        )

    def __str__(self):
        return f"{self.get_name()} for Level {self.target_level}"


class FindingItemGoal(Goal):
    # Keep training until reach a given level
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.target_items = kwargs.get("target_items", {})
        self.target_item_types = kwargs.get("target_item_types", [])
        self.target_rarity = kwargs.get("target_rarity", Rarity.COMMON)
        self.collected_item_name = []

    @classmethod
    def is_finding_item(cls):
        return True

    def get_target_item_types(self):
        return self.target_item_types

    def get_target_rarity(self):
        return self.target_rarity

    # Check if the item's rarity and type satisfy the target items to collect of the goal
    def is_item_satisfy_goal(self, item):
        if item.get_type() not in self.target_item_types:
            return False
        if item.get_final_rarity() < self.target_rarity:
            return False
        logger.debug(
            f"Item {item.get_name()} is satisfied with the goal to collect items with type={[item_type.name for item_type in self.target_item_types]}, rarity>={self.target_rarity.name}"
        )
        return True

    # Check if either the tile contain specific items in the target items, or match the types and rarity
    def is_collectable_items_match(self, items_list):
        for collectable_item in items_list:
            for item_name in self.target_items.keys():
                if item_name == collectable_item.get_name():
                    return True
            # TODO: Currently the character SHOULD know the list of collectable item when step on it
            # We should use the properties of the tile, instead of the direct information of the items
            if self.is_item_satisfy_goal(collectable_item):
                return True

        return False

    # User want to get better equipment in the tile
    # when see the tile at close range, user know what are the exact equipments can be dropped
    # TODO: May this won't work for stackable item, when user need to collect a bunch of resource
    def add_item_to_goal(self, item):
        item_name = item.get_name()
        if item_name in self.collected_item_name:
            logger.debug(f"Item {item_name} is already collected")
        elif item_name not in self.target_items:
            self.target_items[item_name] = item
            logger.debug(f"Added {item_name} to the FindingItemGoal goal")

    # TODO: Later change to find the specific items
    def is_complete(self, character):

        if character.is_just_act(ActionResult.SUCCESS_FIND_ITEM):
            recently_collected_item_names = (
                character.get_recently_added_inventory_item_names()
            )
            if recently_collected_item_names:
                for recently_collected_item_name in recently_collected_item_names:
                    if recently_collected_item_name in self.target_items.keys():
                        self.target_items.pop(recently_collected_item_name)
                        self.collected_item_name.append(recently_collected_item_name)
                character.clear_recently_added_inventory_item_names()
            if len(self.target_items.keys()) == 0:
                return True
        return False

    # TODO: Take a deeper look at this, FindingItem goal complete -> reset character action to basic
    def on_complete(self, character):
        character.reset_to_basic_character_action()

    # def can_apply_to(self, character):
    #     return character.get_character_action().has_action(ActionType.MOVE)

    # def apply_to_actions(self, character):
    #     character.get_character_action().modify_probabilities(
    #         ActionType.MOVE, 5, "multiply", CharacterActionModifyReason.APPLY_GOAL
    #     )

    def __str__(self):
        return f"{self.get_name()} for Item {self.target_items}"


class RecoveryGoal(Goal):
    target_debuff_classes_key = "debuff"
    target_health_ratio_key = "health_ratio"
    # recovery_targets_key = "recovery_targets"

    # class RecovertyTarget(Enum):
    #     HEALTH = 1
    #     DEBUFF = 2

    # kwargs:
    # {target_debuff_classes_key: [status_class.INJURY], target_health_ratio_key: 0.9}

    # Keep recover until no longer has debuff or fully health
    def __init__(self, **kwargs) -> None:
        super().__init__()
        # self.recovery_targets = kwargs.get(RecoveryGoal.recovery_targets_key)
        self.target_debuff_classes = kwargs.get(
            RecoveryGoal.target_debuff_classes_key, None
        )
        self.target_health_ratio = kwargs.get(
            RecoveryGoal.target_health_ratio_key, None
        )

    def is_complete(self, character):
        if self.target_debuff_classes:
            for target_debuff_class in self.target_debuff_classes:
                if character.get_character_status().has_status_class(
                    target_debuff_class
                ):
                    return False
        if self.target_health_ratio:
            if (
                character.get_character_stat().get_health_ratio()
                < self.target_health_ratio
            ):
                return False
        return True

    def on_complete(self, character):
        character.get_character_action().reset_probabilities(
            CharacterActionModifyReason.APPLY_GOAL
        )

    def can_apply_to(self, character):
        return character.get_character_action().has_action(ActionType.RECOVER)

    def apply_to_actions(self, character):
        character.get_character_action().modify_probabilities(
            ActionType.RECOVER, 100, "fixed", CharacterActionModifyReason.APPLY_GOAL
        )

    def update_with_goal(self, other_goal):
        # Add debuff classes not in the goal target
        if other_goal.target_debuff_classes:
            if not self.target_debuff_classes:
                self.target_debuff_classes = []
            for debuff_class in other_goal.target_debuff_classes:
                if debuff_class not in self.target_debuff_classes:
                    self.target_debuff_classes.append(debuff_class)

        # Update the higher target health ratio
        if other_goal.target_health_ratio:
            if not self.target_health_ratio:
                self.target_health_ratio = 0
            if other_goal.target_health_ratio > self.target_health_ratio:
                self.target_health_ratio = other_goal.target_health_ratio

    def __str__(self):
        return f"{self.get_name()} for Debuff {[dc.name for dc in self.target_debuff_classes]}, Health ratio {self.target_health_ratio}"
