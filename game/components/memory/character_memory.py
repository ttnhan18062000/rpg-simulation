from enum import Enum

from components.world.store import EntityType, Store
from components.memory.memory import (
    Memory,
    MemoryCharacter,
    MemoryEvent,
    MemoryTile,
)
from components.common.point import Point


class CharacterMemoryType(Enum):
    TEMPORARY = 1
    PERMANENT = 2


class CharacterMemory:
    memory_map = {
        EntityType.CHARACTER: MemoryCharacter,
        EntityType.EVENT: MemoryEvent,
        EntityType.TILE: MemoryTile,
    }

    def __init__(self) -> None:
        self.temporary_memories = {}
        self.permanent_memories = {}

    def add(
        self,
        entity_type: EntityType,
        id,
        memory: Memory,
        memory_type: CharacterMemoryType,
    ):
        if entity_type in CharacterMemory.memory_map:
            if not isinstance(memory, CharacterMemory.memory_map[entity_type]):
                raise Exception(
                    f"Wrong memory class used, should be '{CharacterMemory.memory_map[entity_type].__name__}' instead of '{memory.__class__.__name__}'"
                )
        key = Store.get_key(entity_type, id)
        if memory_type is CharacterMemoryType.TEMPORARY:
            self.temporary_memories[key] = memory
        elif memory_type is CharacterMemoryType.PERMANENT:
            self.permanent_memories[key] = memory

    def delete(self, entity_type: EntityType, id):
        key = Store.get_key(entity_type, id)
        if key in self.memories:
            self.memories.pop(key)

    def get_all(self, entity_type: EntityType):
        return [
            obj
            for key, obj in self.temporary_memories.items()
            if key.startswith(f"{entity_type.value}")
        ]

    # TODO: Better management for temporary and permanent memories
    def get_all(
        self, entity_type: EntityType, target_point: Point, is_sorted_distance=True
    ):
        if entity_type is EntityType.TILE:
            unsorted_memories = [
                obj
                for key, obj in self.permanent_memories.items()
                if key.startswith(f"{entity_type.value}")
            ]
            if is_sorted_distance:
                return sorted(
                    unsorted_memories,
                    key=lambda memory: Point.get_distance_man(
                        memory.get_location(), target_point
                    ),
                )
            else:
                return unsorted_memories
        else:
            unsorted_memories = [
                obj
                for key, obj in self.temporary_memories.items()
                if key.startswith(f"{entity_type.value}")
            ]
            if is_sorted_distance:
                return sorted(
                    unsorted_memories,
                    key=lambda memory: Point.get_distance_man(
                        memory.get_location(), target_point
                    ),
                )
            else:
                return unsorted_memories

    def reset(self):
        self.temporary_memories = {}
