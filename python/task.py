from dataclasses import dataclass
from enum import Enum

class Color(Enum):
    YELLOW = 'y'
    BLUE = 'b'
    ORANGE = 'darkorange'

@dataclass
class Cone:
    color: Color
    x: float
    y: float

@dataclass
class Point2D:
    x: float
    y: float

@dataclass
class CarState:
    x: float
    y: float
    theta: float


def calc_centerline(cones: list[Cone], car_state: CarState) -> list[Point2D]:
    points = [Point2D(cone.x, cone.y) for cone in cones if cone.color == Color.YELLOW]
    return points

def control_car(centerline: list[Point2D], car_state: CarState) -> tuple[float, float]:
    return None


