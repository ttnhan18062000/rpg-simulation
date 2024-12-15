from components.archetype.archetype import Archetype
from components.archetype.skill.character_skill import CharacterSkill

from data.logs.logger import logger


class CharacterArchetype:
    def __init__(self):
        self.archetypes = []
        self.character_skill = CharacterSkill()

    def is_able_to_unlock_archetype(self, character, archetype: Archetype):
        return archetype.is_able_to_unlock(character)

    def has_archetype(self, archetype: Archetype):
        return archetype in self.archetypes

    def add_archetype(self, archetype: Archetype):
        if self.has_archetype(archetype):
            raise Exception(f"{archetype.get_name()} already existed in {self}")
        self.archetypes.append(archetype)
        logger.debug(f"Added Achertype {archetype.get_name()}")

    def get_archetypes(self):
        return self.archetypes

    def get_archetype_names(self):
        return [a.get_name() for a in self.archetypes]

    def is_archetype(self, archetype: Archetype):
        return archetype.get_name() in self.get_archetype_names()

    def get_character_skill(self):
        return self.character_skill

    def get_all_skills(self):
        return self.character_skill.get_skills()

    def get_skill_names_string(self):
        return " ".join(self.character_skill.get_skill_names())

    def get_skill(self, skill):
        return self.character_skill.get_skill(skill)

    def add_skill(self, skill):
        return self.character_skill.add_skill(skill)

    def has_skill(self, skill):
        return self.character_skill.has_skill(skill)

    def gain_mastery_proficiency(self, skill, mastery_point: int):
        return self.character_skill.gain_mastery_proficiency(skill, mastery_point)

    def __str__(self):
        return " ".join(self.get_archetype_names())
