from components.item.equipment import EquipmentType
from components.item.item import Item


class CharacterInventory:
    def __init__(self) -> None:
        self.items = {}

    def get_items(self, item_name):
        if item_name in self.items:
            return self.items

    def get_equipment_by_types(self, equipment_type: EquipmentType):
        return {
            item_name: item
            for item_name, item in self.items
            if item.is_equipment() and item.get_equipment_type() is equipment_type
        }

    def get_materials(self):
        return {
            item_name: item for item_name, item in self.items if item.get_material()
        }

    def get_consumables(self):
        return {
            item_name: item for item_name, item in self.items if item.is_consumable()
        }

    def add_item(self, item: Item):
        item_name = item.get_name()
        if item_name in self.items:
            self.items[item_name].append(item)
        else:
            self.items[item_name] = [item]
