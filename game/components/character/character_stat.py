import random
from enum import Enum
import copy

from components.character.stat import NumericalStat, CategoricalStat, Stat


from data.logs.logger import logger


class StatDefinition(Enum):
    MAX_HEALTH = 1
    CURRENT_HEALTH = 2
    POWER = 3
    SPEED = 4
    REGENATION = 5
    DEFENSE = 6
    RESISTANCE = 7


stat_class = {
    StatDefinition.MAX_HEALTH: NumericalStat,
    StatDefinition.CURRENT_HEALTH: NumericalStat,
    StatDefinition.POWER: NumericalStat,
    StatDefinition.SPEED: NumericalStat,
    StatDefinition.REGENATION: NumericalStat,
    StatDefinition.DEFENSE: NumericalStat,
    StatDefinition.RESISTANCE: NumericalStat,
}


class CharacterStat:
    def __init__(self, character_attr) -> None:
        self.stats_list = {}
        self.apply_character_attributes(character_attr)

    # @staticmethod
    # def get_applied_stat_effects(base_character_stat, stat_effects):
    #     applied_character_stat = copy.deepcopy(base_character_stat)
    #     for stat_def, stat in stat_effects.items():
    #         if stat_def in applied_character_stat.stats_list:
    #             applied_character_stat.get_stat(stat_def).modify(stat)
    #         else:
    #             applied_character_stat.stats_list[stat_def] = stat
    #     return applied_character_stat

    # Increase stats by gained a number of specific attribute
    # Usually used for level up a attribute
    def update_stat_with_new_attribute_gained(self, attr):
        total_stat_effect = attr.get_total_stat_effect()
        # TODO: optimize later, here is slightly hard-code
        for stat_def, stat in total_stat_effect.items():
            if stat_def in self.stats_list:
                self.get_stat(stat_def).modify(stat)
            else:
                self.stats_list[stat_def] = stat
            logger.debug(f"Character gained {stat_def.name}={stat}")

    def apply_character_attributes(self, character_attr):
        final_attrs = character_attr.get_final_attributes()
        for attr in final_attrs.values():
            if attr.has_stat_effect():
                total_stat_effect = attr.get_total_stat_effect()
                # TODO: optimize later, here is slightly hard-code
                for stat_def, stat in total_stat_effect.items():
                    if stat_def in self.stats_list:
                        self.get_stat(stat_def).modify(stat)
                    else:
                        self.stats_list[stat_def] = stat

        # TODO: Currently inefficiently when first initialization, we need to set current health = max health
        self.stats_list[StatDefinition.CURRENT_HEALTH] = CharacterStat.create_stat(
            StatDefinition.CURRENT_HEALTH,
            self.get_stat_value(StatDefinition.MAX_HEALTH),
            **{NumericalStat.numerical_type_key: NumericalStat.NumericalType.REAL},
        )

        logger.debug(
            f"Applied new character attributes: {character_attr}, new stats: {self}"
        )

    @staticmethod
    def create_stat(stat_def, value, **kwargs):
        return stat_class[stat_def](value, **kwargs)

    def add_stat(self, stat_def: StatDefinition, value):
        if stat_def in self.stats_list:
            raise Exception(f"Already added the stat type '{stat_def}'")
        new_stat = CharacterStat.create_stat(stat_def, value)
        self.stats_list[stat_def] = new_stat

    def get_stat(self, stat_def: StatDefinition, force=True):
        if stat_def in self.stats_list:
            return self.stats_list[stat_def]
        else:
            if force:
                raise Exception(f"No {stat_def} found")
            else:
                return None

    def get_stat_value(self, stat_def: StatDefinition, force=True):
        if stat_def in self.stats_list:
            return self.stats_list[stat_def].value
        else:
            if force:
                raise Exception(f"No {stat_def} found")
            else:
                return 0

    def update_stat(self, stat_def: StatDefinition, value):
        if stat_def in self.stats_list:
            if not isinstance(value, Stat):
                delta_stat = CharacterStat.create_stat(stat_def, value)
            else:
                delta_stat = value
            self.stats_list[stat_def] += delta_stat

            if stat_def == StatDefinition.CURRENT_HEALTH:
                self.stats_list[stat_def].value = min(
                    self.stats_list[StatDefinition.MAX_HEALTH].value,
                    self.stats_list[stat_def].value,
                )
        else:
            raise Exception(f"No {stat_def} found")

    # TODO: Refactor this, currently duplicated, inefficient
    def get_applied_statuses_character_stat(self, character_stat, character_status):
        """
        Apply all effects to a given CharacterStats object.
        :param stats: The CharacterStats instance to modify
        """
        applied_character_stat = copy.deepcopy(character_stat)

        stat_effect_statuses = {
            status_name: status
            for status_name, status in character_status.get_statuses().items()
            if status.is_stat_effect_status()
        }

        for status_name, status in stat_effect_statuses.items():
            stat_effects = status.get_stat_effects()
            for stat_def, stat in stat_effects.items():
                applied_character_stat.get_stat(stat_def).modify(stat)

        return applied_character_stat

    # TODO: Refactor this, currently duplicated, inefficient
    def get_applied_equipments_character_stat(self, character_equipment):
        applied_character_stat = copy.deepcopy(self)

        weapon = character_equipment.get_weapon()
        armor = character_equipment.get_armor()
        if weapon:
            for stat_def, stat in weapon.get_affect_stats().items():
                applied_character_stat.get_stat(stat_def).modify(stat)
        if armor:
            for stat_def, stat in armor.get_affect_stats().items():
                applied_character_stat.get_stat(stat_def).modify(stat)

        return applied_character_stat

    def get_final_stat(self, character):
        equipment_applied_character_stat = self.get_applied_equipments_character_stat(
            character.get_character_equipment()
        )

        if character.get_character_status().is_empty():
            return equipment_applied_character_stat
        return self.get_applied_statuses_character_stat(
            equipment_applied_character_stat, character.get_character_status()
        )

    def get_health_ratio(self):
        return (
            self.get_stat(StatDefinition.CURRENT_HEALTH).value
            / self.get_stat(StatDefinition.MAX_HEALTH).value
        )

    def __str__(self) -> str:
        return " ".join(
            [
                f"{stat_def.name}={stat.get_value()}"
                for stat_def, stat in list(self.stats_list.items())
            ]
        )
