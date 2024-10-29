import pygame


class Tile:
    id_counter = 1

    def __init__(self) -> None:
        self.id = Tile.id_counter
        Tile.id_counter += 1
        self.image = None
        self.character_ids = {}

    def is_obstacle(self):
        return False

    def get_character_ids(self):
        return self.character_ids

    def add_character_id(self, character_id):
        self.character_ids[character_id] = 1

    def remove_character_id(self, character_id):
        self.character_ids.pop(character_id)


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
