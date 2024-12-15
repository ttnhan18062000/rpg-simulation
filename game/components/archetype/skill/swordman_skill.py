from components.archetype.skill.skill import Skill, SkillType, TargetType, SkillMastery
from components.attribute.attribute import Attribute, Strength, Agility


class Slash(Skill):
    skill_type: SkillType = SkillType.ACTIVE
    target_type: TargetType = TargetType.SINGLE
    scale_attributes: dict[Attribute, float] = {Strength: 0.02, Agility: 0.02}
    mastery_multipliers: dict[SkillMastery, float] = {
        SkillMastery.BEGINNER: 1,
        SkillMastery.ADEPT: 1.2,
        SkillMastery.MASTER: 1.5,
        SkillMastery.PERFECTION: 2,
    }
    base_multiplier = 1.5
    energy_cost = 30


class SwordDance(Skill):
    skill_type: SkillType = SkillType.ACTIVE
    target_type: TargetType = TargetType.AOE
    scale_attributes: dict[Attribute, float] = {Strength: 0.02, Agility: 0.02}
    mastery_multipliers: dict[SkillMastery, float] = {
        SkillMastery.BEGINNER: 1,
        SkillMastery.ADEPT: 1.2,
        SkillMastery.MASTER: 1.5,
        SkillMastery.PERFECTION: 2,
    }
    base_multiplier = 2
    energy_cost = 60
