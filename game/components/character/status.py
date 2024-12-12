from components.character.character_stat import CharacterStat, StatDefinition
from components.character.stat import NumericalStat

from enum import Enum


from data.logs.logger import logger


class StatusType(Enum):
    BUFF = 1
    DEBUFF = 2


class StatusCategory(Enum):
    STAT_AFFECT = 1
    ACTION_AFFECT = 2


class StatusClass(Enum):
    NONE = 1
    INJURY = 2
    TOWN_BUFF = 3
    TOWN_DEBUFF = 4
    GROUND_BUFF = 5
    GROUND_DEBUFF = 6


class Status:
    status_class = StatusClass.NONE
    status_level = 1
    affect_stats = {}
    affect_actions = []
    type: StatusType = None
    categories = []
    img = None
    expirable = True
    recoverable = True

    def __init__(self, duration: int) -> None:
        self.duration = duration

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def get_status_class(cls):
        return cls.status_class

    @classmethod
    def get_status_level(cls):
        return cls.status_level

    @classmethod
    def get_stat_effects(cls):
        if StatusCategory.STAT_AFFECT not in cls.categories:
            raise f"The {cls.__name__} is not a STAT_AFFECT status StatusCategory"
        return cls.affect_stats

    @classmethod
    def get_action_effects(cls):
        if StatusCategory.ACTION_AFFECT not in cls.categories:
            raise f"The {cls.__name__} is not a ACTION_AFFECT status StatusCategory"
        return cls.affect_actions

    @classmethod
    def get_type(cls):
        return cls.type

    @classmethod
    def is_buff(cls):
        return cls.type == StatusType.BUFF

    @classmethod
    def is_debuff(cls):
        return cls.type == StatusType.DEBUFF

    @classmethod
    def get_categories(cls):
        return cls.categories

    @classmethod
    def is_stat_effect_status(cls):
        return StatusCategory.STAT_AFFECT in cls.get_categories()

    @classmethod
    def can_be_expired(cls):
        return cls.expirable

    @classmethod
    def can_be_recovered(cls):
        return cls.recoverable

    def change_duration(self, delta_duration: int):
        self.duration += delta_duration

    def set_duration(self, new_duration: int):
        self.duration = new_duration

    def get_duration(self):
        return self.duration

    def is_expired(self):
        return self.duration <= 0


class LightInjury(Status):
    status_class = StatusClass.INJURY
    status_level = 1
    affect_stats = {
        StatDefinition.POWER: CharacterStat.create_stat(
            StatDefinition.POWER,
            -0.3,
            **{
                NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
            },
        ),
        StatDefinition.SPEED: CharacterStat.create_stat(
            StatDefinition.SPEED,
            -0.3,
            **{
                NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
            },
        ),
    }
    type = StatusType.DEBUFF
    categories = [StatusCategory.STAT_AFFECT]
    expirable = False
    recoverable = True

    def __init__(self, duration: int) -> None:
        super().__init__(duration)


class HeavyInjury(Status):
    status_class = StatusClass.INJURY
    status_level = 2
    affect_stats = {
        StatDefinition.POWER: CharacterStat.create_stat(
            StatDefinition.POWER,
            -0.3,
            **{
                NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
            },
        ),
        StatDefinition.SPEED: CharacterStat.create_stat(
            StatDefinition.SPEED,
            -0.3,
            **{
                NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
            },
        ),
    }
    type = StatusType.DEBUFF
    categories = [StatusCategory.STAT_AFFECT]
    expirable = False
    recoverable = True

    def __init__(self, duration: int) -> None:
        super().__init__(duration)


class TownTileBuff(Status):
    status_class = StatusClass.TOWN_BUFF
    status_level = 1
    affect_stats = {
        StatDefinition.SPEED: CharacterStat.create_stat(
            StatDefinition.SPEED,
            0.3,
            **{
                NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
            },
        ),
    }
    type = StatusType.BUFF
    categories = [StatusCategory.STAT_AFFECT]
    expirable = True
    recoverable = True

    def __init__(self, duration: int) -> None:
        super().__init__(duration)


class GroundTileBuff(Status):
    status_class = StatusClass.GROUND_BUFF
    status_level = 1
    affect_stats = {
        StatDefinition.POWER: CharacterStat.create_stat(
            StatDefinition.POWER,
            0.3,
            **{
                NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
            },
        ),
    }
    type = StatusType.BUFF
    categories = [StatusCategory.STAT_AFFECT]
    expirable = True
    recoverable = True

    def __init__(self, duration: int) -> None:
        super().__init__(duration)
