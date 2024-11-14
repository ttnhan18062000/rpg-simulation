from components.character.character_stat import StatDefinition, CharacterStat


class CharacterPower:
    def __init__(self) -> None:
        pass

    # TODO: some cases should use MAX_HEALTH to calculate max power instead
    @staticmethod
    def get_power(character_stats: CharacterStat):
        power = character_stats.get_stat(StatDefinition.POWER).value
        speed = character_stats.get_stat(StatDefinition.SPEED).value
        cur_hp = character_stats.get_stat(StatDefinition.CURRENT_HEALTH).value

        return int(cur_hp * power * (speed / 100))
