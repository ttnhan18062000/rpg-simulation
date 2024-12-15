from components.archetype.skill.skill import Skill, SkillMastery

from data.logs.logger import logger


class CharacterSkill:
    def __init__(self):
        self.skills: dict[str, Skill] = {}

    def has_skill(self, skill: Skill):
        return skill.get_name() in self.skills

    def add_skill(self, skill: Skill):
        if self.has_skill(skill):
            logger.debug(f"Already learned the skill {skill}")
        else:
            self.skills[skill.get_name()] = skill
            logger.debug(f"Learned the skill {skill}")

    def get_skills(self) -> dict[str, Skill]:
        return self.skills

    def get_skill_names(self):
        return list(self.skills.keys())

    def get_skill(self, skill: Skill):
        skill_name = skill.get_name()
        if skill_name not in self.skills:
            raise Exception(
                f"{skill_name} not appear in {[s.get_name() for s in self.skills]}"
            )
        return self.skills[skill.get_name()]

    def gain_mastery_proficiency(self, skill, mastery_point: int):
        return self.get_skill(skill).gain_mastery_proficiency(mastery_point)
