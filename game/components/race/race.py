from components.character.character_stat import CharacterStat, StatDefinition
from components.character.class_level import ClassLevel
from components.world.tile import tile_map, RuinTile, ForestTile
from components.attribute.attribute import Vitality, Endurance, Strength, Agility


class Race:
    attributes_cap_gain = {}

    def __init__(self) -> None:
        self.class_level = ClassLevel()
        self.hostile_races = []
        self.friendly_races = []
        self.restricted_tile_types = []

    def get_hostile_races(self):
        return self.hostile_races

    def get_friendly_races(self):
        return self.friendly_races

    def get_restricted_tile_types(self):
        return self.restricted_tile_types

    @classmethod
    def get_attributes_cap_gain(cls):
        return cls.attributes_cap_gain

    @classmethod
    def get_name(cls):
        return cls.__name__


class Human(Race):
    attributes_cap_gain = {
        Vitality.get_name(): 2,
        Endurance.get_name(): 2,
        Strength.get_name(): 3,
        Agility.get_name(): 4,
    }

    def __init__(self) -> None:
        super().__init__()
        self.class_level = ClassLevel()
        self.hostile_races = [
            Demon.__name__,
            Forest.__name__,
            Ruin.__name__,
        ]  # TODO: mobs here just for testing, change to "farm" factions later
        self.friendly_races = [Human.__name__]
        self.restricted_tile_types = []


class Demon(Race):
    attributes_cap_gain = {
        Vitality.get_name(): 3,
        Endurance.get_name(): 3,
        Strength.get_name(): 4,
        Agility.get_name(): 2,
    }

    def __init__(self) -> None:
        super().__init__()
        self.class_level = ClassLevel()
        self.hostile_races = [
            Human.__name__,
            Forest.__name__,
            Ruin.__name__,
        ]  # TODO: mobs here just for testing, change to "farm" factions later
        self.friendly_races = [Demon.__name__]
        self.restricted_tile_types = []


class Ruin(Race):
    attributes_cap_gain = {
        Vitality.get_name(): 4,
        Endurance.get_name(): 4,
        Strength.get_name(): 4,
        Agility.get_name(): 1,
    }

    def __init__(self) -> None:
        super().__init__()
        self.class_level = ClassLevel()
        self.hostile_races = [Human.__name__, Demon.__name__]
        self.friendly_races = [Ruin.__name__]
        self.restricted_tile_types = [
            tile_type for tile_type in tile_map.values() if tile_type != RuinTile
        ]


class Forest(Race):
    attributes_cap_gain = {
        Vitality.get_name(): 2,
        Endurance.get_name(): 2,
        Strength.get_name(): 2,
        Agility.get_name(): 5,
    }

    def __init__(self) -> None:
        super().__init__()
        self.class_level = ClassLevel()
        self.hostile_races = [Demon.__name__]
        self.friendly_races = [Forest.__name__]
        self.restricted_tile_types = [
            tile_type for tile_type in tile_map.values() if tile_type != ForestTile
        ]
