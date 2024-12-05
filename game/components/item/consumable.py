from .item import Rarity
from components.item.item import Item, ItemType, Stackable


class Consumable(Item, Stackable):
    item_type: ItemType = ItemType.CONSUMABLE
    description = "Consumable"
    base_rarity = Rarity.COMMON
    is_stackable = True

    def __init__(self, number_of_items: int = 1):
        super().__init__(Consumable.base_rarity)
        self.stack = number_of_items

    def on_consume_all(self):
        pass


class ValorMedal(Item):
    description = "Advance Class Type for Human"
    base_rarity = Rarity.UNCOMMON

    def __init__(self):
        super().__init__(ValorMedal.base_rarity)


class RuinMark(Item):
    description = "Advance Class Type for Demon"
    base_rarity = Rarity.UNCOMMON

    def __init__(self):
        super().__init__(RuinMark.base_rarity)
