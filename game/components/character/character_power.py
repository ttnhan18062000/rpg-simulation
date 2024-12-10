import copy

from components.character.character_stat import StatDefinition, CharacterStat

from data.logs.logger import logger


class CharacterPower:
    def __init__(self) -> None:
        pass

    # TODO: some cases should use MAX_HEALTH to calculate max power instead
    # TODO: refactor this, currently inefficient and duplicated code
    @staticmethod
    def get_power(character_stats: CharacterStat):
        power = character_stats.get_stat_value(StatDefinition.POWER)
        speed = character_stats.get_stat_value(StatDefinition.SPEED)
        cur_hp = character_stats.get_stat_value(StatDefinition.CURRENT_HEALTH)
        defense = character_stats.get_stat_value(StatDefinition.DEFENSE)

        return int(cur_hp * power * defense * (speed / 100))

    @staticmethod
    def get_max_power(character_stats: CharacterStat):
        power = character_stats.get_stat_value(StatDefinition.POWER)
        speed = character_stats.get_stat_value(StatDefinition.SPEED)
        cur_hp = character_stats.get_stat_value(StatDefinition.MAX_HEALTH)
        defense = character_stats.get_stat_value(StatDefinition.DEFENSE)

        return int(cur_hp * power * defense * (speed / 100))

    @staticmethod
    def get_character_before_and_after_equip_equipment(character, target_equipment):
        character_base_stat = character.get_character_stat()
        # Current equipment total power
        before_equipment_applied_stat = (
            character_base_stat.get_applied_equipments_character_stat(
                character.get_character_equipment()
            )
        )
        before_equipment_applied_stat_power = CharacterPower.get_max_power(
            before_equipment_applied_stat
        )

        # After applied equipment total power
        after_applied_character_equipment = character.get_character_equipment().clone()
        after_applied_character_equipment.equip(target_equipment)

        after_equipment_applied_stat = (
            character_base_stat.get_applied_equipments_character_stat(
                after_applied_character_equipment
            )
        )
        after_equipment_applied_stat_power = CharacterPower.get_max_power(
            after_equipment_applied_stat
        )

        logger.debug(
            f"Power before and after equip {target_equipment.get_name()}: {before_equipment_applied_stat_power} and {after_equipment_applied_stat_power}"
        )

        return before_equipment_applied_stat_power, after_equipment_applied_stat_power

    # TODO: think about refactor this too
    # TODO: better formula for total power and additional powers
    # since equipment power + status power + base power is not equal to the total value
    @staticmethod
    def get_detailed_character_power(character):
        base_stat_power = 0
        equipment_power = 0
        status_power = 0

        character_base_stat = character.get_character_stat()
        base_stat_power = CharacterPower.get_power(character_base_stat)

        equipment_applied_stat = (
            character_base_stat.get_applied_equipments_character_stat(
                character.get_character_equipment()
            )
        )
        equipment_applied_stat_power = CharacterPower.get_power(equipment_applied_stat)
        equipment_power = equipment_applied_stat_power - base_stat_power

        if character.get_character_status().is_empty():
            status_power = 0
        else:
            status_applied_stat = (
                character_base_stat.get_applied_statuses_character_stat(
                    character_base_stat, character.get_character_status()
                )
            )
            status_applied_stat_power = CharacterPower.get_power(status_applied_stat)
            status_power = status_applied_stat_power - base_stat_power

        return base_stat_power, equipment_power, status_power
