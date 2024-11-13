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
    global_points_blue = []
    distances_blue = []
    blue_points_dict = {}
    for cone in cones:
        if cone.color == Color.BLUE:
            glob_point = get_global_coord(car_state, Point2D(cone.x, cone.y))
            global_points_blue.append(glob_point)
            dist = get_point_distance(car_state, glob_point)
            distances_blue.append(dist)
            blue_points_dict[dist] = glob_point

    distances_yellow = []
    global_points_yellow = []
    yellow_points_dict = {}
    for cone in cones:
        if cone.color == Color.YELLOW:
            glob_point = get_global_coord(car_state, Point2D(cone.x, cone.y))
            global_points_yellow.append(glob_point)
            dist = get_point_distance(car_state, glob_point)
            distances_yellow.append(dist)
            yellow_points_dict[dist] = glob_point

    distances_blue.sort()
    distances_yellow.sort()

    result_points = []
    for i in range(min(len(distances_blue), len(distances_yellow))):
        point = get_middle_point(blue_points_dict[distances_blue[i]], yellow_points_dict[distances_yellow[i]])
        result_points.append(point)

    return result_points
    
def get_point_distance(car_state: CarState, point: Point2D) -> float:
    x_distance = point.x - car_state.x
    y_distance = point.y - car_state.y
    return math.sqrt(x_distance ** 2 + y_distance ** 2)

# def get_global_pos(car_state: CarState, distance: float) -> Point2D:
#     x_coord = car_state.x + distance * math.cos(car_state.theta)
#     y_coord = car_state.y + distance * math.sin(car_state.theta)
#     return Point2D(x_coord, y_coord)

def get_global_coord(car_state: CarState, point: Point2D) -> Point2D:
    x_coord = car_state.x + point.x * math.cos(car_state.theta) - point.y * math.sin(car_state.theta)
    y_coord = car_state.y + point.x * math.sin(car_state.theta) + point.y * math.cos(car_state.theta)
    return Point2D(x_coord, y_coord)

def get_middle_point(p1: Point2D, p2: Point2D) -> Point2D:
    x_dist = p1.x - p2.x
    y_dist = p1.y - p2.y
    return Point2D((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)

