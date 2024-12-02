from components.character.character_stat import CharacterStat, StatDefinition
from components.character.class_level import (
    ClassLevel,
    HumanLevel,
    DemonLevel,
    RuinMobLevel,
    ForestMobLevel,
)
from components.world.tile import tile_map, RuinTile, ForestTile


class CharacterClass:
    def __init__(self) -> None:
        self.stats_gain = {}
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


class Human(CharacterClass):
    def __init__(self) -> None:
        super().__init__()
        self.stats_gain = {
            StatDefinition.MAX_HEALTH: 25,
            StatDefinition.POWER: 5,
            StatDefinition.SPEED: 20,
        }
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
    def __init__(self) -> None:
        super().__init__()
        self.stats_gain = {
            StatDefinition.MAX_HEALTH: 50,
            StatDefinition.POWER: 10,
            StatDefinition.SPEED: 10,
        }
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
    def __init__(self) -> None:
        super().__init__()
        self.stats_gain = {
            StatDefinition.MAX_HEALTH: 50,
            StatDefinition.POWER: 15,
            StatDefinition.SPEED: 3,
        }
        self.class_level = RuinMobLevel()
        self.hostile_factions = [Human.__name__, Demon.__name__]
        self.ally_factions = [RuinMob.__name__]
        self.restricted_tile_types = [
            tile_type for tile_type in tile_map.values() if tile_type != RuinTile
        ]

    def is_mob(self):
        return True


class ForestMob(CharacterClass):
    def __init__(self) -> None:
        super().__init__()
        self.stats_gain = {
            StatDefinition.MAX_HEALTH: 15,
            StatDefinition.POWER: 3,
            StatDefinition.SPEED: 20,
        }
        self.class_level = ForestMobLevel()
        self.hostile_factions = [Demon.__name__]
        self.ally_factions = [ForestMob.__name__]
        self.restricted_tile_types = [
            tile_type for tile_type in tile_map.values() if tile_type != ForestTile
        ]

    def is_mob(self):
        return True
