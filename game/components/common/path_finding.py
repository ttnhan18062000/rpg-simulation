from components.common.point import Point
from components.world.store import get_store, EntityType
from components.utils.tile_utils import get_tile_object


def check_valid_step(character, new_pos: Point):
    tile = get_tile_object(new_pos)
    restricted_tiles = character.get_restricted_tile_types()
    if tile.is_obstacle() or isinstance(tile, tuple(restricted_tiles)):
        return False
    return True


def get_move_from_target(character, current: Point, target: Point, is_chasing=True):
    """
    Calculate the next move to either chase or escape from a target point in a 2D matrix,
    prioritizing the axis with the greater distance difference.
    """
    moves = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]
    best_move = None
    base_distance = float("inf") if is_chasing else float("-inf")

    # Calculate axis priorities
    delta_x = abs(target.x - current.x)
    delta_y = abs(target.y - current.y)

    # Determine dominant axis
    if delta_x > delta_y:
        prioritized_moves = [Point(-1, 0), Point(1, 0)] + [Point(0, -1), Point(0, 1)]
    else:
        prioritized_moves = [Point(0, -1), Point(0, 1)] + [Point(-1, 0), Point(1, 0)]

    for move in prioritized_moves:
        new_pos = current + move

        # Skip invalid steps
        if not check_valid_step(character, new_pos):
            continue

        distance = Point.get_distance_man(new_pos, target)

        # Update the best move based on the chasing/escaping logic
        if (is_chasing and distance < base_distance) or (
            not is_chasing and distance > base_distance
        ):
            base_distance = distance
            best_move = move

            # Early exit for optimal case
            if is_chasing and base_distance == 1:
                return best_move

    return best_move
