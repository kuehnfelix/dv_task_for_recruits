import csv

import matplotlib.colors
from task import *
import task
import math
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
plt.ion()
from typing import Generator

def pi_to_pi(x: float):
    return math.remainder(x, 2*math.pi)

class Sim:
    def __init__(self):
        self.cones = []
        self.visible_cones = []
        self.car_state = CarState(0, 0, 0)
        self.centerline = []

        self.fig, self.ax = plt.subplots()
        self.scatter = None
        self.arrow = self.ax.arrow(0, 0, 1, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
        self.car_arrow = None
        
        self.ax.set_aspect('equal')

    def load_track_from_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=",")
            self.cones = []
            for row in reader:
                if row[0] == "BLUE":
                    self.cones.append(Cone(Color.BLUE, float(row[1]), float(row[2])))
                elif row[0] == "YELLOW":
                    self.cones.append(Cone(Color.YELLOW, float(row[1]), float(row[2])))
                elif row[0] == "ORANGE":
                    self.cones.append(Cone(Color.ORANGE, float(row[1]), float(row[2])))
        
    def get_visible_cones(self) -> Generator[Cone, None, None]:
        for c in self.cones:
            distance_squared = (c.x-self.car_state.x)**2 + (c.y-self.car_state.y)**2
            if distance_squared  < 625 and distance_squared > 4:
                detection_angle = pi_to_pi(pi_to_pi(math.atan2(c.y-self.car_state.y, c.x-self.car_state.x)) - pi_to_pi(self.car_state.theta))
                if math.fabs(detection_angle) < 60/180*math.pi:
                    yield c

    def visualize(self):
        x = [c.x for c in self.visible_cones]
        y = [c.y for c in self.visible_cones]
        color = [(0.0, 0.0, 1.0) if c.color==Color.BLUE else (1.0, 1.0, 0.0) if c.color==Color.YELLOW else (1.0, 0.5, 0.0) for c in self.visible_cones]

        self.ax.clear()
        self.scatter = self.ax.scatter(x, y, c=color, s=50)

        if self.car_state:
            car_x, car_y, car_theta = self.car_state.x, self.car_state.y, self.car_state.theta

            # Define the box size
            box_length = 25

            d_x = (box_length/2) * np.cos(car_theta)
            d_y = (box_length/2) * np.sin(car_theta)

            center_x = car_x + d_x
            center_y = car_y + d_y

            self.ax.set_xlim(center_x - 15, center_x + 15)
            self.ax.set_ylim(center_y - 15, center_y + 15)
            self.ax.plot([center_x],[center_y], 'ro')


        # Plot the car as an arrow
        if self.car_state:
            car_x, car_y, car_theta = self.car_state.x, self.car_state.y, self.car_state.theta
            car_length = 1.0  # Length of the car's arrow (visual representation)

            # Calculate the car's direction using trigonometry
            dx = car_length * np.cos(car_theta)
            dy = car_length * np.sin(car_theta)

            self.arrow.remove()
            self.arrow = self.ax.arrow(car_x, car_y, dx, dy, head_width=0.5, head_length=0.5, fc='blue', ec='blue', width=0.1)
        
        centerline_x = [c.x for c in self.centerline]
        centerline_y = [c.y for c in self.centerline]
        self.ax.plot(centerline_x, centerline_y, 'r-')


        plt.draw()
        plt.pause(0.035)

    def simulation_step(self):
        # Update car position
        if self.centerline is not None and len(self.centerline) >0:
            direction_vector = [self.centerline[0].x- self.car_state.x, self.centerline[0].y - self.car_state.y]
            direction_norm = np.linalg.norm(direction_vector)
            self.car_state.x += direction_vector[0] / direction_norm * 0.1
            self.car_state.y += direction_vector[1] / direction_norm * 0.1
            self.car_state.theta = math.atan2(direction_vector[1], direction_vector[0])

        self.visible_cones = list(self.get_visible_cones())
        # visible cones should be transformed here to the car's frame of reference
        transformed_cones = []

        for cone in self.visible_cones:
            # Translate cone position relative to the car
            dx = cone.x - self.car_state.x
            dy = cone.y - self.car_state.y

            # Rotate according to the car's heading (theta)
            rotated_x = dx * np.cos(-self.car_state.theta) - dy * np.sin(-self.car_state.theta)
            rotated_y = dx * np.sin(-self.car_state.theta) + dy * np.cos(-self.car_state.theta)
            transformed_cones.append(Cone(cone.color, rotated_x, rotated_y))

        self.centerline = task.calc_centerline(transformed_cones, self.car_state)
        


if __name__ == "__main__":
    sim = Sim()
    sim.load_track_from_csv("track.csv")
    while 1:        
        sim.simulation_step()
        sim.visualize()