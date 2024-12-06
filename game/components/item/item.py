from enum import IntEnum, Enum


class ItemType(Enum):
    ITEM = 1
    EQUIPMENT = 2
    MATERIAL = 3
    CONSUMABLE = 4


class Rarity(IntEnum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    MYTHIC = 6
    SUPREME = 7
    PRIMODIAL = 8


class Stackable:

    def __init__(self, number_of_items: int = 1):
        self.stack = number_of_items

    def get_stack(self):
        return self.stack

    def increase_stack(self, number_of_items: int):
        self.stack += number_of_items

    def decrease_stack(self, number_of_items: int):
        if number_of_items >= 0:
            self.stack -= number_of_items
        else:
            raise Exception("Consume more than the number of stack")
        if self.stack == 0:
            self.on_zero_stack()

    def on_zero_stack(self):
        pass


class Item:
    item_type: ItemType = ItemType.ITEM
    description = "Basic Item"
    base_rarity = Rarity.COMMON
    is_stackable = True

    def __init__(self):
        self.rarity = Item.base_rarity

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def get_type(cls):
        return cls.item_type

    @classmethod
    def is_equipment(cls):
        return cls.item_type == ItemType.EQUIPMENT

    @classmethod
    def is_material(cls):
        return cls.item_type == ItemType.MATERIAL

    @classmethod
    def is_consumable(cls):
        return cls.item_type == ItemType.CONSUMABLE

    def get_final_rarity(self):
        return self.base_rarity

    @classmethod
    def can_be_stacked(cls):
        return cls.is_stackable
