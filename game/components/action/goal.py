from components.character.character_action import (
    ActionType,
    CharacterActionModifyReason,
)
from components.action.action import ActionResult
from components.item.item import Rarity, ItemType
from components.item.equipment import DamagedAncientArmor, DamagedAncientSword

from data.logs.logger import logger


class Goal:
    def __init__(self) -> None:
        pass

    def is_complete(self, character):
        pass

    def can_apply_to(self, character):
        pass

    def apply_to_actions(self, character):
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


class TrainingGoal(Goal):
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
        character.add_goal(
            1, FightingGoal(**{"target_level": character.get_current_level() + 1})
        )

    def can_apply_to(self, character):
        return character.get_character_action().has_action(ActionType.TRAIN)

    def apply_to_actions(self, character):
        character.get_character_action().modify_probabilities(
            ActionType.TRAIN, 5, CharacterActionModifyReason.APPLY_GOAL
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
            ActionType.MOVE, 5, CharacterActionModifyReason.APPLY_GOAL
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
            f"Item {item.get_name()} is satisfied with the goal to collect items with type={self.target_item_types}, rarity>={self.target_rarity}"
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
        if character.get_last_action_result() is ActionResult.SUCCESS_FIND_ITEM:
            recently_collected_item_names = (
                character.get_recently_added_inventory_item_names()
            )
            if recently_collected_item_names:
                for recently_collected_item_name in recently_collected_item_names:
                    if recently_collected_item_name in self.target_items.keys():
                        self.target_items.pop(recently_collected_item_name)
                        self.collected_item_name.append(recently_collected_item_name)
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
    #         ActionType.MOVE, 5, CharacterActionModifyReason.APPLY_GOAL
    #     )

    # def __str__(self):
    #     return f"{self.get_name()} for Level {self.target_level}"
