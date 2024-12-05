from enum import Enum

from components.item.equipment import EquipmentType
from components.item.item import Item

from data.logs.logger import logger


class OnAddItemAction(Enum):
    CAN_EQUIP_ITEM = 1
    CAN_CONSUME_ITEM = 2


class CharacterInventory:
    def __init__(self) -> None:
        self.items = {}
        self.recently_added_item_names = []

    def get_item(self, item_name):
        if item_name in self.items:
            return self.items[item_name]
        return None

    def remove_item(self, item_name, stack=1):
        if item_name not in self.items:
            raise Exception(f"Item {item_name} is not found in the character inventory")
        # TODO: Refactor this, currently inefficient
        if (
            not isinstance(self.items[item_name], list)
            and self.items[item_name].can_be_stacked()
        ):
            self.items[item_name].decrease_stack(stack)
        else:
            # TODO: get the most suitable/powerful version of the item if there are multiple duplicated item
            self.items[item_name].pop(0)
            logger.debug(
                f"Successfully remove one item {item_name} from the character inventory, left {len(self.items[item_name])} coppies"
            )
            if len(self.items[item_name]) == 0:
                self.items.pop(item_name)
                logger.debug(
                    f"Successfully remove the whole item {item_name} from the character inventory"
                )

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

    # Currently infinite stack, can be changed later
    def add_item(self, item: Item):
        item_name = item.get_name()
        if item_name in self.items:
            if item.can_be_stacked():
                self.items[item_name].increase_stack(item.get_stack())
            else:
                self.items[item_name].append(item)
        else:
            if item.can_be_stacked():
                self.items[item_name] = item
            else:
                self.items[item_name] = [item]

        if item.is_equipment():
            return OnAddItemAction.CAN_EQUIP_ITEM
        elif item.is_consumable():
            return OnAddItemAction.CAN_CONSUME_ITEM

        self.recently_added_item_names.append(item_name)

    def get_recently_added_item_names(self):
        return self.recently_added_item_names

    def clear_recently_added_item_names(self):
        self.recently_added_item_names = []
