import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def get_distance_man(A: "Point", B: "Point") -> int:
        return abs(A.x - B.x) + abs(A.y - B.y)

    @staticmethod
    def get_distance_euc(A: "Point", B: "Point") -> float:
        return math.sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def reverse(self):
        self.x = -self.x
        self.y = -self.y
