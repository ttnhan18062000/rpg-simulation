from pygame import Surface

from components.common.point import Point


class GameObject:
    def __init__(self, pos: Point, img: str):
        self.pos = pos
        self.img = img

    def draw(self, screen: Surface):
        pass
