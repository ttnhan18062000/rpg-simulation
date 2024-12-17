import heapq


class DStarLite:
    def __init__(self, grid, start, goal):
        self.grid = grid  # Grid map
        self.start = start  # Starting position
        self.goal = goal  # Goal position (can be out of bounds)
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.km = 0  # Key modifier
        self.rhs = {}  # RHS values
        self.g = {}  # G values
        self.open_list = []  # Priority queue for open nodes
        self.last = start

        # Initialize RHS and G values
        for i in range(self.rows):
            for j in range(self.cols):
                self.g[(i, j)] = float("inf")
                self.rhs[(i, j)] = float("inf")

        # Handle goals outside the grid
        if not self.in_bounds(goal):
            self.goal = self.find_closest_visible_tile(goal)
            if self.goal is None:
                raise ValueError("No visible tiles found near the goal.")

        self.rhs[self.goal] = 0
        heapq.heappush(self.open_list, (self.calculate_key(self.goal), self.goal))

    def in_bounds(self, pos):
        """Check if position is inside grid bounds"""
        x, y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols

    def is_blocked(self, pos):
        """Check if position is blocked"""
        x, y = pos
        return not self.in_bounds(pos) or self.grid[x][y] == 1

    def calculate_key(self, pos):
        """Calculate key for the priority queue"""
        g_rhs = min(self.g[pos], self.rhs[pos])
        h = self.heuristic(self.start, pos)
        return (g_rhs + h + self.km, g_rhs)

    def heuristic(self, a, b):
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos):
        """Return valid neighbors of a cell"""
        x, y = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        neighbors = [(x + dx, y + dy) for dx, dy in directions]
        return [n for n in neighbors if self.in_bounds(n) and not self.is_blocked(n)]

    def find_closest_visible_tile(self, goal):
        """Find the closest visible and movable tile to an out-of-bounds goal"""
        candidates = []
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.is_blocked((i, j)):
                    dist = self.heuristic((i, j), goal)
                    candidates.append(((i, j), dist))

        candidates.sort(key=lambda x: x[1])
        return candidates[0][0] if candidates else None

    def update_vertex(self, pos):
        """Update RHS and reinsert into the open list"""
        if pos != self.goal:
            self.rhs[pos] = min(
                self.g[neighbor] + 1 for neighbor in self.get_neighbors(pos)
            )

        self.remove_from_open_list(pos)

        if self.g[pos] != self.rhs[pos]:
            heapq.heappush(self.open_list, (self.calculate_key(pos), pos))

    def remove_from_open_list(self, pos):
        """Remove a vertex from the open list"""
        self.open_list = [(k, v) for k, v in self.open_list if v != pos]
        heapq.heapify(self.open_list)

    def compute_shortest_path(self):
        """Main function to compute the shortest path"""
        while self.open_list and (
            self.open_list[0][0] < self.calculate_key(self.start)
            or self.rhs[self.start] != self.g[self.start]
        ):
            _, u = heapq.heappop(self.open_list)

            if self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for neighbor in self.get_neighbors(u):
                    self.update_vertex(neighbor)
            else:
                self.g[u] = float("inf")
                for neighbor in self.get_neighbors(u) + [u]:
                    self.update_vertex(neighbor)

    def get_path(self):
        """Reconstruct the path"""
        path = []
        current = self.start

        while current != self.goal:
            path.append(current)
            if self.g[current] == float("inf"):
                print("No valid path found.")
                return path

            # Choose next step based on minimal cost
            neighbors = self.get_neighbors(current)
            current = min(neighbors, key=lambda n: self.g[n] + 1, default=current)

            # Stop if we are stuck
            if current in path:
                break

        path.append(self.goal)
        return path


# Example usage
grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
]
start = (4, 0)
goal = (0, 2)

dstar = DStarLite(grid, start, goal)
dstar.compute_shortest_path()
path = dstar.get_path()

print("Path:", path)

for x, y in path:
    if x < len(grid) and y < len(grid[0]):
        if grid[x][y] == 1:
            raise Exception("Wrong path, cannot move into non-movable tile")
        elif (x == start[0] and y == start[1]) or (x == goal[0] and y == goal[1]):
            grid[x][y] = 3
        else:
            grid[x][y] = 2


for row in grid:
    print(row)
