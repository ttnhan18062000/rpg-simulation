import heapq

from components.common.point import Point
from components.world.store import get_store, EntityType
from components.utils.tile_utils import get_tile_object


def check_valid_step(character, new_pos: Point):
    tile = get_tile_object(new_pos)
    restricted_tiles = character.get_restricted_tile_types()
    if not tile or tile.is_obstacle() or isinstance(tile, tuple(restricted_tiles)):
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


class DStarLite:
    def __init__(
        self, character, grid_dict: dict[Point, float], start: Point, goal: Point
    ):
        self.character = character
        self.grid_dict = grid_dict
        self.start = start  # Instance of Point
        self.goal = goal  # Instance of Point
        self.km = 0
        self.U = []  # Priority queue
        self.rhs = {}
        self.g = {}
        self.init()

    def init(self):
        """Initialize g-values and rhs-values for all points."""
        for position in self.grid_dict.keys():
            self.g[position] = float("inf")
            self.rhs[position] = float("inf")
        self.rhs[self.goal] = 0
        heapq.heappush(self.U, (self.calculate_key(self.goal), self.goal))

    def calculate_key(self, s):
        """Calculate the key for a given point."""
        g_rhs = min(self.g[s], self.rhs[s])
        return (g_rhs + Point.get_distance_man(self.start, s) + self.km, g_rhs)

    def update_vertex(self, u):
        """Update a vertex in the priority queue."""
        if u != self.goal:
            neighbors = self.get_neighbors(u)
            self.rhs[u] = min(self.g[v] + 1 for v in neighbors if self.is_valid(v))
        # Remove u from the queue
        self.U = [(k, v) for k, v in self.U if v != u]
        heapq.heapify(self.U)
        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.U, (self.calculate_key(u), u))

    def get_neighbors(self, s):
        """Get neighboring points."""
        directions = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]
        neighbors = [s + direction for direction in directions]
        valid_neighbors = [n for n in neighbors if self.is_valid(n)]

        # Initialize g and rhs for unseen points
        for n in valid_neighbors:
            if n not in self.g:
                self.g[n] = float("inf")
                self.rhs[n] = float("inf")
        return valid_neighbors

    def is_valid(self, s):
        """Check if a point is within bounds and walkable."""
        return s not in self.grid_dict or self.grid_dict[s] == True

    def compute_shortest_path(self):
        """Compute the shortest path."""
        while self.U and (
            self.U[0][0] < self.calculate_key(self.start)
            or self.rhs[self.start] != self.g[self.start]
        ):
            _, u = heapq.heappop(self.U)
            if self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.get_neighbors(u):
                    self.update_vertex(s)
            else:
                self.g[u] = float("inf")
                self.update_vertex(u)
                for s in self.get_neighbors(u):
                    self.update_vertex(s)

    def extract_path(self):
        """Extract the shortest path from start to goal."""
        path = []
        s = self.start
        while s != self.goal:
            path.append(s)
            neighbors = self.get_neighbors(s)
            s = min(neighbors, key=lambda n: self.g[n] + 1, default=None)
            if not s or self.g[s] == float("inf"):
                return []  # No path found
        path.append(self.goal)
        return path


def compute_shortest_path(character, vision_tiles, start, goal):
    """High-level function to compute the shortest path."""
    vision_tiles = {p: check_valid_step(character, p) for p in vision_tiles.keys()}
    # Adding the starting location because it is not appear in the vision tiles
    vision_tiles.update({start: True})
    dstar = DStarLite(character, vision_tiles, start, goal)
    dstar.compute_shortest_path()
    result_path = dstar.extract_path()
    return result_path[1] - start if len(result_path) > 1 else None
