from enum import Enum


class ItemType:
    ITEM = 1
    EQUIPMENT = 2
    MATERIAL = 3
    CONSUMABLE = 4


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    MYTHIC = 6
    SUPREME = 7
    PRIMODIAL = 8


class Item:
    item_type: ItemType = ItemType.ITEM
    description = "Basic Item"
    base_rarity = Rarity.COMMON

    def __init__(self):
        self.rarity = Item.base_rarity

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def is_equipment(cls):
        return cls.item_type == ItemType.EQUIPMENT

    @classmethod
    def is_material(cls):
        return cls.item_type == ItemType.MATERIAL

    @classmethod
    def is_consumable(cls):
        return cls.item_type == ItemType.CONSUMABLE
