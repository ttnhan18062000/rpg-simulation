import pygame

from components.action.event import EventType
from components.character.status import GroundTileBuff, TownTileBuff
from components.item.equipment import DamagedAncientArmor, DamagedAncientSword


# TODO: Change to class-level properties instead, to make it more efficient
# TODO: WHERE TF IS THE TILE's LOCATION POINT PROPERTY
class Tile:
    id_counter = 1
    image = None

    def __init__(self) -> None:
        self.id = Tile.id_counter
        Tile.id_counter += 1
        self.character_ids = {}
        self.is_tile_display_changed = False
        self.is_combat = False
        self.event_dict_ids = {}
        self.collectable_items = {}

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def get_image(cls):
        return cls.image

    def get_id(self):
        return self.id

    def is_obstacle(self):
        return False

    def is_block_vision(self):
        return False

    def is_combat_happen(self):
        return self.is_combat

    def get_event(self, event_type: EventType):
        if event_type in self.event_dict_ids:
            return self.event_dict_ids[event_type]
        return None

    def set_tile_combat_status(self, is_combat: bool, combat_event_id=None):
        if self.is_combat != is_combat:
            self.is_tile_display_changed = True
        self.is_combat = is_combat

        if self.is_combat:
            self.event_dict_ids[EventType.COMBAT] = combat_event_id
        else:
            self.event_dict_ids.pop(EventType.COMBAT)

    def get_character_ids(self):
        return self.character_ids

    def add_character_id(self, character_id):
        self.character_ids[character_id] = 1
        self.is_tile_display_changed = False

    def remove_character_id(self, character_id):
        self.character_ids.pop(character_id)
        if len(self.character_ids) == 0:
            self.is_tile_display_changed = True

    def should_redraw(self):
        return self.is_tile_display_changed

    def reset_redraw_status(self):
        self.is_tile_display_changed = False

    def character_move_in(self, character):
        self.add_character_id(character.get_info().id)
        self.check_and_apply_status(character)

    def check_and_apply_status(self, charater):
        pass

    def get_collectable_items(self):
        return self.collectable_items

    def get_collectable_item_list(self):
        return list(self.collectable_items.keys())

    def is_collectable(self):
        return len(self.collectable_items) > 0


class HumanGeneratorTile(Tile):
    image = pygame.image.load("data/sprites/generator.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class DemonGeneratorTile(Tile):
    image = pygame.image.load("data/sprites/generator.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class WaterTile(Tile):
    image = pygame.image.load("data/sprites/water1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return True


class GroundTile(Tile):
    image = pygame.image.load("data/sprites/ground1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False

    def check_and_apply_status(self, character):
        from components.character.character_class import Demon

        if character.get_faction() is Demon.__name__:
            character.add_status(GroundTileBuff(3))


class VillageTile(Tile):
    image = pygame.image.load("data/sprites/village1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class TownTile(Tile):
    image = pygame.image.load("data/sprites/town1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False

    def check_and_apply_status(self, character):
        from components.character.character_class import Human

        if character.get_faction() is Human.__name__:
            character.add_status(TownTileBuff(3))


class SwampTile(Tile):
    image = pygame.image.load("data/sprites/swamp1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class ForestTile(Tile):
    image = pygame.image.load("data/sprites/forest1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class CorruptedTile(Tile):
    image = pygame.image.load("data/sprites/corrupted1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class AshTile(Tile):
    image = pygame.image.load("data/sprites/ash1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class CastleTile(Tile):
    image = pygame.image.load("data/sprites/castle1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class BattlefieldTile(Tile):
    image = pygame.image.load("data/sprites/battlefield1.png")

    def __init__(self) -> None:
        super().__init__()
        self.collectable_items = {
            DamagedAncientArmor(): 0.5,
            DamagedAncientSword(): 0.5,
        }

    def is_obstacle(self):
        return False


class MysticTile(Tile):
    image = pygame.image.load("data/sprites/mystic1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class RuinTile(Tile):
    image = pygame.image.load("data/sprites/ruin1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


class CoreTile(Tile):
    image = pygame.image.load("data/sprites/core1.png")

    def __init__(self) -> None:
        super().__init__()

    def is_obstacle(self):
        return False


tile_map = {
    -1: DemonGeneratorTile,
    -2: HumanGeneratorTile,
    0: WaterTile,
    1: GroundTile,
    2: VillageTile,
    3: TownTile,
    4: SwampTile,
    5: ForestTile,
    6: CorruptedTile,
    7: AshTile,
    8: CastleTile,
    9: BattlefieldTile,
    10: MysticTile,
    11: RuinTile,
    12: CoreTile,
}
