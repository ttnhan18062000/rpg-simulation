from components.character.character_action import (
    ActionType,
    CharacterActionModifyReason,
)

from components.action.action import ActionResult

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
        # self.target_level = kwargs.get("target_level")

    # TODO: Later change to find the specific items
    def is_complete(self, character):
        return character.get_last_action_result() is ActionResult.SUCCESS_FIND_ITEM

    # def on_complete(self, character):
    #     character.get_character_action().reset_probabilities(
    #         CharacterActionModifyReason.APPLY_GOAL
    #     )
    #     character.add_goal(
    #         1, FightingGoal(**{"target_level": character.get_current_level() + 1})
    #     )

    # def can_apply_to(self, character):
    #     return character.get_character_action().has_action(ActionType.MOVE)

    # def apply_to_actions(self, character):
    #     character.get_character_action().modify_probabilities(
    #         ActionType.MOVE, 5, CharacterActionModifyReason.APPLY_GOAL
    #     )

    # def __str__(self):
    #     return f"{self.get_name()} for Level {self.target_level}"
