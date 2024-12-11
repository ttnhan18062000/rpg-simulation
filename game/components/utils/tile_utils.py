from components.common.point import Point
from components.world.store import get_store, EntityType
from components.world.tile import Tile


def get_tile_object(pos: Point) -> Tile:
    store = get_store()
    tile_id = store.get(EntityType.GRID, 0).get_tile(pos)
    tile = store.get(EntityType.TILE, tile_id)
    return tile


def get_tile_objects(pos_list: list) -> Tile:
    store = get_store()
    tiles = []
    for pos in pos_list:
        tile_id = store.get(EntityType.GRID, 0).get_tile(pos)
        tile = store.get(EntityType.TILE, tile_id)
        tiles.append(tile)
    return tiles
