from components.common.point import Point
from components.world.store import get_store, EntityType
from components.utils.tile_utils import get_tile_objects


class CharacterVision:
    def __init__(self, range) -> None:
        self.range = range

    def set_range(self, range: int):
        self.range = range

    # TODO: This LIED, it get visible location instead of tile object
    def get_visible_tiles(self, current_pos: Point):
        store = get_store()
        grid = store.get(EntityType.GRID, 0)
        tile_ids = grid.tiles
        obstacle_matrix = [
            [
                1 if store.get(EntityType.TILE, tile_id).is_block_vision() else 0
                for tile_id in row
            ]
            for row in tile_ids
        ]
        return self.find_visible_points(
            obstacle_matrix, current_pos.x, current_pos.y, grid.width, grid.height
        )

    def get_visible_tile_objects(self, current_pos: Point):
        store = get_store()
        grid = store.get(EntityType.GRID, 0)
        tile_ids = grid.tiles
        obstacle_matrix = [
            [
                1 if store.get(EntityType.TILE, tile_id).is_block_vision() else 0
                for tile_id in row
            ]
            for row in tile_ids
        ]
        visible_points = self.find_visible_points(
            obstacle_matrix, current_pos.x, current_pos.y, grid.width, grid.height
        )
        return get_tile_objects(visible_points)

    def find_visible_points(self, obstacle_matrix, x, y, width, height):
        d = self.range
        rows = width
        cols = height
        visible_points = []

        # Iterate over all points within a square boundary around (x, y)
        for i in range(x - d, x + d + 1):
            for j in range(y - d, y + d + 1):
                # Skip the starting position itself and out of map points
                if (i, j) == (x, y):
                    continue

                # Check if the point is within bounds and within the Manhattan distance
                if 0 <= i < rows and 0 <= j < cols and abs(i - x) + abs(j - y) <= d:
                    # Determine the direction from (x, y) to (i, j)
                    dx, dy = i - x, j - y
                    step = max(abs(dx), abs(dy))  # Number of steps in that direction
                    is_visible = True

                    # Check each intermediate point along the line from (x, y) to (i, j)
                    for k in range(1, step + 1):
                        intermediate_x = x + (dx // step) * k
                        intermediate_y = y + (dy // step) * k

                        # Stop if an obstacle is encountered
                        if obstacle_matrix[intermediate_x][intermediate_y]:
                            is_visible = False
                            break

                    # If no obstacle was encountered along the line of sight, add the point
                    if is_visible:
                        visible_points.append(Point(i, j))

        return visible_points
