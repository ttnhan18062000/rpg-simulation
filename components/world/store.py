from enum import Enum


class EntityType(Enum):
    CHARACTER = "character"
    ITEM = "item"
    TILE = "tile"
    GRID = "grid"


class Store:
    def __init__(self) -> None:
        self.data = {}

    def get_key(self, entity_type: EntityType, id):
        return f"{entity_type.value}@{id}"

    def add(self, entity_type: EntityType, id, obj):
        key = self.get_key(entity_type, id)
        if key in self.data:
            raise Exception(f"Id: '{id}' already exists in data store")
        self.data[key] = obj

    def remove(self, entity_type: EntityType, id):
        key = self.get_key(entity_type, id)
        if key in self.data:
            self.data.pop(key)

    def get(self, entity_type: EntityType, id):
        key = self.get_key(entity_type, id)
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
