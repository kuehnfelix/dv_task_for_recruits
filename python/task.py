from dataclasses import dataclass
from enum import Enum
import math

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
    """This is the task you need to implement. Given a list of cones and the car's state, return a list of points that represent the centerline of the track."""
     
    return [Point2D(1, 0), Point2D(1, 1)] //Placeholder
    


