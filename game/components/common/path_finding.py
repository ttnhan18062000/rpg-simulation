from components.common.point import Point
from components.world.store import get_store, EntityType


def check_valid_step(new_pos: Point):
    store = get_store()
    tile_id = store.get(EntityType.GRID, 0).get_tile(new_pos)
    tile = store.get(EntityType.TILE, tile_id)
    if tile.is_obstacle():
        return False
    return True


def get_move_from_target(current: Point, target: Point, is_chasing=True):
    """
    Calculate the next move to escape from a target point in a 2D matrix.
    """
    moves = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]

    best_move = None
    if is_chasing:
        base_distance = float("inf")
    else:
        base_distance = float("-inf")

    for move in moves:
        new_pos = current + move
        distance = Point.get_distance_man(new_pos, target)

        if check_valid_step(current + move):
            if is_chasing and distance < base_distance:
                base_distance = distance
                best_move = move
            elif not is_chasing and distance > base_distance:
                base_distance = distance
                best_move = move

    return best_move
