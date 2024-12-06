from components.character.character_stat import CharacterStat, StatDefinition
from components.character.class_level import (
    ClassLevel,
    HumanLevel,
    DemonLevel,
    RuinMobLevel,
    ForestMobLevel,
)
from components.world.tile import tile_map, RuinTile, ForestTile
from components.attribute.attribute import Vitality, Endurance, Strength, Agility


class CharacterClass:
    attributes_cap_gain = {}

    def __init__(self) -> None:
        self.class_level = ClassLevel()
        self.hostile_factions = []
        self.ally_factions = []
        self.restricted_tile_types = []

    def get_hostile_factions(self):
        return self.hostile_factions

    def get_ally_factions(self):
        return self.ally_factions

    def get_restricted_tile_types(self):
        return self.restricted_tile_types

    def is_mob(self):
        return True

    @classmethod
    def get_attributes_cap_gain(cls):
        return cls.attributes_cap_gain


class Human(CharacterClass):
    attributes_cap_gain = {
        Vitality.get_name(): 4,
        Endurance.get_name(): 4,
        Strength.get_name(): 5,
        Agility.get_name(): 8,
    }

    def __init__(self) -> None:
        super().__init__()
        self.class_level = HumanLevel()
        self.hostile_factions = [
            Demon.__name__,
            ForestMob.__name__,
            RuinMob.__name__,
        ]  # TODO: mobs here just for testing, change to "farm" factions later
        self.ally_factions = [Human.__name__]
        self.restricted_tile_types = []

    def is_mob(self):
        return False


class Demon(CharacterClass):
    attributes_cap_gain = {
        Vitality.get_name(): 6,
        Endurance.get_name(): 6,
        Strength.get_name(): 7,
        Agility.get_name(): 3,
    }

    def __init__(self) -> None:
        super().__init__()
        self.class_level = DemonLevel()
        self.hostile_factions = [
            Human.__name__,
            ForestMob.__name__,
            RuinMob.__name__,
        ]  # TODO: mobs here just for testing, change to "farm" factions later
        self.ally_factions = [Demon.__name__]
        self.restricted_tile_types = []

    def is_mob(self):
        return False


class RuinMob(CharacterClass):
    attributes_cap_gain = {
        Vitality.get_name(): 10,
        Endurance.get_name(): 10,
        Strength.get_name(): 10,
        Agility.get_name(): 3,
    }

    def __init__(self) -> None:
        super().__init__()
        self.class_level = RuinMobLevel()
        self.hostile_factions = [Human.__name__, Demon.__name__]
        self.ally_factions = [RuinMob.__name__]
        self.restricted_tile_types = [
            tile_type for tile_type in tile_map.values() if tile_type != RuinTile
        ]

    def is_mob(self):
        return True


class ForestMob(CharacterClass):
    attributes_cap_gain = {
        Vitality.get_name(): 3,
        Endurance.get_name(): 3,
        Strength.get_name(): 2,
        Agility.get_name(): 5,
    }

    def __init__(self) -> None:
        super().__init__()
        self.class_level = ForestMobLevel()
        self.hostile_factions = [Demon.__name__]
        self.ally_factions = [ForestMob.__name__]
        self.restricted_tile_types = [
            tile_type for tile_type in tile_map.values() if tile_type != ForestTile
        ]

    def is_mob(self):
        return True
