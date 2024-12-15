from enum import Enum

from components.attribute.attribute import Attribute, Strength, Agility
from components.character.character_stat import StatDefinition

from data.logs.logger import logger


class SkillType(Enum):
    ACTIVE = 1
    PASSIVE = 2


class TargetType(Enum):
    SINGLE = 1
    AOE = 2


class SkillMastery(Enum):
    LEARNING = 1
    BEGINNER = 2
    ADEPT = 3
    MASTER = 4
    PERFECTION = 5


class Skill:
    skill_type: SkillType = None
    target_type: TargetType = None
    scale_attributes: dict[Attribute, float] = None
    mastery_multipliers: dict[SkillMastery, float] = {
        SkillMastery.LEARNING: 0.1,
        SkillMastery.BEGINNER: 1,
        SkillMastery.ADEPT: 1.2,
        SkillMastery.MASTER: 1.5,
        SkillMastery.PERFECTION: 2,
    }
    # How much times it cost for each level to be level up
    mastery_gain: dict[SkillMastery, int] = {
        SkillMastery.LEARNING: 1,
        SkillMastery.BEGINNER: 2,
        SkillMastery.ADEPT: 5,
        SkillMastery.MASTER: 10,
    }
    base_multiplier = 1
    energy_cost = 0

    def __init__(self):
        self.mastery: SkillMastery = SkillMastery.LEARNING
        self.mastery_proficiency: int = 0

    @classmethod
    def get_name(cls):
        return cls.__name__

    def __str__(self):
        return self.get_name()

    def get_mastery(self):
        return self.mastery

    def is_learned(self):
        return self.mastery != SkillMastery.LEARNING

    def get_damage(self, character_stat, character_final_attrs) -> int:
        total_multiplier = (
            self.get_scale_factor(character_final_attrs)
            * self.mastery_multipliers[self.mastery]
            * self.base_multiplier
        )
        logger.debug(f"Total multiplier of {self.get_name()}: {total_multiplier}")
        return int(
            character_stat.get_stat_value(StatDefinition.POWER) * total_multiplier
        )

    def increase_mastery_level(self):
        # Get the next level if it exists, otherwise return the same level
        next_level_value = self.mastery.value + 1
        self.mastery = (
            SkillMastery(next_level_value)
            if next_level_value in SkillMastery._value2member_map_
            else self.mastery
        )

    def gain_mastery_proficiency(self, mastery_point: int):
        if self.mastery_proficiency == SkillMastery.PERFECTION:
            logger.debug(
                f"Perfection mastery of {self.get_name()}, cannot learn anything more"
            )
            return False, "Perfection"
        real_mastery_gain = int(mastery_point / self.mastery_gain[self.mastery])
        self.mastery_proficiency += real_mastery_gain
        if self.mastery_proficiency >= 100:
            self.increase_mastery_level()
            logger.debug(
                f"Mastery of {self.get_name()} leveled up, current is {self.mastery}"
            )
            if self.mastery == SkillMastery.BEGINNER:
                return True, "Learned"
            else:
                return True, "Level up"
        return True, ""

    @classmethod
    def get_scale_factor(cls, character_final_attrs):
        total_multiplier = 1
        for attr, multiplier in cls.scale_attributes.items():
            attr_value = character_final_attrs[attr.get_name()].get_value()
            total_multiplier += multiplier * attr_value
        return total_multiplier

    @classmethod
    def get_energy_cost(cls):
        return cls.energy_cost

    @classmethod
    def get_skill_type(cls):
        return cls.skill_type

    @classmethod
    def get_target_type(cls):
        return cls.target_type

    @classmethod
    def get_scale_attributes(cls):
        return cls.scale_attributes
