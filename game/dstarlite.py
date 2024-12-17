import heapq


class DStarLite:
    def __init__(self, grid_dict, start, goal):
        self.grid_dict = grid_dict
        self.start = start
        self.goal = goal
        self.km = 0
        self.U = []
        self.rhs = {}
        self.g = {}
        self.init()

    def init(self):
        """Initialize g-values and rhs-values for all points."""
        for position, value in self.grid_dict.items():
            self.g[position] = float("inf")
            self.rhs[position] = float("inf")
        self.rhs[self.goal] = 0
        heapq.heappush(self.U, (self.calculate_key(self.goal), self.goal))
        print(self.U)

    def calculate_key(self, s):
        """Calculate the key for a given point."""
        g_rhs = min(self.g[s], self.rhs[s])
        return (g_rhs + self.h(self.start, s) + self.km, g_rhs)

    def h(self, a, b):
        """Heuristic: Manhattan distance."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def update_vertex(self, u):
        """Update a vertex in the priority queue."""
        if u != self.goal:
            neighbors = self.get_neighbors(u)
            print(f"{u} > {neighbors}")
            self.rhs[u] = min(self.g[v] + 1 for v in neighbors if self.is_valid(v))
        self.U = [(k, v) for k, v in self.U if v != u]
        heapq.heapify(self.U)
        print(self.U)
        print(f"g = {self.g[u]}, rhs = {self.rhs[u]}")
        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.U, (self.calculate_key(u), u))
        print(self.U)

    def get_neighbors(self, s):
        """Get neighboring points."""
        x, y = s
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = [(x + dx, y + dy) for dx, dy in directions]
        valid_neightbors = [n for n in neighbors if self.is_valid(n)]
        for n in valid_neightbors:
            if n not in self.g:
                self.g[n] = float("inf")
                self.rhs[n] = float("inf")
        return valid_neightbors

    def is_valid(self, s):
        """Check if a point is within bounds and walkable."""
        x, y = s
        # return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] == 0
        return s not in self.grid_dict or self.grid_dict[s] == True

    def compute_shortest_path(self):
        """Compute the shortest path."""
        while self.U and (
            self.U[0][0] < self.calculate_key(self.start)
            or self.rhs[self.start] != self.g[self.start]
        ):
            _, u = heapq.heappop(self.U)
            if self.g[u] > self.rhs[u]:
                print(f"{u} g = {self.g[u]}, rhs = {self.rhs[u]}")
                self.g[u] = self.rhs[u]
                for s in self.get_neighbors(u):
                    self.update_vertex(s)
            else:
                self.g[u] = float("inf")
                self.update_vertex(u)
                for s in self.get_neighbors(u):
                    self.update_vertex(s)
            # print(self.U)
            # print(
            #     self.U[0][0] < self.calculate_key(self.start)
            #     or self.rhs[self.start] != self.g[self.start]
            # )

    def extract_path(self):
        """Extract the shortest path from start to goal."""
        path = []
        s = self.start
        while s != self.goal:
            path.append(s)
            neighbors = self.get_neighbors(s)
            print(neighbors)
            print(f"{[self.g[n] for n in neighbors]}")
            s = min(neighbors, key=lambda n: self.g[n] + 1)
            if self.g[s] == float("inf"):
                return []  # No path found
        path.append(self.goal)
        return path


def compute_shortest_path(grid, start, goal):
    """High-level function to compute the shortest path."""
    # grid_dict = {
    #     (x, y): grid[x][y] for y in range(len(grid)) for x in range(len(grid[0]))
    # }

    # grid_dict = {t: v for t, v in grid.items()}
    grid_dict = grid
    grid_dict.update({start: True})
    dstar = DStarLite(grid_dict, start, goal)
    dstar.compute_shortest_path()
    result_path = dstar.extract_path()

    # g_dict = dict_to_grid(dstar.g)
    # for x in range(len(g_dict)):
    #     for y in range(len(g_dict[x])):
    #         if (x == start[0] and y == start[1]) or (x == goal[0] and y == goal[1]):
    #             print(3, end=" ")
    #         elif (x, y) in result_path:
    #             print(2, end=" ")
    #         elif x < len(grid) and y < len(grid[0]):
    #             print(grid[x][y], end=" ")
    #         else:
    #             print(0, end=" ")
    #     print()

    return result_path


def dict_to_grid(grid_dict, start, goal):
    # Find the maximum x and y values to determine grid size
    max_x = max(x for x, y in grid_dict.keys())
    max_y = max(y for x, y in grid_dict.keys())

    # Initialize an empty grid with zeros
    grid = [[0 for _ in range(max_y + 1)] for _ in range(max_x + 1)]

    # Populate the grid using the dictionary values
    for (x, y), value in grid_dict.items():
        if (x == start[0] and y == start[1]) or (x == goal[0] and y == goal[1]):
            grid[x][y] = "2"
        elif value == False:
            grid[x][y] = "1"
        else:
            grid[x][y] = "0"

    return grid


# Example usage
data = {
    (10, 3): True,
    (11, 2): True,
    (11, 3): True,
    (11, 4): True,
    (12, 1): False,
    (12, 2): False,
    (12, 3): True,
    (12, 4): True,
    (12, 5): True,
    (13, 0): False,
    (13, 1): False,
    (13, 2): False,
    (13, 3): True,
    (13, 4): True,
    (13, 5): True,
    (13, 6): False,
    (14, 0): False,
    (14, 1): False,
    (14, 2): False,
    (14, 3): True,
    (14, 4): True,
    (14, 5): True,
    (14, 6): False,
    (14, 7): False,
    (15, 0): False,
    (15, 1): False,
    (15, 2): False,
    (15, 4): True,
    (15, 5): True,
    (15, 6): False,
    (15, 7): False,
    (15, 8): False,
    (16, 0): False,
    (16, 1): True,
    (16, 2): True,
    (16, 3): True,
    (16, 4): True,
    (16, 5): True,
    (16, 6): False,
    (16, 7): False,
    (17, 0): False,
    (17, 1): True,
    (17, 2): True,
    (17, 3): True,
    (17, 4): True,
    (17, 5): True,
    (17, 6): False,
    (18, 1): True,
    (18, 2): True,
    (18, 3): True,
    (18, 4): True,
    (18, 5): True,
    (19, 2): True,
    (19, 3): True,
    (19, 4): True,
    (20, 3): True,
    (9, 3): True,
    (10, 2): True,
    (10, 4): True,
    (11, 1): True,
    (11, 5): True,
    (12, 0): False,
    (12, 6): False,
    (13, 7): False,
    (14, 8): False,
    (15, 3): True,
    (8, 3): True,
    (9, 2): True,
    (9, 4): True,
    (10, 1): True,
    (10, 5): True,
    (11, 0): False,
    (11, 6): False,
    (12, 7): False,
    (13, 8): False,
    (8, 4): True,
    (9, 5): True,
    (10, 6): False,
    (11, 7): False,
    (12, 8): False,
    (13, 9): False,
    (7, 4): True,
    (8, 5): True,
    (9, 6): False,
    (10, 7): False,
    (11, 8): False,
    (12, 9): False,
    (7, 5): True,
    (8, 6): False,
    (9, 7): False,
    (10, 8): False,
    (11, 9): False,
    (12, 10): False,
    (13, 10): False,
    (14, 9): False,
    (6, 5): True,
    (7, 6): False,
    (8, 7): False,
    (9, 8): False,
    (10, 9): False,
    (11, 10): False,
    (5, 5): False,
    (6, 4): True,
    (6, 6): False,
    (7, 3): True,
    (7, 7): False,
    (8, 2): True,
    (8, 8): False,
    (9, 1): True,
    (9, 9): False,
    (10, 0): False,
    (10, 10): False,
}

start = (10, 5)
goal = (10, 10)


grid = dict_to_grid(data, start, goal)

for row in grid:
    for cell in row:
        print(cell, end=" ")
    print()

path = compute_shortest_path(data, start, goal)
print("Path:", path)
