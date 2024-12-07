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
        self.recently_added = {
            EntityType.CHARACTER: None,
            EntityType.ITEM: None,
            EntityType.EVENT: None,
        }

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
        if entity_type in (EntityType.CHARACTER, EntityType.ITEM, EntityType.EVENT):
            self.recently_added[entity_type] = obj

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

    def get_recently_added(self, entity_type: EntityType):
        if entity_type in self.recently_added:
            return self.recently_added[entity_type]
        return None

    def get_all(self, entity_type: EntityType):
        all_entities = [
            obj
            for key, obj in self.data.items()
            if key.startswith(f"{entity_type.value}")
        ]
        # Get character descending by level, because when drawing, we should draw the highest level character
        # if multiple characters are standing on the same tile
        if entity_type == EntityType.CHARACTER:
            all_entities = sorted(
                all_entities,
                key=lambda char: char.get_level().get_current_level(),
                reverse=True,
            )
        return all_entities


store = Store()


def get_store():
    return store
