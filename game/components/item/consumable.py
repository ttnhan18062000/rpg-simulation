from .item import Rarity
from components.item.item import Item, ItemType


class ValorMedal(Item):
    item_type: ItemType = ItemType.CONSUMABLE
    description = "Advance Class Type for Human"
    base_rarity = Rarity.UNCOMMON

    def __init__(self):
        super().__init__(ValorMedal.base_rarity)


class RuinMark(Item):
    item_type: ItemType = ItemType.CONSUMABLE
    description = "Advance Class Type for Demon"
    base_rarity = Rarity.UNCOMMON

    def __init__(self):
        super().__init__(ValorMedal.base_rarity)
