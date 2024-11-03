from components.world.tile import Tile, GroundTile, TownTile, tile_map
from components.world.store import get_store, EntityType
from components.common.point import Point


class Grid:
    def __init__(self, grid_data) -> None:
        self.tiles = []
        self.initialize_tiles(grid_data)
        self.width = len(self.tiles)
        self.height = len(self.tiles[0])

    # def convert_grid_data(self, grid_data):
    #     new_grid_data = [
    #         [0 for _ in range(len(grid_data))] for _ in range(len(grid_data[0]))
    #     ]
    #     for i in range(len(grid_data)):
    #         for j in range(len(grid_data[0])):
    #             new_grid_data[j][i] = grid_data[i][j]
    #     return new_grid_data

    def initialize_tiles(self, grid_data):
        store = get_store()
        # self.tiles = [
        #     [tile_map[tile_id]() for tile_id in row]
        #     for row in self.convert_grid_data(grid_data)
        # ]
        self.tiles = [[tile_map[tile_id]() for tile_id in row] for row in grid_data]
        for row in self.tiles:
            for tile in row:
                store.add(EntityType.TILE, tile.id, tile)
        self.tiles = [[tile.id for tile in row] for row in self.tiles]

    def is_valid_location(self, pos: Point):
        if pos.x < 0 or pos.x >= self.width or pos.y < 0 or pos.y > self.height:
            return False
        return True

    def get_tile(self, pos: Point):
        if self.is_valid_location(pos):
            return self.tiles[pos.x][pos.y]
        raise Exception(f"The povided location {pos.x},{pos.y} is not valid")

    def is_moveable_tile(self, pos: Point):
        if not self.is_valid_location(pos):
            return False
        if self.tiles[pos.x][pos.y].is_obstacle:
            return False
        return True

    def print_tiles(self):
        for row in self.tiles:
            print(" ".join([tile.__class__.__name__ for tile in row]))
