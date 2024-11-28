from components.world.store import EntityType, Store
from components.character.memory.memory import Memory, MemoryCharacter, MemoryEvent
from components.common.point import Point


class CharacterMemory:
    memory_map = {
        EntityType.CHARACTER: MemoryCharacter,
        EntityType.EVENT: MemoryEvent,
    }

    def __init__(self) -> None:
        self.memories = {}

    def add(self, entity_type: EntityType, id, memory: Memory):
        if entity_type in CharacterMemory.memory_map:
            if not isinstance(memory, CharacterMemory.memory_map[entity_type]):
                raise Exception(
                    f"Wrong memory class used, should be '{CharacterMemory.memory_map[entity_type].__name__}' instead of '{memory.__class__.__name__}'"
                )
        key = Store.get_key(entity_type, id)
        self.memories[key] = memory

    def delete(self, entity_type: EntityType, id):
        key = Store.get_key(entity_type, id)
        if key in self.memories:
            self.memories.pop(key)

    def get_all(self, entity_type: EntityType):
        return [
            obj
            for key, obj in self.memories.items()
            if key.startswith(f"{entity_type.value}")
        ]

    def get_all_sorted_distant(self, entity_type: EntityType, target_point: Point):
        unsorted_memories = [
            obj
            for key, obj in self.memories.items()
            if key.startswith(f"{entity_type.value}")
        ]
        return sorted(
            unsorted_memories,
            key=lambda memory: Point.get_distance_man(
                memory.get_location(), target_point
            ),
        )

    def reset(self):
        self.memories = {}
