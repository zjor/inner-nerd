from math import sqrt
from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: float
    y: float

    def to_array(self):
        return [self.x, self.y, 0]

    def middle(self, that: "Point") -> "Point":
        return Point((self.x + that.x) / 2, (self.y + that.y) / 2)

    def dist2(self, that: "Point") -> float:
        return (self.x - that.x) ** 2 + (self.y - that.y) ** 2

    def find_nearest(self, points: List["Point"]) -> "Point":
        return min(points, key=lambda p: self.dist2(p))

    @staticmethod
    def from_array(a: List[float]):
        return Point(a[0], a[1])


def find_circles_intersection(a: Point, b: Point, r: float) -> List[Point]:
    o = a.middle(b)
    l2 = o.dist2(a)

    if l2 > r ** 2:
        return []

    if abs(a.x - b.x) > abs(a.y - b.y):
        alpha = (o.y - a.y) / (o.x - a.x)
        beta = sqrt((r ** 2 - l2) / (1 + alpha ** 2))
        return [
            Point(o.x - alpha * beta, o.y + beta),
            Point(o.x + alpha * beta, o.y - beta)
        ]

    else:
        alpha = (o.x - a.x) / (o.y - a.y)
        beta = sqrt((r ** 2 - l2) / (1 + alpha ** 2))
        return [
            Point(o.x - beta, o.y + alpha * beta),
            Point(o.x + beta, o.y - alpha * beta)
        ]
