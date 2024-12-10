from enum import Enum

from components.character.character_stat import CharacterStat, StatDefinition
from components.character.stat import NumericalStat
from components.utils.visualization_converter import convert_to_progress_string

from data.logs.logger import logger


class AttributeProficiencyResult(Enum):
    IS_INCREASED = 1
    IS_CAPPED = 2
    IS_LEVELED_UP = 3


class Attribute:
    description = ""
    stat_effect_mutlipliers = {}
    contain_special_effect = False
    contain_stat_effect = False

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def get_display_name(cls):
        attr_name = cls.get_name()
        return attr_name[:3].upper() if len(attr_name) >= 3 else attr_name.upper()

    def __init__(self, value: int, cap=None) -> None:
        self.value = value
        if cap:
            self.cap = cap
        else:
            self.cap = value * 2
        self.current_proficiency = 0

    def __add__(self, other):
        if self.get_name() != other.get_name():
            raise Exception(
                f"The addition operation between two attributes must be the same type {self.get_name()} different from {other.get_name()}"
            )
        if isinstance(other, Attribute):
            return self.__class__(self.value + other.value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Attribute):
            # Define how to multiply two Attribute objects
            if isinstance(other, int):
                return self.__class__(self.value * other)
            elif isinstance(other, self.__class__):
                return self.__class__(self.value * other.value)
        return NotImplemented

    def get_info(self):
        return f"{self.get_proficiency_visualization()} {self.value} ({self.cap})"

    def get_proficiency_visualization(self):
        progress_string = convert_to_progress_string(
            percentage=(self.current_proficiency / self.get_next_level_proficiency()),
            block_length=10,
        )
        return progress_string

    def __str__(self):
        return f"{self.__class__.get_display_name()} {self.get_info()}"

    def get_next_level_proficiency(self):
        return 10 * (self.value + 1)

    def clone(self):
        return self.__class__(self.value, self.cap)

    def set_value(self, value: int):
        self.value = value

    def get_value(self):
        return self.value

    def get_cap(self):
        return self.cap

    def is_capped(self):
        return self.value >= self.cap

    def modify_cap(self, value: int):
        before_cap = self.get_cap()
        self.cap += value
        logger.debug(
            f"{self.get_name()} cap increase from {before_cap} to {self.get_cap()}"
        )

    def increase_proficiency(self, value: int):
        self.current_proficiency += value
        next_level_proficiency = self.get_next_level_proficiency()
        if self.current_proficiency >= next_level_proficiency:
            if not self.is_capped():
                self.increase_level()
                self.current_proficiency -= next_level_proficiency
                return AttributeProficiencyResult.IS_LEVELED_UP
            else:
                return AttributeProficiencyResult.IS_CAPPED
        return AttributeProficiencyResult.IS_INCREASED

    def increase_level(self):
        self.modify_value(1)

    def modify_value(self, value: int):
        self.value += value

    @classmethod
    def get_stat_effect_mutlipliers(cls):
        return cls.stat_effect_mutlipliers

    def get_total_stat_effect(self):
        total_stat_effect = {}
        for (
            stat_type,
            stat_effect_multiplier,
        ) in self.get_stat_effect_mutlipliers().items():
            total_stat_effect.update(
                {
                    stat_type: CharacterStat.create_stat(
                        stat_type,
                        self.value * stat_effect_multiplier,
                        **{
                            NumericalStat.numerical_type_key: NumericalStat.NumericalType.REAL
                        },
                    )
                }
            )
        return total_stat_effect

    @classmethod
    def has_stat_effect(cls):
        return cls.contain_stat_effect

    @classmethod
    def has_special_effect(cls):
        return cls.contain_special_effect

    def apply_special_effect(self, character):
        pass


# --------- Character base stats


class Vitality(Attribute):
    description = "Tankiness of the character"
    stat_effect_mutlipliers = {
        StatDefinition.MAX_HEALTH: 20,
        StatDefinition.REGENATION: 2,
    }
    contain_stat_effect = True
    contain_special_effect = False


class Endurance(Attribute):
    description = "Tankiness of the character"
    stat_effect_mutlipliers = {
        StatDefinition.DEFENSE: 1,
        StatDefinition.RESISTANCE: 1,
    }
    contain_stat_effect = True
    contain_special_effect = False


class Strength(Attribute):
    description = "Powerness of the character"
    stat_effect_mutlipliers = {StatDefinition.POWER: 5}
    contain_stat_effect = True


class Agility(Attribute):
    description = "Quickiness of the character"
    stat_effect_mutlipliers = {StatDefinition.SPEED: 10}
    contain_stat_effect = True
    contain_special_effect = True

    # TODO: implement this, increase the chane of escape from combat event
    def apply_special_effect(self, character):
        pass


# --------- Character decision


class Perception(Attribute):
    description = "Sensiness of the character"
    stat_effect_mutlipliers = {}
    contain_stat_effect = False
    contain_special_effect = True

    # TODO: implement this, increase the vision range and accuracy of the power estimation
    def apply_special_effect(self, character):
        pass


class Intellect(Attribute):
    description = "How smart is the character"
    stat_effect_mutlipliers = {}
    contain_stat_effect = False
    contain_special_effect = True

    # TODO: implement this, increase the depth of thinking, strategy, decision of actions
    def apply_special_effect(self, character):
        pass


# --------- Character core


class Insight(Attribute):
    description = "Ability to learn new things"
    stat_effect_mutlipliers = {}
    contain_stat_effect = False
    contain_special_effect = True

    # TODO: implement this, increase the speed to master something, unlock complex skills or something
    def apply_special_effect(self, character):
        pass


class Heritage(Attribute):
    description = "How powerful is the bloodline of the character"
    stat_effect_mutlipliers = {}
    contain_stat_effect = False
    contain_special_effect = True

    # TODO: implement this, unlock the potential to learn powerful skills or masteries
    def apply_special_effect(self, character):
        pass


class Essence(Attribute):
    description = "How potential is the character"
    stat_effect_mutlipliers = {}
    contain_stat_effect = False
    contain_special_effect = True

    # TODO: implement this, unlock the potential to growth in general
    def apply_special_effect(self, character):
        pass
