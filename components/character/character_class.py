from components.character.character_stat import CharacterStat, StatDefinition
from components.character.class_level import ClassLevel, HumanLevel, DemonLevel


class CharacterClass:
    def __init__(self) -> None:
        self.stats_gain = {}
        self.class_level = ClassLevel()


class Human(CharacterClass):
    def __init__(self) -> None:
        super().__init__()
        self.stats_gain = {
            StatDefinition.HEALTH: 20,
            StatDefinition.POWER: 5,
            StatDefinition.SPEED: 15,
        }
        self.class_level = HumanLevel()


class Demon(CharacterClass):
    def __init__(self) -> None:
        super().__init__()
        self.stats_gain = {
            StatDefinition.HEALTH: 30,
            StatDefinition.POWER: 10,
            StatDefinition.SPEED: 5,
        }
        self.class_level = DemonLevel()
