from dataclasses import dataclass
from enum import Enum
import math
from typing import List


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
    yellow_points = get_global_points(car_state, Color.YELLOW, cones)
    blue_points = get_global_points(car_state, Color.BLUE, cones)

    blue_points_order = []
    first_blue_point = get_nearest_point(Point2D(car_state.x, car_state.y), blue_points)
    blue_points.remove(first_blue_point)
    blue_points_order.append(first_blue_point)

    yellow_points_order = []
    first_yellow_point = get_nearest_point(Point2D(car_state.x, car_state.y), yellow_points)
    yellow_points.remove(first_yellow_point)
    yellow_points_order.append(first_yellow_point)

    for i in range(min(len(blue_points), len(yellow_points))):
        next_blue_point = get_nearest_point(blue_points_order[i], blue_points)
        next_yellow_point = get_nearest_point(yellow_points_order[i], yellow_points)

        dist_to_last_blue = get_point_distance(next_blue_point, blue_points_order[i])
        dist_to_last_yellow = get_point_distance(next_yellow_point, yellow_points_order[i])
        # print(f"Dist to last blue: {dist_to_last_blue}")
        # print(f"Dist to last yellow: {dist_to_last_yellow}")
        if dist_to_last_blue > 3.5 or dist_to_last_yellow > 3.5:
            print(f"Distance between neighboring cones too long, not realistic!")
            break

        blue_points.remove(next_blue_point)
        blue_points_order.append(next_blue_point)

        yellow_points.remove(next_yellow_point)
        yellow_points_order.append(next_yellow_point)

    result_points = []
    for i in range(len(blue_points_order)):
        p1 = blue_points_order[i]
        p2 = yellow_points_order[i]
        middle = get_middle_point(p1, p2)
        result_points.append(middle)

    result_points = result_points

    return result_points
# def calc_centerline(cones: list[Cone], car_state: CarState) -> list[Point2D]:
#     """This is the task you need to implement. Given a list of cones and the car's state, return a list of points that represent the centerline of the track."""
#     global_points_blue = []
#     distances_blue = []
#     blue_points_dict = {}
#     for cone in cones:
#         if cone.color == Color.BLUE:
#             glob_point = get_global_coord(car_state, Point2D(cone.x, cone.y))
#             global_points_blue.append(glob_point)
#             dist = get_point_distance(car_state, glob_point)
#             distances_blue.append(dist)
#             blue_points_dict[dist] = glob_point
#
#     distances_yellow = []
#     global_points_yellow = []
#     yellow_points_dict = {}
#     for cone in cones:
#         if cone.color == Color.YELLOW:
#             glob_point = get_global_coord(car_state, Point2D(cone.x, cone.y))
#             global_points_yellow.append(glob_point)
#             dist = get_point_distance(car_state, glob_point)
#             distances_yellow.append(dist)
#             yellow_points_dict[dist] = glob_point
#
#     distances_blue.sort()
#     distances_yellow.sort()
#
#     result_points = []
#     for i in range(min(len(distances_blue), len(distances_yellow))):
#         point = get_middle_point(blue_points_dict[distances_blue[i]], yellow_points_dict[distances_yellow[i]])
#         result_points.append(point)
#
#     return result_points
    
def get_point_distance(p1: Point2D, p2: Point2D) -> float:
    x_distance = p1.x - p2.x
    y_distance = p1.y - p2.y
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
    return Point2D((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)

def get_nearest_point(point: Point2D, points_list: List[Point2D]) -> Point2D:
    nearest_point = None
    for curr_point in points_list:
        if nearest_point is None:
            nearest_point = curr_point
        elif get_point_distance(curr_point, point) < get_point_distance(nearest_point, point):
            nearest_point = curr_point

    return nearest_point

def get_global_points(car_state: CarState, color: Color, cones: List[Cone]) -> List[Point2D]:
    result_points = []
    for cone in cones:
        if cone.color == color:
            next_point = get_global_coord(car_state, Point2D(cone.x, cone.y))
            result_points.append(next_point)

    return result_points
