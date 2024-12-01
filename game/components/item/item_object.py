from enum import Enum

from ..common.point import Point
from components.common.game_object import GameObject
from components.item.item import Item


class ItemObject(GameObject):
    def __init__(self, pos: Point, img: str, item: Item):
        super().__init__(pos, img)
        self.item = item

    def on_collect(self):
        pass

    def on_expire(self):
        pass
