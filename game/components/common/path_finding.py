from components.common.point import Point


def get_move_to_target(current: Point, target: Point):
    current_x = current.x
    current_y = current.y
    target_x = target.x
    target_y = target.y
    if current_x < target_x:
        return Point(1, 0)
    elif current_x > target_x:
        return Point(-1, 0)
    elif current_y < target_y:
        return Point(0, 1)
    elif current_y > target_y:
        return Point(0, -1)
    return Point(0, 0)
