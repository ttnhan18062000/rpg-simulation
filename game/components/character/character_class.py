from components.character.character_stat import CharacterStat, StatDefinition
from components.character.class_level import ClassLevel, HumanLevel, DemonLevel


class CharacterClass:
    def __init__(self) -> None:
        self.stats_gain = {}
        self.class_level = ClassLevel()
        self.hostile_faction = []

    def get_hostile_factions(self):
        return self.hostile_faction


class Human(CharacterClass):
    def __init__(self) -> None:
        super().__init__()
        self.stats_gain = {
            StatDefinition.MAX_HEALTH: 20,
            StatDefinition.POWER: 5,
            StatDefinition.SPEED: 15,
        }
        self.class_level = HumanLevel()
        self.hostile_faction = [Demon.__name__]


class Demon(CharacterClass):
    def __init__(self) -> None:
        super().__init__()
        self.stats_gain = {
            StatDefinition.MAX_HEALTH: 30,
            StatDefinition.POWER: 10,
            StatDefinition.SPEED: 5,
        }
        self.class_level = DemonLevel()
        self.hostile_faction = [Human.__name__]
