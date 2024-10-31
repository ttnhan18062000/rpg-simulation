import pygame


class Tile:
    id_counter = 1

    def __init__(self) -> None:
        self.id = Tile.id_counter
        Tile.id_counter += 1
        self.image = None
        self.character_ids = {}
        self.is_tile_display_changed = False
        self.is_combat = False

    def is_obstacle(self):
        return False

    def is_combat_happen(self):
        return self.is_combat

    def change_tile_combat_status(self, is_combat: bool):
        if self.is_combat != is_combat:
            self.is_tile_display_changed = True
        self.is_combat = is_combat

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


class GroundTile(Tile):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("data/sprites/ground.png")

    def is_obstacle(self):
        return False


class TownTile(Tile):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("data/sprites/town.png")

    def is_obstacle(self):
        return False


class WaterTile(Tile):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("data/sprites/water.png")

    def is_obstacle(self):
        return True


class HumanGeneratorTile(Tile):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("data/sprites/generator.png")

    def is_obstacle(self):
        return True


class DemonGeneratorTile(Tile):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("data/sprites/generator.png")

    def is_obstacle(self):
        return True


class SwampTile(Tile):
    pass


tile_map = {
    0: GroundTile,
    1: TownTile,
    2: WaterTile,
    3: DemonGeneratorTile,
    4: HumanGeneratorTile,
}
