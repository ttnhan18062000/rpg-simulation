class MapLoader:
    def init(self):
        pass

    @staticmethod
    def load_map(file_path):
        text_to_tile_map = {
            "water": 0,
            "ground": 1,
            "village": 2,
            "town": 3,
            "swamp": 4,
            "forest": 5,
            "corrupted": 6,
            "ash": 7,
            "castle": 8,
            "battlefield": 9,
            "mystic": 10,
            "ruin": 11,
            "core": 12,
        }
        grid = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                row = [text_to_tile_map[c] for c in line.split()]
                grid.append(row)
        grid = [
            [grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))
        ]  # transpose
        return grid


# grid = MapLoader.load_map("../../data/world/map1.txt")
# for row in grid:
#     print(row)
# print(f"{len(grid)} {len(grid[0])}")
