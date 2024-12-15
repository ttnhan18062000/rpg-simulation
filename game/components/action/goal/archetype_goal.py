from components.action.goal.goal import Goal
from components.character.character_action import (
    ActionType,
    CharacterActionModifyReason,
)
from components.archetype.skill.skill import Skill, SkillMastery

from data.logs.logger import logger


class UnlockArchetypeGoal(Goal):
    target_archetype_key = "target_archetype"
    unique = True
    # kwargs:
    # {target_archetype_key: SwordTrainee}

    # Unlock a archetype
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.target_archetype = kwargs.get(UnlockArchetypeGoal.target_archetype_key)

    def get_target_archetype(self):
        return self.target_archetype

    def is_complete(self, character):
        return (
            character.has_archetype(self.target_archetype)
            or self.is_applied_to_character()
        )

    def on_complete(self, character):
        pass

    def can_apply_to(self, character):
        return True

    def apply_to_actions(self, character):
        pass

    def apply_to_character(self, character):
        character.add_archetype(self.target_archetype)
        self.set_applied_to_character()

    def update_with_goal(self, other_goal):
        pass

    def __str__(self):
        return f"{self.get_name()} for unlocking Archetype {self.target_archetype}"

    def __eq__(self, other):
        # Custom equality: Check if the names are the same
        if isinstance(other, UnlockArchetypeGoal):
            return self.target_archetype == other.target_archetype
        return False


class LearningSkillGoal(Goal):
    target_skills_key = "skill"
    # kwargs:
    # {target_skill_key: SlashSkill}

    # Learn a specific skill
    def __init__(self, **kwargs) -> None:
        super().__init__()
        # self.recovery_targets = kwargs.get(RecoveryGoal.recovery_targets_key)
        self.target_skill = kwargs.get(LearningSkillGoal.target_skills_key)

    def get_target_skill(self):
        return self.target_skill

    def is_complete(self, character):
        return (
            character.get_skill(self.target_skill).get_mastery()
            == SkillMastery.BEGINNER
        )

    def on_complete(self, character):
        character.get_character_action().reset_probabilities(
            CharacterActionModifyReason.APPLY_GOAL
        )

    def can_apply_to(self, character):
        return character.get_character_action().has_action(ActionType.LEARN_SKILL)

    def apply_to_actions(self, character):
        character.get_character_action().modify_probabilities(
            ActionType.LEARN_SKILL, 100, "fixed", CharacterActionModifyReason.APPLY_GOAL
        )

    def apply_to_character(self, character):
        character.add_skill(self.target_skill())
        self.set_applied_to_character()

    def update_with_goal(self, other_goal):
        pass

    def __str__(self):
        return f"{self.get_name()} for learning skill {self.target_skill.get_name()}"
