import numpy as np
import random


def generate_voronoi_map(width, height):
    # Define region types (0 for ground, 1 for town)
    region_types = [0, 0, 1, 1]  # Two ground regions and two town regions

    # Number of rows and columns to split the map into quadrants
    num_quadrants_x = 2
    num_quadrants_y = 2

    # Determine the quadrant size
    quadrant_width = width // num_quadrants_x
    quadrant_height = height // num_quadrants_y

    # Place seeds in each quadrant with some randomness
    seeds = []
    for i in range(num_quadrants_y):
        for j in range(num_quadrants_x):
            # Random position within the quadrant
            seed_x = random.randint(j * quadrant_width, (j + 1) * quadrant_width - 1)
            seed_y = random.randint(i * quadrant_height, (i + 1) * quadrant_height - 1)
            region_type = region_types.pop(0)
            seeds.append((seed_x, seed_y, region_type))

    # Initialize the map
    map_matrix = np.zeros((height, width), dtype=int)

    # For each cell in the map, find the closest seed and assign its type
    for y in range(height):
        for x in range(width):
            # Find the closest seed to this cell
            closest_seed = min(seeds, key=lambda s: (s[0] - x) ** 2 + (s[1] - y) ** 2)
            # Assign the cell the type of the closest seed
            map_matrix[y, x] = closest_seed[2]

    return map_matrix


# Example usage
width, height = 20, 20  # Define the map dimensions
voronoi_map = generate_voronoi_map(width, height)

# Replace border with water tiles


# Display the map
for row in voronoi_map:
    print("[", end="")
    print(", ".join(str(cell) for cell in row), end="],\n")
