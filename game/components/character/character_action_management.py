from components.character.character_action import (
    CharacterAction,
    BasicCharacterAction,
    CombatCharacterAction,
    CharacterActionModifyReason,
)

from components.character.character_goal import CharacterGoalStatus, CharacterGoal


from data.logs.logger import logger


class CharacterActionManagement:
    def __init__(self, character_goal) -> None:
        self.character_action: CharacterAction = None
        self.character_goal: CharacterGoal = character_goal

    def get_character_action(self):
        return self.character_action

    def set(self, character_action: CharacterAction, character):
        if self.character_action:
            self.character_action.on_change()
        if self.character_goal.is_already_applied_goal():
            self.character_goal.reset_status_to_waiting()

        self.character_action = character_action
        self.on_start_character_action(character)

        logger.debug(
            f"{character.get_info()} has changed character action to {character_action.get_name()}"
        )

    def check_and_apply_goal(self, character):
        if self.character_goal.is_waiting_to_apply():
            self.character_goal.apply_goal(character)

    def on_start_character_action(self, character):
        self.check_and_apply_goal(character)

    def on_new_goal_added(self, character):
        self.check_and_apply_goal(character)

    def on_goal_completed(self, character):
        self.check_and_apply_goal(character)
