from .item import Rarity
from components.item.item import Item, ItemType


class Gold(Item):
    item_type: ItemType = ItemType.MATERIAL
    description = "Basic Currency"
    base_rarity = Rarity.COMMON

    def __init__(self):
        super().__init__(Gold.base_rarity)
