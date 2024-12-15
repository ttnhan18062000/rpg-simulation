from components.action.goal.goal import Goal
from components.character.character_action import (
    ActionType,
    CharacterActionModifyReason,
)

from data.logs.logger import logger


class AttributeTrainingGoal(Goal):
    target_attribute_key = "target_attribute"
    # kwargs:
    # {target_attribute_key: Strength(value)}

    # Learn a specific skill
    def __init__(self, **kwargs) -> None:
        super().__init__()
        # self.recovery_targets = kwargs.get(RecoveryGoal.recovery_targets_key)
        self.target_attribute = kwargs.get(AttributeTrainingGoal.target_attribute_key)

    def get_target_attribute(self):
        return self.target_attribute

    def is_complete(self, character):
        return (
            character.get_character_attributes()
            .get_base_attr(self.target_attribute.get_name())
            .get_value()
            >= self.target_attribute.get_value()
        )

    def on_complete(self, character):
        character.get_character_action().reset_probabilities(
            CharacterActionModifyReason.APPLY_GOAL
        )
        character.get_character_action().reset_kwargs_key(
            AttributeTrainingGoal.target_attribute_key
        )

    def is_block(self, character):
        character_attr = character.get_character_attributes().get_base_attr(
            self.target_attribute.get_name()
        )
        if character_attr.is_capped():
            logger.debug(
                f"Attribute {character_attr} of the character reached the cap, but require {self.target_attribute}"
            )
            return True
        return False

    def add_resolve_block_goals(self, character):
        from components.knowledge.knowledge import KnowledgeType

        logger.debug(
            f"{self.get_name()} is currently blocked due to capped Attribute {self.target_attribute}"
        )

        # TODO: is_increased let character know it already maxed out or not
        # later we can change goal when maxed out proficiency
        knowledge_increase_attr_cap = (
            character.get_character_knowledge().get_knowledge_with_type(
                KnowledgeType.INCREASE_ATTRIBUTE_CAP_GOAL
            )
        )
        increase_attr_cap_goal = knowledge_increase_attr_cap.get_goal(character)
        logger.debug(
            f"Resolve block of {self.get_name()} with character knowledge {knowledge_increase_attr_cap.get_name()}, that add the {increase_attr_cap_goal.get_name()}"
        )
        priority = character.add_goal(1, increase_attr_cap_goal)
        return priority

    def can_apply_to(self, character):
        return character.get_character_action().has_action(ActionType.TRAIN)

    def apply_to_actions(self, character):
        character.get_character_action().modify_probabilities(
            ActionType.TRAIN, 100, "fixed", CharacterActionModifyReason.APPLY_GOAL
        )
        character.get_character_action().set_kwargs(
            AttributeTrainingGoal.target_attribute_key, self.target_attribute
        )

    def update_with_goal(self, other_goal):
        pass

    def __str__(self):
        return f"{self.get_name()} for Attribute {self.target_attribute.get_name()}({self.target_attribute.get_value()})"
