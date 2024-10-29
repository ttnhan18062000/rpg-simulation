import random
from enum import Enum

from components.character.stat import NumericalStat, CategoricalStat, Stat


class StatDefinition(Enum):
    HEALTH = 1
    POWER = 2
    SPEED = 3


stat_class = {
    StatDefinition.HEALTH: NumericalStat,
    StatDefinition.POWER: NumericalStat,
    StatDefinition.SPEED: NumericalStat,
}


class CharacterStat:
    def __init__(self) -> None:
        self.stats_list = {}

    @staticmethod
    def create_stat(stat_def, value):
        return stat_class[stat_def](value)

    def add_stat(self, stat_def: StatDefinition, value):
        if stat_def in self.stats_list:
            raise Exception(f"Already added the stat type '{stat_def}'")
        new_stat = CharacterStat.create_stat(stat_def, value)
        self.stats_list[stat_def] = new_stat

    def get_stat(self, stat_def: StatDefinition):
        if stat_def in self.stats_list:
            return self.stats_list[stat_def]
        raise Exception(f"No {stat_def} found")

    def update_stat(self, stat_def: StatDefinition, value):
        if stat_def in self.stats_list:
            if not isinstance(value, Stat):
                delta_stat = CharacterStat.create_stat(stat_def, value)
            else:
                delta_stat = value
            self.stats_list[stat_def] += delta_stat
        else:
            raise Exception(f"No {stat_def} found")

    def __str__(self) -> str:
        return " ".join([str(stat.value) for stat in list(self.stats_list.values())])
