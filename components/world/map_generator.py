import numpy as np
import random


def generate_voronoi_map(width, height):
    # Define region types (0 for ground, 1 for town)
    region_types = [
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
    ]  # Two ground regions and two town regions

    # Number of rows and columns to split the map into quadrants
    num_quadrants_x = 3
    num_quadrants_y = 3

    # Determine the quadrant size
    quadrant_width = width // num_quadrants_x
    quadrant_height = height // num_quadrants_y

    # Place seeds in each quadrant with some randomness
    seeds = []
    for i in range(num_quadrants_y):
        for j in range(num_quadrants_x):
            # Random position within the quadrant
            seed_x = random.randint(
                max(1, j * quadrant_width), min(width - 1, (j + 1) * quadrant_width - 1)
            )
            seed_y = random.randint(
                max(1, i * quadrant_height),
                min(height - 1, (i + 1) * quadrant_height - 1),
            )
            region_type = region_types.pop(0)
            seeds.append((seed_x, seed_y, region_type))

    # Initialize the map
    map_matrix = np.zeros((height, width), dtype=int)

    # For each cell in the map, find the closest seed and assign its type
    for y in range(height):
        for x in range(width):
            # Find the closest seed to this cell
            closest_seed = min(seeds, key=lambda s: abs(s[0] - x) + abs(s[1] - y))
            # Assign the cell the type of the closest seed
            map_matrix[y, x] = closest_seed[2]

    for x, y, type in seeds:
        map_matrix[x][y] = type + 3

    # Replace border tiles with water
    for x in range(width):
        map_matrix[0][x] = 2  # Top border
        map_matrix[height - 1][x] = 2  # Bottom border
    for y in range(height):
        map_matrix[y][0] = 2  # Left border
        map_matrix[y][width - 1] = 2  # Right border

    return map_matrix


# print(generate_voronoi_map(20, 20))
