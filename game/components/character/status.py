from components.character.character_stat import CharacterStat, StatDefinition
from components.character.stat import NumericalStat

from enum import Enum


from data.logs.logger import logger


class StatusType(Enum):
    BUFF = 1
    DEBUFF = 2


class StatusCategory(Enum):
    STAT_AFFECT = 1
    MOVEMENT_AFFECT = 2


class Status:
    name = ""

    def __init__(self, duration: int) -> None:
        self.duration = duration
        self.affect_stats = {}
        self.affect_actions = []
        self.type: StatusType = None
        self.categories = []
        self.img = None

    @classmethod
    def get_name(cls):
        return cls.name

    def get_stat_effects(self):
        return self.affect_stats

    def get_categories(self):
        return self.categories

    def is_stat_effect_status(self):
        return StatusCategory.STAT_AFFECT in self.get_categories()

    def change_duration(self, duration_value: int):
        self.duration += duration_value

    def get_duration(self):
        return self.duration

    def is_expired(self):
        return self.duration <= 0


class LightInjury(Status):
    name = "LightInjury"

    def __init__(self, duration: int) -> None:
        super().__init__(duration)
        self.affect_stats = {
            StatDefinition.POWER: CharacterStat.create_stat(
                StatDefinition.POWER,
                -0.15,
                **{
                    NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
                }
            ),
            StatDefinition.SPEED: CharacterStat.create_stat(
                StatDefinition.SPEED,
                -0.15,
                **{
                    NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
                }
            ),
        }
        self.type = StatusType.DEBUFF
        self.categories = [StatusCategory.STAT_AFFECT]


class HeavyInjury(Status):
    name = "HeavyInjury"

    def __init__(self, duration: int) -> None:
        super().__init__(duration)
        self.affect_stats = {
            StatDefinition.POWER: CharacterStat.create_stat(
                StatDefinition.POWER,
                -0.3,
                **{
                    NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
                }
            ),
            StatDefinition.SPEED: CharacterStat.create_stat(
                StatDefinition.SPEED,
                -0.3,
                **{
                    NumericalStat.numerical_type_key: NumericalStat.NumericalType.PERCENTAGE
                }
            ),
        }
        self.type = StatusType.DEBUFF
        self.categories = [StatusCategory.STAT_AFFECT]
