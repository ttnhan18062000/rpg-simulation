def find_visible_points(matrix, x, y, d):
    rows, cols = len(matrix), len(matrix[0])
    visible_points = []

    # Iterate over all points within a square boundary around (x, y)
    for i in range(x - d, x + d + 1):
        for j in range(y - d, y + d + 1):
            # Skip the starting position itself
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
                    if matrix[intermediate_x][intermediate_y] == 1:
                        is_visible = False
                        break

                # If no obstacle was encountered along the line of sight, add the point
                if is_visible:
                    visible_points.append((i, j))

    return visible_points


matrix = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0],
]

# Starting position
x, y = 3, 3  # Start from the center of the matrix
d = 3  # Set the Manhattan distance

# Find visible points
visible_points = find_visible_points(matrix, x, y, d)

# Output the result
print("Visible points:", visible_points)

matrix[x][y] = 3
for x, y in visible_points:
    matrix[x][y] = 2


for row in matrix:
    print(row)
