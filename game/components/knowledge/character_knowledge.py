from enum import Enum

from components.knowledge.knowledge import (
    AttributeToGoalKnowledge,
    AttributeCapToGoalKnowledge,
    KnowledgeType,
    Knowledge,
)


# TODO: NEED TO THINK MORE, CURRENTLY LOOK RESTRICTED
class CharacterKnowledge:
    def __init__(self):
        self.knowledges = {}
        self.init_base_knowledges()

    def init_base_knowledges(self):
        self.knowledges[KnowledgeType.INCREASE_ATTRIBUTE_GOAL] = (
            AttributeToGoalKnowledge()
        )
        self.knowledges[KnowledgeType.INCREASE_ATTRIBUTE_CAP_GOAL] = (
            AttributeCapToGoalKnowledge()
        )

    def has_knowledge_with_type(self, knowledge_type: KnowledgeType) -> bool:
        return knowledge_type in self.knowledges

    def get_knowledge_with_type(self, knowledge_type: KnowledgeType) -> Knowledge:
        return self.knowledges[knowledge_type]
