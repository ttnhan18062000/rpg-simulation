from enum import Enum
from components.database.producer import produce_messages


class EntityType(Enum):
    CHARACTER = "character"
    ITEM = "item"
    TILE = "tile"
    GRID = "grid"
    EVENT = "event"


class Store:
    def __init__(self) -> None:
        self.data = {}

    @staticmethod
    def get_key(entity_type: EntityType, id):
        return f"{entity_type.value}@{id}"

    def add(self, entity_type: EntityType, id, obj):
        key = Store.get_key(entity_type, id)
        if key in self.data:
            raise Exception(f"Id: '{id}' already exists in data store")

        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            obj_dict = obj.to_dict()
            obj_dict["data_action"] = "update"
            produce_messages(obj_dict)

        self.data[key] = obj

    def remove(self, entity_type: EntityType, id):
        key = Store.get_key(entity_type, id)

        obj = self.data[key]
        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            obj_dict = obj.to_dict()
            obj_dict["data_action"] = "delete"
            produce_messages(obj_dict)

        if key in self.data:
            self.data.pop(key)

    def get(self, entity_type: EntityType, id):
        key = Store.get_key(entity_type, id)
        if key in self.data:
            return self.data[key]
        return None

    def get_all(self, entity_type: EntityType):
        return [
            obj
            for key, obj in self.data.items()
            if key.startswith(f"{entity_type.value}")
        ]


store = Store()


def get_store():
    return store
