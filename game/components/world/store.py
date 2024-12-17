from enum import Enum
import threading

from components.database.producer import produce_messages


class EntityType(Enum):
    CHARACTER = "character"
    ITEM = "item"
    TILE = "tile"
    GRID = "grid"
    EVENT = "event"


class Store:
    def __init__(self) -> None:
        self.data = {entity_type.value: {} for entity_type in EntityType}
        self.recently_added = {entity_type.value: None for entity_type in EntityType}

    @staticmethod
    def get_key(entity_type: EntityType, id):
        return f"{entity_type.value}@{id}"

    def get_sub_dict(self, entity_type: EntityType):
        return self.data[entity_type.value]

    def add(self, entity_type: EntityType, id, obj):
        sub_dict = self.get_sub_dict(entity_type)
        if id in sub_dict:
            raise Exception(f"Id: '{id}' already exists in data store")

        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            obj_dict = obj.to_dict()
            obj_dict["data_action"] = "update"
            produce_messages(obj_dict)

        sub_dict[id] = obj
        if entity_type in (EntityType.CHARACTER, EntityType.ITEM, EntityType.EVENT):
            self.recently_added[entity_type] = obj

    def remove(self, entity_type: EntityType, id):
        sub_dict = self.get_sub_dict(entity_type)

        obj = sub_dict
        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            obj_dict = obj.to_dict()
            obj_dict["data_action"] = "delete"
            produce_messages(obj_dict)

        if id in sub_dict:
            sub_dict.pop(id)

    def get(self, entity_type: EntityType, id):
        sub_dict = self.get_sub_dict(entity_type)
        if id in sub_dict:
            return sub_dict[id]
        return None

    def get_recently_added(self, entity_type: EntityType):
        if entity_type in self.recently_added:
            return self.recently_added[entity_type]
        return None

    def get_all(self, entity_type: EntityType):
        result = self.get_sub_dict(entity_type).values()
        # Get character descending by level, because when drawing, we should draw the highest level character
        # if multiple characters are standing on the same tile
        if entity_type == EntityType.CHARACTER:
            result = sorted(
                result,
                key=lambda char: char.get_level().get_current_level(),
                reverse=True,
            )
        return result


store = Store()

_lock = threading.Lock()


def get_store():
    with _lock:
        return store
