from enum import Enum

from components.attribute.attribute import Attribute
from components.action.action import Action
from components.action.goal.basic_development_goal import AttributeTrainingGoal
from components.action.goal.goal import TrainingGoal


class KnowledgeType(Enum):
    INCREASE_ATTRIBUTE_GOAL = 1
    INCREASE_ATTRIBUTE_CAP_GOAL = 2


# TODO: NEED TO THINK MORE, CURRENTLY LOOK RESTRICTED
class Knowledge:
    # TODO: Need to find a better way to access the key for specific knowledge (assume not knowing itself, just the KnowledgeType)
    INCREASE_ATTRIBUTE_GOAL_KEY = "source_attribute"
    INCREASE_ATTRIBUTE_CAP_GOAL_KEY = "target_level"

    def __init__(self):
        pass

    @classmethod
    def get_goal(cls, character, **kwargs):
        pass

    @classmethod
    def get_name(cls):
        return cls.__name__


class AttributeToGoalKnowledge(Knowledge):

    def __init__(self):
        pass

    @classmethod
    def get_goal(cls, character, **kwargs):
        attr = kwargs.get(AttributeToGoalKnowledge.AttributeToGoalKnowledge_key)
        return AttributeTrainingGoal(
            **{AttributeTrainingGoal.target_attribute_key: attr}
        )


class AttributeCapToGoalKnowledge(Knowledge):

    def __init__(self):
        pass

    @classmethod
    def get_goal(cls, character, **kwargs):
        # target_level = kwargs.get(
        #     AttributeToGoalKnowledge.AttributeCapToGoalKnowledge_key
        # )
        return TrainingGoal(
            **{TrainingGoal.target_level_key: character.get_current_level() + 1}
        )
