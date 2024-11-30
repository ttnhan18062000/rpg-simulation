from components.character.character_action import (
    ActionType,
    CharacterActionModifyReason,
)


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
        return f"TrainingGoal for Level {self.target_level}"


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
        return f"TrainingGoal for Level {self.target_level}"
