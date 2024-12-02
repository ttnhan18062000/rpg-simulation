from enum import Enum

from components.item.item import Item, ItemType, Rarity
from components.character.character_stat import CharacterStat, StatDefinition
from components.character.stat import NumericalStat


class EquipmentType(Enum):
    WEAPON = 1
    ARMOR = 2


class Equipment(Item):
    item_type: ItemType = ItemType.EQUIPMENT
    description = ""
    base_rarity = Rarity.COMMON
    equipment_type = None
    affect_stats = {}
    require_stats = {}  # For example: require some STR
    is_stackable = False

    def __init__(self):
        self.rarity = Equipment.base_rarity

    @classmethod
    def get_equipment_type(cls):
        return cls.equipment_type

    @classmethod
    def get_affect_stats(cls):
        return cls.affect_stats


class SteelSword(Equipment):
    description = "Starter Weapon"
    base_rarity = Rarity.COMMON
    equipment_type = EquipmentType.WEAPON
    affect_stats = {
        StatDefinition.POWER: CharacterStat.create_stat(
            StatDefinition.POWER,
            20,
            **{NumericalStat.numerical_type_key: NumericalStat.NumericalType.REAL},
        ),
    }
    require_stats = {}

    def __init__(self):
        self.rarity = SteelSword.base_rarity


class DamagedAncientSword(Equipment):
    description = "Damaged Rare Weapon"
    base_rarity = Rarity.UNCOMMON
    equipment_type = EquipmentType.WEAPON
    affect_stats = {
        StatDefinition.POWER: CharacterStat.create_stat(
            StatDefinition.POWER,
            30,
            **{NumericalStat.numerical_type_key: NumericalStat.NumericalType.REAL},
        ),
    }
    require_stats = {}

    def __init__(self):
        self.rarity = SteelSword.base_rarity


class SteelArmor(Equipment):
    description = "Starter Armor"
    base_rarity = Rarity.COMMON
    equipment_type = EquipmentType.ARMOR
    affect_stats = {
        StatDefinition.MAX_HEALTH: CharacterStat.create_stat(
            StatDefinition.MAX_HEALTH,
            100,
            **{NumericalStat.numerical_type_key: NumericalStat.NumericalType.REAL},
        ),
    }
    require_stats = {}

    def __init__(self):
        self.rarity = SteelArmor.base_rarity


class DamagedAncientArmor(Equipment):
    description = "Damaged Rare Armor"
    base_rarity = Rarity.UNCOMMON
    equipment_type = EquipmentType.ARMOR
    affect_stats = {
        StatDefinition.MAX_HEALTH: CharacterStat.create_stat(
            StatDefinition.MAX_HEALTH,
            150,
            **{NumericalStat.numerical_type_key: NumericalStat.NumericalType.REAL},
        ),
    }
    require_stats = {}

    def __init__(self):
        self.rarity = SteelArmor.base_rarity
